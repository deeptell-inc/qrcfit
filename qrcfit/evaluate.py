"""Ridge readout, validation-tuned lambda, NMSE, and finite-shot feature noise."""
import numpy as np

LAMBDAS = np.logspace(-10, 1, 12)
SHOTS = [1e2, 1e3, 1e4, 1e5, 1e6, np.inf]


def nmse(y, yhat):
    return float(np.mean(np.sum((y - yhat) ** 2, 0) / np.sum((y - y.mean(0)) ** 2, 0)))


def val_test(X, task, lambdas=LAMBDAS):
    """X: (T,F) features aligned with task['u']. Lambda tuned on the last 20% of train.
    Returns (validation nmse of the chosen lambda, test nmse after refit on full train)."""
    w0, Tr, Te = task["washout"], task["T_train"], task["T_test"]
    y = task["y"]
    full = slice(w0, w0 + Tr)
    mu, sd = X[full].mean(0), X[full].std(0)
    X = np.where(sd > 1e-10, (X - mu) / np.maximum(sd, 1e-10), 0.0)  # z-score on train stats
    Xb = np.hstack([X, np.ones((len(X), 1))])
    nv = max(20, Tr // 5)
    tr = slice(w0, w0 + Tr - nv); va = slice(w0 + Tr - nv, w0 + Tr); te = slice(w0 + Tr, w0 + Tr + Te)
    A, B = Xb[tr].T @ Xb[tr], Xb[tr].T @ y[tr]
    best = (np.inf, lambdas[0])
    for lam in lambdas:
        W = np.linalg.solve(A + lam * np.eye(len(A)), B)
        e = nmse(y[va], Xb[va] @ W)
        if e < best[0]:
            best = (e, lam)
    lam = best[1]
    W = np.linalg.solve(Xb[full].T @ Xb[full] + lam * np.eye(Xb.shape[1]), Xb[full].T @ y[full])
    return best[0], nmse(y[te], Xb[te] @ W)


def fit_predict(X, task):
    return val_test(X, task)[1]


def shot_curve(X, V, task, rng, shots=SHOTS):
    """V: per-feature single-shot variance (T,F) or (F,). Returns {S: nmse}. Noise is fresh per shot level,
    applied to train and test alike (features are estimated from S repetitions at every time step)."""
    out = {}
    V = np.broadcast_to(V, X.shape)
    for S in shots:
        Xs = X if np.isinf(S) else X + rng.standard_normal(X.shape) * np.sqrt(V / S)
        out[S] = fit_predict(Xs, task)
    return out
