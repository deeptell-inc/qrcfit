"""Equal-tuning-effort test (Pandey+ 2026 protocol) for the quantum Kerr delay line: random search over
(chi, kappa, eps0) with the SAME 20-draw budget and validation selection as the classical baselines, at matched
D (F = 3D). Compares with the tuned semiclassical kerr_delay baseline of the same D and with the best classical
of any size. Parallel over (task, seed). Usage: python scripts/tune_qkerr.py [seeds]. Writes results/tune_qkerr.json/.md."""
import json, os, sys
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qrcfit.tasks import all_tasks
from qrcfit.reservoirs import KerrDelayQ
from qrcfit.evaluate import val_test, shot_curve

ROOT = os.path.join(os.path.dirname(__file__), "..", "results")
TASKS = ["narma10", "mg10", "mc30", "xor_n5", "lorenz_multi", "narma20", "xprod_n5", "mg10_small"]
SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 3


def job(tn, seed):
    """Both D values for one (task, seed); classical baselines for an uncached seed are computed once in memory."""
    base = json.load(open(os.path.join(ROOT, "baselines.json")))
    t = all_tasks(seed)[tn]
    bl = base.get(f"{tn}|{seed}")
    if bl is None:
        from qrcfit.baselines import all_baselines
        bl = all_baselines(t, seed)
    res = {}
    for D in (30, 100):
        rng = np.random.default_rng(seed + 777)
        best = (np.inf, None, None, None)
        for b in range(20):
            chi, kappa, eps0 = 10 ** rng.uniform(-1.5, 0.5), 10 ** rng.uniform(-1.7, -0.3), 10 ** rng.uniform(-0.7, 0.3)
            R = KerrDelayQ(D=D, chi=chi, kappa=kappa, eps0=eps0, dim=16, seed=seed * 100 + b)
            X, V = R.run(t["u"])
            if not np.all(np.isfinite(X)) or X[:, 2::3].max() > 9:  # truncation guard (dim 16)
                continue
            val, test = val_test(X, t)
            if val < best[0]:
                best = (val, test, (chi, kappa, eps0), (X, V))
        X, V = best[3]
        c = shot_curve(X, V, t, np.random.default_rng(seed), [1e3, 1e4, np.inf])
        res[f"{tn}|D{D}|s{seed}"] = dict(q_test=best[1], q_1e3=c[1e3], q_1e4=c[1e4], params=best[2], kd_same_D=bl[f"kerr_delay:{D}"]["nmse"],
                                         cls_best=min(v["nmse"] for v in bl.values()), cls_name=min(bl, key=lambda k: bl[k]["nmse"]))
    return res


if __name__ == "__main__":
    out = {}
    with ProcessPoolExecutor(8) as ex:
        futs = [ex.submit(job, tn, s) for tn in TASKS for s in range(SEEDS)]
        for f in as_completed(futs):
            r = f.result(); out.update(r)
            for k, v in r.items():
                print(f"{k}: tuned-quantum={v['q_test']:.4g} (1e4 shots {v['q_1e4']:.3g}) kd_same_D={v['kd_same_D']:.4g} cls={v['cls_best']:.3g}", flush=True)
    json.dump(out, open(os.path.join(ROOT, "tune_qkerr.json"), "w"), indent=1)
    L = ["# Equal-tuning-effort test: tuned quantum Kerr delay vs tuned semiclassical kerr_delay at matched D, median [IQR] over %d seeds" % SEEDS, "",
         "| task | D | tuned quantum | quantum @1e4 shots | tuned kerr_delay (same D) | ratio Q/classical | best classical (any size) |", "|---|---|---|---|---|---|---|"]
    for tn in TASKS:
        for D in (30, 100):
            v = [out[f"{tn}|D{D}|s{s}"] for s in range(SEEDS)]
            q = np.percentile([x["q_test"] for x in v], [25, 50, 75]); q4 = np.median([x["q_1e4"] for x in v]); kd = np.percentile([x["kd_same_D"] for x in v], [25, 50, 75]); cb = np.median([x["cls_best"] for x in v])
            L.append(f"| {tn} | {D} | {q[1]:.3g} [{q[0]:.3g}–{q[2]:.3g}] | {q4:.3g} | {kd[1]:.3g} [{kd[0]:.3g}–{kd[2]:.3g}] | {q[1] / kd[1]:.2f} | {cb:.3g} |")
    open(os.path.join(ROOT, "tune_qkerr.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))
