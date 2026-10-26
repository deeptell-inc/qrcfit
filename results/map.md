# QRC vs tuned classical: map

3451 cells, 57 quantum configs × 49 tasks, seeds per cell = 3–10.

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

| config | task | F_q | q | q@3e5 ops | cls (best) | eqW (best ≤F_q) | S*_eq | S*_cls | W | M* | A | a | ★ | ◆ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cv_gauss_N12 | lorenz_multi | 324 | 0.0191 | 0.445 | 4.22e-06 (esn:1000) | 4.22e-06 (esn:300) | — | — | 30 | 30 |  |  |  |  |
| cv_gauss_N12 | lorenz_uni | 324 | 0.0475 | 0.392 | 0.000172 (esn:300) | 0.000172 (esn:300) | — | — | 30 | 30 |  |  |  |  |
| cv_gauss_N12 | mc30 | 324 | 0.161 | 0.494 | 1.5e-07 (kerr_delay:300) | 3.79e-07 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| cv_gauss_N12 | mc30_n5 | 324 | 0.193 | 0.511 | 0.0389 (kerr_delay:100) | 0.0389 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| cv_gauss_N12 | mg10 | 324 | 0.00034 | 0.174 | 2.77e-09 (kerr_delay:300) | 8.06e-08 (esn:300) | — | — | 30 | 100 |  |  |  |  |
| cv_gauss_N12 | mg10_small | 324 | 0.0186 | 0.372 | 0.00471 (kerr_delay:300) | 0.00471 (esn:300) | — | — | 30 | 30 |  |  |  |  |
| cv_gauss_N12 | mg20 | 324 | 0.000263 | 0.0508 | 9.57e-08 (esn:1000) | 8.29e-07 (esn:300) | — | — | 30 | 100 |  |  |  |  |
| cv_gauss_N12 | narma10 | 324 | 0.0346 | 0.227 | 0.0134 (kerr_delay:300) | 0.0259 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| cv_gauss_N12 | narma10_n5 | 324 | 0.0742 | 0.264 | 0.0554 (kerr_delay:100) | 0.0608 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| cv_gauss_N12 | narma10_small | 324 | 0.814 | 0.514 | 0.143 (polynarx:(20, 2)) | 0.143 (polynarx:(20, 2)) | — | — | 30 | 3 |  |  |  |  |
| cv_gauss_N12 | narma2 | 324 | 0.000312 | 0.00696 | 5.73e-06 (esn:1000) | 1.8e-05 (esn:300) | — | — | 30 | 100 |  |  |  |  |
| cv_gauss_N12 | narma20 | 324 | 0.289 | 0.747 | 0.1 (kerr_delay:300) | 0.136 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| cv_gauss_N12 | narma5 | 324 | 0.00164 | 0.0195 | 0.000111 (esn:1000) | 0.000244 (kerr_delay:100) | — | — | 30 | 300 |  |  |  |  |
| cv_gauss_N12 | xor | 324 | 0.011 | 0.049 | 4.38e-25 (polynarx:(20, 2)) | 4.38e-25 (polynarx:(20, 2)) | — | — | 30 | 1000 |  |  |  |  |
| cv_gauss_N12 | xor_n1 | 324 | 0.0115 | 0.05 | 0.00101 (kerr_delay:100) | 0.00102 (kerr_delay:100) | — | — | 30 | 1000 |  |  |  |  |
| cv_gauss_N12 | xor_n5 | 324 | 0.0229 | 0.062 | 0.023 (esn:1000) | 0.023 (esn:300) | ∞ | ∞ | 30 | >1000 |  |  |  |  |
| cv_gauss_N12 | xprod | 324 | 0.00743 | 0.0916 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 300 |  |  |  |  |
| cv_gauss_N12 | xprod_n1 | 324 | 0.0103 | 0.0942 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 300 |  |  |  |  |
| cv_gauss_N12 | xprod_n5 | 324 | 0.0757 | 0.149 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | >1000 |  |  |  |  |
| cv_gauss_N4 | lorenz_multi | 44 | 0.0876 | 0.456 | 4.22e-06 (esn:1000) | 0.016 (esn:30) | — | — | 30 | 10 |  |  |  |  |
| cv_gauss_N4 | lorenz_uni | 44 | 0.0545 | 0.35 | 0.000172 (esn:300) | 0.016 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| cv_gauss_N4 | mc30 | 44 | 0.79 | 0.812 | 1.5e-07 (kerr_delay:300) | 0.0345 (polynarx:(30, 1)) | — | — | 30 | 10 |  |  |  |  |
| cv_gauss_N4 | mc30_n5 | 44 | 0.794 | 0.817 | 0.0389 (kerr_delay:100) | 0.0628 (polynarx:(30, 1)) | — | — | 30 | 10 |  |  |  |  |
| cv_gauss_N4 | mg10 | 44 | 0.0182 | 0.294 | 2.77e-09 (kerr_delay:300) | 0.000807 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| cv_gauss_N4 | mg10_small | 44 | 0.256 | 0.398 | 0.00471 (kerr_delay:300) | 0.011 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| cv_gauss_N4 | mg20 | 44 | 0.00339 | 0.0748 | 9.57e-08 (esn:1000) | 0.000672 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| cv_gauss_N4 | narma10 | 44 | 0.641 | 0.663 | 0.0134 (kerr_delay:300) | 0.147 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv_gauss_N4 | narma10_n5 | 44 | 0.646 | 0.659 | 0.0554 (kerr_delay:100) | 0.171 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv_gauss_N4 | narma10_small | 44 | 0.807 | 0.736 | 0.143 (polynarx:(30, 1)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv_gauss_N4 | narma2 | 44 | 0.0122 | 0.0267 | 5.73e-06 (esn:1000) | 0.00499 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| cv_gauss_N4 | narma20 | 44 | 0.679 | 0.698 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv_gauss_N4 | narma5 | 44 | 0.126 | 0.257 | 0.000111 (kerr_delay:300) | 0.0591 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| cv_gauss_N4 | xor | 44 | 0.295 | 0.363 | 4.38e-25 (polynarx:(20, 2)) | 0.283 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| cv_gauss_N4 | xor_n1 | 44 | 0.296 | 0.363 | 0.00101 (kerr_delay:100) | 0.299 (kerr_delay:10) | — | — | 30 | 100 |  |  |  |  |
| cv_gauss_N4 | xor_n5 | 44 | 0.303 | 0.371 | 0.023 (kerr_delay:100) | 0.336 (kerr_delay:10) | — | — | 30 | 100 |  |  |  |  |
| cv_gauss_N4 | xprod | 44 | 0.291 | 0.454 | 6.6e-24 (polynarx:(10, 2)) | 0.457 (kerr_delay:10) | 1e+04 | — | 30 | 100 |  |  |  |  |
| cv_gauss_N4 | xprod_n1 | 44 | 0.294 | 0.455 | 0.00248 (polynarx:(10, 2)) | 0.459 (kerr_delay:10) | 1e+04 | — | 30 | 100 |  |  |  |  |
| cv_gauss_N4 | xprod_n5 | 44 | 0.331 | 0.483 | 0.0592 (polynarx:(10, 2)) | 0.499 (kerr_delay:10) | 1e+04 | — | 30 | 100 |  |  |  |  |
| cv_kerr_chi0 | lorenz_multi | 4 | 0.6 | 0.609 | 4.22e-06 (esn:1000) | 0.345 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | lorenz_uni | 4 | 0.525 | 0.527 | 0.000172 (esn:300) | 0.304 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | mc30 | 4 | 0.977 | 0.976 | 1.5e-07 (kerr_delay:300) | 0.926 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | mc30_n5 | 4 | 0.98 | 0.98 | 0.0389 (kerr_delay:100) | 0.928 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | mg10 | 4 | 0.962 | 0.965 | 2.77e-09 (kerr_delay:300) | 0.166 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | mg10_small | 4 | 0.995 | 1.01 | 0.00471 (kerr_delay:300) | 0.199 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | mg20 | 4 | 0.559 | 0.563 | 9.57e-08 (esn:1000) | 0.0698 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | narma10 | 4 | 0.876 | 0.881 | 0.0134 (kerr_delay:300) | 0.488 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | narma10_n5 | 4 | 0.852 | 0.858 | 0.0554 (kerr_delay:100) | 0.504 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | narma10_small | 4 | 0.913 | 1.03 | 0.143 (polynarx:(20, 2)) | 0.683 (polynarx:(3, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | narma2 | 4 | 0.623 | 0.622 | 5.73e-06 (esn:1000) | 0.166 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | narma20 | 4 | 0.846 | 0.85 | 0.1 (kerr_delay:300) | 0.607 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | narma5 | 4 | 0.864 | 0.867 | 0.000111 (kerr_delay:300) | 0.454 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | xor | 4 | 0.955 | 0.955 | 4.38e-25 (polynarx:(20, 2)) | 0.831 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | xor_n1 | 4 | 0.955 | 0.955 | 0.00101 (kerr_delay:100) | 0.843 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | xor_n5 | 4 | 0.958 | 0.958 | 0.023 (kerr_delay:100) | 0.887 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | xprod | 4 | 0.992 | 0.994 | 6.6e-24 (polynarx:(10, 2)) | 0.992 (esn:3) | 1e+03 | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | xprod_n1 | 4 | 0.993 | 0.994 | 0.00248 (polynarx:(10, 2)) | 0.992 (esn:3) | 1e+03 | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0 | xprod_n5 | 4 | 0.994 | 0.995 | 0.0592 (polynarx:(10, 2)) | 0.993 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | lorenz_multi | 4 | 0.505 | 0.51 | 4.22e-06 (esn:1000) | 0.345 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | lorenz_uni | 4 | 0.602 | 0.606 | 0.000172 (esn:1000) | 0.304 (polynarx:(3, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | mc30 | 4 | 0.971 | 0.971 | 1.5e-07 (kerr_delay:300) | 0.926 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | mc30_n5 | 4 | 0.971 | 0.971 | 0.0389 (kerr_delay:100) | 0.928 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | mg10 | 4 | 0.765 | 0.769 | 2.77e-09 (kerr_delay:300) | 0.166 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | mg10_small | 4 | 0.868 | 0.869 | 0.00471 (esn:1000) | 0.199 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | mg20 | 4 | 0.349 | 0.36 | 9.57e-08 (esn:1000) | 0.0698 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | narma10 | 4 | 0.79 | 0.792 | 0.0134 (kerr_delay:300) | 0.488 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | narma10_n5 | 4 | 0.794 | 0.797 | 0.0554 (kerr_delay:100) | 0.504 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | narma10_small | 4 | 0.876 | 0.874 | 0.143 (polynarx:(30, 1)) | 0.683 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | narma2 | 4 | 0.61 | 0.612 | 5.73e-06 (esn:1000) | 0.166 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | narma20 | 4 | 0.822 | 0.824 | 0.1 (kerr_delay:100) | 0.607 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | narma5 | 4 | 0.767 | 0.772 | 0.000111 (esn:1000) | 0.454 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | xor | 4 | 0.954 | 0.953 | 4.38e-25 (polynarx:(20, 2)) | 0.831 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | xor_n1 | 4 | 0.954 | 0.954 | 0.00101 (kerr_delay:100) | 0.843 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | xor_n5 | 4 | 0.959 | 0.958 | 0.023 (kerr_delay:100) | 0.887 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi0.3 | xprod | 4 | 0.979 | 0.978 | 6.18e-24 (polynarx:(10, 2)) | 0.986 (esn:3) | 1e+02 | — | 30 | 5 |  |  |  |  |
| cv_kerr_chi0.3 | xprod_n1 | 4 | 0.979 | 0.979 | 0.00261 (polynarx:(10, 2)) | 0.986 (esn:3) | 1e+02 | — | 30 | 5 |  |  |  |  |
| cv_kerr_chi0.3 | xprod_n5 | 4 | 0.98 | 0.981 | 0.0633 (polynarx:(10, 2)) | 0.986 (esn:3) | 1e+02 | — | 30 | 5 |  |  |  |  |
| cv_kerr_chi1_V4 | lorenz_multi | 16 | 0.405 | 0.511 | 4.22e-06 (esn:1000) | 0.0501 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | lorenz_uni | 16 | 0.385 | 0.507 | 0.000172 (esn:300) | 0.084 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | mc30 | 16 | 0.946 | 0.948 | 1.5e-07 (kerr_delay:300) | 0.713 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | mc30_n5 | 16 | 0.948 | 0.949 | 0.0389 (kerr_delay:100) | 0.719 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | mg10 | 16 | 0.425 | 0.555 | 2.77e-09 (kerr_delay:300) | 0.0186 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | mg10_small | 16 | 0.473 | 0.751 | 0.00471 (esn:1000) | 0.0755 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | mg20 | 16 | 0.114 | 0.211 | 9.57e-08 (esn:1000) | 0.0121 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | narma10 | 16 | 0.73 | 0.74 | 0.0134 (kerr_delay:300) | 0.282 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | narma10_n5 | 16 | 0.744 | 0.757 | 0.0554 (kerr_delay:100) | 0.288 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | narma10_small | 16 | 0.807 | 0.85 | 0.143 (polynarx:(30, 1)) | 0.385 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | narma2 | 16 | 0.396 | 0.438 | 5.73e-06 (esn:1000) | 0.027 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | narma20 | 16 | 0.77 | 0.766 | 0.1 (kerr_delay:300) | 0.383 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | narma5 | 16 | 0.573 | 0.614 | 0.000111 (esn:1000) | 0.138 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv_kerr_chi1_V4 | xor | 16 | 0.699 | 0.762 | 4.38e-25 (polynarx:(20, 2)) | 0.626 (esn:10) | — | — | 30 | 10 |  |  |  |  |
| cv_kerr_chi1_V4 | xor_n1 | 16 | 0.7 | 0.763 | 0.00101 (kerr_delay:100) | 0.64 (esn:10) | — | — | 30 | 10 |  |  |  |  |
| cv_kerr_chi1_V4 | xor_n5 | 16 | 0.708 | 0.768 | 0.023 (esn:1000) | 0.699 (esn:10) | — | — | 30 | 10 |  |  |  |  |
| cv_kerr_chi1_V4 | xprod | 16 | 0.86 | 0.88 | 6.6e-24 (polynarx:(10, 2)) | 0.764 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| cv_kerr_chi1_V4 | xprod_n1 | 16 | 0.861 | 0.88 | 0.00248 (polynarx:(10, 2)) | 0.765 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| cv_kerr_chi1_V4 | xprod_n5 | 16 | 0.875 | 0.89 | 0.0592 (polynarx:(10, 2)) | 0.777 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| cv2_bs_chi0_fock | lorenz_multi | 16 | 0.496 | 0.519 | 4.22e-06 (esn:1000) | 0.0501 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | lorenz_uni | 16 | 0.24 | 0.283 | 0.000172 (esn:300) | 0.084 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| cv2_bs_chi0_fock | mc30 | 16 | 0.963 | 0.963 | 1.5e-07 (kerr_delay:300) | 0.713 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | mc30_n5 | 16 | 0.965 | 0.962 | 0.0389 (kerr_delay:100) | 0.719 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | mg10 | 16 | 0.705 | 0.779 | 2.77e-09 (kerr_delay:300) | 0.0186 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | mg10_small | 16 | 0.892 | 0.896 | 0.00471 (kerr_delay:300) | 0.0755 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | mg20 | 16 | 0.251 | 0.372 | 9.57e-08 (esn:1000) | 0.0121 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | narma10 | 16 | 0.687 | 0.676 | 0.0134 (kerr_delay:300) | 0.282 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | narma10_n5 | 16 | 0.681 | 0.684 | 0.0554 (kerr_delay:100) | 0.288 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | narma10_small | 16 | 1.04 | 0.952 | 0.143 (polynarx:(30, 1)) | 0.385 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | narma2 | 16 | 0.588 | 0.592 | 5.73e-06 (esn:1000) | 0.027 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | narma20 | 16 | 0.848 | 0.849 | 0.1 (kerr_delay:300) | 0.383 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | narma5 | 16 | 0.628 | 0.641 | 0.000111 (kerr_delay:300) | 0.138 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | xor | 16 | 0.843 | 0.855 | 4.38e-25 (polynarx:(20, 2)) | 0.626 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | xor_n1 | 16 | 0.842 | 0.855 | 0.00101 (esn:1000) | 0.64 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_bs_chi0_fock | xor_n5 | 16 | 0.839 | 0.857 | 0.023 (kerr_delay:100) | 0.699 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| cv2_bs_chi0_fock | xprod | 16 | 0.976 | 0.984 | 6.6e-24 (polynarx:(10, 2)) | 0.764 (polynarx:(3, 2)) | — | — | 30 | 5 |  |  |  |  |
| cv2_bs_chi0_fock | xprod_n1 | 16 | 0.977 | 0.984 | 0.00248 (polynarx:(10, 2)) | 0.765 (polynarx:(3, 2)) | — | — | 30 | 5 |  |  |  |  |
| cv2_bs_chi0_fock | xprod_n5 | 16 | 0.975 | 0.984 | 0.0592 (polynarx:(10, 2)) | 0.777 (polynarx:(3, 2)) | — | — | 30 | 5 |  |  |  |  |
| cv2_cascade_chi0_fock | lorenz_multi | 16 | 0.383 | 0.608 | 4.22e-06 (esn:1000) | 0.0501 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | lorenz_uni | 16 | 0.287 | 0.653 | 0.000172 (esn:300) | 0.084 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| cv2_cascade_chi0_fock | mc30 | 16 | 0.972 | 0.982 | 1.5e-07 (kerr_delay:300) | 0.713 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | mc30_n5 | 16 | 0.973 | 0.982 | 0.0389 (kerr_delay:100) | 0.719 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | mg10 | 16 | 0.598 | 0.787 | 2.77e-09 (kerr_delay:300) | 0.0186 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | mg10_small | 16 | 0.811 | 0.864 | 0.00471 (kerr_delay:300) | 0.0755 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | mg20 | 16 | 0.267 | 0.462 | 9.57e-08 (esn:1000) | 0.0121 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | narma10 | 16 | 0.837 | 0.842 | 0.0134 (kerr_delay:300) | 0.282 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | narma10_n5 | 16 | 0.835 | 0.851 | 0.0554 (kerr_delay:100) | 0.288 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | narma10_small | 16 | 0.898 | 0.95 | 0.143 (polynarx:(30, 1)) | 0.385 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | narma2 | 16 | 0.482 | 0.557 | 5.73e-06 (esn:1000) | 0.027 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | narma20 | 16 | 0.799 | 0.821 | 0.1 (kerr_delay:300) | 0.383 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | narma5 | 16 | 0.723 | 0.778 | 0.000111 (esn:1000) | 0.138 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | xor | 16 | 0.904 | 0.943 | 4.38e-25 (polynarx:(20, 2)) | 0.626 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | xor_n1 | 16 | 0.904 | 0.946 | 0.00101 (esn:1000) | 0.64 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | xor_n5 | 16 | 0.9 | 0.942 | 0.023 (kerr_delay:100) | 0.699 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_fock | xprod | 16 | 0.965 | 0.976 | 6.6e-24 (polynarx:(10, 2)) | 0.764 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| cv2_cascade_chi0_fock | xprod_n1 | 16 | 0.965 | 0.974 | 0.00248 (polynarx:(10, 2)) | 0.765 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| cv2_cascade_chi0_fock | xprod_n5 | 16 | 0.964 | 0.974 | 0.0592 (polynarx:(10, 2)) | 0.777 (polynarx:(3, 2)) | — | — | 30 | 5 |  |  |  |  |
| cv2_cascade_chi0_moments | lorenz_multi | 8 | 0.52 | 0.586 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | lorenz_uni | 8 | 0.5 | 0.52 | 0.000172 (esn:300) | 0.17 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | mc30 | 8 | 0.973 | 0.976 | 1.5e-07 (kerr_delay:300) | 0.869 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | mc30_n5 | 8 | 0.975 | 0.977 | 0.0389 (kerr_delay:100) | 0.873 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | mg10 | 8 | 0.859 | 0.903 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | mg10_small | 8 | 0.929 | 0.947 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | mg20 | 8 | 0.374 | 0.516 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | narma10 | 8 | 0.83 | 0.814 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | narma10_n5 | 8 | 0.818 | 0.811 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | narma10_small | 8 | 0.927 | 0.965 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | narma2 | 8 | 0.465 | 0.482 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | narma20 | 8 | 0.767 | 0.777 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | narma5 | 8 | 0.726 | 0.742 | 0.000111 (kerr_delay:300) | 0.314 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | xor | 8 | 0.939 | 0.94 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | xor_n1 | 8 | 0.939 | 0.94 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | xor_n5 | 8 | 0.94 | 0.942 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_chi0_moments | xprod | 8 | 0.971 | 0.983 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| cv2_cascade_chi0_moments | xprod_n1 | 8 | 0.972 | 0.984 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| cv2_cascade_chi0_moments | xprod_n5 | 8 | 0.974 | 0.985 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | lorenz_multi | 16 | 0.342 | 0.512 | 4.22e-06 (esn:1000) | 0.0501 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | lorenz_uni | 16 | 0.183 | 0.42 | 0.000172 (esn:300) | 0.084 (esn:10) | — | — | 30 | 10 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | mc30 | 16 | 0.941 | 0.944 | 1.5e-07 (kerr_delay:300) | 0.713 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | mc30_n5 | 16 | 0.942 | 0.944 | 0.0389 (kerr_delay:100) | 0.719 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | mg10 | 16 | 0.413 | 0.636 | 2.77e-09 (kerr_delay:300) | 0.0186 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | mg10_small | 16 | 0.92 | 0.765 | 0.00471 (kerr_delay:300) | 0.0755 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | mg20 | 16 | 0.144 | 0.228 | 9.57e-08 (esn:1000) | 0.0121 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | narma10 | 16 | 0.756 | 0.765 | 0.0134 (kerr_delay:300) | 0.282 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | narma10_n5 | 16 | 0.762 | 0.768 | 0.0554 (kerr_delay:100) | 0.288 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | narma10_small | 16 | 0.859 | 0.903 | 0.143 (polynarx:(30, 1)) | 0.385 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | narma2 | 16 | 0.429 | 0.447 | 5.73e-06 (esn:1000) | 0.027 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | narma20 | 16 | 0.771 | 0.78 | 0.1 (kerr_delay:300) | 0.383 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | narma5 | 16 | 0.697 | 0.716 | 0.000111 (esn:1000) | 0.138 (polynarx:(10, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | xor | 16 | 0.752 | 0.784 | 4.38e-25 (polynarx:(20, 2)) | 0.626 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | xor_n1 | 16 | 0.754 | 0.785 | 0.00101 (esn:1000) | 0.64 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | xor_n5 | 16 | 0.767 | 0.79 | 0.023 (esn:1000) | 0.699 (esn:10) | — | — | 30 | 10 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | xprod | 16 | 0.892 | 0.907 | 6.6e-24 (polynarx:(10, 2)) | 0.764 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | xprod_n1 | 16 | 0.89 | 0.906 | 0.00248 (polynarx:(10, 2)) | 0.765 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| cv2_cascade_kerr0.5_fock | xprod_n5 | 16 | 0.897 | 0.913 | 0.0592 (polynarx:(10, 2)) | 0.777 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | lorenz_multi | 8 | 0.439 | 0.467 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | lorenz_uni | 8 | 0.526 | 0.563 | 0.000172 (esn:300) | 0.17 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | mc30 | 8 | 0.943 | 0.944 | 1.5e-07 (kerr_delay:300) | 0.869 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | mc30_n5 | 8 | 0.945 | 0.946 | 0.0389 (kerr_delay:100) | 0.873 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | mg10 | 8 | 0.447 | 0.57 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | mg10_small | 8 | 0.781 | 0.782 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | mg20 | 8 | 0.109 | 0.149 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | narma10 | 8 | 0.722 | 0.721 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | narma10_n5 | 8 | 0.721 | 0.718 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | narma10_small | 8 | 0.889 | 0.89 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | narma2 | 8 | 0.44 | 0.433 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | narma20 | 8 | 0.767 | 0.767 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | narma5 | 8 | 0.573 | 0.585 | 0.000111 (kerr_delay:300) | 0.314 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | xor | 8 | 0.816 | 0.82 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | xor_n1 | 8 | 0.816 | 0.82 | 0.00101 (esn:1000) | 0.771 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | xor_n5 | 8 | 0.821 | 0.824 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | xprod | 8 | 0.951 | 0.949 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | 1e+03 | — | 30 | 10 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | xprod_n1 | 8 | 0.952 | 0.95 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | 1e+03 | — | 30 | 10 |  |  |  |  |
| cv2_cascade_kerr0.5_moments | xprod_n5 | 8 | 0.954 | 0.955 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | 1e+03 | — | 30 | 10 |  |  |  |  |
| forr_qrc | drift_kloos_n12 | 1 | 0.00604 | 0.00669 | 0.00604 (forr_full:4096) | 0.0113 (forr_pairs:20000) | 6e+04 | ∞ | 1 | >1000 |  |  |  |  |
| forr_qrc | drift_kloos_n16 | 1 | 0.000406 | 0.00107 | 0.000406 (forr_full:65536) | 0.000406 (forr_full:65536) | — | — | 1 | >1000 |  |  |  |  |
| forr_qrc | forr_gold_n10 | 1 | 0.00157 | 0.00172 | 0.00157 (forr_full:1024) | 0.00157 (forr_anf2:176) | ∞ | ∞ | 1 | >1000 |  |  |  |  |
| forr_qrc | forr_gold_n12 | 1 | 0.00157 | 0.00172 | 0.00157 (forr_full:4096) | 0.00157 (forr_anf2:222) | ∞ | ∞ | 1 | >1000 |  |  |  |  |
| forr_qrc | forr_gold_n14 | 1 | 0.00157 | 0.00172 | 0.00157 (forr_full:16384) | 0.00157 (forr_anf2:276) | ∞ | ∞ | 1 | >1000 |  |  |  |  |
| forr_qrc | forr_gold_n16 | 1 | 0.00157 | 0.00172 | 0.00157 (forr_full:65536) | 0.00157 (forr_anf2:338) | ∞ | ∞ | 1 | >1000 |  |  |  |  |
| forr_qrc | forr_kloos_n10 | 1 | 0.00102 | 0.00106 | 0.00102 (forr_full:1024) | 0.928 (forr_anf2:176) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_kloos_n12 | 1 | 0.000999 | 0.00103 | 0.000999 (forr_full:4096) | 1.01 (forr_anf2:222) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_kloos_n14 | 1 | 0.000945 | 0.00096 | 0.000945 (forr_full:16384) | 1.02 (forr_anf2:276) | 1e+02 | 6e+06 | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_kloos_n16 | 1 | 0.001 | 0.00106 | 0.001 (forr_full:65536) | 1.04 (forr_anf2:338) | 1e+02 | 6e+06 | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_kloos_n18 | 1 | 0.000973 | 0.00103 | 0.000973 (forr_full:262144) | 1.04 (forr_anf2:408) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_kloos_n20 | 1 | 0.000961 | 0.00101 | 0.000961 (forr_full:1048576) | 1.01 (forr_anf2:486) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_mm_n10 | 1 | 0.00148 | 0.00156 | 0.00148 (forr_full:1024) | 0.891 (forr_anf2:176) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_mm_n12 | 1 | 0.00148 | 0.00156 | 0.00148 (forr_full:4096) | 0.991 (forr_anf2:222) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_mm_n14 | 1 | 0.00148 | 0.00156 | 0.00148 (forr_full:16384) | 1.03 (forr_anf2:276) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_mm_n16 | 1 | 0.00148 | 0.00156 | 0.00148 (forr_full:65536) | 1.03 (forr_anf2:338) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_mmx_n10 | 1 | 0.00148 | 0.00156 | 0.00148 (forr_full:1024) | 0.908 (forr_anf2:176) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_mmx_n12 | 1 | 0.00148 | 0.00156 | 0.00148 (forr_full:4096) | 0.95 (forr_anf2:222) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_mmx_n14 | 1 | 0.00148 | 0.00156 | 0.00148 (forr_full:16384) | 1.01 (forr_anf2:276) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_mmx_n16 | 1 | 0.00148 | 0.00156 | 0.00148 (forr_full:65536) | 1.03 (forr_anf2:338) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_rand_n10 | 1 | 0.00117 | 0.00118 | 0.00117 (forr_full:1024) | 0.96 (forr_anf2:176) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_rand_n12 | 1 | 0.000964 | 0.000993 | 0.000964 (forr_full:4096) | 1.01 (forr_anf2:222) | 1e+02 | ∞ | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_rand_n14 | 1 | 0.000829 | 0.000924 | 0.000829 (forr_full:16384) | 1.01 (forr_anf2:276) | 1e+02 | — | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_rand_n16 | 1 | 0.000861 | 0.000902 | 0.000861 (forr_full:65536) | 1.01 (forr_anf2:338) | 1e+02 | 6e+06 | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_rand_n18 | 1 | 0.000858 | 0.000938 | 0.000858 (forr_full:262144) | 1.03 (forr_anf2:408) | 1e+02 | 6e+06 | 1 | >1000 |  | y |  |  |
| forr_qrc | forr_rand_n20 | 1 | 0.00083 | 0.0009 | 0.00083 (forr_full:1048576) | 1.02 (forr_anf2:486) | 1e+02 | — | 1 | >1000 |  | y |  |  |
| qkerr_delay_D100_chi0 | lorenz_multi | 300 | 0.485 | 0.508 | 4.22e-06 (esn:300) | 4.22e-06 (esn:300) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D100_chi0 | lorenz_uni | 300 | 0.572 | 0.672 | 0.000172 (esn:300) | 0.000172 (esn:300) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D100_chi0 | mc30 | 300 | 0.0324 | 0.0377 | 1.5e-07 (kerr_delay:300) | 3.79e-07 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_chi0 | mc30_n5 | 300 | 0.0579 | 0.0662 | 0.0389 (kerr_delay:100) | 0.0389 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_chi0 | mg10 | 300 | 0.0118 | 0.0148 | 2.77e-09 (kerr_delay:300) | 8.06e-08 (kerr_delay:100) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi0 | mg10_small | 300 | 0.11 | 0.124 | 0.00471 (kerr_delay:100) | 0.00471 (kerr_delay:100) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_chi0 | mg20 | 300 | 0.0113 | 0.0135 | 9.57e-08 (esn:1000) | 8.29e-07 (esn:300) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_chi0 | narma10 | 300 | 0.134 | 0.153 | 0.0134 (kerr_delay:300) | 0.0259 (kerr_delay:100) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D100_chi0 | narma10_n5 | 300 | 0.172 | 0.199 | 0.0554 (kerr_delay:100) | 0.0608 (kerr_delay:100) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D100_chi0 | narma10_small | 300 | 0.709 | 0.563 | 0.143 (polynarx:(20, 2)) | 0.143 (polynarx:(20, 2)) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D100_chi0 | narma2 | 300 | 0.179 | 0.198 | 5.73e-06 (esn:1000) | 1.8e-05 (esn:300) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D100_chi0 | narma20 | 300 | 0.131 | 0.142 | 0.1 (kerr_delay:100) | 0.136 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_chi0 | narma5 | 300 | 0.13 | 0.143 | 0.000111 (esn:1000) | 0.000244 (kerr_delay:100) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi0 | xor | 300 | 0.875 | 0.965 | 4.38e-25 (polynarx:(20, 2)) | 4.38e-25 (polynarx:(20, 2)) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D100_chi0 | xor_n1 | 300 | 0.872 | 0.966 | 0.00101 (esn:1000) | 0.00102 (polynarx:(20, 2)) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D100_chi0 | xor_n5 | 300 | 0.876 | 0.968 | 0.023 (kerr_delay:100) | 0.023 (kerr_delay:100) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D100_chi0 | xprod | 300 | 0.878 | 0.991 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_chi0 | xprod_n1 | 300 | 0.895 | 0.998 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_chi0 | xprod_n5 | 300 | 0.908 | 1.03 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | lorenz_multi | 300 | 0.262 | 0.322 | 4.22e-06 (esn:1000) | 4.22e-06 (esn:300) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | lorenz_uni | 300 | 0.191 | 0.239 | 0.000172 (esn:300) | 0.000172 (esn:300) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | mc30 | 300 | 0.117 | 0.119 | 1.5e-07 (kerr_delay:300) | 3.79e-07 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | mc30_n5 | 300 | 0.153 | 0.155 | 0.0389 (kerr_delay:100) | 0.0389 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | mg10 | 300 | 0.00219 | 0.00353 | 2.77e-09 (kerr_delay:300) | 8.06e-08 (esn:300) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | mg10_small | 300 | 0.00905 | 0.0109 | 0.00471 (kerr_delay:300) | 0.00471 (esn:300) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | mg20 | 300 | 0.00388 | 0.0068 | 9.57e-08 (esn:1000) | 8.29e-07 (esn:300) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | narma10 | 300 | 0.137 | 0.134 | 0.0134 (kerr_delay:300) | 0.0259 (kerr_delay:100) | — | — | 30 | 300 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | narma10_n5 | 300 | 0.159 | 0.159 | 0.0554 (kerr_delay:100) | 0.0608 (kerr_delay:100) | — | — | 30 | 300 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | narma10_small | 300 | 0.281 | 0.276 | 0.143 (polynarx:(30, 1)) | 0.143 (polynarx:(30, 1)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | narma2 | 300 | 0.114 | 0.114 | 5.73e-06 (esn:1000) | 1.8e-05 (esn:300) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | narma20 | 300 | 0.215 | 0.218 | 0.1 (kerr_delay:100) | 0.136 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | narma5 | 300 | 0.0898 | 0.0932 | 0.000111 (kerr_delay:300) | 0.000244 (kerr_delay:100) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | xor | 300 | 0.78 | 0.771 | 4.38e-25 (polynarx:(20, 2)) | 4.38e-25 (polynarx:(20, 2)) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | xor_n1 | 300 | 0.783 | 0.774 | 0.00101 (kerr_delay:100) | 0.00102 (kerr_delay:100) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | xor_n5 | 300 | 0.785 | 0.776 | 0.023 (esn:1000) | 0.023 (esn:300) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | xprod | 300 | 0.466 | 0.475 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | xprod_n1 | 300 | 0.481 | 0.49 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D100_chi0.3 | xprod_n5 | 300 | 0.519 | 0.524 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D100_chi1 | lorenz_multi | 300 | 0.251 | 0.304 | 4.22e-06 (esn:1000) | 4.22e-06 (esn:300) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_chi1 | lorenz_uni | 300 | 0.171 | 0.196 | 0.000172 (esn:300) | 0.000172 (esn:300) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_chi1 | mc30 | 300 | 0.104 | 0.106 | 1.5e-07 (kerr_delay:300) | 3.79e-07 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_chi1 | mc30_n5 | 300 | 0.142 | 0.144 | 0.0389 (kerr_delay:100) | 0.0389 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_chi1 | mg10 | 300 | 0.00239 | 0.0036 | 2.77e-09 (kerr_delay:300) | 8.06e-08 (esn:300) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi1 | mg10_small | 300 | 0.0101 | 0.012 | 0.00471 (esn:1000) | 0.00471 (kerr_delay:100) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D100_chi1 | mg20 | 300 | 0.00317 | 0.00519 | 9.57e-08 (esn:1000) | 8.29e-07 (esn:300) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi1 | narma10 | 300 | 0.167 | 0.167 | 0.0134 (kerr_delay:300) | 0.0259 (kerr_delay:100) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D100_chi1 | narma10_n5 | 300 | 0.179 | 0.18 | 0.0554 (kerr_delay:100) | 0.0608 (kerr_delay:100) | — | — | 30 | 300 |  |  |  |  |
| qkerr_delay_D100_chi1 | narma10_small | 300 | 0.311 | 0.311 | 0.143 (polynarx:(30, 1)) | 0.143 (polynarx:(30, 1)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_chi1 | narma2 | 300 | 0.115 | 0.115 | 5.73e-06 (esn:1000) | 1.8e-05 (esn:300) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D100_chi1 | narma20 | 300 | 0.199 | 0.196 | 0.1 (kerr_delay:300) | 0.136 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_chi1 | narma5 | 300 | 0.101 | 0.102 | 0.000111 (kerr_delay:300) | 0.000244 (kerr_delay:100) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi1 | xor | 300 | 0.584 | 0.589 | 4.38e-25 (polynarx:(20, 2)) | 4.38e-25 (polynarx:(20, 2)) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi1 | xor_n1 | 300 | 0.585 | 0.589 | 0.00101 (kerr_delay:100) | 0.00102 (kerr_delay:100) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi1 | xor_n5 | 300 | 0.597 | 0.6 | 0.023 (kerr_delay:100) | 0.023 (kerr_delay:100) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi1 | xprod | 300 | 0.56 | 0.565 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi1 | xprod_n1 | 300 | 0.566 | 0.576 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_chi1 | xprod_n5 | 300 | 0.578 | 0.589 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_tuned | lorenz_multi | 300 | 0.115 | 0.15 | 4.22e-06 (esn:1000) | 4.22e-06 (esn:300) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_tuned | lorenz_uni | 300 | 0.0358 | 0.0458 | 0.000172 (esn:300) | 0.000172 (esn:300) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_tuned | mc30 | 300 | 0.026 | 0.0294 | 7.66e-07 (kerr_delay:300) | 3.29e-06 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_tuned | mc30_n5 | 300 | 0.0617 | 0.0642 | 0.0401 (kerr_delay:100) | 0.0401 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_tuned | mg10 | 300 | 0.00164 | 0.00292 | 2.77e-09 (kerr_delay:300) | 8.06e-08 (kerr_delay:100) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_tuned | mg10_small | 300 | 0.0225 | 0.0339 | 0.00471 (kerr_delay:300) | 0.00471 (esn:300) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_tuned | mg20 | 300 | 0.00218 | 0.00345 | 9.57e-08 (esn:1000) | 8.29e-07 (esn:300) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_tuned | narma10 | 300 | 0.0925 | 0.1 | 0.0134 (kerr_delay:300) | 0.0259 (kerr_delay:100) | — | — | 30 | 1000 |  |  |  |  |
| qkerr_delay_D100_tuned | narma10_n5 | 300 | 0.107 | 0.109 | 0.0554 (kerr_delay:100) | 0.0608 (kerr_delay:100) | — | — | 30 | 1000 |  |  |  |  |
| qkerr_delay_D100_tuned | narma10_small | 300 | 0.477 | 0.46 | 0.143 (polynarx:(30, 1)) | 0.143 (polynarx:(30, 1)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D100_tuned | narma2 | 300 | 0.0097 | 0.0103 | 5.73e-06 (esn:1000) | 1.8e-05 (esn:300) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D100_tuned | narma20 | 300 | 0.2 | 0.22 | 0.109 (kerr_delay:300) | 0.154 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_tuned | narma5 | 300 | 0.0132 | 0.0195 | 0.000111 (kerr_delay:300) | 0.000244 (kerr_delay:100) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D100_tuned | xor | 300 | 0.0563 | 0.0835 | 4.38e-25 (polynarx:(20, 2)) | 4.38e-25 (polynarx:(20, 2)) | — | — | 30 | 1000 |  |  |  |  |
| qkerr_delay_D100_tuned | xor_n1 | 300 | 0.0586 | 0.0856 | 0.00101 (kerr_delay:100) | 0.00102 (kerr_delay:100) | — | — | 30 | 1000 |  |  |  |  |
| qkerr_delay_D100_tuned | xor_n5 | 300 | 0.0653 | 0.0879 | 0.0241 (kerr_delay:100) | 0.0241 (kerr_delay:100) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D100_tuned | xprod | 300 | 0.086 | 0.106 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 300 |  |  |  |  |
| qkerr_delay_D100_tuned | xprod_n1 | 300 | 0.0879 | 0.108 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 300 |  |  |  |  |
| qkerr_delay_D100_tuned | xprod_n5 | 300 | 0.143 | 0.169 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 300 |  |  |  |  |
| qkerr_delay_D30_chi0 | lorenz_multi | 90 | 0.484 | 0.502 | 4.22e-06 (esn:1000) | 0.0135 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0 | lorenz_uni | 90 | 0.618 | 0.631 | 0.000172 (esn:1000) | 0.00808 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0 | mc30 | 90 | 0.289 | 0.297 | 1.5e-07 (kerr_delay:300) | 0.0345 (kerr_delay:30) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D30_chi0 | mc30_n5 | 90 | 0.321 | 0.33 | 0.0389 (kerr_delay:100) | 0.0613 (polynarx:(30, 1)) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D30_chi0 | mg10 | 90 | 0.136 | 0.146 | 2.77e-09 (kerr_delay:300) | 9.82e-05 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0 | mg10_small | 90 | 0.3 | 0.514 | 0.00471 (esn:1000) | 0.011 (esn:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0 | mg20 | 90 | 0.102 | 0.113 | 9.57e-08 (esn:1000) | 0.000114 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0 | narma10 | 90 | 0.342 | 0.365 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi0 | narma10_n5 | 90 | 0.429 | 0.426 | 0.0554 (kerr_delay:100) | 0.112 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi0 | narma10_small | 90 | 0.7 | 1.07 | 0.143 (polynarx:(30, 1)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0 | narma2 | 90 | 0.393 | 0.403 | 5.73e-06 (esn:1000) | 0.00449 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0 | narma20 | 90 | 0.308 | 0.31 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D30_chi0 | narma5 | 90 | 0.348 | 0.354 | 0.000111 (esn:1000) | 0.00305 (polynarx:(10, 2)) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi0 | xor | 90 | 0.951 | 0.968 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0 | xor_n1 | 90 | 0.951 | 0.967 | 0.00101 (esn:1000) | 0.0502 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0 | xor_n5 | 90 | 0.952 | 0.969 | 0.023 (kerr_delay:100) | 0.0887 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0 | xprod | 90 | 0.963 | 0.996 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi0 | xprod_n1 | 90 | 0.964 | 0.994 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi0 | xprod_n5 | 90 | 0.969 | 0.998 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | lorenz_multi | 90 | 0.361 | 0.378 | 4.22e-06 (esn:1000) | 0.0135 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | lorenz_uni | 90 | 0.39 | 0.413 | 0.000172 (esn:300) | 0.00808 (esn:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | mc30 | 90 | 0.304 | 0.307 | 1.5e-07 (kerr_delay:300) | 0.0345 (kerr_delay:30) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | mc30_n5 | 90 | 0.31 | 0.314 | 0.0389 (kerr_delay:100) | 0.0613 (polynarx:(30, 1)) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | mg10 | 90 | 0.0176 | 0.024 | 2.77e-09 (kerr_delay:300) | 9.82e-05 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | mg10_small | 90 | 0.101 | 0.127 | 0.00471 (kerr_delay:300) | 0.011 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | mg20 | 90 | 0.0171 | 0.0221 | 9.57e-08 (esn:1000) | 0.000114 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | narma10 | 90 | 0.235 | 0.236 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | narma10_n5 | 90 | 0.247 | 0.245 | 0.0554 (kerr_delay:100) | 0.112 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | narma10_small | 90 | 0.945 | 0.637 | 0.143 (polynarx:(20, 2)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | narma2 | 90 | 0.177 | 0.179 | 5.73e-06 (esn:1000) | 0.00449 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | narma20 | 90 | 0.292 | 0.293 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | narma5 | 90 | 0.193 | 0.196 | 0.000111 (esn:1000) | 0.00305 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | xor | 90 | 0.939 | 0.937 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | xor_n1 | 90 | 0.939 | 0.937 | 0.00101 (kerr_delay:100) | 0.0502 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | xor_n5 | 90 | 0.943 | 0.942 | 0.023 (kerr_delay:100) | 0.0887 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | xprod | 90 | 0.81 | 0.822 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | xprod_n1 | 90 | 0.817 | 0.828 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi0.3 | xprod_n5 | 90 | 0.835 | 0.846 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | lorenz_multi | 90 | 0.297 | 0.329 | 4.22e-06 (esn:1000) | 0.0135 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | lorenz_uni | 90 | 0.22 | 0.239 | 0.000172 (esn:300) | 0.00808 (esn:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | mc30 | 90 | 0.494 | 0.498 | 1.5e-07 (kerr_delay:300) | 0.0345 (kerr_delay:30) | — | — | 30 | 1000 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | mc30_n5 | 90 | 0.499 | 0.503 | 0.0389 (kerr_delay:100) | 0.0613 (polynarx:(30, 1)) | — | — | 30 | 1000 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | mg10 | 90 | 0.0117 | 0.0147 | 2.77e-09 (kerr_delay:300) | 9.82e-05 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | mg10_small | 90 | 0.0473 | 0.0533 | 0.00471 (kerr_delay:300) | 0.011 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | mg20 | 90 | 0.0112 | 0.0135 | 9.57e-08 (esn:1000) | 0.000114 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | narma10 | 90 | 0.232 | 0.232 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | narma10_n5 | 90 | 0.258 | 0.258 | 0.0554 (kerr_delay:100) | 0.112 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | narma10_small | 90 | 0.618 | 0.645 | 0.143 (polynarx:(30, 1)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | narma2 | 90 | 0.123 | 0.124 | 5.73e-06 (esn:1000) | 0.00449 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | narma20 | 90 | 0.375 | 0.375 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | narma5 | 90 | 0.139 | 0.139 | 0.000111 (esn:1000) | 0.00305 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | xor | 90 | 0.811 | 0.813 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | xor_n1 | 90 | 0.812 | 0.814 | 0.00101 (kerr_delay:100) | 0.0502 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | xor_n5 | 90 | 0.822 | 0.824 | 0.023 (kerr_delay:100) | 0.0887 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | xprod | 90 | 0.636 | 0.644 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | xprod_n1 | 90 | 0.638 | 0.646 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi0.3_bright | xprod_n5 | 90 | 0.66 | 0.666 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi1 | lorenz_multi | 90 | 0.338 | 0.38 | 4.22e-06 (esn:1000) | 0.0135 (polynarx:(3, 2)) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi1 | lorenz_uni | 90 | 0.395 | 0.433 | 0.000172 (esn:300) | 0.00808 (esn:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi1 | mc30 | 90 | 0.29 | 0.293 | 1.5e-07 (kerr_delay:300) | 0.0345 (polynarx:(30, 1)) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D30_chi1 | mc30_n5 | 90 | 0.301 | 0.303 | 0.0389 (kerr_delay:100) | 0.0613 (polynarx:(30, 1)) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D30_chi1 | mg10 | 90 | 0.00957 | 0.0125 | 2.77e-09 (kerr_delay:300) | 9.82e-05 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi1 | mg10_small | 90 | 0.106 | 0.0696 | 0.00471 (esn:1000) | 0.011 (esn:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi1 | mg20 | 90 | 0.0117 | 0.0134 | 9.57e-08 (esn:1000) | 0.000114 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi1 | narma10 | 90 | 0.26 | 0.264 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_chi1 | narma10_n5 | 90 | 0.273 | 0.276 | 0.0554 (kerr_delay:100) | 0.112 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_chi1 | narma10_small | 90 | 0.877 | 0.725 | 0.143 (polynarx:(20, 2)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi1 | narma2 | 90 | 0.181 | 0.182 | 5.73e-06 (esn:1000) | 0.00449 (esn:30) | — | — | 30 | 3 |  |  |  |  |
| qkerr_delay_D30_chi1 | narma20 | 90 | 0.367 | 0.372 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi1 | narma5 | 90 | 0.184 | 0.186 | 0.000111 (kerr_delay:300) | 0.00305 (polynarx:(10, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi1 | xor | 90 | 0.82 | 0.817 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi1 | xor_n1 | 90 | 0.819 | 0.817 | 0.00101 (kerr_delay:100) | 0.0502 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi1 | xor_n5 | 90 | 0.826 | 0.824 | 0.023 (kerr_delay:100) | 0.0887 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi1 | xprod | 90 | 0.853 | 0.854 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi1 | xprod_n1 | 90 | 0.85 | 0.853 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi1 | xprod_n5 | 90 | 0.854 | 0.857 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | lorenz_multi | 90 | 0.253 | 0.346 | 4.22e-06 (esn:1000) | 0.0135 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | lorenz_uni | 90 | 0.138 | 0.292 | 0.000172 (esn:300) | 0.00808 (esn:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | mc30 | 90 | 0.499 | 0.547 | 1.5e-07 (kerr_delay:300) | 0.0345 (kerr_delay:30) | — | — | 30 | 300 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | mc30_n5 | 90 | 0.518 | 0.562 | 0.0389 (kerr_delay:100) | 0.0613 (kerr_delay:30) | — | — | 30 | 300 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | mg10 | 90 | 0.0314 | 0.0682 | 2.77e-09 (kerr_delay:300) | 9.82e-05 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | mg10_small | 90 | 0.176 | 0.398 | 0.00471 (esn:1000) | 0.011 (esn:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | mg20 | 90 | 0.0105 | 0.0282 | 9.57e-08 (esn:1000) | 0.000114 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | narma10 | 90 | 0.205 | 0.255 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | narma10_n5 | 90 | 0.23 | 0.295 | 0.0554 (kerr_delay:100) | 0.112 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | narma10_small | 90 | 0.611 | 0.619 | 0.143 (polynarx:(30, 1)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | narma2 | 90 | 0.0298 | 0.0358 | 5.73e-06 (esn:1000) | 0.00449 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | narma20 | 90 | 0.632 | 0.664 | 0.1 (kerr_delay:300) | 0.187 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | narma5 | 90 | 0.0467 | 0.0553 | 0.000111 (kerr_delay:300) | 0.00305 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | xor | 90 | 0.265 | 0.289 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | xor_n1 | 90 | 0.265 | 0.291 | 0.00101 (kerr_delay:100) | 0.0502 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | xor_n5 | 90 | 0.276 | 0.305 | 0.023 (kerr_delay:100) | 0.0887 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | xprod | 90 | 0.293 | 0.35 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | xprod_n1 | 90 | 0.293 | 0.355 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_chi1_lossy | xprod_n5 | 90 | 0.327 | 0.39 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_tuned | lorenz_multi | 90 | 0.196 | 0.253 | 4.22e-06 (esn:1000) | 0.0135 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_tuned | lorenz_uni | 90 | 0.0963 | 0.118 | 0.000172 (esn:300) | 0.00808 (esn:30) | — | — | 30 | 10 |  |  |  |  |
| qkerr_delay_D30_tuned | mc30 | 90 | 0.123 | 0.134 | 1.5e-07 (kerr_delay:300) | 0.0345 (kerr_delay:30) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D30_tuned | mc30_n5 | 90 | 0.148 | 0.158 | 0.0389 (kerr_delay:100) | 0.0613 (kerr_delay:30) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D30_tuned | mg10 | 90 | 0.00804 | 0.0128 | 2.77e-09 (kerr_delay:300) | 9.82e-05 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_tuned | mg10_small | 90 | 0.0318 | 0.0386 | 0.00471 (kerr_delay:300) | 0.011 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_tuned | mg20 | 90 | 0.00715 | 0.0109 | 9.57e-08 (esn:1000) | 0.000114 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_tuned | narma10 | 90 | 0.17 | 0.18 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_tuned | narma10_n5 | 90 | 0.184 | 0.184 | 0.0554 (kerr_delay:100) | 0.112 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_tuned | narma10_small | 90 | 0.542 | 0.462 | 0.143 (polynarx:(30, 1)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 5 |  |  |  |  |
| qkerr_delay_D30_tuned | narma2 | 90 | 0.0194 | 0.0224 | 5.73e-06 (esn:1000) | 0.00449 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| qkerr_delay_D30_tuned | narma20 | 90 | 0.238 | 0.244 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | >1000 |  |  |  |  |
| qkerr_delay_D30_tuned | narma5 | 90 | 0.0612 | 0.0749 | 0.000111 (esn:1000) | 0.00305 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_tuned | xor | 90 | 0.203 | 0.263 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_tuned | xor_n1 | 90 | 0.207 | 0.263 | 0.00101 (esn:1000) | 0.0502 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_tuned | xor_n5 | 90 | 0.236 | 0.283 | 0.023 (kerr_delay:100) | 0.0887 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_tuned | xprod | 90 | 0.307 | 0.348 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_tuned | xprod_n1 | 90 | 0.314 | 0.354 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| qkerr_delay_D30_tuned | xprod_n5 | 90 | 0.342 | 0.409 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | lorenz_multi | 90 | 0.000517 | 0.141 | 7.28e-06 (esn:1000) | 0.0135 (polynarx:(3, 2)) | ∞ | — | 30 | 100 |  | y |  |  |
| spin_hamenc_chain_N6_xyz_V5 | lorenz_uni | 90 | 0.0101 | 0.368 | 0.000172 (esn:1000) | 0.00808 (kerr_delay:30) | — | — | 30 | 100 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | mc30 | 90 | 0.955 | 1.02 | 1.5e-07 (kerr_delay:300) | 0.0345 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | mc30_n5 | 90 | 0.957 | 1.02 | 0.0389 (kerr_delay:100) | 0.0613 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | mg10 | 90 | 0.1 | 0.65 | 2.77e-09 (kerr_delay:300) | 9.82e-05 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | mg10_small | 90 | 0.236 | 1.11 | 0.00471 (kerr_delay:300) | 0.011 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | mg20 | 90 | 0.0144 | 0.17 | 9.57e-08 (esn:1000) | 0.000114 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | narma10 | 90 | 0.69 | 0.803 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | narma10_n5 | 90 | 0.703 | 0.815 | 0.0554 (kerr_delay:100) | 0.112 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | narma10_small | 90 | 0.84 | 1.05 | 0.143 (polynarx:(30, 1)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | narma2 | 90 | 0.129 | 0.303 | 5.73e-06 (esn:1000) | 0.00449 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | narma20 | 90 | 0.741 | 0.762 | 0.1 (kerr_delay:300) | 0.187 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | narma5 | 90 | 0.618 | 0.695 | 0.000111 (esn:1000) | 0.00305 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | xor | 90 | 0.578 | 0.821 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | xor_n1 | 90 | 0.592 | 0.818 | 0.00101 (kerr_delay:100) | 0.0502 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | xor_n5 | 90 | 0.645 | 0.819 | 0.023 (kerr_delay:100) | 0.0887 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | xprod | 90 | 0.786 | 1 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | xprod_n1 | 90 | 0.785 | 1 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_chain_N6_xyz_V5 | xprod_n5 | 90 | 0.812 | 1 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | lorenz_multi | 180 | 0.0222 | 0.36 | 4.22e-06 (esn:1000) | 0.000251 (esn:100) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | lorenz_uni | 180 | 0.0629 | 0.525 | 0.000172 (esn:1000) | 0.000664 (esn:100) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | mc30 | 180 | 0.705 | 0.856 | 1.5e-07 (kerr_delay:300) | 0.0345 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | mc30_n5 | 180 | 0.716 | 0.863 | 0.0389 (kerr_delay:100) | 0.0613 (polynarx:(30, 1)) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | mg10 | 180 | 0.00126 | 0.263 | 2.77e-09 (kerr_delay:300) | 4.15e-06 (esn:100) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | mg10_small | 180 | 0.111 | 0.628 | 0.00471 (kerr_delay:300) | 0.00857 (esn:100) | — | — | 30 | 10 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | mg20 | 180 | 0.000492 | 0.126 | 9.57e-08 (esn:1000) | 2.26e-05 (esn:100) | — | — | 30 | 100 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | narma10 | 180 | 0.606 | 0.782 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | narma10_n5 | 180 | 0.63 | 0.791 | 0.0554 (kerr_delay:100) | 0.112 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | narma10_small | 180 | 0.944 | 1.12 | 0.143 (polynarx:(30, 1)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | narma2 | 180 | 0.119 | 0.485 | 5.73e-06 (esn:1000) | 0.000151 (esn:100) | — | — | 30 | 5 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | narma20 | 180 | 0.697 | 0.83 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | narma5 | 180 | 0.226 | 0.565 | 0.000111 (esn:1000) | 0.00292 (esn:100) | — | — | 30 | 10 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | xor | 180 | 0.416 | 0.814 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | xor_n1 | 180 | 0.42 | 0.814 | 0.00101 (kerr_delay:100) | 0.0502 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | xor_n5 | 180 | 0.443 | 0.822 | 0.023 (esn:1000) | 0.0887 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | xprod | 180 | 0.431 | 0.927 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | xprod_n1 | 180 | 0.433 | 0.927 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT | xprod_n5 | 180 | 0.471 | 0.934 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | lorenz_multi | 180 | 0.00176 | 0.26 | 4.22e-06 (esn:1000) | 0.000251 (esn:100) | — | — | 30 | 100 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | lorenz_uni | 180 | 0.00522 | 0.43 | 0.000172 (esn:300) | 0.000664 (esn:100) | — | — | 30 | 100 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | mc30 | 180 | 0.967 | 1.13 | 1.5e-07 (kerr_delay:300) | 0.0345 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | mc30_n5 | 180 | 0.968 | 1.13 | 0.0389 (kerr_delay:100) | 0.0613 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | mg10 | 180 | 0.00325 | 0.681 | 2.77e-09 (kerr_delay:300) | 4.15e-06 (esn:100) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | mg10_small | 180 | 0.0793 | 0.943 | 0.00471 (esn:1000) | 0.00857 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | mg20 | 180 | 0.000458 | 0.232 | 9.57e-08 (esn:1000) | 2.26e-05 (esn:100) | — | — | 30 | 100 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | narma10 | 180 | 0.789 | 0.989 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | narma10_n5 | 180 | 0.799 | 0.997 | 0.0554 (kerr_delay:100) | 0.112 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | narma10_small | 180 | 0.992 | 2.07 | 0.143 (polynarx:(30, 1)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | narma2 | 180 | 0.311 | 0.788 | 5.73e-06 (esn:1000) | 0.000151 (esn:100) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | narma20 | 180 | 0.905 | 1.03 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | narma5 | 180 | 0.698 | 0.975 | 0.000111 (esn:1000) | 0.00292 (esn:100) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | xor | 180 | 0.68 | 1.12 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | xor_n1 | 180 | 0.716 | 1.12 | 0.00101 (kerr_delay:100) | 0.0502 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | xor_n5 | 180 | 0.726 | 1.11 | 0.023 (kerr_delay:100) | 0.0887 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | xprod | 180 | 0.781 | 1.09 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | xprod_n1 | 180 | 0.781 | 1.09 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V10_weakT_amp1 | xprod_n5 | 180 | 0.813 | 1.1 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | lorenz_multi | 90 | 0.000861 | 0.149 | 7.28e-06 (esn:300) | 0.0135 (esn:30) | ∞ | — | 30 | 100 |  | y |  |  |
| spin_hamenc_rand_N6_xyz_V5 | lorenz_uni | 90 | 0.00516 | 0.365 | 0.000172 (esn:300) | 0.00808 (esn:30) | ∞ | — | 30 | 100 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | mc30 | 90 | 0.957 | 0.988 | 1.5e-07 (kerr_delay:300) | 0.0345 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | mc30_n5 | 90 | 0.959 | 0.99 | 0.0389 (kerr_delay:100) | 0.0613 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | mg10 | 90 | 0.0339 | 0.638 | 2.77e-09 (kerr_delay:300) | 9.82e-05 (kerr_delay:30) | — | — | 30 | 10 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | mg10_small | 90 | 0.254 | 0.961 | 0.00471 (kerr_delay:300) | 0.011 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | mg20 | 90 | 0.00391 | 0.121 | 9.57e-08 (esn:1000) | 0.000114 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | narma10 | 90 | 0.713 | 0.857 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | narma10_n5 | 90 | 0.726 | 0.841 | 0.0554 (kerr_delay:100) | 0.112 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | narma10_small | 90 | 0.852 | 0.996 | 0.143 (polynarx:(20, 2)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | narma2 | 90 | 0.159 | 0.453 | 5.73e-06 (esn:1000) | 0.00449 (kerr_delay:30) | — | — | 30 | 5 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | narma20 | 90 | 0.829 | 0.858 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | narma5 | 90 | 0.637 | 0.76 | 0.000111 (esn:1000) | 0.00305 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | xor | 90 | 0.557 | 0.95 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | xor_n1 | 90 | 0.579 | 0.948 | 0.00101 (kerr_delay:100) | 0.0502 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | xor_n5 | 90 | 0.672 | 0.952 | 0.023 (kerr_delay:100) | 0.0887 (kerr_delay:30) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | xprod | 90 | 0.771 | 0.972 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | xprod_n1 | 90 | 0.776 | 0.973 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5 | xprod_n5 | 90 | 0.804 | 0.978 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | lorenz_multi | 90 | 1.19 | 1.15 | 4.22e-06 (esn:300) | 0.0135 (esn:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | lorenz_uni | 90 | 1.27 | 1.27 | 0.000172 (esn:300) | 0.00808 (esn:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | mc30 | 90 | 1.04 | 1.05 | 1.5e-07 (kerr_delay:300) | 0.0345 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | mc30_n5 | 90 | 1.04 | 1.05 | 0.0389 (kerr_delay:100) | 0.0613 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | mg10 | 90 | 1.05 | 1.07 | 2.77e-09 (kerr_delay:300) | 9.82e-05 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | mg10_small | 90 | 1.34 | 1.34 | 0.00471 (kerr_delay:300) | 0.011 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | mg20 | 90 | 1.07 | 1.07 | 9.57e-08 (esn:1000) | 0.000114 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | narma10 | 90 | 1.04 | 1.03 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | narma10_n5 | 90 | 1.02 | 1.02 | 0.0554 (kerr_delay:100) | 0.112 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | narma10_small | 90 | 1.33 | 1.29 | 0.143 (polynarx:(30, 1)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | narma2 | 90 | 1.08 | 1.08 | 5.73e-06 (esn:1000) | 0.00449 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | narma20 | 90 | 1.03 | 1.06 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | narma5 | 90 | 1.03 | 1.05 | 0.000111 (kerr_delay:300) | 0.00305 (polynarx:(10, 2)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | xor | 90 | 1.03 | 1.08 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | xor_n1 | 90 | 1.03 | 1.05 | 0.00101 (kerr_delay:100) | 0.0502 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | xor_n5 | 90 | 1.04 | 1.04 | 0.023 (kerr_delay:100) | 0.0887 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | xprod | 90 | 1.03 | 1.04 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | xprod_n1 | 90 | 1.03 | 1.05 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 3 |  |  |  |  |
| spin_hamenc_rand_N6_xyz_V5_noT | xprod_n5 | 90 | 1.03 | 1.04 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 3 |  |  |  |  |
| spin_qin_rand_N6_xyz_V5 | qin_full | 90 | 1.05 | 1.18 | 0.113 (esn:1000) | 0.528 (esn:30) | — | — | 30 | 3 |  |  |  |  |
| spin_qin_rand_N6_xyz_V5 | qin_full_S | 90 | 1.06 | 1.15 | 0.126 (esn:1000) | 0.532 (esn:30) | — | — | 30 | 3 |  |  |  |  |
| spin_qin_rand_N6_xyz_V5 | qin_local | 90 | 1.05 | 1.18 | 0.0912 (polynarx:(3, 2)) | 0.623 (kerr_delay:30) | — | — | 30 | 3 |  |  |  |  |
| spin_qin_rand_N6_xyz_V5 | qin_local_S | 90 | 1.06 | 1.15 | 0.0922 (polynarx:(3, 2)) | 0.607 (esn:30) | — | — | 30 | 3 |  |  |  |  |
| spin_qin_rand_N6_zz | qin_full | 21 | 0.938 | 0.973 | 0.113 (esn:1000) | 0.708 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_qin_rand_N6_zz | qin_full_S | 21 | 0.946 | 0.986 | 0.126 (esn:1000) | 0.715 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_qin_rand_N6_zz | qin_local | 21 | 0.938 | 0.973 | 0.0912 (polynarx:(3, 2)) | 0.814 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_qin_rand_N6_zz | qin_local_S | 21 | 0.946 | 0.986 | 0.0922 (polynarx:(3, 2)) | 0.816 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_qin_rand_N6_zz_T1 | qin_full | 21 | 0.89 | 0.966 | 0.113 (esn:1000) | 0.708 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_qin_rand_N6_zz_T1 | qin_full_S | 21 | 0.903 | 0.97 | 0.126 (esn:1000) | 0.715 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_qin_rand_N6_zz_T1 | qin_local | 21 | 0.89 | 0.966 | 0.0912 (polynarx:(3, 2)) | 0.814 (esn:3) | — | — | 30 | 5 |  |  |  |  |
| spin_qin_rand_N6_zz_T1 | qin_local_S | 21 | 0.903 | 0.97 | 0.0922 (polynarx:(3, 2)) | 0.816 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_qin_rand_N6_zz_hybrid | qin_full | 221 | 0.595 | 0.62 | 0.113 (esn:1000) | 0.318 (esn:100) | — | — | 30 | 10 |  |  |  |  |
| spin_qin_rand_N6_zz_hybrid | qin_full_S | 221 | 0.596 | 0.618 | 0.126 (esn:1000) | 0.316 (esn:100) | — | — | 30 | 10 |  |  |  |  |
| spin_qin_rand_N6_zz_hybrid | qin_local | 221 | 0.595 | 0.62 | 0.0912 (polynarx:(3, 2)) | 0.0912 (polynarx:(3, 2)) | — | — | 30 | 100 |  |  |  |  |
| spin_qin_rand_N6_zz_hybrid | qin_local_S | 221 | 0.596 | 0.618 | 0.0922 (polynarx:(3, 2)) | 0.0922 (polynarx:(3, 2)) | — | — | 30 | 100 |  |  |  |  |
| spin_qin_rand_N6_zz_weak0.3 | qin_full | 21 | 0.949 | 0.983 | 0.113 (esn:1000) | 0.708 (esn:10) | — | — | 1 | 5 |  |  |  |  |
| spin_qin_rand_N6_zz_weak0.3 | qin_full_S | 21 | 0.943 | 0.978 | 0.126 (esn:1000) | 0.715 (esn:10) | — | — | 1 | 5 |  |  |  |  |
| spin_qin_rand_N6_zz_weak0.3 | qin_local | 21 | 0.949 | 0.983 | 0.0912 (polynarx:(3, 2)) | 0.814 (esn:3) | — | — | 1 | 5 |  |  |  |  |
| spin_qin_rand_N6_zz_weak0.3 | qin_local_S | 21 | 0.943 | 0.978 | 0.0922 (polynarx:(3, 2)) | 0.816 (esn:3) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_chain_N4_z | lorenz_multi | 4 | 0.484 | 0.696 | 4.22e-06 (esn:1000) | 0.345 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | lorenz_uni | 4 | 0.655 | 0.749 | 0.000172 (esn:300) | 0.304 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | mc30 | 4 | 0.907 | 0.909 | 7.66e-07 (kerr_delay:300) | 0.936 (esn:3) | 1e+03 | — | 30 | 5 |  | y |  |  |
| spin_reset_chain_N4_z | mc30_n5 | 4 | 0.909 | 0.912 | 0.0401 (kerr_delay:100) | 0.937 (esn:3) | 1e+03 | — | 30 | 5 |  | y |  |  |
| spin_reset_chain_N4_z | mg10 | 4 | 0.317 | 0.33 | 2.77e-09 (kerr_delay:300) | 0.166 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | mg10_small | 4 | 0.338 | 0.352 | 0.00471 (kerr_delay:300) | 0.199 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | mg20 | 4 | 0.291 | 0.306 | 9.57e-08 (esn:1000) | 0.0698 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | narma10 | 4 | 0.52 | 0.515 | 0.0134 (kerr_delay:300) | 0.488 (esn:3) | 1e+04 | — | 30 | 5 |  |  |  |  |
| spin_reset_chain_N4_z | narma10_n5 | 4 | 0.526 | 0.522 | 0.0554 (kerr_delay:100) | 0.504 (esn:3) | 1e+05 | — | 30 | 5 |  |  |  |  |
| spin_reset_chain_N4_z | narma10_small | 4 | 0.562 | 0.562 | 0.143 (polynarx:(30, 1)) | 0.683 (esn:3) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_chain_N4_z | narma2 | 4 | 0.196 | 0.197 | 5.73e-06 (esn:1000) | 0.166 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | narma20 | 4 | 0.722 | 0.723 | 0.109 (kerr_delay:300) | 0.773 (esn:3) | 1e+03 | — | 30 | 5 |  | y |  |  |
| spin_reset_chain_N4_z | narma5 | 4 | 0.483 | 0.481 | 0.000111 (esn:1000) | 0.454 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | xor | 4 | 1.01 | 1.01 | 4.38e-25 (polynarx:(20, 2)) | 0.831 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | xor_n1 | 4 | 1.01 | 1.01 | 0.00101 (kerr_delay:100) | 0.843 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | xor_n5 | 4 | 1.01 | 1.01 | 0.023 (kerr_delay:100) | 0.887 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | xprod | 4 | 1.01 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.992 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | xprod_n1 | 4 | 1.01 | 1.01 | 0.00248 (polynarx:(10, 2)) | 0.992 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N4_z | xprod_n5 | 4 | 1.01 | 1.01 | 0.0592 (polynarx:(10, 2)) | 0.993 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | lorenz_multi | 6 | 0.541 | 0.603 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | lorenz_uni | 6 | 0.422 | 0.546 | 0.000172 (esn:300) | 0.17 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | mc30 | 6 | 0.843 | 0.85 | 7.66e-07 (kerr_delay:300) | 0.871 (esn:5) | 1e+04 | — | 30 | 10 |  | y |  |  |
| spin_reset_chain_N6_z | mc30_n5 | 6 | 0.848 | 0.855 | 0.0401 (kerr_delay:100) | 0.875 (esn:5) | 1e+04 | — | 30 | 10 |  | y |  |  |
| spin_reset_chain_N6_z | mg10 | 6 | 0.238 | 0.283 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | mg10_small | 6 | 0.255 | 0.302 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | mg20 | 6 | 0.267 | 0.298 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | narma10 | 6 | 0.44 | 0.442 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_chain_N6_z | narma10_n5 | 6 | 0.449 | 0.451 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_chain_N6_z | narma10_small | 6 | 0.473 | 0.475 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_chain_N6_z | narma2 | 6 | 0.413 | 0.423 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | narma20 | 6 | 0.472 | 0.477 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | 1e+04 | — | 30 | 10 |  |  |  |  |
| spin_reset_chain_N6_z | narma5 | 6 | 0.496 | 0.502 | 0.000111 (kerr_delay:300) | 0.314 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | xor | 6 | 1.01 | 1.01 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | xor_n1 | 6 | 1.01 | 1.01 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | xor_n5 | 6 | 1.01 | 1.01 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | xprod | 6 | 1.01 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | xprod_n1 | 6 | 1.01 | 1.01 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N6_z | xprod_n5 | 6 | 1.01 | 1.01 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | lorenz_multi | 8 | 0.601 | 0.624 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | lorenz_uni | 8 | 0.451 | 0.598 | 0.000172 (esn:300) | 0.17 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | mc30 | 8 | 0.782 | 0.793 | 7.66e-07 (kerr_delay:300) | 0.871 (esn:5) | 1e+03 | — | 30 | 30 |  | y |  |  |
| spin_reset_chain_N8_z | mc30_n5 | 8 | 0.787 | 0.798 | 0.0401 (kerr_delay:100) | 0.875 (esn:5) | 1e+03 | — | 30 | 30 |  | y |  |  |
| spin_reset_chain_N8_z | mg10 | 8 | 0.257 | 0.3 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | mg10_small | 8 | 0.326 | 0.379 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | mg20 | 8 | 0.272 | 0.296 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | narma10 | 8 | 0.428 | 0.432 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_chain_N8_z | narma10_n5 | 8 | 0.424 | 0.432 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_chain_N8_z | narma10_small | 8 | 0.525 | 0.528 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_chain_N8_z | narma2 | 8 | 0.338 | 0.347 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | narma20 | 8 | 0.483 | 0.489 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | 1e+04 | — | 30 | 10 |  |  |  |  |
| spin_reset_chain_N8_z | narma5 | 8 | 0.343 | 0.364 | 0.000111 (esn:1000) | 0.314 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_chain_N8_z | xor | 8 | 1.01 | 1.01 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | xor_n1 | 8 | 1.01 | 1.01 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | xor_n5 | 8 | 1.01 | 1.01 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | xprod | 8 | 1 | 1 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | xprod_n1 | 8 | 1 | 1 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chain_N8_z | xprod_n5 | 8 | 1 | 1 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | lorenz_multi | 6 | 0.91 | 0.873 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | lorenz_uni | 6 | 0.814 | 0.814 | 0.000172 (esn:300) | 0.17 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | mc30 | 6 | 0.958 | 0.981 | 1.5e-07 (kerr_delay:300) | 0.869 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | mc30_n5 | 6 | 0.961 | 0.985 | 0.0389 (kerr_delay:100) | 0.873 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | mg10 | 6 | 0.114 | 0.355 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_chaotic_N6_z | mg10_small | 6 | 0.737 | 0.644 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | mg20 | 6 | 0.115 | 0.22 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | narma10 | 6 | 0.691 | 0.722 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | narma10_n5 | 6 | 0.668 | 0.726 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | narma10_small | 6 | 1.05 | 1.01 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | narma2 | 6 | 0.646 | 0.761 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | narma20 | 6 | 0.564 | 0.689 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_chaotic_N6_z | narma5 | 6 | 0.711 | 0.828 | 0.000111 (kerr_delay:300) | 0.314 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | xor | 6 | 1 | 1.01 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | xor_n1 | 6 | 1 | 1.01 | 0.00101 (esn:1000) | 0.771 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | xor_n5 | 6 | 1 | 1.01 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | xprod | 6 | 1.01 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | xprod_n1 | 6 | 1.01 | 1.01 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_chaotic_N6_z | xprod_n5 | 6 | 1.01 | 1.01 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N10_zz | lorenz_multi | 55 | 0.139 | 0.629 | 4.22e-06 (esn:1000) | 0.0135 (polynarx:(3, 2)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N10_zz | lorenz_uni | 55 | 0.223 | 0.763 | 0.000172 (esn:300) | 0.016 (esn:30) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N10_zz | mc30 | 55 | 0.545 | 0.973 | 1.5e-07 (kerr_delay:300) | 0.0345 (polynarx:(30, 1)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N10_zz | mc30_n5 | 55 | 0.562 | 0.973 | 0.0389 (kerr_delay:100) | 0.0628 (polynarx:(30, 1)) | — | — | 30 | 300 |  |  |  |  |
| spin_reset_rand_N10_zz | mg10 | 55 | 0.00119 | 0.153 | 4.55e-09 (kerr_delay:300) | 0.000915 (esn:30) | — | — | 30 | 65 |  |  |  |  |
| spin_reset_rand_N10_zz | mg10_small | 55 | 0.294 | 0.422 | 0.00471 (kerr_delay:300) | 0.011 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N10_zz | mg20 | 55 | 0.0012 | 0.174 | 9.57e-08 (esn:1000) | 0.000672 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N10_zz | narma10 | 55 | 0.196 | 0.568 | 0.0157 (kerr_delay:300) | 0.144 (polynarx:(30, 1)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N10_zz | narma10_n5 | 55 | 0.177 | 0.43 | 0.0554 (kerr_delay:100) | 0.171 (polynarx:(30, 1)) | — | — | 30 | 300 |  |  |  |  |
| spin_reset_rand_N10_zz | narma10_small | 55 | 0.404 | 1.03 | 0.143 (polynarx:(20, 2)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N10_zz | narma2 | 55 | 0.128 | 0.416 | 5.73e-06 (esn:1000) | 0.00499 (esn:30) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N10_zz | narma20 | 55 | 0.272 | 0.492 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | 1000 |  |  |  |  |
| spin_reset_rand_N10_zz | narma5 | 55 | 0.141 | 0.606 | 0.000111 (esn:1000) | 0.0591 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N10_zz | xor | 55 | 0.416 | 0.736 | 4.38e-25 (polynarx:(20, 2)) | 0.283 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N10_zz | xor_n1 | 55 | 0.414 | 0.737 | 0.00101 (kerr_delay:100) | 0.299 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N10_zz | xor_n5 | 55 | 0.416 | 0.746 | 0.023 (kerr_delay:100) | 0.336 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N10_zz | xprod | 55 | 0.695 | 1.05 | 6.6e-24 (polynarx:(10, 2)) | 0.457 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N10_zz | xprod_n1 | 55 | 0.696 | 1.05 | 0.00248 (polynarx:(10, 2)) | 0.459 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N10_zz | xprod_n5 | 55 | 0.718 | 1.05 | 0.0592 (polynarx:(10, 2)) | 0.499 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N4_z | lorenz_multi | 4 | 0.591 | 0.699 | 4.22e-06 (esn:1000) | 0.345 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | lorenz_uni | 4 | 0.62 | 0.693 | 0.000172 (esn:300) | 0.304 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | mc30 | 4 | 0.915 | 0.925 | 7.66e-07 (kerr_delay:300) | 0.936 (esn:3) | 1e+04 | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N4_z | mc30_n5 | 4 | 0.918 | 0.928 | 0.0401 (kerr_delay:100) | 0.937 (esn:3) | 1e+04 | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N4_z | mg10 | 4 | 0.29 | 0.305 | 2.77e-09 (kerr_delay:300) | 0.166 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | mg10_small | 4 | 0.307 | 0.375 | 0.00471 (kerr_delay:300) | 0.199 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | mg20 | 4 | 0.225 | 0.304 | 9.57e-08 (esn:1000) | 0.0698 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | narma10 | 4 | 0.518 | 0.526 | 0.0134 (kerr_delay:300) | 0.488 (esn:3) | 1e+04 | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N4_z | narma10_n5 | 4 | 0.54 | 0.548 | 0.0554 (kerr_delay:100) | 0.504 (esn:3) | 1e+04 | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N4_z | narma10_small | 4 | 0.523 | 0.537 | 0.143 (polynarx:(30, 1)) | 0.683 (esn:3) | 1e+03 | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N4_z | narma2 | 4 | 0.227 | 0.254 | 5.73e-06 (esn:1000) | 0.166 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | narma20 | 4 | 0.611 | 0.609 | 0.1 (kerr_delay:100) | 0.607 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | narma5 | 4 | 0.396 | 0.441 | 0.000111 (kerr_delay:300) | 0.454 (esn:3) | 1e+03 | — | 30 | 5 |  | y |  |  |
| spin_reset_rand_N4_z | xor | 4 | 0.998 | 1 | 4.38e-25 (polynarx:(20, 2)) | 0.831 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | xor_n1 | 4 | 0.998 | 1 | 0.00101 (esn:1000) | 0.843 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | xor_n5 | 4 | 0.999 | 0.999 | 0.023 (kerr_delay:100) | 0.887 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | xprod | 4 | 1 | 1 | 6.6e-24 (polynarx:(10, 2)) | 0.992 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | xprod_n1 | 4 | 1 | 1 | 0.00248 (polynarx:(10, 2)) | 0.992 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N4_z | xprod_n5 | 4 | 1 | 1 | 0.0592 (polynarx:(10, 2)) | 0.993 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_xyz | lorenz_multi | 18 | 0.319 | 0.545 | 4.22e-06 (esn:1000) | 0.0501 (polynarx:(5, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_xyz | lorenz_uni | 18 | 0.297 | 0.696 | 0.000172 (esn:300) | 0.084 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_xyz | mc30 | 18 | 0.76 | 0.899 | 1.5e-07 (kerr_delay:300) | 0.713 (polynarx:(10, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_xyz | mc30_n5 | 18 | 0.779 | 0.904 | 0.0389 (kerr_delay:100) | 0.719 (polynarx:(10, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_xyz | mg10 | 18 | 0.0355 | 0.261 | 2.77e-09 (kerr_delay:300) | 0.0186 (esn:10) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_xyz | mg10_small | 18 | 0.119 | 0.294 | 0.00471 (kerr_delay:300) | 0.0755 (esn:10) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_xyz | mg20 | 18 | 0.0158 | 0.0775 | 9.57e-08 (esn:1000) | 0.0121 (esn:10) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_xyz | narma10 | 18 | 0.397 | 0.44 | 0.0134 (kerr_delay:300) | 0.282 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_xyz | narma10_n5 | 18 | 0.425 | 0.457 | 0.0554 (kerr_delay:100) | 0.288 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_xyz | narma10_small | 18 | 0.488 | 0.564 | 0.143 (polynarx:(30, 1)) | 0.385 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_xyz | narma2 | 18 | 0.28 | 0.408 | 5.73e-06 (esn:1000) | 0.027 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_xyz | narma20 | 18 | 0.515 | 0.544 | 0.1 (kerr_delay:300) | 0.383 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_xyz | narma5 | 18 | 0.274 | 0.446 | 0.000111 (esn:1000) | 0.138 (polynarx:(10, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_xyz | xor | 18 | 1 | 1.01 | 4.38e-25 (polynarx:(20, 2)) | 0.626 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_xyz | xor_n1 | 18 | 1.01 | 1.01 | 0.00101 (kerr_delay:100) | 0.64 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_xyz | xor_n5 | 18 | 1.01 | 1.01 | 0.023 (kerr_delay:100) | 0.699 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_xyz | xprod | 18 | 0.984 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.764 (polynarx:(3, 2)) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_xyz | xprod_n1 | 18 | 0.984 | 1.01 | 0.00248 (polynarx:(10, 2)) | 0.765 (polynarx:(3, 2)) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_xyz | xprod_n5 | 18 | 0.991 | 1.01 | 0.0592 (polynarx:(10, 2)) | 0.777 (polynarx:(3, 2)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z | lorenz_multi | 6 | 0.627 | 0.682 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z | lorenz_uni | 6 | 0.515 | 0.751 | 0.000172 (esn:1000) | 0.17 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z | mc30 | 6 | 0.858 | 0.913 | 7.66e-07 (kerr_delay:300) | 0.871 (polynarx:(5, 1)) | 6e+05 | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z | mc30_n5 | 6 | 0.861 | 0.914 | 0.0401 (kerr_delay:100) | 0.875 (esn:5) | 6e+05 | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z | mg10 | 6 | 0.104 | 0.287 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z | mg10_small | 6 | 0.114 | 0.313 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z | mg20 | 6 | 0.148 | 0.278 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z | narma10 | 6 | 0.45 | 0.441 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z | narma10_n5 | 6 | 0.47 | 0.458 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z | narma10_small | 6 | 0.489 | 0.541 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z | narma2 | 6 | 0.306 | 0.417 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z | narma20 | 6 | 0.524 | 0.543 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z | narma5 | 6 | 0.341 | 0.469 | 0.000111 (esn:1000) | 0.314 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z | xor | 6 | 1 | 1 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z | xor_n1 | 6 | 1 | 1 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z | xor_n5 | 6 | 1 | 1 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z | xprod | 6 | 1 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z | xprod_n1 | 6 | 1 | 1 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z | xprod_n5 | 6 | 1.01 | 1 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | lorenz_multi | 6 | 0.393 | 0.595 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | lorenz_uni | 6 | 0.457 | 0.678 | 0.000172 (esn:300) | 0.17 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | mc30 | 6 | 0.892 | 0.935 | 1.5e-07 (kerr_delay:300) | 0.869 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | mc30_n5 | 6 | 0.898 | 0.937 | 0.0389 (kerr_delay:100) | 0.873 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | mg10 | 6 | 0.153 | 0.374 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | mg10_small | 6 | 0.205 | 0.42 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | mg20 | 6 | 0.0428 | 0.147 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | ∞ | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | narma10 | 6 | 0.611 | 0.644 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | narma10_n5 | 6 | 0.616 | 0.663 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | narma10_small | 6 | 0.666 | 0.682 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | narma2 | 6 | 0.0891 | 0.116 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | narma20 | 6 | 0.667 | 0.672 | 0.1 (kerr_delay:100) | 0.483 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | narma5 | 6 | 0.352 | 0.427 | 0.000111 (kerr_delay:300) | 0.314 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | xor | 6 | 0.873 | 0.956 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | xor_n1 | 6 | 0.874 | 0.957 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | xor_n5 | 6 | 0.879 | 0.961 | 0.023 (esn:1000) | 0.776 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | xprod | 6 | 0.984 | 1 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | xprod_n1 | 6 | 0.985 | 1 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_T1 | xprod_n5 | 6 | 0.988 | 1 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | lorenz_multi | 60 | 0.155 | 0.649 | 4.22e-06 (esn:300) | 0.0135 (esn:30) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | lorenz_uni | 60 | 0.163 | 0.543 | 0.000172 (esn:1000) | 0.016 (polynarx:(5, 3)) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | mc30 | 60 | 0.568 | 0.844 | 1.5e-07 (kerr_delay:300) | 0.0345 (polynarx:(30, 1)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | mc30_n5 | 60 | 0.585 | 0.848 | 0.0389 (kerr_delay:100) | 0.0628 (polynarx:(30, 1)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | mg10 | 60 | 0.00518 | 0.197 | 2.77e-09 (kerr_delay:300) | 0.000807 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | mg10_small | 60 | 0.0249 | 0.33 | 0.00471 (esn:1000) | 0.011 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | mg20 | 60 | 0.0025 | 0.196 | 9.57e-08 (esn:1000) | 0.000672 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | narma10 | 60 | 0.173 | 0.413 | 0.0134 (kerr_delay:300) | 0.147 (polynarx:(30, 1)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | narma10_n5 | 60 | 0.185 | 0.408 | 0.0554 (kerr_delay:100) | 0.171 (polynarx:(30, 1)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | narma10_small | 60 | 0.375 | 0.656 | 0.143 (polynarx:(20, 2)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | narma2 | 60 | 0.141 | 0.234 | 5.73e-06 (esn:1000) | 0.00499 (esn:30) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | narma20 | 60 | 0.45 | 0.502 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | narma5 | 60 | 0.139 | 0.351 | 0.000111 (kerr_delay:300) | 0.0591 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | xor | 60 | 0.413 | 1 | 4.38e-25 (polynarx:(20, 2)) | 0.283 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | xor_n1 | 60 | 0.412 | 1 | 0.00101 (esn:1000) | 0.299 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | xor_n5 | 60 | 0.418 | 1 | 0.023 (kerr_delay:100) | 0.336 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | xprod | 60 | 0.769 | 1.02 | 6.6e-24 (polynarx:(10, 2)) | 0.457 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | xprod_n1 | 60 | 0.771 | 1.02 | 0.00248 (polynarx:(10, 2)) | 0.459 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V10 | xprod_n5 | 60 | 0.79 | 1.02 | 0.0592 (polynarx:(10, 2)) | 0.499 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | lorenz_multi | 30 | 0.208 | 0.678 | 4.22e-06 (esn:1000) | 0.016 (esn:30) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | lorenz_uni | 30 | 0.156 | 0.586 | 0.000172 (esn:300) | 0.016 (esn:30) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | mc30 | 30 | 0.639 | 0.861 | 1.5e-07 (kerr_delay:300) | 0.0345 (polynarx:(30, 1)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | mc30_n5 | 30 | 0.649 | 0.865 | 0.0389 (kerr_delay:100) | 0.0628 (polynarx:(30, 1)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | mg10 | 30 | 0.00673 | 0.232 | 2.77e-09 (kerr_delay:300) | 0.000807 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | mg10_small | 30 | 0.023 | 0.331 | 0.00471 (kerr_delay:300) | 0.011 (esn:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | mg20 | 30 | 0.0045 | 0.219 | 9.57e-08 (esn:1000) | 0.000672 (esn:30) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | narma10 | 30 | 0.203 | 0.418 | 0.0134 (kerr_delay:300) | 0.147 (polynarx:(30, 1)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | narma10_n5 | 30 | 0.221 | 0.425 | 0.0554 (kerr_delay:100) | 0.171 (polynarx:(30, 1)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | narma10_small | 30 | 0.376 | 0.742 | 0.143 (polynarx:(20, 2)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | narma2 | 30 | 0.162 | 0.238 | 5.73e-06 (esn:1000) | 0.00499 (esn:30) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | narma20 | 30 | 0.439 | 0.511 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | narma5 | 30 | 0.157 | 0.375 | 0.000111 (kerr_delay:300) | 0.0591 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | xor | 30 | 0.574 | 0.967 | 4.38e-25 (polynarx:(20, 2)) | 0.283 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | xor_n1 | 30 | 0.573 | 0.969 | 0.00101 (kerr_delay:100) | 0.299 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | xor_n5 | 30 | 0.578 | 0.976 | 0.023 (kerr_delay:100) | 0.336 (kerr_delay:10) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | xprod | 30 | 0.86 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.457 (kerr_delay:10) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | xprod_n1 | 30 | 0.86 | 1.01 | 0.00248 (polynarx:(10, 2)) | 0.459 (kerr_delay:10) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_V5 | xprod_n5 | 30 | 0.869 | 1.01 | 0.0592 (polynarx:(10, 2)) | 0.499 (kerr_delay:10) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_edge | lorenz_multi | 6 | 0.627 | 0.682 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_edge | lorenz_uni | 6 | 0.515 | 0.751 | 0.000172 (esn:1000) | 0.17 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_edge | mc30 | 6 | 0.858 | 0.913 | 7.66e-07 (kerr_delay:300) | 0.871 (polynarx:(5, 1)) | 6e+05 | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_edge | mc30_n5 | 6 | 0.861 | 0.914 | 0.0401 (kerr_delay:100) | 0.875 (esn:5) | 6e+05 | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_edge | mg10 | 6 | 0.104 | 0.287 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_edge | mg10_small | 6 | 0.114 | 0.313 | 0.00471 (esn:1000) | 0.116 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_edge | mg20 | 6 | 0.148 | 0.278 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_edge | narma10 | 6 | 0.45 | 0.441 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_edge | narma10_n5 | 6 | 0.47 | 0.458 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_edge | narma10_small | 6 | 0.489 | 0.541 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_edge | narma2 | 6 | 0.306 | 0.417 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_edge | narma20 | 6 | 0.524 | 0.543 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_edge | narma5 | 6 | 0.341 | 0.469 | 0.000111 (kerr_delay:300) | 0.314 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_edge | xor | 6 | 1 | 1 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_edge | xor_n1 | 6 | 1 | 1 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_edge | xor_n5 | 6 | 1 | 1 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_edge | xprod | 6 | 1 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_edge | xprod_n1 | 6 | 1 | 1 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_edge | xprod_n5 | 6 | 1.01 | 1 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | lorenz_multi | 6 | 0.911 | 0.922 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | lorenz_uni | 6 | 0.788 | 0.789 | 0.000172 (esn:1000) | 0.17 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | mc30 | 6 | 1.02 | 1.02 | 1.5e-07 (kerr_delay:300) | 0.869 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | mc30_n5 | 6 | 1.02 | 1.02 | 0.0389 (kerr_delay:100) | 0.873 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | mg10 | 6 | 0.951 | 0.951 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | mg10_small | 6 | 4.57 | 4.82 | 0.00471 (esn:1000) | 0.116 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | mg20 | 6 | 0.509 | 0.507 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | narma10 | 6 | 1.13 | 1.12 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | narma10_n5 | 6 | 1.11 | 1.11 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | narma10_small | 6 | 1.36 | 1.26 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | narma2 | 6 | 1.1 | 1.09 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | narma20 | 6 | 1.33 | 1.3 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | narma5 | 6 | 1.04 | 1.05 | 0.000111 (kerr_delay:300) | 0.314 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | xor | 6 | 1.01 | 1.01 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | xor_n1 | 6 | 1.01 | 1.01 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | xor_n5 | 6 | 1.01 | 1 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | xprod | 6 | 1.01 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | xprod_n1 | 6 | 1.01 | 1.01 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_frozen | xprod_n5 | 6 | 1.01 | 1.01 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm | lorenz_multi | 6 | 0.537 | 0.671 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm | lorenz_uni | 6 | 0.533 | 0.727 | 0.000172 (esn:300) | 0.17 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm | mc30 | 6 | 0.872 | 0.948 | 1.5e-07 (kerr_delay:300) | 0.869 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm | mc30_n5 | 6 | 0.876 | 0.95 | 0.0389 (kerr_delay:100) | 0.873 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm | mg10 | 6 | 0.0796 | 0.262 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm | mg10_small | 6 | 0.148 | 0.303 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | ∞ | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_pm | mg20 | 6 | 0.0559 | 0.256 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm | narma10 | 6 | 0.457 | 0.486 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm | narma10_n5 | 6 | 0.479 | 0.513 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm | narma10_small | 6 | 0.551 | 0.573 | 0.143 (polynarx:(20, 2)) | 0.509 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm | narma2 | 6 | 0.193 | 0.357 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm | narma20 | 6 | 0.594 | 0.601 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm | narma5 | 6 | 0.366 | 0.455 | 0.000111 (kerr_delay:300) | 0.314 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm | xor | 6 | 0.975 | 0.992 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm | xor_n1 | 6 | 0.975 | 0.993 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm | xor_n5 | 6 | 0.976 | 0.994 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm | xprod | 6 | 0.995 | 1 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm | xprod_n1 | 6 | 0.995 | 1 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm | xprod_n5 | 6 | 0.997 | 1 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | lorenz_multi | 6 | 0.561 | 0.7 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | lorenz_uni | 6 | 0.625 | 0.753 | 0.000172 (esn:1000) | 0.17 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | mc30 | 6 | 0.868 | 0.953 | 7.66e-07 (kerr_delay:300) | 0.871 (esn:5) | ∞ | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | mc30_n5 | 6 | 0.873 | 0.953 | 0.0401 (kerr_delay:100) | 0.875 (polynarx:(5, 1)) | ∞ | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | mg10 | 6 | 0.0652 | 0.288 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | mg10_small | 6 | 0.195 | 0.331 | 0.00471 (kerr_delay:100) | 0.116 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | mg20 | 6 | 0.1 | 0.29 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | narma10 | 6 | 0.428 | 0.444 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | narma10_n5 | 6 | 0.445 | 0.463 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | narma10_small | 6 | 0.54 | 0.567 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | narma2 | 6 | 0.227 | 0.427 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | narma20 | 6 | 0.541 | 0.557 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | narma5 | 6 | 0.341 | 0.504 | 0.000111 (esn:1000) | 0.314 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | xor | 6 | 0.957 | 0.999 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | xor_n1 | 6 | 0.958 | 0.999 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | xor_n5 | 6 | 0.961 | 1 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | xprod | 6 | 1 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | xprod_n1 | 6 | 1 | 1.01 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_pm_slow | xprod_n5 | 6 | 1 | 1.01 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | lorenz_multi | 6 | 0.507 | 0.745 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | lorenz_uni | 6 | 0.585 | 0.732 | 0.000172 (esn:300) | 0.17 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | mc30 | 6 | 0.908 | 0.922 | 1.5e-07 (kerr_delay:300) | 0.869 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | mc30_n5 | 6 | 0.909 | 0.922 | 0.0389 (kerr_delay:100) | 0.873 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | mg10 | 6 | 0.247 | 0.337 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | mg10_small | 6 | 0.358 | 0.741 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | mg20 | 6 | 0.119 | 0.158 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | narma10 | 6 | 0.517 | 0.543 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | narma10_n5 | 6 | 0.519 | 0.545 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | narma10_small | 6 | 0.58 | 0.659 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | narma2 | 6 | 0.217 | 0.26 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | narma20 | 6 | 0.635 | 0.653 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | narma5 | 6 | 0.401 | 0.44 | 0.000111 (kerr_delay:300) | 0.314 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | xor | 6 | 0.847 | 0.858 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | xor_n1 | 6 | 0.847 | 0.858 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | xor_n5 | 6 | 0.849 | 0.86 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | xprod | 6 | 0.96 | 0.984 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | xprod_n1 | 6 | 0.96 | 0.984 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_scrambled | xprod_n5 | 6 | 0.964 | 0.986 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | lorenz_multi | 6 | 0.618 | 0.711 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | lorenz_uni | 6 | 0.5 | 0.753 | 0.000172 (esn:1000) | 0.17 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | mc30 | 6 | 0.849 | 0.948 | 1.5e-07 (kerr_delay:300) | 0.869 (esn:5) | ∞ | — | 1 | 10 |  | y |  |  |
| spin_reset_rand_N6_z_weak0.1 | mc30_n5 | 6 | 0.855 | 0.949 | 0.0389 (kerr_delay:100) | 0.873 (esn:5) | ∞ | — | 1 | 10 |  | y |  |  |
| spin_reset_rand_N6_z_weak0.1 | mg10 | 6 | 0.103 | 0.321 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | mg10_small | 6 | 0.115 | 0.34 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | mg20 | 6 | 0.141 | 0.313 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | narma10 | 6 | 0.45 | 0.477 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | narma10_n5 | 6 | 0.471 | 0.493 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | narma10_small | 6 | 0.49 | 0.591 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | narma2 | 6 | 0.294 | 0.536 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | narma20 | 6 | 0.527 | 0.616 | 0.1 (kerr_delay:100) | 0.483 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | narma5 | 6 | 0.333 | 0.555 | 0.000111 (kerr_delay:300) | 0.314 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | xor | 6 | 1 | 1.01 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | xor_n1 | 6 | 1 | 1.01 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | xor_n5 | 6 | 1 | 1.01 | 0.023 (esn:1000) | 0.776 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | xprod | 6 | 1 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | xprod_n1 | 6 | 1 | 1.01 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.1 | xprod_n5 | 6 | 1 | 1.01 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | lorenz_multi | 6 | 0.57 | 0.702 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | lorenz_uni | 6 | 0.451 | 0.722 | 0.000172 (esn:300) | 0.17 (polynarx:(5, 1)) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | mc30 | 6 | 0.85 | 0.916 | 1.5e-07 (kerr_delay:300) | 0.869 (esn:5) | ∞ | — | 1 | 10 |  | y |  |  |
| spin_reset_rand_N6_z_weak0.3 | mc30_n5 | 6 | 0.855 | 0.919 | 0.0389 (kerr_delay:100) | 0.873 (esn:5) | ∞ | — | 1 | 10 |  | y |  |  |
| spin_reset_rand_N6_z_weak0.3 | mg10 | 6 | 0.101 | 0.308 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | mg10_small | 6 | 0.105 | 0.311 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | mg20 | 6 | 0.101 | 0.297 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | narma10 | 6 | 0.452 | 0.459 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | narma10_n5 | 6 | 0.46 | 0.485 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | narma10_small | 6 | 0.494 | 0.526 | 0.143 (polynarx:(20, 2)) | 0.509 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | narma2 | 6 | 0.21 | 0.371 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | narma20 | 6 | 0.54 | 0.576 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | narma5 | 6 | 0.299 | 0.465 | 0.000111 (esn:1000) | 0.314 (esn:5) | ∞ | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | xor | 6 | 1 | 1 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | xor_n1 | 6 | 1 | 1 | 0.00101 (esn:1000) | 0.771 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | xor_n5 | 6 | 1 | 1 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | xprod | 6 | 1 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | xprod_n1 | 6 | 1 | 1.01 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.3 | xprod_n5 | 6 | 1 | 1.01 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | lorenz_multi | 6 | 0.509 | 0.688 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | lorenz_uni | 6 | 0.373 | 0.708 | 0.000172 (esn:1000) | 0.17 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | mc30 | 6 | 0.853 | 0.908 | 1.5e-07 (kerr_delay:300) | 0.869 (esn:5) | ∞ | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | mc30_n5 | 6 | 0.856 | 0.911 | 0.0389 (kerr_delay:100) | 0.873 (esn:5) | ∞ | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | mg10 | 6 | 0.135 | 0.304 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | mg10_small | 6 | 0.237 | 0.327 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | mg20 | 6 | 0.072 | 0.269 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | narma10 | 6 | 0.394 | 0.458 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | narma10_n5 | 6 | 0.403 | 0.461 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | narma10_small | 6 | 0.508 | 0.532 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | ∞ | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | narma2 | 6 | 0.161 | 0.202 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | narma20 | 6 | 0.577 | 0.59 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | narma5 | 6 | 0.282 | 0.43 | 0.000111 (esn:1000) | 0.314 (esn:5) | ∞ | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | xor | 6 | 0.966 | 1 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | xor_n1 | 6 | 0.966 | 1 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | xor_n5 | 6 | 0.968 | 1 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | xprod | 6 | 0.982 | 1 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | xprod_n1 | 6 | 0.983 | 1 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_z_weak0.6 | xprod_n5 | 6 | 0.985 | 1 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz | lorenz_multi | 21 | 0.288 | 0.619 | 4.22e-06 (esn:1000) | 0.0501 (polynarx:(5, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz | lorenz_uni | 21 | 0.205 | 0.728 | 0.000172 (esn:300) | 0.084 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz | mc30 | 21 | 0.716 | 0.9 | 1.5e-07 (kerr_delay:300) | 0.713 (polynarx:(10, 1)) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz | mc30_n5 | 21 | 0.724 | 0.902 | 0.0389 (kerr_delay:100) | 0.719 (polynarx:(10, 1)) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz | mg10 | 21 | 0.0127 | 0.0893 | 2.77e-09 (kerr_delay:300) | 0.0186 (esn:10) | ∞ | — | 30 | 30 |  | y |  |  |
| spin_reset_rand_N6_zz | mg10_small | 21 | 0.0323 | 0.115 | 0.00471 (kerr_delay:300) | 0.0755 (esn:10) | 1e+06 | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz | mg20 | 21 | 0.00717 | 0.116 | 9.57e-08 (esn:1000) | 0.0121 (esn:10) | ∞ | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz | narma10 | 21 | 0.332 | 0.435 | 0.0134 (kerr_delay:300) | 0.282 (esn:10) | 1e+06 | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz | narma10_n5 | 21 | 0.346 | 0.453 | 0.0554 (kerr_delay:100) | 0.288 (esn:5) | 1e+05 | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_zz | narma10_small | 21 | 0.479 | 0.755 | 0.143 (polynarx:(30, 1)) | 0.385 (esn:10) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz | narma2 | 21 | 0.216 | 0.412 | 5.73e-06 (esn:1000) | 0.027 (esn:10) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N6_zz | narma20 | 21 | 0.407 | 0.525 | 0.1 (kerr_delay:100) | 0.383 (esn:5) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz | narma5 | 21 | 0.247 | 0.442 | 0.000111 (esn:1000) | 0.138 (polynarx:(10, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz | xor | 21 | 0.534 | 0.641 | 4.38e-25 (polynarx:(20, 2)) | 0.508 (polynarx:(5, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz | xor_n1 | 21 | 0.534 | 0.643 | 0.00101 (kerr_delay:100) | 0.507 (polynarx:(5, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz | xor_n5 | 21 | 0.538 | 0.655 | 0.023 (esn:1000) | 0.516 (polynarx:(5, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz | xprod | 21 | 0.914 | 0.993 | 6.6e-24 (polynarx:(10, 2)) | 0.518 (polynarx:(5, 2)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz | xprod_n1 | 21 | 0.915 | 0.993 | 0.00248 (polynarx:(10, 2)) | 0.519 (polynarx:(5, 2)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz | xprod_n5 | 21 | 0.922 | 0.993 | 0.0592 (polynarx:(10, 2)) | 0.546 (polynarx:(5, 2)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | lorenz_multi | 210 | 0.173 | 0.621 | 4.22e-06 (esn:1000) | 0.000251 (esn:100) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | lorenz_uni | 210 | 0.175 | 0.621 | 0.000172 (esn:300) | 0.000664 (esn:100) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | mc30 | 210 | 0.344 | 0.883 | 1.5e-07 (kerr_delay:300) | 0.0345 (polynarx:(30, 1)) | — | — | 30 | >1000 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | mc30_n5 | 210 | 0.379 | 0.888 | 0.0389 (kerr_delay:100) | 0.0613 (polynarx:(30, 1)) | — | — | 30 | 1000 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | mg10 | 210 | 6.29e-05 | 0.0713 | 2.77e-09 (kerr_delay:300) | 4.15e-06 (esn:100) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | mg10_small | 210 | 0.0164 | 0.152 | 0.00471 (kerr_delay:300) | 0.00857 (esn:100) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | mg20 | 210 | 0.000116 | 0.0621 | 9.57e-08 (esn:1000) | 2.26e-05 (esn:100) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | narma10 | 210 | 0.143 | 0.376 | 0.0134 (kerr_delay:300) | 0.0924 (kerr_delay:30) | — | — | 30 | 300 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | narma10_n5 | 210 | 0.155 | 0.385 | 0.0554 (kerr_delay:300) | 0.112 (kerr_delay:30) | — | — | 30 | 300 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | narma10_small | 210 | 0.469 | 1.29 | 0.143 (polynarx:(30, 1)) | 0.278 (polynarx:(30, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | narma2 | 210 | 0.0987 | 0.267 | 5.73e-06 (esn:1000) | 0.000151 (esn:100) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | narma20 | 210 | 0.264 | 0.457 | 0.1 (kerr_delay:300) | 0.187 (polynarx:(30, 1)) | — | — | 30 | 1000 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | narma5 | 210 | 0.0734 | 0.328 | 0.000111 (esn:1000) | 0.00292 (esn:100) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | xor | 210 | 0.0807 | 0.506 | 4.38e-25 (polynarx:(20, 2)) | 0.0343 (kerr_delay:30) | — | — | 30 | 300 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | xor_n1 | 210 | 0.082 | 0.507 | 0.00101 (kerr_delay:100) | 0.0502 (kerr_delay:30) | — | — | 30 | 1000 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | xor_n5 | 210 | 0.0968 | 0.515 | 0.023 (kerr_delay:100) | 0.0887 (kerr_delay:30) | ∞ | — | 30 | 1000 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | xprod | 210 | 0.378 | 1.05 | 6.6e-24 (polynarx:(10, 2)) | 6.6e-24 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | xprod_n1 | 210 | 0.381 | 1.05 | 0.00248 (polynarx:(10, 2)) | 0.00248 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_zz_V10 | xprod_n5 | 210 | 0.44 | 1.05 | 0.0592 (polynarx:(10, 2)) | 0.0592 (polynarx:(10, 2)) | — | — | 30 | 100 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | lorenz_multi | 21 | 0.211 | 0.585 | 4.22e-06 (esn:1000) | 0.0501 (polynarx:(5, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | lorenz_uni | 21 | 0.167 | 0.706 | 0.000172 (esn:300) | 0.084 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | mc30 | 21 | 0.765 | 0.938 | 1.5e-07 (kerr_delay:300) | 0.713 (polynarx:(10, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | mc30_n5 | 21 | 0.777 | 0.94 | 0.0389 (kerr_delay:100) | 0.719 (polynarx:(10, 1)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | mg10 | 21 | 0.00624 | 0.116 | 2.77e-09 (kerr_delay:300) | 0.0186 (esn:10) | ∞ | — | 30 | 30 |  | y |  |  |
| spin_reset_rand_N6_zz_pm | mg10_small | 21 | 0.0241 | 0.15 | 0.00471 (kerr_delay:300) | 0.0755 (esn:10) | ∞ | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | mg20 | 21 | 0.00636 | 0.101 | 9.57e-08 (esn:1000) | 0.0121 (esn:10) | ∞ | — | 30 | 30 |  | y |  |  |
| spin_reset_rand_N6_zz_pm | narma10 | 21 | 0.319 | 0.49 | 0.0134 (kerr_delay:300) | 0.282 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | narma10_n5 | 21 | 0.336 | 0.51 | 0.0554 (kerr_delay:100) | 0.288 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | narma10_small | 21 | 0.565 | 0.797 | 0.143 (polynarx:(30, 1)) | 0.385 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | narma2 | 21 | 0.0864 | 0.259 | 5.73e-06 (esn:1000) | 0.027 (polynarx:(5, 2)) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | narma20 | 21 | 0.548 | 0.595 | 0.1 (kerr_delay:300) | 0.383 (esn:10) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | narma5 | 21 | 0.185 | 0.421 | 0.000111 (kerr_delay:300) | 0.138 (polynarx:(10, 1)) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | xor | 21 | 0.546 | 0.805 | 4.38e-25 (polynarx:(20, 2)) | 0.508 (polynarx:(5, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | xor_n1 | 21 | 0.543 | 0.806 | 0.00101 (kerr_delay:100) | 0.507 (polynarx:(5, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | xor_n5 | 21 | 0.539 | 0.814 | 0.023 (kerr_delay:100) | 0.516 (polynarx:(5, 2)) | — | — | 30 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | xprod | 21 | 0.81 | 0.983 | 6.6e-24 (polynarx:(10, 2)) | 0.518 (polynarx:(5, 2)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | xprod_n1 | 21 | 0.811 | 0.983 | 0.00248 (polynarx:(10, 2)) | 0.519 (polynarx:(5, 2)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_pm | xprod_n5 | 21 | 0.833 | 0.985 | 0.0592 (polynarx:(10, 2)) | 0.546 (polynarx:(5, 2)) | — | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | lorenz_multi | 21 | 0.26 | 0.652 | 4.22e-06 (esn:1000) | 0.0501 (polynarx:(5, 1)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | lorenz_uni | 21 | 0.189 | 0.771 | 0.000172 (esn:300) | 0.084 (esn:10) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | mc30 | 21 | 0.719 | 0.962 | 1.5e-07 (kerr_delay:300) | 0.713 (polynarx:(10, 1)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | mc30_n5 | 21 | 0.727 | 0.964 | 0.0389 (kerr_delay:100) | 0.719 (polynarx:(10, 1)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | mg10 | 21 | 0.0121 | 0.157 | 2.77e-09 (kerr_delay:300) | 0.0186 (esn:10) | ∞ | — | 1 | 30 |  | y |  |  |
| spin_reset_rand_N6_zz_weak0.1 | mg10_small | 21 | 0.0271 | 0.195 | 0.00471 (kerr_delay:300) | 0.0755 (esn:10) | ∞ | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | mg20 | 21 | 0.00658 | 0.14 | 9.57e-08 (esn:1000) | 0.0121 (esn:10) | ∞ | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | narma10 | 21 | 0.325 | 0.49 | 0.0134 (kerr_delay:300) | 0.282 (esn:10) | ∞ | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | narma10_n5 | 21 | 0.338 | 0.506 | 0.0554 (kerr_delay:100) | 0.288 (esn:5) | ∞ | — | 1 | 100 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | narma10_small | 21 | 0.473 | 0.854 | 0.143 (polynarx:(30, 1)) | 0.385 (esn:10) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | narma2 | 21 | 0.209 | 0.534 | 5.73e-06 (esn:1000) | 0.027 (polynarx:(5, 2)) | — | — | 1 | 3 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | narma20 | 21 | 0.416 | 0.594 | 0.1 (kerr_delay:300) | 0.383 (esn:10) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | narma5 | 21 | 0.243 | 0.55 | 0.000111 (kerr_delay:300) | 0.138 (polynarx:(10, 1)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | xor | 21 | 0.529 | 0.821 | 4.38e-25 (polynarx:(20, 2)) | 0.508 (polynarx:(5, 2)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | xor_n1 | 21 | 0.529 | 0.824 | 0.00101 (kerr_delay:100) | 0.507 (polynarx:(5, 2)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | xor_n5 | 21 | 0.533 | 0.834 | 0.023 (kerr_delay:100) | 0.516 (polynarx:(5, 2)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | xprod | 21 | 0.908 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.518 (polynarx:(5, 2)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | xprod_n1 | 21 | 0.909 | 1.01 | 0.00248 (polynarx:(10, 2)) | 0.519 (polynarx:(5, 2)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.1 | xprod_n5 | 21 | 0.917 | 1.01 | 0.0592 (polynarx:(10, 2)) | 0.546 (polynarx:(5, 2)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | lorenz_multi | 21 | 0.243 | 0.602 | 4.22e-06 (esn:1000) | 0.0501 (polynarx:(5, 1)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | lorenz_uni | 21 | 0.16 | 0.74 | 0.000172 (esn:300) | 0.084 (esn:10) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | mc30 | 21 | 0.75 | 0.923 | 1.5e-07 (kerr_delay:300) | 0.713 (polynarx:(10, 1)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | mc30_n5 | 21 | 0.758 | 0.926 | 0.0389 (kerr_delay:100) | 0.719 (polynarx:(10, 1)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | mg10 | 21 | 0.00963 | 0.0993 | 4.55e-09 (kerr_delay:300) | 0.0247 (esn:10) | ∞ | — | 1 | 30 |  | y |  |  |
| spin_reset_rand_N6_zz_weak0.3 | mg10_small | 21 | 0.0125 | 0.122 | 0.00133 (esn:1000) | 0.0521 (esn:10) | ∞ | — | 1 | 65 |  | y |  |  |
| spin_reset_rand_N6_zz_weak0.3 | mg20 | 21 | 0.00557 | 0.112 | 1e-07 (esn:1000) | 0.0118 (esn:10) | ∞ | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | narma10 | 21 | 0.294 | 0.47 | 0.0134 (kerr_delay:300) | 0.282 (esn:10) | ∞ | — | 1 | 100 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | narma10_n5 | 21 | 0.308 | 0.488 | 0.0554 (kerr_delay:100) | 0.288 (esn:5) | ∞ | — | 1 | 100 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | narma10_small | 21 | 0.451 | 0.701 | 0.143 (polynarx:(30, 1)) | 0.385 (esn:10) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | narma2 | 21 | 0.163 | 0.366 | 5.73e-06 (esn:1000) | 0.027 (polynarx:(5, 2)) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | narma20 | 21 | 0.449 | 0.564 | 0.1 (kerr_delay:300) | 0.383 (esn:10) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | narma5 | 21 | 0.218 | 0.443 | 0.000111 (kerr_delay:300) | 0.138 (polynarx:(10, 1)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | xor | 21 | 0.512 | 0.671 | 4.38e-25 (polynarx:(20, 2)) | 0.508 (polynarx:(5, 2)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | xor_n1 | 21 | 0.513 | 0.673 | 0.00101 (kerr_delay:100) | 0.507 (polynarx:(5, 2)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | xor_n5 | 21 | 0.517 | 0.679 | 0.0241 (kerr_delay:100) | 0.52 (polynarx:(5, 2)) | ∞ | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | xprod | 21 | 0.865 | 0.996 | 6.6e-24 (polynarx:(10, 2)) | 0.518 (polynarx:(5, 2)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | xprod_n1 | 21 | 0.866 | 0.996 | 0.00248 (polynarx:(10, 2)) | 0.519 (polynarx:(5, 2)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.3 | xprod_n5 | 21 | 0.874 | 0.997 | 0.0592 (polynarx:(10, 2)) | 0.546 (polynarx:(5, 2)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | lorenz_multi | 21 | 0.121 | 0.591 | 4.22e-06 (esn:1000) | 0.0501 (polynarx:(5, 1)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | lorenz_uni | 21 | 0.16 | 0.718 | 0.000172 (esn:300) | 0.084 (esn:10) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | mc30 | 21 | 0.798 | 0.922 | 1.5e-07 (kerr_delay:300) | 0.713 (polynarx:(10, 1)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | mc30_n5 | 21 | 0.804 | 0.924 | 0.0389 (kerr_delay:100) | 0.719 (polynarx:(10, 1)) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | mg10 | 21 | 0.01 | 0.0888 | 4.55e-09 (kerr_delay:300) | 0.0247 (esn:10) | ∞ | — | 1 | 30 |  | y |  |  |
| spin_reset_rand_N6_zz_weak0.6 | mg10_small | 21 | 0.0189 | 0.113 | 0.00133 (kerr_delay:300) | 0.0521 (esn:10) | ∞ | — | 1 | 65 |  | y |  |  |
| spin_reset_rand_N6_zz_weak0.6 | mg20 | 21 | 0.00477 | 0.0745 | 9.57e-08 (esn:1000) | 0.0121 (esn:10) | ∞ | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | narma10 | 21 | 0.315 | 0.468 | 0.0134 (kerr_delay:300) | 0.282 (esn:10) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | narma10_n5 | 21 | 0.327 | 0.473 | 0.0554 (kerr_delay:100) | 0.288 (esn:10) | — | — | 1 | 10 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | narma10_small | 21 | 0.533 | 0.688 | 0.143 (polynarx:(30, 1)) | 0.385 (esn:10) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | narma2 | 21 | 0.12 | 0.21 | 5.73e-06 (esn:1000) | 0.027 (esn:10) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | narma20 | 21 | 0.574 | 0.586 | 0.1 (kerr_delay:300) | 0.383 (esn:10) | — | — | 1 | 5 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | narma5 | 21 | 0.22 | 0.396 | 0.000111 (kerr_delay:300) | 0.138 (polynarx:(10, 1)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | xor | 21 | 0.485 | 0.641 | 4.38e-25 (polynarx:(20, 2)) | 0.508 (polynarx:(5, 2)) | ∞ | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | xor_n1 | 21 | 0.485 | 0.643 | 0.00101 (esn:1000) | 0.507 (polynarx:(5, 2)) | ∞ | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | xor_n5 | 21 | 0.49 | 0.653 | 0.023 (esn:1000) | 0.516 (polynarx:(5, 2)) | ∞ | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | xprod | 21 | 0.736 | 0.974 | 6.6e-24 (polynarx:(10, 2)) | 0.518 (polynarx:(5, 2)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | xprod_n1 | 21 | 0.739 | 0.975 | 0.00248 (polynarx:(10, 2)) | 0.519 (polynarx:(5, 2)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N6_zz_weak0.6 | xprod_n5 | 21 | 0.76 | 0.977 | 0.0592 (polynarx:(10, 2)) | 0.546 (polynarx:(5, 2)) | — | — | 1 | 30 |  |  |  |  |
| spin_reset_rand_N8_z | lorenz_multi | 8 | 0.528 | 0.705 | 4.22e-06 (esn:1000) | 0.169 (polynarx:(2, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N8_z | lorenz_uni | 8 | 0.55 | 0.732 | 0.000172 (esn:300) | 0.17 (polynarx:(5, 1)) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N8_z | mc30 | 8 | 0.81 | 0.919 | 1.5e-07 (kerr_delay:300) | 0.869 (esn:5) | 1e+06 | — | 30 | 10 |  | y |  |  |
| spin_reset_rand_N8_z | mc30_n5 | 8 | 0.816 | 0.921 | 0.0389 (kerr_delay:100) | 0.873 (esn:5) | 1e+06 | — | 30 | 10 |  | y |  |  |
| spin_reset_rand_N8_z | mg10 | 8 | 0.118 | 0.285 | 2.77e-09 (kerr_delay:300) | 0.0627 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N8_z | mg10_small | 8 | 0.289 | 0.3 | 0.00471 (kerr_delay:300) | 0.116 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N8_z | mg20 | 8 | 0.094 | 0.273 | 9.57e-08 (esn:1000) | 0.0426 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N8_z | narma10 | 8 | 0.294 | 0.405 | 0.0134 (kerr_delay:300) | 0.333 (esn:5) | 1e+06 | — | 30 | 30 |  | y |  |  |
| spin_reset_rand_N8_z | narma10_n5 | 8 | 0.309 | 0.416 | 0.0554 (kerr_delay:100) | 0.343 (esn:5) | 1e+05 | — | 30 | 30 |  | y |  |  |
| spin_reset_rand_N8_z | narma10_small | 8 | 0.482 | 0.641 | 0.143 (polynarx:(30, 1)) | 0.509 (esn:3) | 1e+06 | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N8_z | narma2 | 8 | 0.171 | 0.39 | 5.73e-06 (esn:1000) | 0.0889 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N8_z | narma20 | 8 | 0.409 | 0.457 | 0.1 (kerr_delay:300) | 0.483 (esn:5) | 1e+04 | — | 30 | 10 |  |  |  |  |
| spin_reset_rand_N8_z | narma5 | 8 | 0.261 | 0.523 | 0.000111 (kerr_delay:300) | 0.314 (esn:5) | — | — | 30 | 5 |  |  |  |  |
| spin_reset_rand_N8_z | xor | 8 | 0.984 | 1.01 | 4.38e-25 (polynarx:(20, 2)) | 0.748 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N8_z | xor_n1 | 8 | 0.984 | 1.01 | 0.00101 (kerr_delay:100) | 0.771 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N8_z | xor_n5 | 8 | 0.985 | 1.01 | 0.023 (kerr_delay:100) | 0.776 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N8_z | xprod | 8 | 0.996 | 1.01 | 6.6e-24 (polynarx:(10, 2)) | 0.969 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N8_z | xprod_n1 | 8 | 0.996 | 1.01 | 0.00248 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |
| spin_reset_rand_N8_z | xprod_n5 | 8 | 0.997 | 1.01 | 0.0592 (polynarx:(10, 2)) | 0.968 (esn:5) | — | — | 30 | 3 |  |  |  |  |

## Wins by axis

- **A: accuracy vs best classical (any size), all seeds:** 0/1015 cells
- **a: accuracy vs equal-readout-cost classical, all seeds:** 46/1015 cells
  - forr_qrc: forr_kloos_n10, forr_kloos_n12, forr_kloos_n14, forr_kloos_n16, forr_kloos_n18, forr_kloos_n20, forr_mm_n10, forr_mm_n12, forr_mm_n14, forr_mm_n16, forr_mmx_n10, forr_mmx_n12, forr_mmx_n14, forr_mmx_n16, forr_rand_n10, forr_rand_n12, forr_rand_n14, forr_rand_n16, forr_rand_n18, forr_rand_n20
  - spin_hamenc_chain_N6_xyz_V5: lorenz_multi
  - spin_hamenc_rand_N6_xyz_V5: lorenz_multi
  - spin_reset_chain_N4_z: mc30, mc30_n5, narma20
  - spin_reset_chain_N6_z: mc30, mc30_n5
  - spin_reset_chain_N8_z: mc30, mc30_n5
  - spin_reset_rand_N4_z: narma5
  - spin_reset_rand_N6_z_weak0.1: mc30, mc30_n5
  - spin_reset_rand_N6_z_weak0.3: mc30, mc30_n5
  - spin_reset_rand_N6_zz: mg10
  - spin_reset_rand_N6_zz_pm: mg10, mg20
  - spin_reset_rand_N6_zz_weak0.1: mg10
  - spin_reset_rand_N6_zz_weak0.3: mg10, mg10_small
  - spin_reset_rand_N6_zz_weak0.6: mg10, mg10_small
  - spin_reset_rand_N8_z: mc30, mc30_n5, narma10, narma10_n5
- **★ scale win:** 0/1015 cells
- **◆ both (A and S*_cls × W ≤ 3e5):** 0/1015 cells

## Best quantum config per task (median over seeds)

| task | best quantum (F_q) | q | cls (best) | q/cls | eqW | q/eqW |
|---|---|---|---|---|---|---|
| drift_kloos_n12 | forr_qrc (1) | 0.00604 | 0.00604 (forr_full:4096) | 1 | 0.0113 | 0.54 |
| drift_kloos_n16 | forr_qrc (1) | 0.000406 | 0.000406 (forr_full:65536) | 1 | 0.000406 | 1 |
| forr_gold_n10 | forr_qrc (1) | 0.00157 | 0.00157 (forr_full:1024) | 1 | 0.00157 | 1 |
| forr_gold_n12 | forr_qrc (1) | 0.00157 | 0.00157 (forr_full:4096) | 1 | 0.00157 | 1 |
| forr_gold_n14 | forr_qrc (1) | 0.00157 | 0.00157 (forr_full:16384) | 1 | 0.00157 | 1 |
| forr_gold_n16 | forr_qrc (1) | 0.00157 | 0.00157 (forr_full:65536) | 1 | 0.00157 | 1 |
| forr_kloos_n10 | forr_qrc (1) | 0.00102 | 0.00102 (forr_full:1024) | 1 | 0.928 | 0.0011 |
| forr_kloos_n12 | forr_qrc (1) | 0.000999 | 0.000999 (forr_full:4096) | 1 | 1.01 | 0.00098 |
| forr_kloos_n14 | forr_qrc (1) | 0.000945 | 0.000945 (forr_full:16384) | 1 | 1.02 | 0.00092 |
| forr_kloos_n16 | forr_qrc (1) | 0.001 | 0.001 (forr_full:65536) | 1 | 1.04 | 0.00097 |
| forr_kloos_n18 | forr_qrc (1) | 0.000973 | 0.000973 (forr_full:262144) | 1 | 1.04 | 0.00094 |
| forr_kloos_n20 | forr_qrc (1) | 0.000961 | 0.000961 (forr_full:1048576) | 1 | 1.01 | 0.00095 |
| forr_mm_n10 | forr_qrc (1) | 0.00148 | 0.00148 (forr_full:1024) | 1 | 0.891 | 0.0017 |
| forr_mm_n12 | forr_qrc (1) | 0.00148 | 0.00148 (forr_full:4096) | 1 | 0.991 | 0.0015 |
| forr_mm_n14 | forr_qrc (1) | 0.00148 | 0.00148 (forr_full:16384) | 1 | 1.03 | 0.0014 |
| forr_mm_n16 | forr_qrc (1) | 0.00148 | 0.00148 (forr_full:65536) | 1 | 1.03 | 0.0014 |
| forr_mmx_n10 | forr_qrc (1) | 0.00148 | 0.00148 (forr_full:1024) | 1 | 0.908 | 0.0016 |
| forr_mmx_n12 | forr_qrc (1) | 0.00148 | 0.00148 (forr_full:4096) | 1 | 0.95 | 0.0016 |
| forr_mmx_n14 | forr_qrc (1) | 0.00148 | 0.00148 (forr_full:16384) | 1 | 1.01 | 0.0015 |
| forr_mmx_n16 | forr_qrc (1) | 0.00148 | 0.00148 (forr_full:65536) | 1 | 1.03 | 0.0014 |
| forr_rand_n10 | forr_qrc (1) | 0.00117 | 0.00117 (forr_full:1024) | 1 | 0.96 | 0.0012 |
| forr_rand_n12 | forr_qrc (1) | 0.000964 | 0.000964 (forr_full:4096) | 1 | 1.01 | 0.00095 |
| forr_rand_n14 | forr_qrc (1) | 0.000829 | 0.000829 (forr_full:16384) | 1 | 1.01 | 0.00082 |
| forr_rand_n16 | forr_qrc (1) | 0.000861 | 0.000861 (forr_full:65536) | 1 | 1.01 | 0.00085 |
| forr_rand_n18 | forr_qrc (1) | 0.000858 | 0.000858 (forr_full:262144) | 1 | 1.03 | 0.00083 |
| forr_rand_n20 | forr_qrc (1) | 0.00083 | 0.00083 (forr_full:1048576) | 1 | 1.02 | 0.00081 |
| lorenz_multi | spin_hamenc_chain_N6_xyz_V5 (90) | 0.000517 | 7.28e-06 (esn:1000) | 71 | 0.0135 | 0.038 |
| lorenz_uni | spin_hamenc_rand_N6_xyz_V5 (90) | 0.00516 | 0.000172 (esn:300) | 30 | 0.00808 | 0.64 |
| mc30 | qkerr_delay_D100_tuned (300) | 0.026 | 7.66e-07 (kerr_delay:300) | 3.4e+04 | 3.29e-06 | 7.9e+03 |
| mc30_n5 | qkerr_delay_D100_chi0 (300) | 0.0579 | 0.0389 (kerr_delay:100) | 1.5 | 0.0389 | 1.5 |
| mg10 | spin_reset_rand_N6_zz_V10 (210) | 6.29e-05 | 2.77e-09 (kerr_delay:300) | 2.3e+04 | 4.15e-06 | 15 |
| mg10_small | qkerr_delay_D100_chi0.3 (300) | 0.00905 | 0.00471 (kerr_delay:300) | 1.9 | 0.00471 | 1.9 |
| mg20 | spin_reset_rand_N6_zz_V10 (210) | 0.000116 | 9.57e-08 (esn:1000) | 1.2e+03 | 2.26e-05 | 5.1 |
| narma10 | cv_gauss_N12 (324) | 0.0346 | 0.0134 (kerr_delay:300) | 2.6 | 0.0259 | 1.3 |
| narma10_n5 | cv_gauss_N12 (324) | 0.0742 | 0.0554 (kerr_delay:100) | 1.3 | 0.0608 | 1.2 |
| narma10_small | qkerr_delay_D100_chi0.3 (300) | 0.281 | 0.143 (polynarx:(30, 1)) | 2 | 0.143 | 2 |
| narma2 | cv_gauss_N12 (324) | 0.000312 | 5.73e-06 (esn:1000) | 55 | 1.8e-05 | 17 |
| narma20 | qkerr_delay_D100_chi0 (300) | 0.131 | 0.1 (kerr_delay:100) | 1.3 | 0.136 | 0.96 |
| narma5 | cv_gauss_N12 (324) | 0.00164 | 0.000111 (esn:1000) | 15 | 0.000244 | 6.7 |
| qin_full | spin_qin_rand_N6_zz_hybrid (221) | 0.595 | 0.113 (esn:1000) | 5.2 | 0.318 | 1.9 |
| qin_full_S | spin_qin_rand_N6_zz_hybrid (221) | 0.596 | 0.126 (esn:1000) | 4.7 | 0.316 | 1.9 |
| qin_local | spin_qin_rand_N6_zz_hybrid (221) | 0.595 | 0.0912 (polynarx:(3, 2)) | 6.5 | 0.0912 | 6.5 |
| qin_local_S | spin_qin_rand_N6_zz_hybrid (221) | 0.596 | 0.0922 (polynarx:(3, 2)) | 6.5 | 0.0922 | 6.5 |
| xor | cv_gauss_N12 (324) | 0.011 | 4.38e-25 (polynarx:(20, 2)) | 2.5e+22 | 4.38e-25 | 2.5e+22 |
| xor_n1 | cv_gauss_N12 (324) | 0.0115 | 0.00101 (kerr_delay:100) | 11 | 0.00102 | 11 |
| xor_n5 | cv_gauss_N12 (324) | 0.0229 | 0.023 (esn:1000) | 1 | 0.023 | 1 |
| xprod | cv_gauss_N12 (324) | 0.00743 | 6.6e-24 (polynarx:(10, 2)) | 1.1e+21 | 6.6e-24 | 1.1e+21 |
| xprod_n1 | cv_gauss_N12 (324) | 0.0103 | 0.00248 (polynarx:(10, 2)) | 4.1 | 0.00248 | 4.1 |
| xprod_n5 | cv_gauss_N12 (324) | 0.0757 | 0.0592 (polynarx:(10, 2)) | 1.3 | 0.0592 | 1.3 |
