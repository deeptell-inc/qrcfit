"""Paper figures for paper/main.tex, regenerated from results/ only.

Outputs (paper/):
  fig1_map.pdf        accounting rule + map (log10 q/cls and log10 q/eqW), the 4 Kloosterman ★ cells boxed
  fig2_shotwall.pdf   shot wall by readout family at the 3e5 shot-ops budget
  fig3_kerr.pdf       quantum Kerr delay line vs mean-field twin vs tuned semiclassical (kerr_twin.json, tune_qkerr.json)
  fig4_forrelation.pdf NMSE vs queries for Kloosterman / Gold, black-box vs white-box drift monitoring
  numbers.json        every number quoted in the text, with the file it came from
  tab_configs.tex, tab_tasks.tex   supplement tables
Vector PDF, Arial, PRX Quantum column widths (86 mm single, 178 mm double), 8 pt text.
Usage: python scripts/paper_figures.py            (run only after results/ is frozen; see paper/TODO.md)
Classical oracle estimators: the implemented sqrt(N)-query all-pairs estimator 'forr_pairs:<Q>' is used when present
(falls back to the retired 'forr_opt' surrogate with a loud warning); full-information classical = 'forr_full'.
"""
import json, os, sys
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
OUT = os.path.join(HERE, "..", "paper")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(HERE, ".."))

