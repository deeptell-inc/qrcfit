# Demo B: exponential-sum correlation Phi(f^K, g^K) — classical exact time vs quantum shots (target ±0.03)

| n | N | Phi | classical exact (2 FWHT) [s] | quantum shots | quantum queries (2m) | √N (classical query lower-bound scale) |
|---|---|---|---|---|---|---|
| 10 | 1024 | 0.8452 | 0.000 | 318 | 636 | 32 |
| 12 | 4096 | 0.8490 | 0.000 | 311 | 622 | 64 |
| 14 | 16384 | 0.8483 | 0.000 | 312 | 624 | 128 |
| 16 | 65536 | 0.8490 | 0.001 | 311 | 622 | 256 |
| 18 | 262144 | 0.8488 | 0.004 | 311 | 622 | 512 |
| 20 | 1048576 | 0.8488 | 0.018 | 311 | 622 | 1024 |
| 22 | 4194304 | 0.8488 | 0.073 | 311 | 622 | 2048 |
| 24 | 16777216 | 0.8488 | 0.652 | 311 | 622 | 4096 |

Measured classical scaling: log2(time) ≈ 1.22·n + -30.2  (ideal N log N → slope 1). Extrapolation: n=40 → 1.1e+02 h, n=50 → 5.8e+01 y, n=60 → 2.7e+05 y, while the quantum side stays at 622 oracle queries per estimate (precision ±0.03) for every n. Classical query-limited estimators need Ω(√N/log N) queries: √N = 1e6 at n=40, 1e9 at n=60.

Caveat: the quantum oracle cost (GF(2^n) inversion circuit per query) grows polynomially in n and is not included; the classical time is the full-table computation on one CPU core.
