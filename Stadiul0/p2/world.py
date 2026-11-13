"""World of Pilot 2, Stage A (protocol v0.3, sections 4.1 and 4.2).

Vocabulary partition; target, reference and distractor tasks; probe halves A and B; the reference
battery R and the behavioural battery B_beh. A world is a deterministic function of its numpy
Generator. Every example is [TASK, a, b, ARROW] -> answer token (one answer position).
"""
from dataclasses import dataclass
from math import gcd

import numpy as np

# Vocabulary partition (section 4.1). Order fixes the token ids.
PARTITION = [("task", 64), ("v_target", 180), ("v_ref", 84), ("v_distractor", 84),
             ("value", 64), ("digit", 32), ("special", 4)]
VOCAB = 512
TASK_SLOTS = {"target": (0, 40), "reference": (40, 8), "distractor": (48, 8)}   # 8 spare: 56-63


class Vocab:
    def __init__(self):
        off = 0
        self.ranges = {}
        for name, n in PARTITION:
            self.ranges[name] = (off, off + n)
            setattr(self, name, np.arange(off, off + n, dtype=np.int64))
            off += n
        assert off == VOCAB
        self.ARROW = int(self.special[0])
        self.PAD = int(self.special[1])

    def task_token(self, role, i):
        base, n = TASK_SLOTS[role]
        assert 0 <= i < n, (role, i)
        return int(self.task[base + i])


@dataclass
class Task:
    role: str                 # target | reference | distractor
    kind: str                 # fact | rule
    index: int                # index within its role
    token: int
    train_x: np.ndarray       # [n_train, 4] int64
    train_y: np.ndarray       # [n_train] int64 (answer token ids)
    probe_x: np.ndarray       # [256, 4] (target tasks; fact probes are the trained items)
    probe_y: np.ndarray
    half_a: np.ndarray        # indices into probe_x (128)
    half_b: np.ndarray
    n_values: int             # number of distinct target values (64 for facts, m_k for rules)
    modulus: int = 0
    a: int = 0
    b: int = 0

    def train_pairs(self):
        """Input pairs (second and third token) of the training set, as ids t1 * 512 + t2."""
        return self.train_x[:, 1] * VOCAB + self.train_x[:, 2]


def _items(token, k1, k2, arrow):
    n = len(k1)
    return np.stack([np.full(n, token), k1, k2, np.full(n, arrow)], axis=1).astype(np.int64)


