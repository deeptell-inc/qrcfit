# Demo A: black-box dual-relation drift monitoring (Kloosterman reference, n=16, N=65536, 3 seeds)

Targets: device fidelity p_t and Phi_t. NMSE (median over seeds), same tuned readout for every stream.

| monitor | queries/step | NMSE |
|---|---|---|
| quantum, m=1e+02 shots | 200 | 0.1611 |
| quantum, m=1e+03 shots | 2000 | 0.0394 |
| quantum, m=1e+04 shots | 20000 | 0.0052 |
| quantum, exact expectation | ∞ | 0.0003 |
| classical black-box naive | 200 | 0.9989 |
| classical black-box opt (√N surrogate) | 200 | 0.9637 |
| classical black-box naive | 2000 | 1.0101 |
| classical black-box opt (√N surrogate) | 2000 | 0.7160 |
| classical black-box naive | 20000 | 1.0142 |
| classical black-box opt (√N surrogate) | 20000 | 0.2354 |
| classical WHITE-BOX (knows ideal g) | 200 | 0.0685 |
| classical WHITE-BOX (knows ideal g) | 2000 | 0.0117 |
| classical WHITE-BOX (knows ideal g) | 20000 | 0.0017 |

Reading: in the black-box setting the quantum monitor at 200 queries/step beats every classical monitor up to 20000 queries/step; if the classical monitor knows the ideal device function g, sampling g_t g at Q points has variance (1-p^2)/Q with no N dependence and the advantage disappears.
