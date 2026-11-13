"""Agent of Pilot 2 (protocol v0.3, section 3): a small pre-LN decoder-only Transformer whose
parameters live in one flat float32 buffer, updated by an explicit AdamW (or SGD) step so that the
pre-decay update, the decay term and the optimizer moments are available exactly at every step.
"""
import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class Block(nn.Module):
    def __init__(self, d, h, dff):
        super().__init__()
        self.h = h
        self.ln1 = nn.LayerNorm(d)
        self.qkv = nn.Linear(d, 3 * d)
        self.proj = nn.Linear(d, d)
        self.ln2 = nn.LayerNorm(d)
        self.fc1 = nn.Linear(d, dff)
        self.fc2 = nn.Linear(dff, d)

    def forward(self, x, mask):
        B, T, D = x.shape
        q, k, v = self.qkv(self.ln1(x)).split(D, dim=-1)
        dh = D // self.h
        q = q.view(B, T, self.h, dh).transpose(1, 2)
        k = k.view(B, T, self.h, dh).transpose(1, 2)
        v = v.view(B, T, self.h, dh).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(dh))
        att = att.masked_fill(~mask[:T, :T], float("-inf")).softmax(dim=-1)
        y = (att @ v).transpose(1, 2).reshape(B, T, D)
        x = x + self.proj(y)
        return x + self.fc2(F.gelu(self.fc1(self.ln2(x))))


class TinyGPT(nn.Module):
    def __init__(self, a):
        super().__init__()
        d = a["d_model"]
        self.tok = nn.Embedding(a["vocab"], d)
        self.pos = nn.Embedding(a["max_ctx"], d)
        self.blocks = nn.ModuleList([Block(d, a["n_head"], a["d_ff"]) for _ in range(a["n_layer"])])
        self.lnf = nn.LayerNorm(d)
        self.head = nn.Linear(d, a["vocab"])            # untied from self.tok
        self.register_buffer("mask", torch.tril(torch.ones(a["max_ctx"], a["max_ctx"], dtype=torch.bool)),
                             persistent=False)
        for m in self.modules():
            if isinstance(m, (nn.Linear, nn.Embedding)):
                nn.init.normal_(m.weight, 0.0, a["init_std"])
                if isinstance(m, nn.Linear):
                    nn.init.zeros_(m.bias)

    def forward(self, idx, reps=False):
        """Logits at the answer position (the last input token); optionally the final-LN representation."""
        T = idx.shape[1]
        x = self.tok(idx) + self.pos.weight[:T]
        for b in self.blocks:
            x = b(x, self.mask)
        h = self.lnf(x[:, -1])
        out = self.head(h)
        return (out, h) if reps else out


