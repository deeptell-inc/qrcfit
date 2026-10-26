"""Benchmark tasks. Each returns dict(u=(T,d_in) in [0,1], y=(T,d_out), washout, T_train, T_test, name).

Task axes covered (see report §2-4): nonlinear memory (NARMA), chaotic forecasting (Mackey-Glass, Lorenz),
univariate vs correlated multivariate (Lorenz uni/multi), linear memory capacity, cross-time products
(Soh's cross-time nonlinear rank), long-memory nonlinear (delayed XOR), and few-data regimes.
"""
import numpy as np

WASHOUT = 100


def _pack(name, u, y, T_train, T_test, washout=WASHOUT):
    u = np.asarray(u, float)
    y = np.asarray(y, float)
    if u.ndim == 1:
        u = u[:, None]
    if y.ndim == 1:
        y = y[:, None]
    T = washout + T_train + T_test
    return dict(name=name, u=u[:T], y=y[:T], washout=washout, T_train=T_train, T_test=T_test)


def narma(n, T_train=1000, T_test=500, seed=0):
    rng = np.random.default_rng(seed)
    T = WASHOUT + T_train + T_test + n + 1
    u = rng.uniform(0, 0.5, T)
    y = np.zeros(T)
    for t in range(n, T - 1):
        if n == 2:
            y[t + 1] = 0.4 * y[t] + 0.4 * y[t] * y[t - 1] + 0.6 * u[t] ** 3 + 0.1
        else:
            v = 0.3 * y[t] + 0.05 * y[t] * y[t - n + 1:t + 1].sum() + 1.5 * u[t - n + 1] * u[t] + 0.1
            y[t + 1] = np.tanh(v) if n >= 20 else v
    return _pack(f"narma{n}", 2 * u[n:], y[n:], T_train, T_test)


def mackey_glass(h=10, T_train=1000, T_test=500, seed=0, tau=17, dt=0.1, sub=10):
    rng = np.random.default_rng(seed)
    T = WASHOUT + T_train + T_test + h + 1
    n_hist = int(tau / dt)
    steps = (T + 200) * sub
    s = np.zeros(steps + n_hist)
    s[:n_hist] = 1.2 + 0.05 * rng.standard_normal(n_hist)

    def f(x, xd):
        return 0.2 * xd / (1 + xd ** 10) - 0.1 * x

    for i in range(n_hist, steps + n_hist - 1):
        xd = s[i - n_hist]
        k1 = f(s[i], xd)
        k2 = f(s[i] + 0.5 * dt * k1, xd)
        k3 = f(s[i] + 0.5 * dt * k2, xd)
        k4 = f(s[i] + dt * k3, xd)
        s[i + 1] = s[i] + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    x = s[n_hist + 200 * sub::sub][:T]
    x = (x - x.min()) / (x.max() - x.min())
    return _pack(f"mg{h}", x[:-h], x[h:], T_train, T_test)


def _lorenz(T, seed, dt=0.01, sub=2):
    rng = np.random.default_rng(seed)
    z = np.array([1.0, 1.0, 1.0]) + 0.1 * rng.standard_normal(3)

    def f(v):
        return np.array([10 * (v[1] - v[0]), v[0] * (28 - v[2]) - v[1], v[0] * v[1] - 8 / 3 * v[2]])

    out = []
    for i in range((T + 500) * sub):
        k1 = f(z); k2 = f(z + 0.5 * dt * k1); k3 = f(z + 0.5 * dt * k2); k4 = f(z + dt * k3)
        z = z + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        if i % sub == 0:
            out.append(z.copy())
    X = np.array(out)[500:]
    X = (X - X.min(0)) / (X.max(0) - X.min(0))
    return X


def lorenz(h=25, multivariate=False, T_train=1000, T_test=500, seed=0):
    T = WASHOUT + T_train + T_test + h + 1
    X = _lorenz(T, seed)
    u = X[:-h] if multivariate else X[:-h, 0]
    y = X[h:, 0]
    return _pack("lorenz_multi" if multivariate else "lorenz_uni", u, y, T_train, T_test)


def memory_capacity(K=30, T_train=1000, T_test=500, seed=0):
    rng = np.random.default_rng(seed)
    T = WASHOUT + T_train + T_test + K
    u = rng.uniform(0, 1, T)
    y = np.stack([u[K - k:T - k] for k in range(1, K + 1)], 1)
    return _pack(f"mc{K}", u[K:], y, T_train, T_test)


