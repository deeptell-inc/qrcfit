import numpy as np
from qrcfit.tasks import narma, memory_capacity
from qrcfit.reservoirs import SpinReset, SpinHamEnc, SpinQInput, GaussianCV, KerrCV, TwoModeCV, KerrDelayQ, _local_kraus, _relax_kraus, _weak_kraus
from qrcfit.tasks import quantum_input, with_noise, cross_products
from qrcfit.evaluate import fit_predict, shot_curve
from qrcfit.baselines import tune


def test_trace_and_hermiticity_preserved():
    for R in [SpinReset(4, "random", 1.0, 2, "z+zz", T1=3.0, T2=2.0), SpinHamEnc(4, "chain", 1.0, 2, "xyz", T1=3.0, T2=2.0)]:
        rho = np.zeros((16, 16), complex); rho[0, 0] = 1
        for u in [0.1, 0.7, 0.3]:
            rho = R._encode(rho, u); rho = R._evolve(rho)
        assert abs(np.trace(rho) - 1) < 1e-10 and np.allclose(rho, rho.conj().T)
        assert np.linalg.eigvalsh(rho).min() > -1e-10


def test_kraus_is_cptp():
    Ks = _relax_kraus(2.0, 1.5, 0.3)
    S = sum(K.conj().T @ K for K in Ks)
    assert np.allclose(S, np.eye(2))


def test_spin_reset_has_memory_and_kerr_is_normalised():
    t = memory_capacity(10, T_train=300, T_test=150)
    X, V = SpinReset(5, "random").run(t["u"])
    assert fit_predict(X, t) < 0.9  # some linear memory beyond the trivially present current input
    k = KerrCV(chi=0.5, dim=12, levels=8)
    X, V = k.run(t["u"][:50])
    assert np.all(np.isfinite(X)) and np.all(V >= 0)


def test_shot_noise_monotone_and_baseline_runs():
    t = narma(5, T_train=300, T_test=150)
    X, V = GaussianCV(4).run(t["u"])
    c = shot_curve(X, V, t, np.random.default_rng(0), shots=[1e2, 1e6, np.inf])
    assert c[1e2] >= c[np.inf] - 1e-9
    nm, F = tune(t, "esn", 30, 3, 0)
    assert 0 < nm < 1.0 and F == 30


def test_exact_lindblad_matches_trotter_kraus_for_small_dt():
    a = SpinReset(3, "random", 0.05, 1, "xyz", T1=2.0, T2=1.5, seed=1)   # exact superoperator path
    b = SpinReset(3, "random", 0.05, 1, "xyz", T1=2.0, T2=1.5, seed=1); b.P = None  # Trotter-Kraus path
    rho = np.zeros((8, 8), complex); rho[0, 0] = 1
    ra = rb = a._encode(rho, 0.4)
    for _ in range(3):
        ra, rb = a._evolve(ra), b._evolve(rb)
    assert abs(np.trace(ra) - 1) < 1e-10 and np.abs(ra - rb).max() < 5e-3  # Trotter split error only; single-qubit channels agree to 1e-16


def test_wave2_pseudomode_and_quantum_input_preserve_trace():
    R = SpinReset(4, "random", 1.0, 1, "z+zz", pm=dict(g=0.5, T1=5.0))
    assert R.Nt == 5 and R.F == 4 + 6
    rho = np.zeros((32, 32), complex); rho[0, 0] = 1
    for u in [0.2, 0.9]:
        rho = R._evolve(R._encode(rho, u))
    assert abs(np.trace(rho) - 1) < 1e-10 and np.linalg.eigvalsh(rho).min() > -1e-10
    t = quantum_input(T_train=60, T_test=30, access="local")
    assert t["u"].shape[1] == 6 and t["rho_seq"].shape == (len(t["u"]), 4, 4)
    assert np.all(t["y"][:, 1] >= 0) and np.all(t["y"][:, 0] <= 1 + 1e-9)
    Q = SpinQInput(4, "random", 1.0, 1, "z+zz")
    X, V = Q.run(t["u"][:20], t["rho_seq"][:20])
    assert np.all(np.isfinite(X)) and X.shape == (20, Q.F)
    tf = quantum_input(T_train=60, T_test=30, access="full")
    assert tf["u"].shape[1] == 15