class FlatAgent:
    """Model plus flat parameter buffer and optimizer state.

    Layout of the flat buffer: decayed matrices first (all Linear weights and the head weight, plus both
    embeddings when optim.wd_embeddings is true), then the non-decayed matrices (the two embeddings when
    optim.wd_embeddings is false; Deep Review D3, 6 Nov 2026), then biases and LayerNorm parameters.
    `layers` lists the slices of all matrices (decayed first): they are the l of D1_rel, as before.
    theta_dec_norm is the norm over the decayed matrices only (the ones weight decay acts on).
    """

    EMBEDDINGS = ("tok.weight", "pos.weight")

    def __init__(self, acfg, ocfg):
        self.model = TinyGPT(acfg)
        named = list(self.model.named_parameters())
        wd_emb = ocfg.get("wd_embeddings", True)
        decayed = [(n, p) for n, p in named if p.dim() == 2 and (wd_emb or n not in self.EMBEDDINGS)]
        mats_nd = [(n, p) for n, p in named if p.dim() == 2 and not (wd_emb or n not in self.EMBEDDINGS)]
        other = [(n, p) for n, p in named if p.dim() != 2]
        self.order = decayed + mats_nd + other
        self.decayed_names = [n for n, _ in decayed]
        self.n_dec_layers = len(decayed)
        self.P = sum(p.numel() for _, p in named)
        self.Pd = sum(p.numel() for _, p in decayed)
        self.P2d = self.Pd + sum(p.numel() for _, p in mats_nd)
        self.flat = torch.zeros(self.P)
        self.layers, off = [], 0
        for n, p in self.order:
            k = p.numel()
            self.flat[off: off + k].copy_(p.data.reshape(-1))
            p.data = self.flat[off: off + k].view_as(p)
            if p.dim() == 2:
                self.layers.append((n, off, off + k))
            off += k
        assert off == self.P
        self.params = [p for _, p in self.order]
        self.module_params = list(self.model.parameters())
        # Gradients live in one flat buffer too: autograd accumulates into an existing .grad in place,
        # so zeroing the buffer replaces set-to-None and no parameter-sized tensor is allocated per step.
        self.gflat = torch.zeros(self.P)
        off = 0
        for _, p in self.order:
            k = p.numel()
            p.grad = self.gflat[off: off + k].view_as(p)
            off += k
        self._gptr = [p.grad.data_ptr() for p in self.params]
        self.o = ocfg
        self.kind = ocfg["kind"]
        self.m = torch.zeros(self.P)
        self.v = torch.zeros(self.P)
        # persistent work buffers (Windows returns large allocations to the OS; per-step allocation
        # of parameter-sized temporaries does not scale across parallel workers)
        self.denom = torch.zeros(self.P)
        self.dpre = torch.zeros(self.P)
        self.decay = torch.zeros(self.Pd)
        self.tmp = torch.zeros(self.P)
        self.t = 0                        # committed optimizer steps since the first childhood step

    # ---- quantities derived from the optimizer state ----
    def vhat(self):
        if self.t == 0:
            return None
        b2 = self.o["betas"][1] if self.kind == "adamw" else self.o["passive_v_beta"]
        return self.v / (1.0 - b2 ** self.t)

    def trace_vhat(self):
        if self.t == 0:
            return float("nan")
        b2 = self.o["betas"][1] if self.kind == "adamw" else self.o["passive_v_beta"]
        return float(self.v.sum(dtype=torch.float64)) / (1.0 - b2 ** self.t)

    def mhat(self):
        if self.kind == "sgd":
            return self.m
        return self.m / (1.0 - self.o["betas"][0] ** self.t)

    def layer_sq(self, vec):
        """Per-layer squared norms of `vec` over the decayed matrices (float64 tensor).

        Each slice is reduced with a float32 dot product (relative error ~1e-6), then promoted.
        """
        return torch.stack([torch.dot(vec[a:b], vec[a:b]) for _, a, b in self.layers]).double()

    # ---- one committed optimizer step ----
    def step(self, x, y, lr, vhat_lag=None):
        """Forward, backward, clip, update. Returns (stats tensor, dpre, decay).

        Clipping is torch.nn.utils.clip_grad_norm_ itself, and the moment and parameter updates use
        the operation order of torch.optim.AdamW (single-tensor path), so that the update is
        bit-compatible with it (checked in checks_stage0.py). Logged norms use float32 dot products.
        """
        o = self.o
        logits = self.model(x)
        loss = F.cross_entropy(logits, y)
        self.gflat.zero_()
        loss.backward()
        if self.t < 8:                                                 # gradients must stay in the flat buffer
            assert [p.grad.data_ptr() for p in self.params] == self._gptr, "autograd replaced a .grad tensor"
        # raw norm; grads clipped in place. Module order, as torch would see model.parameters():
        # the total norm is a sum over parameters, so the order changes its last bits.
        gn = torch.nn.utils.clip_grad_norm_(self.module_params, o["clip"])
        coef = torch.clamp(o["clip"] / (gn + 1e-6), max=1.0)            # the coefficient torch applied
        gt = self.gflat                                                # clipped gradient g~ (a view of .grad)
        self.t += 1
        wd = o["weight_decay"]
        theta = self.flat
        Pd = self.Pd
        dpre, denom, tmp = self.dpre, self.denom, self.tmp
        if self.kind == "adamw":
            b1, b2 = o["betas"]
            self.m.lerp_(gt, 1 - b1)                                  # as torch Adam(W): m + (1-b1)(g - m)
            self.v.mul_(b2).addcmul_(gt, gt, value=1 - b2)
            bc1, bc2 = 1 - b1 ** self.t, 1 - b2 ** self.t
            torch.sqrt(self.v, out=denom)
            denom.div_(bc2 ** 0.5).add_(o["eps"])                      # as torch: (v.sqrt() / bc2_sqrt) + eps
            torch.mul(self.m, -lr / bc1, out=dpre)
            dpre.div_(denom)                                           # as torch addcdiv: (value * m) / denom
            mhat_sq = torch.dot(self.m, self.m) / (bc1 * bc1)
            trv = self.v.sum() / bc2
        else:
            mu, bv = o["sgd_momentum"], o["passive_v_beta"]
            self.m.mul_(mu).add_(gt)
            self.v.mul_(bv).addcmul_(gt, gt, value=1 - bv)
            torch.mul(self.m, -lr, out=dpre)
            mhat_sq = torch.dot(self.m, self.m)
            trv = self.v.sum() / (1 - bv ** self.t)
        decay = torch.mul(theta[:Pd], lr * wd, out=self.decay)     # decoupled weight-decay term (subtracted)
        lay_theta = self.layer_sq(theta)                           # ||theta_l(tau)||^2, before the update
        lay_dpre = self.layer_sq(dpre)
        nd = dpre[self.P2d:]                                       # biases and LayerNorm parameters
        nd_sq = torch.dot(nd, nd).double()
        d1_rel = torch.sqrt((lay_dpre / (lay_theta + 1e-12)).sum())
        full_d = torch.sub(dpre[:Pd], decay, out=tmp[:Pd])
        if self.P2d == Pd:                                         # every matrix decayed: unchanged arithmetic
            rest_sq = nd_sq
        else:                                                      # non-decayed matrices move by dpre only
            rest = dpre[Pd:]
            rest_sq = torch.dot(rest, rest).double()
        dfull_sq = torch.dot(full_d, full_d).double() + rest_sq
        if vhat_lag is not None:
            torch.mul(dpre, dpre, out=tmp)
            d2 = torch.sqrt(torch.dot(vhat_lag, tmp).double())
        else:
            d2 = torch.tensor(float("nan"), dtype=torch.float64)
        gdot = torch.dot(gt, dpre).abs().double()
        # apply: theta <- theta (1 - lr wd) on decayed matrices, then + dpre (torch AdamW order)
        theta[:Pd].mul_(1 - lr * wd)
        theta.add_(dpre)
        stats = torch.stack([
            loss.detach().double(), gn.double(), (gn * coef).double(), torch.sqrt(lay_dpre.sum() + nd_sq),
            torch.sqrt(dfull_sq), torch.sqrt(mhat_sq.double()), gdot, torch.sqrt(torch.dot(theta, theta).double()),
            torch.sqrt(lay_theta[: self.n_dec_layers].sum()), trv.double(), d1_rel, d2,
        ])
        return stats, dpre, decay


STEP_FIELDS = ["loss", "gnorm_raw", "gnorm_clip", "dpre_norm", "D1", "mhat_norm", "gdot",
               "theta_norm", "theta_dec_norm", "trace_vhat", "D1_rel", "D2"]
