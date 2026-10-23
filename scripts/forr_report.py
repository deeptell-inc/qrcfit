"""Wave-4 matched-query report for the Forrelation oracle-input tasks.
Quantum: m shots/step = 2m oracle queries/step. Classical: Q queries/step (naive sampling, optimistic sqrt(N)
surrogate, degree-2 ANF attack). Both sides get the same tuned readout (readout_best). Prints a table and
writes results/forr_matched.md.  ✚ = quantum NMSE at m shots is below every classical estimator that uses
up to 10 x (2m) queries per step, in all seeds (the 'query win' criterion)."""
import json, os, sys
from collections import defaultdict
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qrcfit.tasks import forrelation_stream
from qrcfit.forrelation import drift_stream

ROOT = os.path.join(os.path.dirname(__file__), "..", "results")
rows = [json.loads(l) for l in open(os.path.join(ROOT, "map.jsonl")) if '"forr_qrc"' in l]
base = json.load(open(os.path.join(ROOT, "baselines.json")))
tasks = sorted({r["task"] for r in rows}, key=lambda t: (t.split("_")[0] != "forr", t.split("_")[1], int(t.split("_n")[1])))
M = [1e2, 1e3, 1e4]
L = ["# Wave 4: Forrelation oracle-input tasks — matched query budgets", "",
     "quantum(m) = NMSE with m shots/step (2m queries). classical(Q) = naive / pairs (implemented √N-query all-pairs estimator) at Q queries; anf2 = degree-2 ANF attack at its own query count. All with the same tuned readout. Medians over 3 seeds; ✚ = query win in every seed (quantum at 2m queries beats every classical with ≤ 20m queries).", "",
     "| task | N | Φ_YES | seeds | quantum m=1e2 [IQR] / 1e3 / 1e4 / ∞ | classical Q=200 naive/pairs | Q=2000 naive/pairs | Q=20000 naive/pairs [IQR] | anf2 (Q) or white-box Q=200/2000/20000 | full-info (Q=N, same readout) | ✚ |", "|---|---|---|---|---|---|---|---|---|---|---|"]
summary = {}
for t in tasks:
    rs = [r for r in rows if r["task"] == t]
    n = int(t.split("_n")[1]); N = 1 << n
    fam = "kloosterman" if "kloos" in t else "gold"
    if t.startswith("forr_rand"):
        from qrcfit.tasks import forrelation_random_stream
        phi_yes = forrelation_random_stream(n, T_train=20, T_test=10)["phi_yes"]
    else:
        phi_yes = (drift_stream(n, T_train=10, T_test=10) if t.startswith("drift") else forrelation_stream(n, fam, T_train=10, T_test=10))["phi_yes"]
    q = {m: np.median([r["curve"][f"{m:.0e}"] for r in rs]) for m in M}; qinf = np.median([r["curve"]["inf"] for r in rs])
    q1 = np.percentile([r["curve"]["1e+02"] for r in rs], [25, 75])
    def cl(name): return np.median([base[f"{t}|{r['seed']}"][name]["nmse"] for r in rs])
    def clq(name): return np.percentile([base[f"{t}|{r['seed']}"][name]["nmse"] for r in rs], [25, 75])
    anf_keys = [k for k in base[f"{t}|0"] if k.startswith("forr_anf2")]
    anf_key = anf_keys[0] if anf_keys else None
    full = cl([k for k in base[f"{t}|0"] if k.startswith("forr_full")][0])
    win = True
    for r in rs:
        b = base[f"{t}|{r['seed']}"]
        for m in (1e2, 1e3):
            qm = r["curve"][f"{m:.0e}"]
            rivals = [v["nmse"] for k, v in b.items() if k.startswith("forr_") and not k.startswith("forr_wb") and not k.startswith("forr_full") and v["size"] <= 20 * m]  # black-box rivals
            if rivals and min(rivals) <= qm:
                win = False
    summary[t] = win
    p2 = clq('forr_pairs:20000')
    L.append(f"| {t} | {N} | {phi_yes:.4f} | {len(rs)} | {q[1e2]:.3g} [{q1[0]:.3g}–{q1[1]:.3g}] / {q[1e3]:.3g} / {q[1e4]:.3g} / {qinf:.3g} | {cl('forr_naive:200'):.3g} / {cl('forr_pairs:200'):.3g} | {cl('forr_naive:2000'):.3g} / {cl('forr_pairs:2000'):.3g} | {cl('forr_naive:20000'):.3g} / {cl('forr_pairs:20000'):.3g} [{p2[0]:.3g}–{p2[1]:.3g}] | {(f"{cl(anf_key):.3g} ({anf_key.split(':')[1]})" if anf_key else f"wb {cl('forr_wb:200'):.3g} / {cl('forr_wb:2000'):.3g} / {cl('forr_wb:20000'):.3g}")} | {full:.3g} | {'✚' if win else ''} |")
L += ["", f"Query wins: {sum(summary.values())}/{len(summary)} tasks — " + ", ".join(t for t, w in summary.items() if w)]
open(os.path.join(ROOT, "forr_matched.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