def test_wave2_two_mode_cv_is_normalised_and_noise_variant_differs():
    R = TwoModeCV(chi=0.5, dim=5, readout="fock", nmax=3)
    u = np.random.default_rng(0).uniform(0, 1, (6, 1))
    X, V = R.run(u)
    assert X.shape == (6, 9) and np.all(X >= -1e-12) and np.all(X.sum(1) <= 1 + 1e-9)
    R2 = TwoModeCV(chi=0.0, dim=5, readout="moments"); X2, V2 = R2.run(u)
    assert np.all(np.isfinite(X2)) and np.all(V2 >= 0)
    t = cross_products(T_train=50, T_test=20); tn = with_noise(t, 0.05, 0, "_n5")
    assert tn["name"] == "xprod_n5" and np.allclose(tn["y"], t["y"]) and not np.allclose(tn["u"], t["u"])


def test_wave3_kerr_delay_q_and_weak_measurement():
    R = KerrDelayQ(D=4, chi=0.3, kappa=0.05, eps0=0.5, dim=10, levels=9)
    u = np.random.default_rng(1).uniform(0, 1, (12, 1))
    X, V = R.run(u)
    assert X.shape == (12, 12) and np.all(np.isfinite(X)) and np.all(V >= 0) and np.all(X[:, 2::3] >= -1e-9)  # <n> >= 0
    Ks = _weak_kraus(0.3)
    assert np.allclose(sum(K.conj().T @ K for K in Ks), np.eye(2))
    W = SpinReset(4, "random", 1.0, 1, "z+zz", weak=0.3)
    rho = np.zeros((16, 16), complex); rho[0, 0] = 1
    rho = W._evolve(W._encode(rho, 0.4))
    e, var = W._measure(rho)
    assert abs(np.trace(rho) - 1) < 1e-10 and np.all(var >= (1 - 0.09) / 0.09 - 1e-9)
    t = quantum_input(T_train=40, T_test=20, target="entropy")
    assert t["name"] == "qin_local_S" and np.all(t["y"][:, 0] >= -1e-9) and np.all(t["y"][:, 0] <= 2 + 1e-9)


def test_wave4_forrelation_module():
    from qrcfit.forrelation import gf_tables, gf_trace_table, fwht, kloosterman_pair, gold_pair, phi_all_translations, is_quadratic, classical_estimates, anf2_queries, ForrelationQRC
    from qrcfit.tasks import forrelation_stream
    exp, log = gf_tables(10); N = 1 << 10
    a = np.arange(1, N); inv = exp[(-log[a]) % (N - 1)]
    prod = exp[(log[a] + log[inv]) % (N - 1)]
    assert np.all(prod == 1)                       # a * a^{-1} = 1
    v = np.random.default_rng(0).choice([-1.0, 1.0], N)
    assert np.allclose(fwht(fwht(v)) / N, v)       # involution
    f, g = kloosterman_pair(10); ph = phi_all_translations(f, g)
    assert 0.78 < ph[0] < 0.87 and np.abs(ph[1:]).max() < 0.2 and not is_quadratic(f, 10)
    fg, gg = gold_pair(10, np.random.default_rng(1)); pg = phi_all_translations(fg, gg)
    assert abs(pg[0] - 1) < 1e-9 and is_quadratic(fg, 10) and is_quadratic(gg, 10)
    t = forrelation_stream(10, "gold", T_train=60, T_test=30)
    rng = np.random.default_rng(0)
    assert np.allclose(classical_estimates(t, "anf2", anf2_queries(10), rng), t["phi"])          # exact on quadratic phases
    tk = forrelation_stream(10, "kloosterman", T_train=60, T_test=30)
    est = classical_estimates(tk, "naive", 2000, rng)
    assert abs(np.mean(est - tk["phi"])) < 0.2 and not np.allclose(classical_estimates(tk, "anf2", anf2_queries(10), rng), tk["phi"])
    tk2 = forrelation_stream(10, "kloosterman", T_train=300, T_test=100)
    c = ForrelationQRC().shot_curve_task(tk2, [1e2, np.inf])
    assert np.isfinite(c[1e2]) and c[np.inf] < 0.5


def test_pairs_estimator_is_unbiased_and_sqrtN_efficient():
    from qrcfit.forrelation import classical_estimates
    from qrcfit.tasks import forrelation_stream
    tk = forrelation_stream(12, "kloosterman", T_train=100, T_test=50)
    rng = np.random.default_rng(3)
    est = classical_estimates(tk, "pairs", 2000, rng)   # Q=2000 ≈ 31 sqrt(N): variance ≈ 4/Q + 4N/Q^2 ≈ 0.006
    err = est - tk["phi"]
    assert abs(err.mean()) < 0.05 and err.std() < 0.2
    naive = classical_estimates(tk, "naive", 2000, rng) - tk["phi"]
    assert naive.std() > 3 * err.std()                   # naive variance N/Q ≈ 2 ≫ pairs