def cross_products(pairs=((1, 2), (1, 3), (2, 5), (3, 8)), T_train=1000, T_test=500, seed=0):
    rng = np.random.default_rng(seed)
    D = max(max(p) for p in pairs)
    T = WASHOUT + T_train + T_test + D
    u = rng.uniform(0, 1, T)
    c = u - 0.5
    y = np.stack([c[D - a:T - a] * c[D - b:T - b] for a, b in pairs], 1)
    return _pack("xprod", u[D:], y, T_train, T_test)


def delayed_xor(delays=(1, 3, 5, 10), T_train=1000, T_test=500, seed=0):
    rng = np.random.default_rng(seed)
    D = max(delays)
    T = WASHOUT + T_train + T_test + D
    u = rng.integers(0, 2, T)
    y = np.stack([(u[D:T] ^ u[D - d:T - d]) for d in delays], 1).astype(float)
    return _pack("xor", u[D:].astype(float), y, T_train, T_test)


def with_noise(task, sigma, seed, suffix):
    """Observation noise on the inputs seen by every model; targets stay clean."""
    rng = np.random.default_rng(seed + 12345)
    t = dict(task)
    t["u"] = task["u"] + sigma * rng.standard_normal(task["u"].shape)
    t["name"] = task["name"] + suffix
    return t


_P = {"I": np.eye(2, dtype=complex), "X": np.array([[0, 1], [1, 0]], complex),
      "Y": np.array([[0, -1j], [1j, 0]]), "Z": np.diag([1.0, -1.0]).astype(complex)}
_SWAP = np.eye(4, dtype=complex)[[0, 2, 1, 3]]


def _pswap(alpha):
    return np.cos(alpha) * np.eye(4) + 1j * np.sin(alpha) * _SWAP


def _negativity(rho):
    r = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)  # partial transpose on qubit 2
    ev = np.linalg.eigvalsh(r)
    return float(-ev[ev < 0].sum())


def quantum_input(T_train=1000, T_test=500, seed=0, phi=np.pi / 4, block=20, access="local", target="purity"):
    """Collision-model stream of 2-qubit states rho_t on (system S, ancilla A_t).
    Fresh Haar-random ancilla A_{t+1} first partially swaps with A_t (angle theta_t, piecewise constant per
    block: the non-Markovianity knob), then collides with S (angle phi). rho_t = state of (S, A_{t+1}).
    Quantum reservoirs receive rho_seq directly. Classical models receive u = Pauli expectations:
    access='local' -> 6 single-qubit expectations; 'full' -> all 15 two-qubit Pauli expectations.
    Targets: purity Tr rho^2, negativity, theta_t/(pi/2)."""
    rng = np.random.default_rng(seed)
    T = WASHOUT + T_train + T_test
    labels = [a + b for a in "IXYZ" for b in "IXYZ"][1:]
    if access == "local":
        labels = [l for l in labels if "I" in l]
    paulis = [np.kron(_P[l[0]], _P[l[1]]) for l in labels]
    rho = np.zeros((4, 4), complex); rho[0, 0] = 1
    rho_seq = np.zeros((T, 4, 4), complex); u = np.zeros((T, len(paulis))); y = np.zeros((T, 3))
    theta = 0.0
    for t in range(T):
        if t % block == 0:
            theta = rng.uniform(0, np.pi / 2)
        psi = rng.standard_normal(2) + 1j * rng.standard_normal(2); psi /= np.linalg.norm(psi)
        r3 = np.kron(rho, np.outer(psi, psi.conj()))                    # order S, A_old, A_new
        Uaa = np.kron(np.eye(2), _pswap(theta)); r3 = Uaa @ r3 @ Uaa.conj().T
        Usa = _pswap(phi).reshape(2, 2, 2, 2)                            # acts on (S, A_new)
        U3 = np.einsum("acbd,ef->aecbfd", Usa, np.eye(2)).reshape(8, 8)  # S,A_old,A_new ordering
        r3 = U3 @ r3 @ U3.conj().T
        rho = np.trace(r3.reshape(2, 2, 2, 2, 2, 2), axis1=1, axis2=4).reshape(4, 4)  # trace out A_old
        rho_seq[t] = rho
        u[t] = [np.real(np.trace(rho @ P)) for P in paulis]
        if target == "entropy":  # von Neumann entropy: not a polynomial in the Pauli expectations
            ev = np.linalg.eigvalsh(rho); ev = ev[ev > 1e-12]
            first = float(-(ev * np.log2(ev)).sum())
        else:
            first = np.real(np.trace(rho @ rho))
        y[t] = [first, _negativity(rho), theta / (np.pi / 2)]
    out = _pack(f"qin_{access}" + ("_S" if target == "entropy" else ""), u, y, T_train, T_test)
    out["rho_seq"] = rho_seq
    return out