plt.rcParams.update({"font.family": ["Arial", "DejaVu Sans"], "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 6.5, "pdf.fonttype": 42,
                     "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6, "lines.linewidth": 1.0})
SINGLE, DOUBLE = 3.386, 7.008  # inches (86 mm, 178 mm)
SHOTS = ["1e+02", "1e+03", "1e+04", "1e+05", "1e+06"]
BUDGET = 3e5  # shot-ops budget used for ★

rows = [json.loads(l) for l in open(os.path.join(RES, "map.jsonl"))]
for extra in sys.argv[1:]:  # optional extra row files (same schema as map.jsonl), e.g. while results/map.jsonl is being regenerated
    rows += [json.loads(l) for l in open(extra)]
HAVE_FORR = any(r["config"] == "forr_qrc" for r in rows)
if not HAVE_FORR:
    print("WARNING: no forr_qrc rows in results/map.jsonl; Figs. 1, 2, 4 and the oracle-task numbers are kept from the previous run")
base = json.load(open(os.path.join(RES, "baselines.json")))
twin = json.load(open(os.path.join(RES, "kerr_twin.json")))
tune = json.load(open(os.path.join(RES, "tune_qkerr.json")))
numbers = {}


def note(key, value, src):
    numbers[key] = dict(value=value, source=src)
    return value


# ------------------------------------------------------------------ cell statistics (same definitions as make_report.py)
def derive(r):
    b = base[f"{r['task']}|{r['seed']}"]
    q = r["curve"]["inf"]; Fq = r["F"]
    cls = min(v["nmse"] for v in b.values())
    Fmin = min(v["F"] for v in b.values())
    eqW = min(v["nmse"] for k, v in b.items() if v["F"] <= max(Fq, Fmin))
    esn = sorted((v["size"], v["nmse"]) for v in b.values() if v["family"] == "esn")
    M = next((m for m, e in esn if e <= q), np.inf)

    def sstar(th):
        for S in SHOTS:
            if r["curve"][S] <= th:
                return float(S)
        return np.inf if q > th else 1e7
    return dict(q=q, cls=cls, eqW=eqW, Fq=Fq, M=M, S_eq=sstar(eqW), S_cls=sstar(cls), A=q < cls, a=q < eqW, curve=r["curve"])


cells = defaultdict(list)
for r in rows:
    cells[(r["config"], r["task"])].append(derive(r))


def W_of(cfg):
    return 1 if (("weak" in cfg and "weakT" not in cfg) or cfg.startswith("forr")) else 30  # weakT = weak T1/T2 relaxation (Hamiltonian encoding), not weak measurement


agg = {}
for (c, t), ds in cells.items():
    med = lambda k: float(np.median([d[k] for d in ds]))
    W = W_of(c)
    a = dict(q=med("q"), cls=med("cls"), eqW=med("eqW"), M=med("M"), S_eq=med("S_eq"), S_cls=med("S_cls"), Fq=ds[0]["Fq"], W=W,
             A=all(d["A"] for d in ds), a=all(d["a"] for d in ds), n=len(ds))
    kb = "1e+04" if W == 30 else "1e+05"  # S at the 3e5 shot-ops budget
    a["q_budget"] = float(np.median([d["curve"][kb] for d in ds]))
    a["scale_generic"] = a["a"] and a["S_eq"] * W <= BUDGET and (np.isinf(a["M"]) or a["M"] / a["Fq"] >= 10)  # make_report.py rule
    # On oracle tasks a/eqW/M* are undefined: the ANF stream is stored with F=0, no ESN family is run, and the quantum
    # stream's tuned readout is not charged (adversarial panel, manuscript-REVIEW.md); ★ is therefore reported only on
    # classical-input tasks, and oracle tasks use the query-matched criterion ✚.
    a["scale"] = a["scale_generic"] and not (t.startswith("forr") or t.startswith("drift"))
    a["both"] = a["A"] and a["S_cls"] * W <= BUDGET
    agg[(c, t)] = a

configs = sorted({c for c, _ in agg}, key=lambda c: (c.split("_")[0], c))
tasks = sorted({t for _, t in agg})
cls_tasks = [t for t in tasks if not (t.startswith("forr") or t.startswith("drift"))]
orc_tasks = [t for t in tasks if t.startswith("forr") or t.startswith("drift")]
cls_pairs = [k for k in agg if k[1] in cls_tasks]
note("n_cells", len(rows), "results/map.jsonl (line count)")
note("n_configs", len(configs), "results/map.jsonl")
note("n_tasks", len(tasks), "results/map.jsonl")
note("n_pairs_total", len(agg), "results/map.md 'Wins by axis' denominator")
note("seeds_per_cell", dict(classical_input_min=min(a["n"] for k, a in agg.items() if k[1] in cls_tasks), classical_input_max=max(a["n"] for k, a in agg.items() if k[1] in cls_tasks), classical_input_pairs_with_10=sum(a["n"] >= 10 for k, a in agg.items() if k[1] in cls_tasks), oracle=min(a["n"] for k, a in agg.items() if k[1] in orc_tasks) if orc_tasks else None), "results/map.jsonl")
note("n_pairs_classical_input", len(cls_pairs), "results/map.jsonl (config,task) pairs excluding forr_/drift_ tasks")
note("n_configs_classical_input", len({c for c, _ in cls_pairs}), "results/map.jsonl")
note("n_tasks_classical_input", len(cls_tasks), "results/map.jsonl")
note("n_tasks_oracle", len(orc_tasks), "results/map.jsonl")
note("A_wins", sum(a["A"] for a in agg.values()), "results/map.md 'Wins by axis'")
note("a_wins", sum(a["a"] for a in agg.values()), "results/map.md 'Wins by axis'")
note("a_wins_classical_input", sum(agg[k]["a"] for k in cls_pairs), "results/map.jsonl")
note("star_wins", sum(a["scale"] for a in agg.values()), "★ restricted to classical-input tasks (manuscript-REVIEW.md fix 3)")
note("star_wins_generic_rule", sum(a["scale_generic"] for a in agg.values()), "generic make_report.py rule applied to all tasks (counts the oracle cells, where a/eqW/M* are undefined; the manuscript reports ★ = 0)")
note("star_cells_generic_rule", sorted(f"{c}|{t}" for (c, t), a in agg.items() if a["scale_generic"]), "results/map.md")
note("both_wins", sum(a["both"] for a in agg.values()), "results/map.md 'Wins by axis'")
rat = [np.log10(agg[k]["q"] / agg[k]["cls"]) for k in cls_pairs]
note("median_log10_q_over_cls_classical_input", round(float(np.median(rat)), 2), "results/map.jsonl + baselines.json")
note("iqr_log10_q_over_cls_classical_input", [round(float(np.percentile(rat, 25)), 2), round(float(np.percentile(rat, 75)), 2)], "results/map.jsonl + baselines.json")
aw = [k for k in cls_pairs if agg[k]["a"]]
note("a_win_eqW_over_q_range_classical_input", [round(min(agg[k]["eqW"] / agg[k]["q"] for k in aw), 2), round(max(agg[k]["eqW"] / agg[k]["q"] for k in aw), 1)], "results/map.jsonl + baselines.json")
note("a_win_S_eq_le_1e4_count", sum(agg[k]["S_eq"] <= 1e4 for k in aw), "results/map.jsonl")
note("a_win_M_star_max", max(agg[k]["M"] for k in aw if np.isfinite(agg[k]["M"])), "results/map.jsonl + baselines.json")
note("a_win_M_star_unreached", sum(np.isinf(agg[k]["M"]) for k in aw), "results/map.jsonl + baselines.json")
best_cls_names = defaultdict(int)
for r in rows:
    if r["task"] in cls_tasks:
        best_cls_names[r["best_classical_name"].split(":")[0]] += 1
note("best_classical_family_counts_classical_input", dict(best_cls_names), "results/map.jsonl best_classical_name")

# best quantum per task
bestq = {}
for t in tasks:
    q, c = min((agg[(c, t)]["q"], c) for c in configs if (c, t) in agg)
    bestq[t] = dict(config=c, q=q, cls=agg[(c, t)]["cls"], ratio=q / agg[(c, t)]["cls"], eqW=agg[(c, t)]["eqW"], Fq=agg[(c, t)]["Fq"])
note("best_quantum_per_task", {t: {k: (round(v, 6) if isinstance(v, float) else v) for k, v in d.items()} for t, d in bestq.items()}, "results/map.md 'Best quantum config per task'")

# ------------------------------------------------------------------ Fig. 1: accounting rule + map
SHORT = {"spin_reset": "reset", "spin_hamenc": "Hou", "spin_qin": "qin", "cv_gauss": "Gauss", "cv_kerr": "Kerr1", "cv2": "Kerr2",
         "qkerr_delay": "qKerrDL", "forr_qrc": "Forrelation"}


def short(c):
    for k, v in SHORT.items():
        if c.startswith(k):
            return v + c[len(k):]
    return c


if HAVE_FORR:
    fig = plt.figure(figsize=(DOUBLE, 8.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 5.2], hspace=0.08, wspace=0.55, left=0.17, right=0.985, top=0.985, bottom=0.075)
    ax0 = fig.add_subplot(gs[0, :]); ax0.axis("off")


    def box(ax, x, y, w, h, text, fc="#f2f2f2", fs=6.8, fam="Arial"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01", fc=fc, ec="k", lw=0.6, transform=ax.transAxes))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, transform=ax.transAxes, fontfamily=fam)


    def arrow(ax, x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), xycoords="axes fraction", textcoords="axes fraction",
                    arrowprops=dict(arrowstyle="->", lw=0.7))


    box(ax0, 0.00, 0.62, 0.16, 0.30, "quantum reservoir\n(exact density matrix)\n$F_q$ observables", "#dbe9f6", 6.2)
    box(ax0, 0.00, 0.08, 0.16, 0.30, "classical reservoir\nESN / poly-NARX / Kerr delay\nsizes $F\\leq1000$, 20-draw tuning", "#f6e3db", 6.2)
    box(ax0, 0.21, 0.62, 0.17, 0.30, "$S$ shots $\\times$ $W$ restarts\nshot-ops $=S\\,W$\n(projective $W{=}30$, online $W{=}1$)", "#dbe9f6", 6.2)
    box(ax0, 0.21, 0.08, 0.17, 0.30, "same ridge readout,\nvalidation-tuned $\\lambda$", "#eeeeee", 6.2)
    box(ax0, 0.43, 0.35, 0.14, 0.30, "NMSE$_q(S)$ vs\nNMSE$_{\\rm cls}$ (any size),\nNMSE$_{\\rm eqW}$ ($F\\leq F_q$)", "#eeeeee", 6.2)
    box(ax0, 0.62, 0.52, 0.38, 0.46, "A: $q(\\infty)<$ cls (all seeds)      a: $q(\\infty)<$ eqW (all seeds)\n$S^*$: shots to reach eqW     $M^*$: ESN size reaching $q(\\infty)$\n"
                                       "$\\bigstar$: a, $S^*W\\leq3{\\times}10^5$, and $M^*/F_q\\geq10$ or $M^*$ unreached\n◆: A and $S^*_{\\rm cls}W\\leq3{\\times}10^5$", "#fff4d6", 5.9, "DejaVu Sans")
    box(ax0, 0.62, 0.02, 0.38, 0.42, "oracle input: ✚ = quantum at $2m$ queries/step beats every\nblack-box classical estimator with $\\leq20m$ queries/step,\n$m\\in\\{10^2,10^3\\}$, all seeds", "#e2f0d9", 5.9, "DejaVu Sans")
    for (x0, y0, x1, y1) in [(0.16, 0.77, 0.21, 0.77), (0.16, 0.23, 0.21, 0.23), (0.38, 0.77, 0.43, 0.55), (0.38, 0.23, 0.43, 0.45), (0.57, 0.5, 0.62, 0.5)]:
        arrow(ax0, x0, y0, x1, y1)
    ax0.text(-0.19, 1.02, "(a)", transform=ax0.transAxes, fontsize=9, fontweight="bold", va="top")

    for j, (key, lab, panel) in enumerate([("cls", "$\\log_{10}$ NMSE$_q(\\infty)$ / best classical (any size)", "(b)"),
                                            ("eqW", "$\\log_{10}$ NMSE$_q(\\infty)$ / best classical at $F\\leq F_q$", "(c)")]):
        ax = fig.add_subplot(gs[1, j])
        Mx = np.array([[np.log10(agg[(c, t)]["q"] / agg[(c, t)][key]) if (c, t) in agg else np.nan for t in tasks] for c in configs])
        im = ax.imshow(Mx, cmap="RdBu_r", vmin=-2, vmax=2, aspect="auto", interpolation="nearest")
        ax.set_xticks(range(len(tasks))); ax.set_xticklabels(tasks, rotation=90, fontsize=5)
        ax.set_yticks(range(len(configs))); ax.set_yticklabels([short(c) for c in configs] if j == 0 else [], fontsize=5)
        ax.tick_params(length=1.5, pad=1)
        ax.set_title(lab, fontsize=7, pad=3)
        for i, c in enumerate(configs):
            for jj, t in enumerate(tasks):
                if (c, t) in agg and agg[(c, t)]["scale"]:
                    ax.add_patch(Rectangle((jj - 0.5, i - 0.5), 1, 1, fill=False, ec="k", lw=1.4))
                    ax.text(jj, i, "$\\bigstar$", ha="center", va="center", fontsize=5, color="k")
        ax.text(-0.42 if j == 0 else -0.06, 1.012, panel, transform=ax.transAxes, fontsize=9, fontweight="bold")
        cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02, aspect=40)
        cb.ax.tick_params(labelsize=6, length=1.5)
    fig.savefig(os.path.join(OUT, "fig1_map.pdf"))
    plt.close(fig)


# ------------------------------------------------------------------ Fig. 2: shot wall by readout family
FAM_ORDER = ["spin $z$", "spin $z{+}zz$", "spin Hou $xyz$", "spin online weak", "CV Gaussian cov.", "CV Kerr ($x,p,n$)", "Forrelation (1 bit)"]
FAM_COL = dict(zip(FAM_ORDER, ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#d62728", "#8c564b", "#000000"]))


def family(c):
    if c.startswith("forr"):
        return "Forrelation (1 bit)"
    if c.startswith("qkerr") or c.startswith("cv_kerr") or c.startswith("cv2"):
        return "CV Kerr ($x,p,n$)"
    if c.startswith("cv_gauss"):
        return "CV Gaussian cov."
    if "hamenc" in c:
        return "spin Hou $xyz$"  # includes the *_weakT variants (weak T1/T2 relaxation), which are projective readouts
    if "weak" in c:
        return "spin online weak"
    if "zz" in c:
        return "spin $z{+}zz$"
    return "spin $z$"


if HAVE_FORR:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(SINGLE, 4.6), gridspec_kw=dict(hspace=0.42, left=0.2, right=0.98, top=0.97, bottom=0.1))
    degr = defaultdict(list); curves = defaultdict(list)
    for (c, t), a in agg.items():
        f = family(c)
        degr[f].append((a["q"], a["q_budget"]))
        ds = cells[(c, t)]
        curves[f].append([np.median([d["curve"][S] / d["q"] for d in ds]) for S in SHOTS])
    for f in FAM_ORDER:
        v = np.array(degr[f])
        ax1.scatter(v[:, 0], v[:, 1], s=5, color=FAM_COL[f], alpha=0.65, lw=0, label=f, zorder=3)
    lim = (1e-5, 3)
    ax1.plot(lim, lim, "k-", lw=0.6); ax1.plot(lim, [10 * l for l in lim], "k--", lw=0.6); ax1.plot(lim, [100 * l for l in lim], "k:", lw=0.6)
    ax1.text(2e-5, 3e-4, "10×", fontsize=6, rotation=38); ax1.text(2e-5, 3e-3, "100×", fontsize=6, rotation=38)
    ax1.set_xscale("log"); ax1.set_yscale("log"); ax1.set_xlim(lim); ax1.set_ylim(1e-5, 3)
    ax1.set_xlabel("NMSE with exact expectations"); ax1.set_ylabel("NMSE at $3{\\times}10^5$ shot-ops")
    ax1.legend(loc="lower right", ncol=1, frameon=False, handletextpad=0.2, borderpad=0.2, markerscale=1.6)
    ax1.text(-0.25, 1.0, "(a)", transform=ax1.transAxes, fontsize=9, fontweight="bold")
    S = [1e2, 1e3, 1e4, 1e5, 1e6]
    fam_stats = {}
    for f in FAM_ORDER:
        cv = np.array(curves[f])
        med = np.median(cv, 0); p90 = np.percentile(cv, 90, 0)
        ax2.plot(S, med, "-o", ms=3, color=FAM_COL[f], label=f)
        ax2.plot(S, p90, ":", color=FAM_COL[f], lw=0.8)
        fam_stats[f] = dict(n_pairs=len(cv), median_ratio_1e4=round(float(med[2]), 2), p90_ratio_1e4=round(float(p90[2]), 1), max_ratio_1e4=round(float(cv[:, 2].max()), 1),
                            median_ratio_1e5=round(float(med[3]), 2), p90_ratio_1e5=round(float(p90[3]), 1), max_ratio_1e5=round(float(cv[:, 3].max()), 1))
    ax2.axvline(1e4, color="k", lw=0.6, ls="--"); ax2.axvline(1e5, color="k", lw=0.6, ls="--")
    ax2.text(1.1e4, 2e2, "$3{\\times}10^5$ shot-ops,\n$W{=}30$", fontsize=6); ax2.text(1.1e5, 2e2, "$W{=}1$", fontsize=6)
    ax2.set_xscale("log"); ax2.set_yscale("log"); ax2.set_ylim(0.8, 1e3)
    ax2.set_xlabel("shots per feature $S$"); ax2.set_ylabel("NMSE$(S)$ / NMSE$(\\infty)$")
    ax2.text(-0.25, 1.0, "(b)", transform=ax2.transAxes, fontsize=9, fontweight="bold")
    fig.savefig(os.path.join(OUT, "fig2_shotwall.pdf"))
    plt.close(fig)
    note("shot_degradation_by_family", fam_stats, "results/map.jsonl curves (median over seeds per (config,task), then over pairs); solid = median, dotted = 90th percentile")
    # degradation among the most accurate cells (q < 1e-2) by family: this is where the wall bites
    acc = defaultdict(list)
    for (c, t), a in agg.items():
        if a["q"] < 1e-2:
            acc[family(c)].append(a["q_budget"] / a["q"])
    note("shot_degradation_accurate_cells_q_lt_1e-2", {f: dict(n=len(v), median=round(float(np.median(v)), 1), min=round(float(min(v)), 2), max=round(float(max(v)), 1)) for f, v in acc.items()}, "results/map.jsonl: cells with median NMSE(inf) < 1e-2, ratio NMSE(budget)/NMSE(inf)")


# ------------------------------------------------------------------ Fig. 3: Kerr three-way
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(DOUBLE, 2.6), gridspec_kw=dict(wspace=0.4, left=0.09, right=0.99, top=0.9, bottom=0.26))
MK = {"D30_chi0.0_eps0.5": ("s", "#7f7f7f", "$D{=}30$, $\\chi{=}0$ (linear control)"), "D30_chi0.3_eps0.5": ("o", "#1f77b4", "$D{=}30$, $\\chi{=}0.3$"),
      "D30_chi1.0_eps0.5": ("^", "#ff7f0e", "$D{=}30$, $\\chi{=}1$"), "D30_chi0.1_eps1.5": ("v", "#2ca02c", "$D{=}30$, $\\chi{=}0.1$, bright"),
      "D100_chi0.3_eps0.5": ("D", "#d62728", "$D{=}100$, $\\chi{=}0.3$")}
twin_stats = {}
for cfg, (m, col, lab) in MK.items():
    xs, ys = [], []
    for tn in sorted({k.split("|")[0] for k in twin}):
        vs = [v for k, v in twin.items() if k.split("|")[0] == tn and k.split("|")[1] == cfg]
        if vs:
            xs.append(float(np.median([v["meanfield"] for v in vs]))); ys.append(float(np.median([v["q_inf"] for v in vs])))
    ax1.scatter(xs, ys, marker=m, s=18, color=col, label=lab, lw=0.5, ec="k", zorder=3)
    ratios = np.array(xs) / np.array(ys)
    twin_stats[cfg] = dict(n_tasks=len(xs), meanfield_over_quantum_min=round(float(ratios.min()), 2), meanfield_over_quantum_max=round(float(ratios.max()), 1), meanfield_over_quantum_median=round(float(np.median(ratios)), 2))
lim = (1e-3, 2)
ax1.plot(lim, lim, "k-", lw=0.6); ax1.set_xscale("log"); ax1.set_yscale("log"); ax1.set_xlim(lim); ax1.set_ylim(lim)
ax1.set_xlabel("NMSE, mean-field twin (identical $D,\\chi,\\kappa,\\varepsilon_0$, mask)"); ax1.set_ylabel("NMSE, quantum Kerr delay line")
ax1.legend(frameon=False, loc="upper left", handletextpad=0.2, borderpad=0.2)
ax1.text(-0.2, 1.03, "(a)", transform=ax1.transAxes, fontsize=9, fontweight="bold")
note("kerr_twin", twin_stats, "results/kerr_twin.json (median over 10 seeds, 10 tasks per configuration; same as results/kerr_twin.md); ratio = mean-field NMSE / quantum NMSE")
def twin_med(tc):
    vs = [v for k, v in twin.items() if k.rsplit("|", 1)[0] == tc]
    return dict(quantum=float(f"{np.median([v['q_inf'] for v in vs]):.3g}"), meanfield=float(f"{np.median([v['meanfield'] for v in vs]):.3g}"), n_seeds=len(vs))
note("kerr_twin_examples", {k: twin_med(k) for k in ["narma10|D30_chi0.3_eps0.5", "mg10|D30_chi0.3_eps0.5", "mg10|D100_chi0.3_eps0.5", "mc30|D100_chi0.3_eps0.5", "narma10|D30_chi0.0_eps0.5", "mg10|D30_chi0.0_eps0.5"]}, "results/kerr_twin.json (median over seeds; same as results/kerr_twin.md)")
note("kerr_twin_max_photon_number", [round(min(v["maxn"] for v in twin.values()), 2), round(max(v["maxn"] for v in twin.values()), 1)], "results/kerr_twin.json maxn")

TASKS_T = ["narma10", "narma20", "xor_n5", "xprod_n5", "mg10_small", "lorenz_multi", "mc30", "mg10"]
tune_stats = {}
x = np.arange(len(TASKS_T)); wdt = 0.38
for i, D in enumerate(["D30", "D100"]):
    r_kd, r_cls = [], []
    for tn in TASKS_T:
        recs = [v for k, v in tune.items() if k.startswith(f"{tn}|{D}|")]
        q = np.median([r["q_test"] for r in recs]); kd = np.median([r["kd_same_D"] for r in recs]); cb = np.median([r["cls_best"] for r in recs])
        r_kd.append(q / kd); r_cls.append(q / cb)
        tune_stats[f"{tn}|{D}"] = dict(tuned_quantum=float(f"{q:.4g}"), tuned_semiclassical_same_D=float(f"{kd:.4g}"), best_classical=float(f"{cb:.3g}"), ratio_q_over_semiclassical=float(f"{q / kd:.3g}"))
    ax2.bar(x + (i - 0.5) * wdt, r_kd, wdt, color=["#1f77b4", "#d62728"][i], label=f"tuned semiclassical, same $D$ ({D[1:]})", lw=0)
    ax2.scatter(x + (i - 0.5) * wdt, r_cls, marker="_", s=60, color="k", lw=1.0, zorder=4, label="best classical, any size" if i == 0 else None)
ax2.axhline(1, color="k", lw=0.6)
ax2.set_yscale("log"); ax2.set_ylim(0.5, 2e5)
ax2.set_xticks(x); ax2.set_xticklabels(TASKS_T, rotation=35, ha="right")
ax2.set_ylabel("NMSE ratio: tuned quantum / classical")
ax2.legend(frameon=False, loc="upper left", handletextpad=0.2, borderpad=0.2)
ax2.text(-0.26, 1.03, "(b)", transform=ax2.transAxes, fontsize=9, fontweight="bold")
fig.savefig(os.path.join(OUT, "fig3_kerr.pdf"))
plt.close(fig)
note("tune_qkerr", tune_stats, "results/tune_qkerr.json (median over 10 seeds; same as results/tune_qkerr.md)")

# ------------------------------------------------------------------ Fig. 4: Forrelation route
from qrcfit.forrelation import anf2_queries  # noqa: E402

if not HAVE_FORR:
    prev = json.load(open(os.path.join(OUT, "numbers.json"))) if os.path.exists(os.path.join(OUT, "numbers.json")) else {}
    for k, v in prev.items():
        if k.startswith(("forrelation", "query_wins", "drift_n", "kloos_n", "n_tasks_oracle", "star_", "a_wins", "A_wins", "both_wins", "n_cells", "n_configs", "n_tasks", "n_pairs_total", "shot_degradation")):
            numbers[k] = v

if HAVE_FORR:
    HAVE_MM = any(t.startswith("forr_mm") for t in orc_tasks)
    fig, axg = plt.subplots(2, 3, figsize=(DOUBLE, 4.4), gridspec_kw=dict(wspace=0.38, hspace=0.5, left=0.075, right=0.995, top=0.94, bottom=0.1))
    axes = [axg[0, 0], axg[0, 1], axg[0, 2], axg[1, 0], axg[1, 1], axg[1, 2]]  # rand, mm, kloos, gold, drift, Q* vs N
    QS = [20, 200, 2000, 20000]
    NCOL = {10: "#c6dbef", 12: "#6baed6", 14: "#2171b5", 16: "#08306b"}
    forr_stats = {}
    NCOL = {10: "#deebf7", 12: "#c6dbef", 14: "#9ecae1", 16: "#6baed6", 18: "#2171b5", 20: "#08306b"}
    SQRTN_KEY = "forr_pairs" if any(k.startswith("forr_pairs") for k in base[f"{orc_tasks[0]}|0"]) else "forr_opt"
    if SQRTN_KEY == "forr_opt":
        print("WARNING: 'forr_pairs' estimator not in baselines.json; using the retired 'forr_opt' surrogate (do not quote)")
    FORR_N = sorted({int(t.split("_n")[1]) for t in orc_tasks if t.startswith("forr_kloos")})


    def q_med(task, key):
        return float(np.median([r["curve"][key] for r in rows if r["config"] == "forr_qrc" and r["task"] == task]))


    def b_med(task, name):
        return float(np.median([v[name]["nmse"] for k, v in base.items() if k.startswith(task + "|") and name in v]))


    qstar = {}
    for ax, fam, title in [(axes[0], "rand", "Fresh random pairs"), (axes[1], "mm", "Fresh Maiorana--McFarland pairs"), (axes[2], "kloos", "Kloosterman (fixed public $f$)"), (axes[3], "gold", "Gold (quadratic phase)")]:
        if fam == "mm" and not HAVE_MM:
            ax.axis("off"); continue
        fam_n = [n for n in FORR_N if f"forr_{fam}_n{n}|0" in base]
        for n in fam_n:
            t = f"forr_{fam}_n{n}"
            qm = [q_med(t, k) for k in ["1e+02", "1e+03", "1e+04"]]
            ax.plot([200, 2000, 20000], qm, "-o", ms=3.5, color=NCOL[n], label=f"quantum, $n={n}$" if fam in ("rand", "mm") or n == max(fam_n) else None, zorder=4)
            opt = [b_med(t, f"{SQRTN_KEY}:{Q}") for Q in QS]; nai = [b_med(t, f"forr_naive:{Q}") for Q in QS]
            ax.plot(QS, opt, "--s", ms=3, color=NCOL[n], mfc="none", label=f"classical $\\sqrt{{N}}$ all-pairs, $n={n}$" if n == max(fam_n) else None)
            ax.plot(QS, nai, ":", color=NCOL[n], lw=0.8, label="classical naive sampling" if n == max(fam_n) else None)
            kf_path = os.path.join(RES, "forr_knownf.json")
            if os.path.exists(kf_path):
                kf = json.load(open(kf_path)); ks = [k for k in kf if k.startswith(t + "|")]
                if ks:
                    kfm = [float(np.median([kf[k][f"forr_knownf:{Q}"]["nmse"] for k in ks])) for Q in QS]
                    ax.plot(QS, kfm, "-x", ms=4, color=NCOL[n], lw=0.8, label="classical, $f$ public (known-$f$)" if n == max(fam_n) else None, zorder=4)
            Qa = anf2_queries(n); anf = b_med(t, f"forr_anf2:{Qa}")
            ax.plot([Qa], [anf], marker="*", ms=7, color=NCOL[n], mec="k", mew=0.4, ls="none", label="classical degree-2 ANF attack" if n == max(fam_n) else None, zorder=5)
            forr_stats[t] = dict(N=1 << n, quantum_m1e2_1e3_1e4=[float(f"{v:.3g}") for v in qm], quantum_exact=float(f"{q_med(t, 'inf'):.3g}"),
                                 sqrtN_estimator=SQRTN_KEY, sqrtN_Q20_200_2000_20000=[float(f"{v:.3g}") for v in opt], naive_Q20_200_2000_20000=[float(f"{v:.3g}") for v in nai], anf2=dict(Q=Qa, nmse=float(f"{anf:.3g}")))
            if fam in ("rand", "mm", "kloos"):
                qs_ = next((Q for Q, v in zip(QS, opt) if v <= qm[0]), np.inf)  # first classical budget whose median <= quantum at 200 queries
                lq, lo = np.log10(QS), np.log10(opt)
                qi = 10 ** np.interp(np.log10(qm[0]), lo[::-1], lq[::-1]) if qm[0] >= opt[-1] else np.inf  # log-log interpolated crossing
                qstar.setdefault(fam, []).append((n, qs_, qi))
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(12, 4e4); ax.set_ylim(1e-4, 2)
        ax.set_xlabel("oracle queries per step"); ax.set_title(title, fontsize=7.5)
    axes[0].set_ylabel("NMSE (mean of 3 targets)")
    for a_ in axes[:4]:
        if a_.axison:
            a_.legend(frameon=False, loc="lower left", handletextpad=0.2, borderpad=0.2, fontsize=5)
    ax = axes[4]
    for n, col in [(12, "#6baed6"), (16, "#08306b")]:
        t = f"drift_kloos_n{n}"
        qm = [q_med(t, k) for k in ["1e+02", "1e+03", "1e+04"]]
        opt = [b_med(t, f"{SQRTN_KEY}:{Q}") for Q in QS]; nai = [b_med(t, f"forr_naive:{Q}") for Q in QS]; wb = [b_med(t, f"forr_wb:{Q}") for Q in QS]
        ax.plot([200, 2000, 20000], qm, "-o", ms=3.5, color=col, label=f"quantum, $n={n}$", zorder=4)
        ax.plot(QS, opt, "--s", ms=3, mfc="none", color=col, label=f"black-box $\\sqrt{{N}}$ all-pairs, $n={n}$")
        ax.plot(QS, nai, ":", color=col, lw=0.8, label="black-box naive" if n == 16 else None)
        ax.plot(QS, wb, "-.^", ms=3, color=col, mfc="w", label=f"white-box (knows ideal $g$), $n={n}$")
        forr_stats[t] = dict(N=1 << n, quantum_m1e2_1e3_1e4=[float(f"{v:.3g}") for v in qm], quantum_exact=float(f"{q_med(t, 'inf'):.3g}"),
                             sqrtN_estimator=SQRTN_KEY, sqrtN_Q20_200_2000_20000=[float(f"{v:.3g}") for v in opt], naive_Q20_200_2000_20000=[float(f"{v:.3g}") for v in nai], whitebox_Q20_200_2000_20000=[float(f"{v:.3g}") for v in wb])
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(12, 4e4); ax.set_ylim(1e-4, 2)
    ax.set_xlabel("oracle queries per step"); ax.set_ylabel("NMSE (mean of 2 targets)"); ax.set_title("Drift monitoring (fixed $f$)", fontsize=8)
    ax.legend(frameon=False, loc="lower left", handletextpad=0.2, borderpad=0.2, fontsize=5)
    ax = axes[5]
    FC = {"rand": ("#08306b", "o", "fresh random"), "mm": ("#d62728", "s", "fresh Maiorana--McFarland"), "kloos": ("#7f7f7f", "^", "fixed Kloosterman")}
    for fam, pts in qstar.items():
        pts = sorted(pts); Ns = [1 << n for n, _, _ in pts]
        qi = [q for _, _, q in pts]; qs_ = [q for _, q, _ in pts]
        ax.plot([N_ for N_, q in zip(Ns, qi) if np.isfinite(q)], [q for q in qi if np.isfinite(q)], "-" + FC[fam][1], ms=4, color=FC[fam][0], label=FC[fam][2] + " (interpolated)")
        ax.plot([N_ for N_, q in zip(Ns, qs_) if np.isfinite(q)], [q for q in qs_ if np.isfinite(q)], FC[fam][1], ms=7, mfc="none", color=FC[fam][0], lw=0)
        for N_, q in zip(Ns, qi):
            if not np.isfinite(q):
                ax.annotate("", xy=(N_, 3.5e4), xytext=(N_, 2e4), arrowprops=dict(arrowstyle="->", color=FC[fam][0], lw=0.8))
    Nn = np.logspace(3, 6.3, 50); v = (1 - 0.8 ** 2) / 100
    ax.plot(Nn, (2 / v) * (1 + np.sqrt(1 + Nn * v)), "k--", lw=0.7, label="$4/Q+4N/Q^2=(1-\\Phi^2)/m$, $m{=}100$, $\\Phi{=}0.8$")
    slopes = {}
    for fam, pts in qstar.items():
        pp = [(1 << n, q) for n, _, q in pts if np.isfinite(q)]
        if len(pp) >= 2:
            slopes[fam] = dict(n_points=len(pp), exponent=round(float(np.polyfit(np.log10([x for x, _ in pp]), np.log10([y for _, y in pp]), 1)[0]), 2))
    note("query_crossover_exponent", slopes, "log-log slope of the interpolated Q* against N (paper/numbers.json query_crossover_by_family)")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(5e2, 2e6); ax.set_ylim(1e2, 5e4)
    ax.set_xlabel("$N=2^n$"); ax.set_ylabel("classical queries matching\nquantum at 200 queries")
    ax.legend(frameon=False, loc="lower right", handletextpad=0.2, borderpad=0.2, fontsize=5)
    note("query_crossover_by_family", {fam: [dict(n=n, Q_star_grid=(None if np.isinf(a_) else a_), Q_star_interp=(None if np.isinf(b_) else round(float(b_)))) for n, a_, b_ in sorted(pts)] for fam, pts in qstar.items()}, "results/baselines.json " + SQRTN_KEY + " medians vs quantum m=100 (map.jsonl); grid = first Q in {20,200,2000,20000} with median <= quantum; interp = log-log interpolation")
    for ax, p in zip(axes, "abcdef"):
        ax.text(-0.3, 1.05, f"({p})", transform=ax.transAxes, fontsize=9, fontweight="bold")
    fig.savefig(os.path.join(OUT, "fig4_forrelation.pdf"))
    plt.close(fig)
    for t in orc_tasks:
        if t in forr_stats and any(k.startswith("forr_full") for k in base[f"{t}|0"]):
            forr_stats[t]["full_info_same_grid"] = float(f"{b_med(t, next(k for k in base[f'{t}|0'] if k.startswith('forr_full'))):.3g}")
    note("forrelation", forr_stats, "results/map.jsonl (forr_qrc rows) + results/baselines.json; medians over all seeds (10 for Forrelation-family tasks); same as results/forr_matched.md")

    # ✚ query wins (same rule as scripts/forr_report.py)
    plus = {}
    for t in orc_tasks:
        win = True
        for r in [r for r in rows if r["config"] == "forr_qrc" and r["task"] == t]:
            s = r["seed"]; b = base[f"{t}|{s}"]
            for m in (1e2, 1e3):
                rivals = [v["nmse"] for k, v in b.items() if k.startswith("forr_") and not k.startswith(("forr_wb", "forr_full", "forr_knownf")) and v["size"] <= 20 * m]  # black-box rivals only (same predicate as review_numbers.per_seed_query_comparison)
                if rivals and min(rivals) <= r["curve"][f"{m:.0e}"]:
                    win = False
        plus[t] = win
    note("query_wins", dict(n=sum(plus.values()), of=len(plus), tasks=[t for t, w in plus.items() if w]), "results/forr_matched.md")
    # white-box vs quantum at equal queries, drift tasks
    for n in (12, 16):
        t = f"drift_kloos_n{n}"
        note(f"drift_n{n}_whitebox_over_quantum_at_200_2000_20000", [round(q_med(t, k) / b_med(t, f"forr_wb:{Q}"), 2) for k, Q in zip(["1e+02", "1e+03", "1e+04"], [200, 2000, 20000])], "results/map.jsonl + baselines.json")
    # query ratio: quantum queries for NMSE <= 0.01 vs classical opt queries for the same (log-interp)
    for n in (10, 12, 14, 16):
        t = f"forr_kloos_n{n}"
        qm = forr_stats[t]["quantum_m1e2_1e3_1e4"]; opt = forr_stats[t]["sqrtN_Q20_200_2000_20000"]
        # smallest classical Q with NMSE <= quantum NMSE at 200 queries (interpolated in log-log)
        target = qm[0]
        lq, lo = np.log10(QS), np.log10(opt)
        Qc = 10 ** np.interp(np.log10(target), lo[::-1], lq[::-1]) if target >= opt[-1] else np.inf
        note(f"kloos_n{n}_classical_queries_to_match_quantum_200", (round(float(Qc)) if np.isfinite(Qc) else ">20000"), "results/baselines.json " + SQRTN_KEY + " (log-log interpolation); quantum at 200 queries from map.jsonl")
        note(f"kloos_n{n}_sqrtN_over_2", round(np.sqrt(1 << n) / 2, 1), "arithmetic")


# ------------------------------------------------------------------ supplement tables
with open(os.path.join(OUT, "tab_configs.tex"), "w") as fh:
    fh.write("% generated by scripts/paper_figures.py from results/map.jsonl + baselines.json\n")
    fh.write("\\begin{tabular}{llrrr}\n\\hline config & readout family & $F_q$ & $W$ & med.\\ $\\log_{10} q/{\\rm cls}$ \\\\ \\hline\n")
    for c in configs:
        v = [np.log10(agg[(c, t)]["q"] / agg[(c, t)]["cls"]) for t in tasks if (c, t) in agg]
        fh.write(f"{c.replace('_', '\\_')} & {family(c).replace('$', '')} & {agg[(c, tasks[0]) if (c, tasks[0]) in agg else next(k for k in agg if k[0] == c)]['Fq']} & {W_of(c)} & {np.median(v):.2f} \\\\\n")
    fh.write("\\hline\n\\end{tabular}\n")
from qrcfit.tasks import all_tasks  # noqa: E402
TT = all_tasks(0)
with open(os.path.join(OUT, "tab_tasks.tex"), "w") as fh:
    fh.write("% generated by scripts/paper_figures.py from qrcfit/tasks.py, results/map.jsonl, results/baselines.json\n")
    fh.write("\\begin{tabular}{lrrrrlll}\n\\hline task & $d_{\\rm in}$ & $d_{\\rm out}$ & $T_{\\rm train}$ & $T_{\\rm test}$ & best quantum ($F_q$) & NMSE$_q$ & best classical (NMSE) \\\\ \\hline\n")
    for t in tasks:
        tk = TT[t]; bq = bestq[t]
        cname = min(base[f"{t}|0"], key=lambda k: base[f"{t}|0"][k]["nmse"])
        fh.write(f"{t.replace('_', '\\_')} & {tk['u'].shape[1]} & {tk['y'].shape[1]} & {tk['T_train']} & {tk['T_test']} & {bq['config'].replace('_', '\\_')} ({bq['Fq']}) & {bq['q']:.3g} & {cname.replace('_', '\\_')} ({bq['cls']:.3g}) \\\\\n")
    fh.write("\\hline\n\\end{tabular}\n")

json.dump(numbers, open(os.path.join(OUT, "numbers.json"), "w"), indent=1, default=float)
print(json.dumps({k: v["value"] for k, v in numbers.items() if not isinstance(v["value"], dict)}, indent=1, default=str))
print("figures written to", OUT)

# ------------------------------------------------------------------ axis effects quoted in the Results text
CLS_T = cls_tasks


def axis_med(cfg, ts=None):
    ts = ts or CLS_T
    return round(float(np.median([np.log10(agg[(cfg, t)]["q"] / agg[(cfg, t)]["cls"]) for t in ts if (cfg, t) in agg])), 2)


def cell(cfg, t):
    a = agg[(cfg, t)]
    return dict(q=float(f"{a['q']:.3g}"), eqW=float(f"{a['eqW']:.3g}"), cls=float(f"{a['cls']:.3g}"), M_star=(None if np.isinf(a["M"]) else int(a["M"])), S_eq=(None if np.isinf(a["S_eq"]) else a["S_eq"]), q_budget=float(f"{a['q_budget']:.3g}"))


axis = {}
axis["coupling_Jtau_frozen_edge_scrambled"] = [axis_med("spin_reset_rand_N6_z_frozen"), axis_med("spin_reset_rand_N6_z_edge"), axis_med("spin_reset_rand_N6_z_scrambled")]
axis["hamiltonian_chain_random_chaotic_N6_z"] = [axis_med("spin_reset_chain_N6_z"), axis_med("spin_reset_rand_N6_z"), axis_med("spin_reset_chaotic_N6_z")]
axis["readout_z_xyz_zz_N6"] = [axis_med("spin_reset_rand_N6_z"), axis_med("spin_reset_rand_N6_xyz"), axis_med("spin_reset_rand_N6_zz")]
axis["multiplex_V1_V5_V10_z"] = [axis_med("spin_reset_rand_N6_z"), axis_med("spin_reset_rand_N6_z_V5"), axis_med("spin_reset_rand_N6_z_V10")]
axis["multiplex_zz_V1_V10"] = [axis_med("spin_reset_rand_N6_zz"), axis_med("spin_reset_rand_N6_zz_V10")]
axis["T1_none_vs_T1"] = [axis_med("spin_reset_rand_N6_z"), axis_med("spin_reset_rand_N6_z_T1")]
axis["hou_T_strong_weak_none"] = [axis_med("spin_hamenc_rand_N6_xyz_V5"), axis_med("spin_hamenc_rand_N6_xyz_V10_weakT"), axis_med("spin_hamenc_rand_N6_xyz_V5_noT")]
axis["N_4_6_8_z"] = [axis_med("spin_reset_rand_N4_z"), axis_med("spin_reset_rand_N6_z"), axis_med("spin_reset_rand_N8_z")]
axis["cv_gauss_N12_kerr1_chi0_chi0.3_chi1V4"] = [axis_med("cv_gauss_N12"), axis_med("cv_kerr_chi0"), axis_med("cv_kerr_chi0.3"), axis_med("cv_kerr_chi1_V4")]
axis["pseudomode_mg10_z_zz"] = dict(z=cell("spin_reset_rand_N6_z", "mg10")["q"], z_pm=cell("spin_reset_rand_N6_z_pm", "mg10")["q"], zz=cell("spin_reset_rand_N6_zz", "mg10")["q"], zz_pm=cell("spin_reset_rand_N6_zz_pm", "mg10")["q"])
axis["pseudomode_mc30_narma20_z"] = dict(mc30=cell("spin_reset_rand_N6_z", "mc30")["q"], mc30_pm=cell("spin_reset_rand_N6_z_pm", "mc30")["q"], narma20=cell("spin_reset_rand_N6_z", "narma20")["q"], narma20_pm=cell("spin_reset_rand_N6_z_pm", "narma20")["q"])
axis["N10_zz_mg10"] = cell("spin_reset_rand_N10_zz", "mg10"); axis["N6_zz_mg10"] = cell("spin_reset_rand_N6_zz", "mg10"); axis["N10_zz_narma10"] = cell("spin_reset_rand_N10_zz", "narma10")
axis["two_mode_cv_mg10"] = {c: cell(c, "mg10")["q"] for c in ["cv2_cascade_kerr0.5_moments", "cv2_cascade_kerr0.5_fock", "cv2_cascade_chi0_moments", "cv2_cascade_chi0_fock", "cv2_bs_chi0_fock"]}
axis["two_mode_cv_mg10_eqW"] = cell("cv2_cascade_kerr0.5_fock", "mg10")["eqW"]
axis["kerr_delay_D10_mg10_baseline"] = float(f"{np.median([base[f'mg10|{s}']['kerr_delay:10']['nmse'] for s in range(3)]):.3g}")
axis["noise_tasks_best_quantum_vs_cls"] = {t: dict(q=float(f"{bestq[t]['q']:.3g}"), cls=float(f"{bestq[t]['cls']:.3g}"), config=bestq[t]["config"]) for t in ["xor_n5", "xprod_n5", "narma10_n5", "mc30_n5", "xor", "xprod"]}
for t in ["narma10", "mg10", "mg20"]:
    axis[f"weak_vs_projective_{t}"] = dict(projective_zz_S1e4=float(f"{np.median([r['curve']['1e+04'] for r in rows if r['config']=='spin_reset_rand_N6_zz' and r['task']==t]):.3g}"),
                                           weak03_S1e5=float(f"{np.median([r['curve']['1e+05'] for r in rows if r['config']=='spin_reset_rand_N6_zz_weak0.3' and r['task']==t]):.3g}"),
                                           weak06_S1e5=float(f"{np.median([r['curve']['1e+05'] for r in rows if r['config']=='spin_reset_rand_N6_zz_weak0.6' and r['task']==t]):.3g}"),
                                           weak01_S1e5=float(f"{np.median([r['curve']['1e+05'] for r in rows if r['config']=='spin_reset_rand_N6_zz_weak0.1' and r['task']==t]):.3g}"),
                                           projective_zz_S1e6=float(f"{np.median([r['curve']['1e+06'] for r in rows if r['config']=='spin_reset_rand_N6_zz' and r['task']==t]):.3g}"),
                                           weak03_S1e6=float(f"{np.median([r['curve']['1e+06'] for r in rows if r['config']=='spin_reset_rand_N6_zz_weak0.3' and r['task']==t]):.3g}"))
qin = {}
for t in ["qin_local", "qin_full", "qin_local_S", "qin_full_S"]:
    qin[t] = dict(polynarx_3_2=float(f"{np.median([base[f'{t}|{s}']['polynarx:(3, 2)']['nmse'] for s in range(3)]):.3g}"), esn_300=float(f"{np.median([base[f'{t}|{s}']['esn:300']['nmse'] for s in range(3)]):.3g}"),
                  esn_1000=float(f"{np.median([base[f'{t}|{s}']['esn:1000']['nmse'] for s in range(3)]):.3g}"), best_cls=float(f"{bestq[t]['cls']:.3g}"),
                  quantum_zz=cell("spin_qin_rand_N6_zz", t)["q"], quantum_zz_hybrid=cell("spin_qin_rand_N6_zz_hybrid", t)["q"], quantum_zz_weak03=cell("spin_qin_rand_N6_zz_weak0.3", t)["q"],
                  quantum_xyz_V5=cell("spin_qin_rand_N6_xyz_V5", t)["q"], quantum_zz_T1=cell("spin_qin_rand_N6_zz_T1", t)["q"])
axis["quantum_input"] = qin
axis["qkerr_tuned_D100_best_quantum_tasks"] = {t: cell("qkerr_delay_D100_tuned", t) for t in ["mc30", "mc30_n5", "xor_n5", "narma20"]}
note("axis_effects", axis, "results/map.jsonl + results/baselines.json (medians over 3 seeds; axis medians = median over the 23 classical-input tasks of log10 q/cls)")
json.dump(numbers, open(os.path.join(OUT, "numbers.json"), "w"), indent=1, default=float)
print(json.dumps(axis, indent=1, default=str))

# ------------------------------------------------------------------ numbers added after the adversarial review panel (paper/manuscript-REVIEW.md)
rev = {}
# (i) best quantum configuration per task: median over tasks of log10(q_best/cls) (the 2.6-decade figure is the all-pairs median)
rev["best_per_task_median_log10_q_over_cls"] = dict(median=round(float(np.median([np.log10(bestq[t]["q"] / bestq[t]["cls"]) for t in cls_tasks])), 2),
                                                    iqr=[round(float(np.percentile([np.log10(bestq[t]["q"] / bestq[t]["cls"]) for t in cls_tasks], p)), 2) for p in (25, 75)])
# (ii) S*_eq distribution of the a-wins (classical input) and how many are matched by an ESN of <= 30 / 100 nodes
aw = [k for k in cls_pairs if agg[k]["a"]]
Sd = defaultdict(int)
for k in aw:
    S = agg[k]["S_eq"]; Sd["exact_only" if S >= 1e7 else f"{S:.0e}"] += 1
rev["a_wins_S_eq_distribution"] = dict(Sd)
rev["a_wins_q_gt_0.5"] = int(sum(agg[k]["q"] > 0.5 for k in aw)); rev["a_wins_ratio_lt_1.1"] = int(sum(agg[k]["eqW"] / agg[k]["q"] < 1.1 for k in aw))
# (iii) task counts
rev["ten_seed_cells"] = sorted(f"{c}|{t}" for (c, t), a in agg.items() if a["n"] >= 10 and t in cls_tasks)
rev["three_seed_a_wins_reversed_at_ten_seeds"] = sorted(f"{c}|{t}" for (c, t), ds in cells.items() if t in cls_tasks and len(ds) >= 10 and all(d["a"] for d in ds[:3]) and not all(d["a"] for d in ds))
rev["three_seed_a_wins_surviving_at_ten_seeds"] = sorted(f"{c}|{t}" for (c, t), ds in cells.items() if t in cls_tasks and len(ds) >= 10 and all(d["a"] for d in ds))
rev["a_wins_M_star_worst_seed_max"] = max(max((d["M"] if np.isfinite(d["M"]) else 1000) for d in cells[k]) for k in aw)
rev["online_weak_a_wins_M_star"] = {f"{c}|{t}": dict(median=(None if np.isinf(agg[(c, t)]["M"]) else agg[(c, t)]["M"]), worst=max((d["M"] if np.isfinite(d["M"]) else 1000) for d in cells[(c, t)])) for (c, t) in aw if "weak" in c}
rev["task_counts"] = dict(classical_time_series=len([t for t in cls_tasks if not t.startswith("qin")]), quantum_input=len([t for t in cls_tasks if t.startswith("qin")]), oracle=len(orc_tasks))
# (iv) tuned Kerr: IQR width / median and per-seed wins of tuned quantum over tuned semiclassical
tk = {}
for tn in TASKS_T:
    for D in ("D30", "D100"):
        recs = [v for k, v in tune.items() if k.startswith(f"{tn}|{D}|")]
        q = np.array([r["q_test"] for r in recs]); kd = np.array([r["kd_same_D"] for r in recs])
        tk[f"{tn}|{D}"] = dict(n_seeds=len(recs), iqr_over_median_quantum=round(float((np.percentile(q, 75) - np.percentile(q, 25)) / np.median(q)), 2),
                               iqr_over_median_semiclassical=round(float((np.percentile(kd, 75) - np.percentile(kd, 25)) / np.median(kd)), 2),
                               seeds_quantum_better=int(np.sum(q < kd)))
rev["tune_qkerr_spread"] = tk
# (v) mean photon number in the twin runs (median and max over seeds, per configuration, eps0=0.5 configs)
mx = defaultdict(list)
for k, v in twin.items():
    mx[k.split("|")[1]].append(v["maxn"])
rev["kerr_twin_maxn_by_config"] = {c: dict(median=round(float(np.median(v)), 2), max=round(float(max(v)), 2)) for c, v in mx.items()}
# (vi) per-seed oracle comparisons: quantum at m vs best black-box classical with <= 20m queries (same rule as ✚), per n
if HAVE_FORR:
    ps = {}
    for t in orc_tasks:
        rs = [r for r in rows if r["config"] == "forr_qrc" and r["task"] == t]
        d = {}
        for m in (1e2, 1e3):
            wins = 0; ratios = []
            for r in rs:
                b = base[f"{t}|{r['seed']}"]
                rivals = [v["nmse"] for k, v in b.items() if k.startswith("forr_") and not k.startswith(("forr_wb", "forr_full", "forr_knownf")) and v["size"] <= 20 * m]
                best_r = min(rivals); qm = r["curve"][f"{m:.0e}"]
                wins += qm < best_r; ratios.append(qm / best_r)
            d[f"m{m:.0e}"] = dict(seeds_quantum_better=wins, of=len(rs), median_quantum_over_best_classical=round(float(np.median(ratios)), 3))
        ps[t] = d
    rev["per_seed_query_comparison"] = ps
    # (vii) known-f (white-box) estimator, results/forr_knownf.json, if present
    kf_path = os.path.join(RES, "forr_knownf.json")
    if os.path.exists(kf_path):
        kf = json.load(open(kf_path)); kfs = {}
        for t in orc_tasks:
            keys = [k for k in kf if k.startswith(t + "|")]
            if not keys:
                continue
            seeds = [int(k.split("|")[1]) for k in keys]
            med = {Q: round(float(np.median([kf[f"{t}|{s}"][f"forr_knownf:{Q}"]["nmse"] for s in seeds])), 5) for Q in QS}
            qrows = {r["seed"]: r for r in rows if r["config"] == "forr_qrc" and r["task"] == t}
            win200 = int(sum(kf[f"{t}|{s}"]["forr_knownf:200"]["nmse"] < qrows[s]["curve"]["1e+02"] for s in seeds if s in qrows))
            win200_vs_m1e3 = int(sum(kf[f"{t}|{s}"]["forr_knownf:200"]["nmse"] < qrows[s]["curve"]["1e+03"] for s in seeds if s in qrows))
            kfs[t] = dict(n_seeds=len(seeds), knownf_Q20_200_2000_20000=[med[Q] for Q in QS], seeds_knownf200_beats_quantum_m1e2=win200, seeds_knownf200_beats_quantum_m1e3=win200_vs_m1e3)
        rev["knownf"] = kfs
# (viii) tuned mean-field twin, results/tune_meanfield.json, if present
mf_path = os.path.join(RES, "tune_meanfield.json")
if os.path.exists(mf_path):
    mf = json.load(open(mf_path)); mfs = {}
    for tn in TASKS_T:
        for D in (30, 100):
            recs = [v for k, v in mf.items() if k.startswith(f"{tn}|D{D}|") and v["mf_test"] is not None]
            if recs:
                m_ = np.array([r["mf_test"] for r in recs]); q_ = np.array([r["q_test"] for r in recs])
                mfs[f"{tn}|D{D}"] = dict(n_seeds=len(recs), tuned_meanfield=float(f"{np.median(m_):.3g}"), tuned_quantum=float(f"{np.median(q_):.3g}"), ratio_q_over_mf=float(f"{np.median(q_) / np.median(m_):.3g}"), seeds_quantum_better=int(np.sum(q_ < m_)))
    rev["tune_meanfield"] = mfs
# (ix) shot-wall family statistics after the weakT reclassification are already in shot_degradation_* (family() fixed)
note("review_numbers", rev, "recomputed after the adversarial panel; sources: results/map.jsonl, baselines.json, tune_qkerr.json, kerr_twin.json, forr_knownf.json, tune_meanfield.json")
json.dump(numbers, open(os.path.join(OUT, "numbers.json"), "w"), indent=1, default=float)
print(json.dumps(rev, indent=1, default=str)[:6000])

# ------------------------------------------------------------------ settings-charged shot budget (appendix check requested by the review panel)
# Measurement settings per step: xyz spin readouts need 3 bases; Gaussian covariance readouts need x and p homodyne (2, cross
# moments not charged); CV Kerr readouts <x>,<p>,<n> need 3 (two homodyne settings and photon counting); Fock joint-number
# readouts, z/zz readouts, online weak and one-bit readouts need 1. Time multiplexing V > 1 with projective readout needs V
# separate runs. Charged shot-ops = S * W * settings * V; the budget 3e5 then allows S_c = 3e5 / (W * settings * V).
import re as _re


def settings_of(c):
    if c.startswith("forr"):
        return 1
    if c.startswith("cv_gauss"):
        return 2
    if c.startswith("qkerr") or c.startswith("cv_kerr") or ("cv2" in c and "moments" in c):
        return 3
    if "xyz" in c:
        return 3
    return 1


def V_of(c):
    m = _re.search(r"_V(\d+)", c)
    return int(m.group(1)) if m else 1


def q_at(curve, S):
    """log-log interpolation of the shot curve at shot count S (clipped to the simulated grid)."""
    xs = np.array([1e2, 1e3, 1e4, 1e5, 1e6]); ys = np.array([curve[k] for k in SHOTS])
    S = float(np.clip(S, xs[0], xs[-1]))
    return float(10 ** np.interp(np.log10(S), np.log10(xs), np.log10(ys)))


charged = defaultdict(list); charged_acc = defaultdict(list); fam_budget = {}
for (c, t), a in agg.items():
    Wc = W_of(c) * settings_of(c) * V_of(c)
    Sc = BUDGET / Wc
    ds = cells[(c, t)]
    qb = float(np.median([q_at(d["curve"], Sc) for d in ds]))
    a["q_budget_charged"] = qb; a["S_charged"] = Sc
    f = family(c); charged[f].append(float(np.median([q_at(d["curve"], Sc) / d["q"] for d in ds])))  # same statistic as shot_degradation_by_family
    if a["q"] < 1e-2:
        charged_acc[f].append(qb / a["q"])
    fam_budget.setdefault(f, set()).add(Sc)
chg = {f: dict(n_pairs=len(v), median=round(float(np.median(v)), 2), p90=round(float(np.percentile(v, 90)), 1), max=round(float(max(v)), 1),
               accurate_cells_median=(round(float(np.median(charged_acc[f])), 1) if charged_acc[f] else None), accurate_n=len(charged_acc[f]),
               S_at_budget=sorted(fam_budget[f])) for f, v in charged.items()}
note("shot_degradation_settings_charged", chg, "results/map.jsonl curves, log-log interpolated at S = 3e5/(W*settings*V); settings: xyz 3, Gaussian 2, CV Kerr 3, Fock/z/zz/weak/1-bit 1")
json.dump(numbers, open(os.path.join(OUT, "numbers.json"), "w"), indent=1, default=float)
print(json.dumps(chg, indent=1))
