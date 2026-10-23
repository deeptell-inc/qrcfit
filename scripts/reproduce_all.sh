#!/usr/bin/env bash
# Full reproduction of results/ from scratch. Stages are resumable; rerunning skips finished cells.
# Wall-clock on 12–16 cores: stage 1 ≈ 3 h, stage 2 ≈ 40 min, stages 3–6 ≈ 1 h.
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONWARNINGS=ignore OMP_NUM_THREADS=2
W=${WORKERS:-12}

echo "[1/6] map cells: all quantum configs on all tasks, 3 seeds"
python scripts/run_map.py --seeds 3 --workers "$W"
echo "[2/6] Forrelation-family tasks: 10 seeds"
python scripts/run_map.py --seeds 10 --workers "$W" --configs forr_qrc \
  --tasks forr_kloos_n10 forr_kloos_n12 forr_kloos_n14 forr_kloos_n16 forr_kloos_n18 forr_kloos_n20 \
          forr_gold_n10 forr_gold_n12 forr_gold_n14 forr_gold_n16 drift_kloos_n12 drift_kloos_n16
echo "[3/6] quantum Kerr delay vs mean-field twin, 10 seeds"
python scripts/kerr_twin.py 10
echo "[4/6] equal-tuning-effort Kerr test, 10 seeds"
python scripts/tune_qkerr.py 10
echo "[5/6] application demos and tuning-budget sensitivity"
python scripts/apps_demo.py ab
python scripts/tuning_sensitivity.py
echo "[6/6] tables and figures"
python scripts/make_report.py
python scripts/forr_report.py
python scripts/presub_report.py
python scripts/paper_figures.py
echo "done: see results/map.md, results/presubmission.md and the regenerated figures in paper/"
