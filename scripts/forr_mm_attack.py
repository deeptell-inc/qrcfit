"""Exact adaptive black-box attack on the fresh Maiorana–McFarland streams (fixed coordinate split, no affine mixing):
k+1 queries of f_t recover pi_t(0); k+1 queries of g_t recover r = pi_t^{-1}(pi_t(0) xor alpha) (r != 0 -> NO); then for
each basis y = u_j, k+1 queries of f_t give pi_t(u_j) and one query of g_t gives beta_j. YES iff alpha = beta = 0, which
for a bent pair is Phi_t exactly (1 or 0). Worst case k^2+4k+2 queries. Proposed by the adversarial review panel.
Writes results/forr_mm_attack.json (per task|seed: max |Phi_hat - Phi|, max/mean queries, NMSE through readout_best)."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from qrcfit.tasks import forrelation_mm_stream
from qrcfit.forrelation import fresh_pair
from qrcfit.baselines import readout_best
ROOT = os.path.join(os.path.dirname(__file__), "..", "results"); OUT = os.path.join(ROOT, "forr_mm_attack.json")


def attack(f, g, k):
    q = [0]
    F = lambda x, y: (q.__setitem__(0, q[0] + 1), f[x + (y << k)])[1]
    G = lambda a, b: (q.__setitem__(0, q[0] + 1), g[a + (b << k)])[1]
    f00 = F(0, 0); p0 = 0
    for j in range(k):
        if F(1 << j, 0) * f00 < 0:
            p0 |= 1 << j
    g0 = G(p0, 0); r = 0
    for j in range(k):
        if G(p0, 1 << j) * g0 < 0:
            r |= 1 << j
    if r != 0:
        return 0.0, q[0]
    for j in range(k):
        y = 1 << j; f0y = F(0, y); py = 0
        for i in range(k):
            if F(1 << i, y) * f0y < 0:
                py |= 1 << i
        if G(py, 0) * f0y < 0:
            return 0.0, q[0]
    return 1.0, q[0]


if __name__ == "__main__":
    out = json.load(open(OUT)) if os.path.exists(OUT) else {}
    base = json.load(open(os.path.join(ROOT, "baselines.json")))
    for n in (10, 12, 14, 16):
        seeds = sorted(int(k.split("|")[1]) for k in base if k.startswith(f"forr_mm_n{n}|"))
        for seed in seeds:
            key = f"forr_mm_n{n}|{seed}"
            if key in out:
                continue
            task = forrelation_mm_stream(n, seed=seed); T = len(task["phi"]); est = np.zeros(T); qs = np.zeros(T, int)
            for t in range(T):
                ft, gt = fresh_pair(task, t); est[t], qs[t] = attack(ft, gt, n // 2)
            nm, name = readout_best(est[:, None], task, seed)
            out[key] = dict(max_abs_err_phi=float(np.max(np.abs(est - task["phi"]))), max_queries=int(qs.max()), mean_queries=float(qs.mean()), nmse=nm, readout=name)
            json.dump(out, open(OUT, "w"), indent=1); print(key, out[key], flush=True)
    print("DONE")