def forrelation_random_stream(n=12, T_train=1000, T_test=500, seed=0, p_switch=0.1):
    """Fresh random oracle pair at EVERY step (the Aaronson–Ambainis distribution): f_t uniform ±1 (regenerated
    from a per-step seed), g_t = sign(Walsh f_t) on YES steps (Phi ≈ 0.8) and its translate by random e != 0
    on NO steps (|Phi| ~ N^{-1/2}). Nothing is public and nothing persists across steps, so neither the
    known-f white-box attack nor query amortisation over the stream applies; the classical Ω(√N/log N)
    per-step query lower bound holds for this distribution."""
    from .forrelation import fwht
    rng = np.random.default_rng(seed)
    N = 1 << n
    T = WASHOUT + T_train + T_test
    h = np.zeros(T, dtype=np.int64); h[0] = 1
    for t in range(1, T):
        h[t] = h[t - 1] ^ (rng.uniform() < p_switch)
    e = np.where(h == 1, 0, rng.integers(1, N, T))
    fseed = rng.integers(0, 2 ** 62, T)
    phi = np.zeros(T)
    for t in range(T):
        f = 1.0 - 2.0 * np.random.default_rng(int(fseed[t])).integers(0, 2, N)
        fh = fwht(f); g = np.where(fh >= 0, 1.0, -1.0)
        phi[t] = float(np.dot(np.roll(g, 0)[np.arange(N) ^ int(e[t])], fh) / N ** 1.5)  # Phi(f, g o tau_e)
    uu = (1 + phi) / 8
    yn = np.zeros(T)
    for t in range(10, T - 1):
        yn[t + 1] = 0.3 * yn[t] + 0.05 * yn[t] * yn[t - 9:t + 1].sum() + 1.5 * uu[t - 9] * uu[t] + 0.1
    out = _pack(f"forr_rand_n{n}", phi, np.stack([phi, h.astype(float), yn], 1), T_train, T_test)
    out.update(fseed=fseed, e=e, n=n, phi=phi[:out["u"].shape[0]], phi_yes=float(np.median(phi[h == 1])))
    return out


def forrelation_mm_stream(n=12, T_train=1000, T_test=500, seed=0, p_switch=0.1):
    """Fresh Maiorana–McFarland pair at every step (n even, n = 2k): f_t(x,y) = (-1)^{x.pi_t(y) + h_t(y)} with a
    uniformly random permutation pi_t of {0,1}^k and random h_t; its exact dual is
    g_t(a,b) = (-1)^{b.pi_t^{-1}(a) + h_t(pi_t^{-1}(a))} (Phi = 1 exactly, `phi_mm` in the bqp Lean project).
    NO steps translate g_t by random e != 0. Black-box classical hardness of MM pairs reduces to one-way
    functions (Girish–Servedio); algebraic degree of a random pi makes the degree-2 ANF attack fail."""
    from .forrelation import fwht, mm_pair
    rng = np.random.default_rng(seed)
    N = 1 << n
    T = WASHOUT + T_train + T_test
    h = np.zeros(T, dtype=np.int64); h[0] = 1
    for t in range(1, T):
        h[t] = h[t - 1] ^ (rng.uniform() < p_switch)
    e = np.where(h == 1, 0, rng.integers(1, N, T))
    fseed = rng.integers(0, 2 ** 62, T)
    phi = np.zeros(T)
    for t in range(T):
        f, g = mm_pair(n, int(fseed[t]))
        phi[t] = float(np.dot(g[np.arange(N) ^ int(e[t])], fwht(f)) / N ** 1.5)
    uu = (1 + phi) / 8
    yn = np.zeros(T)
    for t in range(10, T - 1):
        yn[t + 1] = 0.3 * yn[t] + 0.05 * yn[t] * yn[t - 9:t + 1].sum() + 1.5 * uu[t - 9] * uu[t] + 0.1
    out = _pack(f"forr_mm_n{n}", phi, np.stack([phi, h.astype(float), yn], 1), T_train, T_test)
    out.update(fseed=fseed, e=e, n=n, family="mm", phi=phi[:out["u"].shape[0]], phi_yes=float(np.median(phi[h == 1])))
    return out


