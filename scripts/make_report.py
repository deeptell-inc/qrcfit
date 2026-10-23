"""Summarise results/map.jsonl (+ results/baselines.json) into map.md and map.png.

All win criteria are recomputed here from the raw curves, so definitions can be changed post hoc.
  q        : NMSE of the quantum reservoir with exact expectations (S = inf)
  cls      : best tuned classical over all families and sizes
  eqW      : best tuned classical among baselines with <= F_q features (equal readout cost)
  S*_eq    : smallest shot count with NMSE_q(S) <= eqW ;  S*_cls : same against cls
  M*       : smallest ESN size with NMSE <= q  (None = no ESN size up to 1000 reaches it)
  A        : accuracy win vs cls in every seed            a : accuracy win vs eqW in every seed
  W        : experiment restarts per time step needed by the readout (30 for projective readout, 1 for an
             online weak-measurement readout, configs named *_weak*); shot-ops = S* × W
  ★ scale  : a  and  S*_eq × W <= 3e5 shot-ops  and  (M* unreachable or M*/F_q >= 10)
  ◆ both   : A  and  S*_cls <= 1e4
Colour = log10(q / cls) (left) and log10(q / eqW) (right); blue = quantum more accurate.
"""
import json, os, sys
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "results")
SHOTS = [1e2, 1e3, 1e4, 1e5, 1e6]
rows = [json.loads(l) for l in open(os.path.join(ROOT, "map.jsonl"))]
base = json.load(open(os.path.join(ROOT, "baselines.json")))


def derive(r):
    b = base[f"{r['task']}|{r['seed']}"]
    Fq = r["F"]; q = r["curve"]["inf"]
    cls = min(v["nmse"] for v in b.values()); cls_name = min(b, key=lambda k: b[k]["nmse"])
    Fmin = min(v["F"] for v in b.values())
    eqc = {k: v for k, v in b.items() if v["F"] <= max(Fq, Fmin)}
    eqW = min(v["nmse"] for v in eqc.values()); eq_name = min(eqc, key=lambda k: eqc[k]["nmse"])

    def sstar(th):
        for S in SHOTS:
            if r["curve"][f"{S:.0e}"] <= th:
                return S
        return np.inf if q > th else 1e7  # 1e7 = only exact expectations reach it
    esn = sorted((v["size"], v["nmse"]) for v in b.values() if v["family"] == "esn")
    M = next((m for m, e in esn if e <= q), np.inf)
    return dict(q=q, cls=cls, cls_name=cls_name, eqW=eqW, eq_name=eq_name, Fq=Fq, S_eq=sstar(eqW), S_cls=sstar(cls), M=M,
                A=q < cls, a=q < eqW, curve=r["curve"])


cells = defaultdict(list)
for r in rows:
    cells[(r["config"], r["task"])].append(derive(r))
configs = sorted({c for c, _ in cells}, key=lambda c: (c.split("_")[0], c))
tasks = sorted({t for _, t in cells})


def agg(ds, cfg=""):
    med = lambda k: float(np.median([d[k] for d in ds]))
    out = dict(q=med("q"), cls=med("cls"), eqW=med("eqW"), S_eq=med("S_eq"), S_cls=med("S_cls"), M=med("M"), Fq=ds[0]["Fq"], n=len(ds),
               cls_name=ds[0]["cls_name"], eq_name=ds[0]["eq_name"],
               A=all(d["A"] for d in ds), a=all(d["a"] for d in ds))
    out["ratio"] = np.log10(out["q"] / out["cls"]); out["ratio_eq"] = np.log10(out["q"] / out["eqW"])
    out["W"] = 1 if ("weak" in cfg or cfg.startswith("forr")) else 30
    # realistic-budget accuracy: 3e5 shot-ops -> S=1e4 for projective readout (W=30), S=1e5 for weak (W=1)
    kb = "1e+04" if out["W"] == 30 else "1e+05"
    out["q_budget"] = float(np.median([d["curve"][kb] for d in ds]))
    out["ratio_budget"] = np.log10(out["q_budget"] / out["cls"])
    out["scale"] = out["a"] and out["S_eq"] * out["W"] <= 3e5 and (np.isinf(out["M"]) or out["M"] / out["Fq"] >= 10)
    out["both"] = out["A"] and out["S_cls"] * out["W"] <= 3e5
    return out


A = {k: agg(v, k[0]) for k, v in cells.items()}

