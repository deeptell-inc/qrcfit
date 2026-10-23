# qrcfit — a resource map of quantum reservoir computing against tuned classical baselines

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23589290.svg)](https://doi.org/10.5281/zenodo.23589290)

Archived snapshot (code, results and manuscript PDF): https://doi.org/10.5281/zenodo.23589290 (concept DOI 10.5281/zenodo.23589289).

Companion code and data for *"A resource map of quantum reservoir computing: where it beats tuned classical
baselines"* (manuscript not included in this repository). The package evaluates 57 quantum reservoir configurations on 35 tasks
against classical baselines that receive the same tuning budget and the same readout, counting measurement
shots, oracle queries and experiment restarts explicitly.

**Headline.** On 23 classical-input tasks no quantum configuration beats the best tuned classical model in
accuracy or in shot/compute cost (0 of 989 configuration×task pairs). On oracle-input tasks whose target is a
Forrelation correlation of two black-box phase functions drawn fresh at every step, the fixed 2-query circuit
wins on both axes from N = 2^16 upward (all seeds), with the matching classical query count growing as √N.
Structured families lose the win to classical structure exploitation: quadratic (Gold) phases are dequantised
by a degree-2 learning attack, a publicly defined Kloosterman f admits a white-box importance-sampling
estimator, and a fixed f lets a black-box classical monitor amortise the cost of reading it over the stream.

## Layout

| path | content |
|---|---|
| `qrcfit/tasks.py` | task generators (NARMA, Mackey–Glass, Lorenz, memory capacity, cross-time products, delayed XOR, noisy variants, quantum-input collision-model streams, Forrelation oracle streams) |
| `qrcfit/reservoirs.py` | exact density-matrix / covariance simulators: spin qubit-reset, Hou-style Hamiltonian encoding, pseudomode embedding, weak measurement, Gaussian CV, single/two-mode Kerr, quantum Kerr delay line, tuned variants |
| `qrcfit/forrelation.py` | GF(2^n) tables, Kloosterman and Gold pairs, two-FWHT Forrelation, query-limited classical estimators (naive, √N all-pairs, degree-2 ANF attack, white-box, known-f importance sampling), Forrelation feature map, drift-monitoring task, fresh-pair regeneration |
| `scripts/forr_knownf.py`, `scripts/tune_meanfield.py` | white-box known-f attack on the Kloosterman tasks; tuned ODE mean-field twin of the quantum Kerr delay line (added after the adversarial review) |
| `qrcfit/baselines.py` | tuned classical baselines (echo-state networks, polynomial NARX, semiclassical Kerr delay line) and the shared readout tuner |
| `qrcfit/evaluate.py` | ridge readout with validation-tuned regularisation, NMSE, finite-shot emulation |
| `scripts/run_map.py` | builds `results/map.jsonl` (resumable, parallel) |
| `scripts/make_report.py` | recomputes all win criteria and writes `results/map.md`, `results/map.png` |
| `scripts/forr_report.py`, `scripts/presub_report.py` | matched-query tables for the Forrelation tasks and the pre-submission aggregate |
| `scripts/kerr_twin.py`, `scripts/tune_qkerr.py` | quantum Kerr delay vs mean-field twin; equal-tuning-effort test |
| `scripts/apps_demo.py`, `scripts/tuning_sensitivity.py` | application demos; classical tuning-budget sensitivity |
| `scripts/paper_figures.py` | the four manuscript figures from `results/` (written to a `paper/` directory it creates) |
| `results/` | all raw cells, baselines, tables and figures used in the manuscript (see `results/README.md`) |
| `tests/` | smoke tests (`python -m pytest tests -q`, ~5 s) |

## Reproduction

```bash
pip install -e .            # numpy, scipy, matplotlib; Python >= 3.10
python -m pytest tests -q   # 10 tests
bash scripts/reproduce_all.sh   # full pipeline, ~6 h on 12 cores; see the script for the stage list
```

Every stage is resumable: `run_map.py` skips cells already present in `results/map.jsonl`, and classical
baselines are cached per task and seed in `results/baselines.json`. To rebuild only the tables and figures
from the shipped results:

```bash
python scripts/make_report.py && python scripts/forr_report.py && python scripts/presub_report.py && python scripts/paper_figures.py
```

## Accounting rule (what "win" means)

- **A**: quantum NMSE with exact expectations below the best tuned classical model of any size.
- **a**: below the best classical model with no more readout features than the quantum one.
- **S\***: smallest shot count reaching a/A; **W**: experiment restarts per step (30 for projective readout, 1 for online weak measurement or the memoryless Forrelation circuit); shot-ops = S\*·W.
- **★**: a, shot-ops ≤ 3×10⁵, and the ESN size needed to match the quantum exact-expectation NMSE is ≥ 10× the quantum feature count (or unreachable up to 1000 nodes). Not evaluated on oracle tasks (their classical side is query-budgeted, not size-budgeted).
- **✚** (Forrelation tasks): quantum at 2m oracle queries beats every black-box classical estimator using ≤ 20m queries, at m = 10² and 10³, in every seed.

Definitions are implemented in `scripts/make_report.py` and `scripts/forr_report.py`; changing them and rerunning the two scripts re-derives every table from the raw cells.

## Environment used for the shipped results

Python 3.13.9, numpy 2.2.6, scipy 1.17.1, matplotlib 3.10.6, macOS 25 (Apple silicon), 16 cores. Seeds: 3 per
cell for classical-input tasks, 10 for the 12 Forrelation-family tasks; all random streams are seeded.

## License

MIT (see `LICENSE`). Please cite the manuscript and the Zenodo archive (`CITATION.cff`, DOI 10.5281/zenodo.23589290).
