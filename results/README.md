# results/ inventory

| file | produced by | content |
|---|---|---|
| `map.jsonl` | `scripts/run_map.py` | one JSON line per (config, task, seed): feature count F, NMSE at shots {1e2..1e6, inf}, simulation time; 3087 cells |
| `baselines.json` | `scripts/run_map.py` | tuned classical baselines per task and seed: NMSE, feature count, family, size (and query budget / readout for Forrelation tasks) |
| `map.md`, `map.png` | `scripts/make_report.py` | all win criteria (A, a, S*, W, M*, ★, ◆) per cell; three-panel heatmap |
| `forr_matched.md` | `scripts/forr_report.py` | Forrelation tasks at matched query budgets, ✚ criterion, 10 seeds with IQR |
| `presubmission.md` | `scripts/presub_report.py` | √N trend of the classical query count, plus the three reports below |
| `kerr_twin.json`, `kerr_twin.md` | `scripts/kerr_twin.py` | quantum Kerr delay vs mean-field twin at identical parameters, 10 seeds |
| `tune_qkerr.json`, `tune_qkerr.md` | `scripts/tune_qkerr.py` | tuned quantum Kerr delay vs tuned semiclassical delay line at matched depth, 10 seeds |
| `tuning_sensitivity.md` | `scripts/tuning_sensitivity.py` | ESN best NMSE with 20 vs 50 tuning draws |
| `apps/` | `scripts/apps_demo.py` | drift-monitoring demo (black-box vs white-box) and exponential-sum scaling demo |
| `map_analysis.md` | hand-written | narrative analysis of the full study, in chronological working order (not the manuscript text) |
