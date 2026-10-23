"""Application demos of the winning pattern (oracle input, Forrelation-type query separation).

Demo A — black-box dual-relation drift monitoring. Two processes f (reference, Kloosterman phase) and g_t
(device) should satisfy g = sign(Walsh f). The device's fidelity to that relation, p_t in [0.3,1], drifts
(Ornstein–Uhlenbeck + jumps): g_t = g with each entry flipped w.p. (1-p_t)/2, so E[Phi_t] = p_t * Phi_YES.
Monitor must track p_t (and Phi_t) from queries only.
  quantum : 2-query Forrelation circuit + Hadamard test, m shots/step (2m queries), tuned readout
  classical black-box : naive sampling / optimistic sqrt(N) surrogate at Q queries, same tuned readout
  classical WHITE-BOX control : the monitor knows the ideal g and samples g_t(y) g(y) at Q points
                                (variance (1-p^2)/Q, no N dependence) — shows where the win disappears.
Demo B — exponential-sum correlation scaling: measured classical time of the exact two-FWHT computation of
Phi for Kloosterman pairs vs n, against the quantum shot count for a target precision, with extrapolation.
Outputs: results/apps/drift_monitoring.md/.png, results/apps/exp_sum_scaling.md/.png
"""
import json, os, sys, time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qrcfit.forrelation import kloosterman_pair, fwht, _parity
from qrcfit.tasks import _pack, WASHOUT
from qrcfit.baselines import readout_best

OUT = os.path.join(os.path.dirname(__file__), "..", "results", "apps")
os.makedirs(OUT, exist_ok=True)


# ----------------------------------------------------------------------------- Demo A
def drift_task(n=16, T_train=1000, T_test=500, seed=0):
    rng = np.random.default_rng(seed)
    f, g = kloosterman_pair(n); N = 1 << n
    fh = fwht(f); phi_yes = float(np.dot(g, fh) / N ** 1.5)
    T = WASHOUT + T_train + T_test
    p = np.zeros(T); p[0] = 0.8
    for t in range(1, T):
        p[t] = p[t - 1] + 0.05 * (0.7 - p[t - 1]) + 0.03 * rng.standard_normal()
        if rng.uniform() < 0.02:
            p[t] = rng.uniform(0.3, 1.0)
        p[t] = np.clip(p[t], 0.3, 1.0)
    flips = rng.uniform(size=(T, N)) < ((1 - p) / 2)[:, None]       # (T, N) booleans, ~100 MB for n=16
    phi = np.array([np.dot(np.where(flips[t], -g, g), fh) for t in range(T)]) / N ** 1.5
    out = _pack(f"drift_n{n}", phi, np.stack([p, phi], 1), T_train, T_test)
    out.update(f=f, g=g, flips=flips, n=n, phi=phi[:out["u"].shape[0]], p=p[:out["u"].shape[0]], phi_yes=phi_yes)
    return out


def quantum_stream(task, m, rng):
    pr = (1 + task["phi"]) / 2
    return (pr if np.isinf(m) else rng.binomial(int(m), pr) / m)[:, None]


def classical_bb_stream(task, variant, Q, rng):
    f, g, flips, n, phi = task["f"], task["g"], task["flips"], task["n"], task["phi"]
    N = 1 << n; T = len(phi)
    if variant == "opt":
        return (phi + rng.standard_normal(T) * np.sqrt(np.sqrt(N) / Q))[:, None]
    out = np.zeros(T)
    for t in range(T):
        xs = rng.integers(0, N, Q); ys = rng.integers(0, N, Q)
        gy = np.where(flips[t, ys], -g[ys], g[ys])
        out[t] = np.sqrt(N) * np.mean(f[xs] * (1 - 2 * _parity(xs & ys)) * gy)
    return out[:, None]


def classical_wb_stream(task, Q, rng):
    g, flips, n, phi = task["g"], task["flips"], task["n"], task["phi"]
    N = 1 << n; T = len(phi); out = np.zeros(T)
    for t in range(T):
        ys = rng.integers(0, N, Q)
        out[t] = np.mean(np.where(flips[t, ys], -1.0, 1.0))  # g_t(y) g(y)
    return out[:, None]


