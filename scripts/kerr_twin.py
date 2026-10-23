"""Matched comparison: quantum Kerr delay line (exact single-mode Lindblad per pulse) vs its mean-field twin
(the same model with the density matrix replaced by a coherent amplitude: d alpha/dt = -2i chi |alpha|^2 alpha
- kappa/2 alpha + eps), same D, chi, kappa, eps0, masks, same 3 features per pulse (<x>,<p>,<n>), same readout.
Also a shot-noise curve for the quantum version. Writes results/kerr_twin.json and prints a table."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qrcfit.tasks import all_tasks
from qrcfit.reservoirs import KerrDelayQ
from qrcfit.evaluate import fit_predict, shot_curve


def meanfield_run(R, u, dt=0.02):
    D = R.D; T = len(u); chi = R.chi; kappa = R.kappa
    al = np.zeros(D, complex); X = np.zeros((T, 3 * D))
    for t in range(T):
        inp = float(np.clip(np.mean(u[t]), 0, 1))
        al = np.roll(al, 1)
        eps = R.eps0 * inp * R.mask
        for _ in range(int(1 / dt)):  # RK2 over one round trip
            f = lambda a: -2j * chi * np.abs(a) ** 2 * a - 0.5 * kappa * a + eps
            k1 = f(al); al = al + dt * f(al + 0.5 * dt * k1)
        X[t] = np.concatenate([np.sqrt(2) * al.real, np.sqrt(2) * al.imag, np.abs(al) ** 2])
    return X


SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 3
out = {}
for seed in range(SEEDS):
    tasks = all_tasks(seed)
    for tn in ["narma10", "narma20", "mg10", "mg20", "xprod", "xor", "mc30", "lorenz_multi", "xprod_n5", "narma10_n5"]:
        t = tasks[tn]
        for D, chi, eps0, dim in [(30, 0.3, 0.5, 16), (30, 1.0, 0.5, 16), (30, 0.1, 1.5, 24), (100, 0.3, 0.5, 16), (30, 0.0, 0.5, 16)]:
            R = KerrDelayQ(D=D, chi=chi, kappa=0.05, eps0=eps0, dim=dim, seed=seed); R.chi, R.kappa, R.eps0 = chi, 0.05, eps0
            Xq, Vq = R.run(t["u"]); Xc = meanfield_run(R, t["u"])
            cq = shot_curve(Xq, Vq, t, np.random.default_rng(seed), [1e2, 1e4, 1e6, np.inf])
            res = dict(q_inf=cq[np.inf], q_1e4=cq[1e4], q_1e6=cq[1e6], meanfield=fit_predict(Xc, t), maxn=float(Xq[:, 2::3].max()))
            out[f"{tn}|D{D}_chi{chi}_eps{eps0}|s{seed}"] = res
            print(f"s{seed} {tn:12s} D={D:3d} chi={chi:.1f} eps0={eps0:.1f} | quantum inf={res['q_inf']:.4g} S1e4={res['q_1e4']:.3g} | mean-field twin={res['meanfield']:.4g}", flush=True)
json.dump(out, open(os.path.join(os.path.dirname(__file__), "..", "results", "kerr_twin.json"), "w"), indent=1)
# summary with quartiles
L = ["# Quantum Kerr delay vs mean-field twin (same parameters), median [IQR] over %d seeds" % SEEDS, "", "| task | config | quantum NMSE(∞) | mean-field twin | ratio twin/quantum |", "|---|---|---|---|---|"]
keys = sorted({k.rsplit("|", 1)[0] for k in out})
for k in keys:
    v = [out[f"{k}|s{s}"] for s in range(SEEDS)]
    qi = np.percentile([x["q_inf"] for x in v], [25, 50, 75]); mf = np.percentile([x["meanfield"] for x in v], [25, 50, 75])
    L.append(f"| {k.split('|')[0]} | {k.split('|')[1]} | {qi[1]:.3g} [{qi[0]:.3g}–{qi[2]:.3g}] | {mf[1]:.3g} [{mf[0]:.3g}–{mf[2]:.3g}] | {mf[1] / qi[1]:.2f} |")
open(os.path.join(os.path.dirname(__file__), "..", "results", "kerr_twin.md"), "w").write("\n".join(L) + "\n")
