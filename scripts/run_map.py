"""Build the QRC-vs-classical map.

For every (quantum config, task, seed):
  - exact-expectation NMSE and the finite-shot curve NMSE(S)
  - tuned classical baselines (ESN sizes, poly-NARX sizes, semiclassical Kerr delay RC), cached per (task, seed)
  - derived cell statistics:
      acc_win_best   : NMSE_q(inf) < best classical over ALL sizes/families
      acc_win_eqW    : NMSE_q(inf) < best classical among baselines with <= F_q features (equal readout cost)
      S_star         : smallest shot count S with NMSE_q(S) <= best classical at equal readout cost (inf if never)
      M_star         : smallest ESN size whose NMSE <= NMSE_q(inf)  (None if no ESN size reaches it)
      scale_win      : S_star <= 1e4 and (M_star is None or M_star > F_q)   [definition stated in the report]
Results are appended to results/map.jsonl (resumable) and summarised by scripts/make_report.py.
"""
import argparse, json, os, sys, time
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qrcfit.tasks import all_tasks, get_task
from qrcfit.reservoirs import quantum_configs
from qrcfit.baselines import all_baselines
from qrcfit.evaluate import shot_curve, SHOTS

ROOT = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(ROOT, exist_ok=True)
BASE_CACHE = os.path.join(ROOT, "baselines.json")
OUT = os.path.join(ROOT, "map.jsonl")


def _save_baselines(base):
    """Merge-with-disk under a file lock so that concurrent run_map processes cannot drop each other's entries."""
    import fcntl
    with open(BASE_CACHE + ".lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        on_disk = json.load(open(BASE_CACHE)) if os.path.exists(BASE_CACHE) else {}
        on_disk.update(base); base.update(on_disk)
        tmp = BASE_CACHE + ".tmp"
        json.dump(on_disk, open(tmp, "w")); os.replace(tmp, BASE_CACHE)
        fcntl.flock(lk, fcntl.LOCK_UN)


def baseline_job(tname, seed, quick):
    task = get_task(tname, seed, quick)
    t0 = time.time()
    b = all_baselines(task, seed, quick=quick)
    return tname, seed, b, time.time() - t0


def quantum_job(cname, tname, seed, quick):
    task = get_task(tname, seed, quick)
    res = quantum_configs(quick)[cname](seed)
    t0 = time.time()
    if getattr(res, "accepts", "u") == "task_shots":
        curve = res.shot_curve_task(task, SHOTS)
        return dict(config=cname, task=tname, seed=seed, F=int(res.F),
                    curve={("inf" if np.isinf(S) else f"{S:.0e}"): float(v) for S, v in curve.items()},
                    sim_seconds=time.time() - t0)
    if getattr(res, "accepts", "u") == "task":
        X, V = res.run_task(task)
    else:
        X, V = res.run(task["u"], task["rho_seq"]) if "rho_seq" in task else res.run(task["u"])
    curve = shot_curve(X, V, task, np.random.default_rng(seed + 7))
    return dict(config=cname, task=tname, seed=seed, F=int(X.shape[1]),
                curve={("inf" if np.isinf(S) else f"{S:.0e}"): float(v) for S, v in curve.items()},
                sim_seconds=time.time() - t0)


def _compat(cname, tname, allt):
    """Quantum-input reservoirs run only on quantum-input tasks and vice versa."""
    qin_cfg = cname.startswith("spin_qin"); forr_cfg = cname.startswith("forr")
    oracle_task = tname.startswith(("forr_", "drift_")); qin_task = tname.startswith("qin_")
    return qin_cfg == qin_task and forr_cfg == oracle_task


def derive(cell, base):
    Fq = cell["F"]
    q_inf = cell["curve"]["inf"]
    best_all = min(v["nmse"] for v in base.values())
    Fmin = min(v["F"] for v in base.values())
    eq = [v["nmse"] for v in base.values() if v["F"] <= max(Fq, Fmin)]
    best_eq = min(eq)
    S_star = None
    for S in SHOTS:
        key = "inf" if np.isinf(S) else f"{S:.0e}"
        if cell["curve"][key] <= best_eq:
            S_star = key; break
    esn = sorted(((v["size"], v["nmse"]) for v in base.values() if v["family"] == "esn"))
    M_star = next((m for m, e in esn if e <= q_inf), None)
    s_ok = S_star is not None and S_star != "inf" and float(S_star) <= 1e4
    cell.update(best_classical=best_all, best_classical_eqW=best_eq, best_classical_name=min(base, key=lambda k: base[k]["nmse"]),
                acc_win_best=bool(q_inf < best_all), acc_win_eqW=bool(q_inf < best_eq),
                S_star=S_star, M_star=M_star, scale_win=bool(s_ok and (M_star is None or M_star > Fq)))
    return cell


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--workers", type=int, default=max(1, os.cpu_count() - 2))
    ap.add_argument("--configs", nargs="*", default=None)
    ap.add_argument("--tasks", nargs="*", default=None)
    ap.add_argument("--pairs", nargs="*", default=None, help="restrict to exact config:task pairs")
    a = ap.parse_args()
    tasks = list(all_tasks(0, a.quick)) if not a.tasks else list(a.tasks)
    if a.tasks:
        tasks = [t for t in tasks if t in a.tasks]
    configs = list(quantum_configs(a.quick))
    if a.configs:
        configs = [c for c in configs if c in a.configs]
    pairs = None
    if a.pairs:
        pairs = {tuple(x.split(":")) for x in a.pairs}
        configs = sorted({c for c, _ in pairs}); tasks = sorted({t for _, t in pairs})
    seeds = list(range(a.seeds))

    base = json.load(open(BASE_CACHE)) if os.path.exists(BASE_CACHE) else {}
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            d = json.loads(line); done.add((d["config"], d["task"], d["seed"]))

    with ProcessPoolExecutor(a.workers) as ex:
        futs = [ex.submit(baseline_job, t, s, a.quick) for t in tasks for s in seeds if f"{t}|{s}" not in base]
        for f in as_completed(futs):
            t, s, b, dt = f.result(); base[f"{t}|{s}"] = b
            _save_baselines(base)
            print(f"[baseline] {t} seed{s} {dt:.0f}s best={min(v['nmse'] for v in b.values()):.3g}", flush=True)
        allt = None  # compatibility is decided from names (no suite build needed)
        futs = [ex.submit(quantum_job, c, t, s, a.quick) for c in configs for t in tasks for s in seeds
                if (c, t, s) not in done and _compat(c, t, allt) and (pairs is None or (c, t) in pairs)]
        with open(OUT, "a") as fo:
            for f in as_completed(futs):
                cell = f.result()
                cell = derive(cell, base[f"{cell['task']}|{cell['seed']}"])
                fo.write(json.dumps(cell) + "\n"); fo.flush()
                print(f"[q] {cell['config']:32s} {cell['task']:14s} s{cell['seed']} q={cell['curve']['inf']:.3g} "
                      f"cls={cell['best_classical']:.3g} eqW={cell['best_classical_eqW']:.3g} S*={cell['S_star']} M*={cell['M_star']} "
                      f"accW={int(cell['acc_win_best'])}/{int(cell['acc_win_eqW'])} scaleW={int(cell['scale_win'])} {cell['sim_seconds']:.0f}s", flush=True)


if __name__ == "__main__":
    main()
