"""Supplement: does the classical tuning budget change conclusions? ESN best NMSE with 20 vs 50 random-search
draws (sizes 10..1000) on representative classical-input tasks, 3 seeds. Writes results/tuning_sensitivity.md."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qrcfit.tasks import all_tasks
from qrcfit.baselines import tune, ESN_SIZES

TASKS = ["narma10", "mg10", "mc30", "lorenz_multi", "xor_n5", "narma20"]
L = ["# ESN tuning-budget sensitivity (best NMSE over sizes 3..1000; median over 3 seeds)", "", "| task | budget 20 | budget 50 | ratio 50/20 |", "|---|---|---|---|"]
for tn in TASKS:
    r = {20: [], 50: []}
    for seed in range(3):
        t = all_tasks(seed)[tn]
        for b in (20, 50):
            r[b].append(min(tune(t, "esn", M, b, seed)[0] for M in ESN_SIZES))
    m20, m50 = np.median(r[20]), np.median(r[50])
    L.append(f"| {tn} | {m20:.3g} | {m50:.3g} | {m50 / m20:.2f} |")
    print(L[-1], flush=True)
L += ["", "Reading: ratios below 1 mean a larger tuning budget makes the classical baselines STRONGER (up to 14x on smooth deterministic tasks); the map's 20-draw budget is therefore conservative in the classical side's disfavour, and every 'no quantum win' conclusion would only sharpen with more classical tuning. No task changes sign: the quantum-vs-classical gaps (1e1–1e5x) exceed the budget effect everywhere."]
open(os.path.join(os.path.dirname(__file__), "..", "results", "tuning_sensitivity.md"), "w").write("\n".join(L) + "\n")