def forrelation_stream(n=12, family="kloosterman", T_train=1000, T_test=500, seed=0, p_switch=0.1):
    """Oracle-pair stream. Hidden two-state Markov chain h_t; YES (h=1): (chi_c f, g o tau_c) with random c
    (Phi unchanged by the §2 invariance), NO (h=0): additionally g translated by random e != 0 (Phi ~ 0).
    u = exact Phi_t (what a full-information classical model sees); y = [Phi_t, h_t, NARMA10 driven by (1+Phi_t)/8].
    The task carries f, g, c_t, e_t so query-limited classical baselines and the quantum circuit can query the oracles."""
    from .forrelation import kloosterman_pair, gold_pair, phi_all_translations
    rng = np.random.default_rng(seed)
    f, g = kloosterman_pair(n) if family == "kloosterman" else gold_pair(n, rng)
    N = 1 << n
    phi_e = phi_all_translations(f, g)
    T = WASHOUT + T_train + T_test
    h = np.zeros(T, dtype=np.int64); h[0] = 1
    for t in range(1, T):
        h[t] = h[t - 1] ^ (rng.uniform() < p_switch)
    c = rng.integers(0, N, T)
    e = np.where(h == 1, 0, rng.integers(1, N, T))
    phi = phi_e[e]
    uu = (1 + phi) / 8  # keeps NARMA10 bounded for a near-constant input
    yn = np.zeros(T)
    for t in range(10, T - 1):
        yn[t + 1] = 0.3 * yn[t] + 0.05 * yn[t] * yn[t - 9:t + 1].sum() + 1.5 * uu[t - 9] * uu[t] + 0.1
    out = _pack(f"forr_{family[:5]}_n{n}", phi, np.stack([phi, h.astype(float), yn], 1), T_train, T_test)
    out.update(f=f, g=g, c=c, e=e, n=n, phi=phi[:out["u"].shape[0]], phi_yes=float(phi_e[0]))
    return out


def all_tasks(seed=0, quick=False):
    kw = dict(seed=seed)
    if quick:
        kw.update(T_train=300, T_test=150)
    ts = [
        narma(2, **kw), narma(5, **kw), narma(10, **kw), narma(20, **kw),
        mackey_glass(10, **kw), mackey_glass(20, **kw),
        lorenz(10, False, **kw), lorenz(10, True, **kw),
        memory_capacity(30, **kw), cross_products(**kw), delayed_xor(**kw),
    ]
    small = dict(seed=seed, T_train=100, T_test=300 if not quick else 150)
    t1 = narma(10, **small); t1["name"] = "narma10_small"
    t2 = mackey_glass(10, **small); t2["name"] = "mg10_small"
    ts += [t1, t2]
    # wave 2: observation-noise variants (poly-NARX can no longer solve xor/xprod exactly) and quantum-input tasks
    ts += [with_noise(cross_products(**kw), 0.01, seed, "_n1"), with_noise(cross_products(**kw), 0.05, seed, "_n5"),
           with_noise(delayed_xor(**kw), 0.01, seed, "_n1"), with_noise(delayed_xor(**kw), 0.05, seed, "_n5"),
           with_noise(narma(10, **kw), 0.05, seed, "_n5"), with_noise(memory_capacity(30, **kw), 0.05, seed, "_n5"),
           quantum_input(access="local", **kw), quantum_input(access="full", **kw),
           quantum_input(access="local", target="entropy", **kw), quantum_input(access="full", target="entropy", **kw)]
    if not quick:
        for n in (10, 12, 14, 16):
            ts += [forrelation_stream(n, "kloosterman", **kw), forrelation_stream(n, "gold", **kw)]
        ts += [forrelation_stream(18, "kloosterman", **kw), forrelation_stream(20, "kloosterman", **kw)]
        ts += [forrelation_random_stream(n, **kw) for n in (10, 12, 14, 16, 18, 20)]
        ts += [forrelation_mm_stream(n, **kw) for n in (10, 12, 14, 16)]
        from .forrelation import drift_stream
        ts += [drift_stream(12, **kw), drift_stream(16, **kw)]
    return {t["name"]: t for t in ts}


def get_task(name, seed=0, quick=False):
    """Build one task by name without constructing the whole suite (expensive oracle tasks are built lazily)."""
    import re
    m = re.match(r"forr_rand_n(\d+)$", name)
    if m:
        return forrelation_random_stream(int(m.group(1)), seed=seed)
    m = re.match(r"forr_mm_n(\d+)$", name)
    if m:
        return forrelation_mm_stream(int(m.group(1)), seed=seed)
    m = re.match(r"forr_(kloos|gold)_n(\d+)$", name)
    if m:
        return forrelation_stream(int(m.group(2)), "kloosterman" if m.group(1) == "kloos" else "gold", seed=seed)
    m = re.match(r"drift_kloos_n(\d+)$", name)
    if m:
        from .forrelation import drift_stream
        return drift_stream(int(m.group(1)), seed=seed)
    return all_tasks(seed, quick)[name]
