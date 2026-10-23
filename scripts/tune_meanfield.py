"""Equal-tuning-effort test for the MEAN-FIELD ODE TWIN of the quantum Kerr delay line (the model of
scripts/kerr_twin.py::meanfield_run), with the SAME 20-draw search, rng, domain, masks and photon guard as
scripts/tune_qkerr.py. Writes results/tune_meanfield.json (checkpoint per task/D/seed). Added after the adversarial
review panel pointed out that the tuned semiclassical kerr_delay baseline is a different classical model."""
import json, os, sys
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qrcfit.tasks import all_tasks
from qrcfit.evaluate import val_test

ROOT = os.path.join(os.path.dirname(__file__), "..", "results")
OUT = os.path.join(ROOT, "tune_meanfield.json")
TASKS = ["narma10", "mg10", "mc30", "xor_n5", "lorenz_multi", "narma20", "xprod_n5", "mg10_small"]


def meanfield_run(D, chi, kappa, eps0, mask, u, dt=0.02):  # verbatim dynamics of scripts/kerr_twin.py::meanfield_run
    T = len(u); al = np.zeros(D, complex); X = np.zeros((T, 3 * D))
    for t in range(T):
        inp = float(np.clip(np.mean(u[t]), 0, 1)); al = np.roll(al, 1); eps = eps0 * inp * mask
        for _ in range(int(1 / dt)):
            f = lambda a: -2j * chi * np.abs(a) ** 2 * a - 0.5 * kappa * a + eps
            k1 = f(al); al = al + dt * f(al + 0.5 * dt * k1)
        X[t] = np.concatenate([np.sqrt(2) * al.real, np.sqrt(2) * al.imag, np.abs(al) ** 2])
    return X


def job(tn, D, seed):
    t = all_tasks(seed)[tn]; rng = np.random.default_rng(seed + 777)
    best = (np.inf, None, None)
    for b in range(20):
        chi, kappa, eps0 = 10 ** rng.uniform(-1.5, 0.5), 10 ** rng.uniform(-1.7, -0.3), 10 ** rng.uniform(-0.7, 0.3)
        mask = np.random.default_rng(seed * 100 + b).uniform(-1, 1, D)  # same mask draw as KerrDelayQ(seed=seed*100+b)
        X = meanfield_run(D, chi, kappa, eps0, mask, t["u"])
        if not np.all(np.isfinite(X)) or X[:, 2::3].max() > 9:
            continue
        val, test = val_test(X, t)
        if val < best[0]:
            best = (val, test, (chi, kappa, eps0))
    return tn, D, seed, dict(mf_test=best[1], params=best[2])


if __name__ == "__main__":
    out = json.load(open(OUT)) if os.path.exists(OUT) else {}
    tq = json.load(open(os.path.join(ROOT, "tune_qkerr.json")))
    jobs = [(tn, D, s) for tn in TASKS for D in (30, 100) for s in range(10) if f"{tn}|D{D}|s{s}" not in out and f"{tn}|D{D}|s{s}" in tq]
    with ProcessPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 6) as ex:
        futs = [ex.submit(job, *j) for j in jobs]
        for f in as_completed(futs):
            tn, D, s, rec = f.result(); r = tq[f"{tn}|D{D}|s{s}"]
            rec.update(q_test=r["q_test"], kd_same_D=r["kd_same_D"], cls_best=r["cls_best"])
            out[f"{tn}|D{D}|s{s}"] = rec
            json.dump(out, open(OUT, "w"), indent=1)
            print(f"{tn:12s} D={D:3d} s{s} tuned mean-field={rec['mf_test']:.4g} | tuned quantum={r['q_test']:.4g} | tuned kerr_delay={r['kd_same_D']:.4g}", flush=True)
    print("DONE")