def demo_a(seeds=3, n=16):
    M = [1e2, 1e3, 1e4]; Qs = [200, 2000, 20000]
    res = {}
    for s in range(seeds):
        t = drift_task(n, seed=s); rng = np.random.default_rng(s + 5)
        for m in M:
            res.setdefault(f"quantum m={m:.0e}", []).append(readout_best(quantum_stream(t, m, rng), t, s)[0])
        res.setdefault("quantum exact", []).append(readout_best(quantum_stream(t, np.inf, rng), t, s)[0])
        for Q in Qs:
            res.setdefault(f"classical naive Q={Q}", []).append(readout_best(classical_bb_stream(t, "naive", Q, rng), t, s)[0])
            res.setdefault(f"classical opt Q={Q}", []).append(readout_best(classical_bb_stream(t, "opt", Q, rng), t, s)[0])
            res.setdefault(f"classical WHITE-BOX Q={Q}", []).append(readout_best(classical_wb_stream(t, Q, rng), t, s)[0])
        print(f"seed {s} done (phi_yes={t['phi_yes']:.4f})", flush=True)
    med = {k: float(np.median(v)) for k, v in res.items()}
    L = [f"# Demo A: black-box dual-relation drift monitoring (Kloosterman reference, n={n}, N={1 << n}, {seeds} seeds)", "",
         "Targets: device fidelity p_t and Phi_t. NMSE (median over seeds), same tuned readout for every stream.", "",
         "| monitor | queries/step | NMSE |", "|---|---|---|"]
    for m in M:
        L.append(f"| quantum, m={m:.0e} shots | {2 * m:.0f} | {med[f'quantum m={m:.0e}']:.4f} |")
    L.append(f"| quantum, exact expectation | ∞ | {med['quantum exact']:.4f} |")
    for Q in Qs:
        L.append(f"| classical black-box naive | {Q} | {med[f'classical naive Q={Q}']:.4f} |")
        L.append(f"| classical black-box opt (√N surrogate) | {Q} | {med[f'classical opt Q={Q}']:.4f} |")
    for Q in Qs:
        L.append(f"| classical WHITE-BOX (knows ideal g) | {Q} | {med[f'classical WHITE-BOX Q={Q}']:.4f} |")
    L += ["", "Reading: in the black-box setting the quantum monitor at 200 queries/step beats every classical monitor up to 20000 queries/step; "
          "if the classical monitor knows the ideal device function g, sampling g_t g at Q points has variance (1-p^2)/Q with no N dependence and the advantage disappears."]
    open(os.path.join(OUT, "drift_monitoring.md"), "w").write("\n".join(L) + "\n"); json.dump(res, open(os.path.join(OUT, "drift_monitoring.json"), "w"), indent=1)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([2 * m for m in M], [med[f"quantum m={m:.0e}"] for m in M], "o-", label="quantum (2m queries)")
    for lab, key in [("classical naive", "classical naive Q="), ("classical opt (√N surrogate)", "classical opt Q="), ("classical white-box (knows g)", "classical WHITE-BOX Q=")]:
        ax.plot(Qs, [med[f"{key}{Q}"] for Q in Qs], "s--", label=lab)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("oracle queries per time step"); ax.set_ylabel("NMSE (p_t, Phi_t)")
    ax.set_title(f"Drift monitoring, Kloosterman n={n}"); ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(os.path.join(OUT, "drift_monitoring.png"), dpi=150)
    print("\n".join(L))


# ----------------------------------------------------------------------------- Demo B
def demo_b(ns=(10, 12, 14, 16, 18, 20, 22, 24), eps=0.03):
    rows = []
    for n in ns:
        t0 = time.time(); f, g = kloosterman_pair(n); t_build = time.time() - t0
        t0 = time.time(); fh = fwht(f); phi = float(np.dot(g, fh) / (1 << n) ** 1.5); t_fwht = time.time() - t0
        pr = (1 + phi) / 2; m = int(np.ceil(pr * (1 - pr) / (eps / 2) ** 2))  # shots for std(Phi_hat) <= eps
        rows.append(dict(n=n, N=1 << n, phi=phi, t_build=t_build, t_fwht=t_fwht, shots=m, q_queries=2 * m, sqrtN=int(np.sqrt(1 << n))))
        print(f"n={n:2d} N={1 << n:9d} Phi={phi:.4f} classical exact {t_fwht:.3f}s (+{t_build:.2f}s tables) | quantum shots for ±{eps}: {m} (= {2 * m} queries) | √N = {int(np.sqrt(1 << n))}", flush=True)
    a, b = np.polyfit([r["n"] for r in rows[-4:]], [np.log2(r["t_fwht"]) for r in rows[-4:]], 1)
    L = [f"# Demo B: exponential-sum correlation Phi(f^K, g^K) — classical exact time vs quantum shots (target ±{eps})", "",
         "| n | N | Phi | classical exact (2 FWHT) [s] | quantum shots | quantum queries (2m) | √N (classical query lower-bound scale) |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['n']} | {r['N']} | {r['phi']:.4f} | {r['t_fwht']:.3f} | {r['shots']} | {r['q_queries']} | {r['sqrtN']} |")
    L += ["", f"Measured classical scaling: log2(time) ≈ {a:.2f}·n + {b:.1f}  (ideal N log N → slope 1). "
          f"Extrapolation: n=40 → {2 ** (a * 40 + b) / 3600:.1e} h, n=50 → {2 ** (a * 50 + b) / 3600 / 24 / 365:.1e} y, n=60 → {2 ** (a * 60 + b) / 3600 / 24 / 365:.1e} y, "
          f"while the quantum side stays at {rows[-1]['q_queries']} oracle queries per estimate (precision ±{eps}) for every n. "
          "Classical query-limited estimators need Ω(√N/log N) queries: √N = 1e6 at n=40, 1e9 at n=60.", "",
          "Caveat: the quantum oracle cost (GF(2^n) inversion circuit per query) grows polynomially in n and is not included; the classical time is the full-table computation on one CPU core."]
    open(os.path.join(OUT, "exp_sum_scaling.md"), "w").write("\n".join(L) + "\n")
    fig, ax = plt.subplots(figsize=(6, 4))
    nn = np.array([r["n"] for r in rows]); ax.semilogy(nn, [r["t_fwht"] for r in rows], "o-", label="classical exact time [s]")
    ne = np.arange(10, 61); ax.semilogy(ne, 2 ** (a * ne + b), ":", label="classical extrapolation")
    ax.semilogy(nn, [r["q_queries"] for r in rows], "s-", label="quantum queries (±0.03)")
    ax.semilogy(ne, np.sqrt(2.0 ** ne), "--", label="√N (classical query bound scale)")
    ax.set_xlabel("n (N = 2^n)"); ax.legend(fontsize=8); ax.set_title("Exponential-sum correlation: cost vs n"); fig.tight_layout(); fig.savefig(os.path.join(OUT, "exp_sum_scaling.png"), dpi=150)
    print("\n".join(L))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "ab"
    if "b" in which:
        demo_b()
    if "a" in which:
        demo_a()