def _split_halves(rng, n):
    perm = rng.permutation(n)
    return np.sort(perm[: n // 2]), np.sort(perm[n // 2:])


class _PairSource:
    """Ordered key pairs over one key vocabulary; every fresh pair is handed out once."""

    def __init__(self, rng, vocab_tokens, pool_size=0):
        n = len(vocab_tokens)
        order = rng.permutation(n * n)
        self.tokens = vocab_tokens
        self.pool = order[:pool_size]
        self.fresh = order[pool_size:]
        self.ptr = 0

    def draw(self, rng, n_items, n_shared):
        shared = rng.choice(self.pool, size=n_shared, replace=False) if n_shared else np.empty(0, np.int64)
        fresh = self.fresh[self.ptr: self.ptr + n_items - n_shared]
        assert len(fresh) == n_items - n_shared, "key vocabulary exhausted"
        self.ptr += len(fresh)
        ids = rng.permutation(np.concatenate([shared, fresh]))
        n = len(self.tokens)
        return self.tokens[ids // n], self.tokens[ids % n]


def _fact_task(rng, vocab, role, i, pairs, n_items, n_shared):
    k1, k2 = pairs.draw(rng, n_items, n_shared)
    x = _items(vocab.task_token(role, i), k1, k2, vocab.ARROW)
    y = vocab.value[rng.integers(0, 64, size=n_items)]
    ha, hb = _split_halves(rng, n_items)
    return Task(role, "fact", i, vocab.task_token(role, i), x, y, x, y, ha, hb, 64)


def _rule_task(rng, vocab, role, i, modulus, n_items, n_inputs, form="affine"):
    """Rule task. form 'affine' (protocol v0.3, section 4.1): y = (a x + b) mod m, x = 32 d1 + d2.
    form 'unary' (Stage 0 alternative, not in the protocol): y = (a d1 + b) mod m; d2 is irrelevant,
    so held-out probes test generalisation to unseen (d1, d2) combinations."""
    a = int(rng.choice([c for c in range(1, modulus) if gcd(c, modulus) == 1]))
    b = int(rng.integers(0, modulus))
    perm = rng.permutation(n_inputs)
    probe_in, train_in = perm[:n_items], perm[n_items: 2 * n_items]   # training drawn from the 768 non-probes

    def enc(xs):
        x = _items(vocab.task_token(role, i), vocab.digit[xs // 32], vocab.digit[xs % 32], vocab.ARROW)
        arg = xs if form == "affine" else xs // 32
        return x, vocab.value[(a * arg + b) % modulus]

    tx, ty = enc(train_in)
    px, py = enc(probe_in)
    ha, hb = _split_halves(rng, n_items)
    n_values = int(len(np.unique(ty)))          # distinct target values in the training set (section 7)
    return Task(role, "rule", i, vocab.task_token(role, i), tx, ty, px, py, ha, hb, n_values, modulus, a, b)


class World:
    def __init__(self, wcfg, rng, rule_frac, pi_overlap):
        self.vocab = v = Vocab()
        n, n_items = wcfg["n_target"], wcfg["items_per_task"]
        assert n <= 40
        n_rule = int(round(rule_frac * n))
        kinds = rng.permutation(["rule"] * n_rule + ["fact"] * (n - n_rule))
        self.pi_overlap = pi_overlap
        form = wcfg.get("rule_form", "affine")
        assert form in ("affine", "unary")
        n_shared = int(round(pi_overlap * n_items))
        tgt_pairs = _PairSource(rng, v.v_target, wcfg["key_pool_size"])
        self.targets = []
        for i, kind in enumerate(kinds):
            if kind == "fact":
                self.targets.append(_fact_task(rng, v, "target", i, tgt_pairs, n_items, n_shared))
            else:
                m = int(rng.choice(wcfg["target_moduli"]))
                self.targets.append(_rule_task(rng, v, "target", i, m, n_items, wcfg["rule_inputs"], form))

        ref_pairs = _PairSource(rng, v.v_ref)
        self.refs = [_fact_task(rng, v, "reference", i, ref_pairs, n_items, 0) for i in range(wcfg["n_ref_fact"])]
        for j, m in enumerate(wcfg["ref_moduli"][: wcfg["n_ref_rule"]]):
            self.refs.append(_rule_task(rng, v, "reference", wcfg["n_ref_fact"] + j, int(m), n_items,
                                         wcfg["rule_inputs"], form))

        dis_pairs = _PairSource(rng, v.v_distractor)
        self.distractors = [_fact_task(rng, v, "distractor", i, dis_pairs, n_items, 0)
                            for i in range(wcfg["n_distractor"])]

        # Batteries R and B_beh: disjoint draws from the reference tasks' trained items.
        m = wcfg["battery_per_ref_task"]
        rx, ry, bx, by = [], [], [], []
        for t in self.refs:
            perm = rng.permutation(len(t.train_x))
            rx.append(t.train_x[perm[:m]]); ry.append(t.train_y[perm[:m]])
            bx.append(t.train_x[perm[m: 2 * m]]); by.append(t.train_y[perm[m: 2 * m]])
        self.R_x, self.R_y = np.concatenate(rx), np.concatenate(ry)
        self.B_x, self.B_y = np.concatenate(bx), np.concatenate(by)
        self.childhood_x = np.concatenate([t.train_x for t in self.refs])
        self.childhood_y = np.concatenate([t.train_y for t in self.refs])
        self.check()

    # ---- assertions (gate G4, structural part) ----
    def check(self):
        v = self.vocab
        lo = lambda name: v.ranges[name]

        def inside(tokens, name):
            a, b = lo(name)
            return bool(np.all((tokens >= a) & (tokens < b)))

        for name_a, name_b in [("v_target", "v_ref"), ("v_target", "v_distractor"), ("v_ref", "v_distractor")]:
            assert not set(getattr(v, name_a)) & set(getattr(v, name_b))
        for t in self.targets:
            keyvocab = "v_target" if t.kind == "fact" else "digit"
            for x in (t.train_x, t.probe_x):
                assert inside(x[:, 1:3], keyvocab), "target key outside its vocabulary"
            if t.kind == "rule":
                assert not set(map(tuple, t.train_x)) & set(map(tuple, t.probe_x)), "rule probe trained"
            assert len(set(map(tuple, t.probe_x))) == len(t.probe_x)
            assert not set(t.half_a) & set(t.half_b) and len(t.half_a) + len(t.half_b) == len(t.probe_x)
        for t in self.refs:
            assert inside(t.train_x[:, 1:3], "v_ref" if t.kind == "fact" else "digit")
            assert t.modulus not in {tt.modulus for tt in self.targets if tt.kind == "rule"}
        for t in self.distractors:
            assert inside(t.train_x[:, 1:3], "v_distractor")
        tokens = [t.token for t in self.targets + self.refs + self.distractors]
        assert len(set(tokens)) == len(tokens)
        probes = set()
        for t in self.targets:
            probes |= set(map(tuple, t.probe_x))
        R = set(map(tuple, self.R_x))
        B = set(map(tuple, self.B_x))
        assert len(R) == len(self.R_x) and len(B) == len(self.B_x)
        assert not R & probes and not B & probes and not R & B, "R, B_beh and probes must be disjoint"
        assert np.all(self.R_x[:, 0] >= TASK_SLOTS["reference"][0]) and np.all(self.R_x[:, 0] < 48)

    def key_overlap(self):
        """Reference predictor C8 (world metadata): overlap of input pairs between target tasks.

        Facts: |P_k & P_j| / |P_k| on key pairs. Rules: Jaccard overlap of training input pairs.
        Returned as a [n, n] matrix (row k, column j); facts and rules never share input pairs.
        """
        n = len(self.targets)
        sets = [set(t.train_pairs().tolist()) for t in self.targets]
        out = np.zeros((n, n))
        for k in range(n):
            for j in range(n):
                if j == k:
                    continue
                inter = len(sets[k] & sets[j])
                if self.targets[k].kind == "rule":
                    out[k, j] = inter / max(1, len(sets[k] | sets[j]))
                else:
                    out[k, j] = inter / len(sets[k])
        return out

    def summary(self):
        return {
            "kinds": [t.kind for t in self.targets],
            "moduli": [t.modulus for t in self.targets],
            "n_values": [t.n_values for t in self.targets],
            "pi_overlap": self.pi_overlap,
        }