fig, axes = plt.subplots(1, 3, figsize=(2 + 0.9 * len(tasks) * 3, 0.45 * len(configs) + 2), gridspec_kw=dict(wspace=0.5))
for ax, key, title in [(axes[0], "ratio", "log10 NMSE_q(∞) / best classical (any size)   ◆ = A & S*_cls×W≤3e5"),
                       (axes[1], "ratio_eq", "log10 NMSE_q(∞) / best classical at ≤ F_q weights   ★ = scale win"),
                       (axes[2], "ratio_budget", "log10 NMSE_q(3e5 shot-ops) / best classical (any size)")]:
    Mx = np.array([[A[(c, t)][key] if (c, t) in A else np.nan for t in tasks] for c in configs])
    im = ax.imshow(Mx, cmap="RdBu_r", vmin=-1.5, vmax=1.5, aspect="auto")
    ax.set_xticks(range(len(tasks))); ax.set_xticklabels(tasks, rotation=60, ha="right", fontsize=8)
    ax.set_yticks(range(len(configs))); ax.set_yticklabels(configs, fontsize=8)
    ax.set_title(title, fontsize=9)
    for i, c in enumerate(configs):
        for j, t in enumerate(tasks):
            if (c, t) not in A:
                continue
            a = A[(c, t)]
            if key == "ratio_budget":
                ax.text(j, i, f"{a['q_budget']:.2g}", ha="center", va="center", fontsize=5.5, color="k")
                continue
            S = a["S_cls"] if key == "ratio" else a["S_eq"]
            s = "" if np.isinf(S) else ("S∞" if S >= 1e7 else f"S{int(np.log10(S))}")
            m = "" if np.isinf(a["M"]) else f"M{int(a['M'])}"
            mark = ("◆ " if (key == "ratio" and a["both"]) else "") + ("★ " if (key == "ratio_eq" and a["scale"]) else "")
            ax.text(j, i, (mark + s + " " + m).strip(), ha="center", va="center", fontsize=5.5, color="k")
    plt.colorbar(im, ax=ax, fraction=0.03)
fig.savefig(os.path.join(ROOT, "map.png"), dpi=160, bbox_inches="tight")

L = ["# QRC vs tuned classical: map", "",
     f"{len(rows)} cells, {len(configs)} quantum configs × {len(tasks)} tasks, seeds per cell = {min(a['n'] for a in A.values())}–{max(a['n'] for a in A.values())}.", "",
     __doc__.split("\n", 2)[2].strip(), "",
     "| config | task | F_q | q | q@3e5 ops | cls (best) | eqW (best ≤F_q) | S*_eq | S*_cls | W | M* | A | a | ★ | ◆ |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
fs = lambda S: "—" if np.isinf(S) else ("∞" if S >= 1e7 else f"{S:.0e}")
for c in configs:
    for t in tasks:
        if (c, t) not in A:
            continue
        a = A[(c, t)]
        L.append(f"| {c} | {t} | {a['Fq']} | {a['q']:.3g} | {a['q_budget']:.3g} | {a['cls']:.3g} ({a['cls_name']}) | {a['eqW']:.3g} ({a['eq_name']}) | {fs(a['S_eq'])} | {fs(a['S_cls'])} | {a['W']} | "
                 f"{'>1000' if np.isinf(a['M']) else int(a['M'])} | {'**Y**' if a['A'] else ''} | {'y' if a['a'] else ''} | {'★' if a['scale'] else ''} | {'◆' if a['both'] else ''} |")
L += ["", "## Wins by axis", ""]
for name, k in [("A: accuracy vs best classical (any size), all seeds", "A"), ("a: accuracy vs equal-readout-cost classical, all seeds", "a"),
                ("★ scale win", "scale"), ("◆ both (A and S*_cls × W ≤ 3e5)", "both")]:
    w = [(c, t) for (c, t), a in A.items() if a[k]]
    L.append(f"- **{name}:** {len(w)}/{len(A)} cells")
    byc = defaultdict(list)
    for c, t in w:
        byc[c].append(t)
    for c in configs:
        if byc.get(c):
            L.append(f"  - {c}: {', '.join(sorted(byc[c]))}")
L += ["", "## Best quantum config per task (median over seeds)", "", "| task | best quantum (F_q) | q | cls (best) | q/cls | eqW | q/eqW |", "|---|---|---|---|---|---|---|"]
for t in tasks:
    cands = [(A[(c, t)]["q"], c) for c in configs if (c, t) in A]
    q, c = min(cands); a = A[(c, t)]
    L.append(f"| {t} | {c} ({a['Fq']}) | {q:.3g} | {a['cls']:.3g} ({a['cls_name']}) | {q / a['cls']:.2g} | {a['eqW']:.3g} | {q / a['eqW']:.2g} |")
open(os.path.join(ROOT, "map.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L[-30:]))
