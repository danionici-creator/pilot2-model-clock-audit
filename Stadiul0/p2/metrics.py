"""Distances on outputs and representations (protocol v0.3, section 5)."""
import math

import numpy as np
import torch

LN2 = math.log(2.0)


def sqrt_js(P, Q):
    """Jensen-Shannon distance, base 2, row-wise, in [0, 1]. P, Q: [n, V] probabilities."""
    P = P.double()
    Q = Q.double()
    M = 0.5 * (P + Q)
    xl = torch.special.xlogy
    js = 0.5 * ((xl(P, P) - xl(P, M)).sum(-1) + (xl(Q, Q) - xl(Q, M)).sum(-1)) / LN2
    return js.clamp(min=0.0).sqrt()


def cka_distance(X, Y):
    """sqrt(1 - CKA) with standard (biased) centred linear CKA; X, Y: [n, d]."""
    X = X.double() - X.double().mean(0, keepdim=True)
    Y = Y.double() - Y.double().mean(0, keepdim=True)
    hsic = (Y.T @ X).pow(2).sum()
    nx = (X.T @ X).pow(2).sum().sqrt()
    ny = (Y.T @ Y).pow(2).sum().sqrt()
    cka = hsic / (nx * ny)
    return float(torch.sqrt(torch.clamp(1.0 - cka, min=0.0)))


def sqrt_js_np(p, q):
    """Jensen-Shannon distance, base 2, between two 1-D distributions (numpy)."""
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    m = 0.5 * (p + q)
    with np.errstate(divide="ignore", invalid="ignore"):
        a = np.where(p > 0, p * (np.log2(p) - np.log2(m)), 0.0).sum()
        b = np.where(q > 0, q * (np.log2(q) - np.log2(m)), 0.0).sum()
    return float(np.sqrt(max(0.0, 0.5 * (a + b))))
