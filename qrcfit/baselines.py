"""Tuned classical baselines. Every baseline gets the same random-search budget per (task, size).

  esn        : leaky echo state network, sizes M; tuned over spectral radius, input scale, leak.
  polynarx   : ridge on polynomial features of lagged inputs (the 'simple classical formula of the
               same size' in Pandey+ 2026). Sizes = (lags L, degree p).
  kerr_delay : semiclassical (coherent-state) Kerr delay-line reservoir with D virtual nodes — the
               classically simulable twin of the Kerr feedback QRC (Soh 2026).
"""
import numpy as np
from itertools import combinations_with_replacement
from .evaluate import val_test as _val_test

ESN_SIZES = [3, 5, 10, 30, 100, 300, 1000]
NARX_SIZES = [(2, 1), (3, 1), (5, 1), (10, 1), (30, 1), (3, 2), (5, 2), (10, 2), (20, 2), (5, 3), (10, 3)]
KERR_SIZES = [10, 30, 100, 300]


def esn_features(u, M, rho, sin, leak, seed):
    rng = np.random.default_rng(seed)
    T, d = u.shape
    W = rng.standard_normal((M, M)) * (rng.uniform(size=(M, M)) < min(1, 10 / M))
    ev = np.abs(np.linalg.eigvals(W)).max()
    W *= rho / max(ev, 1e-12)
    Win = rng.uniform(-sin, sin, (M, d + 1))
    x = np.zeros(M); X = np.zeros((T, M))
    ub = np.hstack([u, np.ones((T, 1))])
    for t in range(T):
        x = (1 - leak) * x + leak * np.tanh(Win @ ub[t] + W @ x)
        X[t] = x
    return X


def polynarx_features(u, L, p):
    T, d = u.shape
    lags = np.stack([np.roll(u, k, 0) for k in range(L)], 1).reshape(T, L * d)
    lags[:L] = 0
    cols = [lags]
    for deg in range(2, p + 1):
        idx = list(combinations_with_replacement(range(L * d), deg))
        cols.append(np.stack([np.prod(lags[:, list(c)], 1) for c in idx], 1))
    return np.hstack(cols)


def kerr_delay_features(u, D, chi, eta, eps, seed):
    rng = np.random.default_rng(seed)
    T = len(u)
    mask = rng.uniform(-1, 1, D)
    w = rng.uniform(-1, 1, u.shape[1]) if u.shape[1] > 1 else np.ones(1)  # random projection for multi-d input
    a = np.zeros(D, complex); X = np.zeros((T, 3 * D))
    for t in range(T):
        inp = float(u[t] @ w)
        a = eta * np.exp(1j * chi * np.abs(a) ** 2) * (np.roll(a, 1) + eps * inp * mask)
        X[t] = np.concatenate([np.abs(a) ** 2, a.real, a.imag])
    return X


def tune(task, family, size, budget, seed):
    """Random-search `budget` hyperparameter draws; select on validation (inside fit_predict's lambda loop
    the validation split is reused). Returns (test_nmse, n_features). Honest protocol: the test score is
    that of the configuration with the best validation score, computed in one pass."""
    rng = np.random.default_rng(seed + 1000)
    u = task["u"]
    best = (np.inf, None, None)
    for b in range(budget):
        if family == "esn":
            X = esn_features(u, size, rng.uniform(0.3, 1.5), 10 ** rng.uniform(-1, 0.5), rng.uniform(0.1, 1.0), seed * 100 + b)
        elif family == "polynarx":
            from math import comb
            L, pdeg = size; nb = L * u.shape[1]
            if sum(comb(nb + k - 1, k) for k in range(1, pdeg + 1)) > 5000:
                return np.inf, 0  # feature explosion for multi-d inputs: skip this size
            X = polynarx_features(u, *size)
        elif family == "kerr_delay":
            X = kerr_delay_features(u, size, 10 ** rng.uniform(-1, 1), rng.uniform(0.5, 0.99), 10 ** rng.uniform(-1, 0.5), seed * 100 + b)
        val, test = _val_test(X, task)
        if val < best[0]:
            best = (val, test, X.shape[1])
        if family == "polynarx":
            break  # deterministic features; lambda is tuned inside
    return best[1], best[2]


FORR_Q = [20, 200, 2000, 20000]


READOUT_SIZES = {"esn": [10, 30, 100, 300], "polynarx": [(5, 1), (10, 2), (20, 2), (30, 1)], "kerr_delay": [10, 30, 100]}


def readout_best(u, task, seed, budget=10):
    """Same tuned readout families for everyone: given a 1-d stream u (T,1) standing in for the input, tune
    ESN / poly-NARX / semiclassical Kerr delay readouts (reduced size grid, `budget` draws) and return
    (best test NMSE, name). Used for both the quantum p_hat(m) stream and the classical Phi_hat(Q) stream."""
    t2 = dict(task); t2["u"] = (u - u.mean()) / max(u.std(), 1e-10)
    best = (np.inf, None)
    for fam, szs in READOUT_SIZES.items():
        for sz in szs:
            nm, F = tune(t2, fam, sz, budget, seed)
            if nm is not None and nm < best[0]:
                best = (nm, f"{fam}:{sz}")
    return best


def forr_classical_stream(task, variant, Q, seed):
    from .forrelation import classical_estimates
    rng = np.random.default_rng(seed + 4242)
    return classical_estimates(task, variant, Q, rng)[:, None]


def all_baselines(task, seed, budget=20, quick=False):
    out = {}
    if "phi" in task:  # Forrelation task: ALL sides (quantum stream, query-limited classical, full-information classical)
        # use the same reduced readout grid (readout_best); the generic families below are skipped for these tasks
        from .forrelation import anf2_queries
        N = 1 << task["n"]
        nm, name = readout_best(task["u"], task, seed)
        out[f"forr_full:{N}"] = dict(nmse=nm, F=int(name.split(":")[1].split(",")[0].strip("()")) if name else 0, family="forr_full", size=N, readout=name)
        variants = ("naive", "pairs", "wb") if "flips" in task else ("naive", "pairs")
        for variant in variants:
            for Q in FORR_Q:
                nm, name = readout_best(forr_classical_stream(task, variant, Q, seed), task, seed)
                out[f"forr_{variant}:{Q}"] = dict(nmse=nm, F=int(name.split(":")[1].split(",")[0].strip("()")) if name else 0, family=f"forr_{variant}", size=Q, readout=name)
        if "flips" not in task:
            Q = anf2_queries(task["n"])
            nm, name = readout_best(forr_classical_stream(task, "anf2", Q, seed), task, seed)
            out[f"forr_anf2:{Q}"] = dict(nmse=nm, F=0, family="forr_anf2", size=Q, readout=name)
        return out
    sizes = {"esn": ESN_SIZES[:6] if quick else ESN_SIZES, "polynarx": NARX_SIZES, "kerr_delay": KERR_SIZES[:3] if quick else KERR_SIZES}
    for fam, szs in sizes.items():
        for sz in szs:
            t, F = tune(task, fam, sz, budget if not quick else 5, seed)
            out[f"{fam}:{sz}"] = dict(nmse=t, F=F, family=fam, size=sz)
    return out
