# ESN tuning-budget sensitivity (best NMSE over sizes 3..1000; median over 3 seeds)

| task | budget 20 | budget 50 | ratio 50/20 |
|---|---|---|---|
| narma10 | 0.0499 | 0.0499 | 1.00 |
| mg10 | 8.04e-09 | 1.32e-09 | 0.16 |
| mc30 | 0.448 | 0.144 | 0.32 |
| lorenz_multi | 4.22e-06 | 2.75e-07 | 0.07 |
| xor_n5 | 0.0317 | 0.0333 | 1.05 |
| narma20 | 0.257 | 0.145 | 0.57 |

Reading: ratios below 1 mean a larger tuning budget makes the classical baselines STRONGER (up to 14x on smooth deterministic tasks); the map's 20-draw budget is therefore conservative in the classical side's disfavour, and every 'no quantum win' conclusion would only sharpen with more classical tuning. No task changes sign: the quantum-vs-classical gaps (1e1–1e5x) exceed the budget effect everywhere.
