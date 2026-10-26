"""Forrelation oracle-input tasks (wave 4).

Oracle pairs (f, g) over {0,1}^n with f, g in {±1}. Phi(f,g) = sum_{x,y} f(x)(-1)^{x.y} g(y) / N^{3/2}.
The 2-query quantum circuit H D_g H D_f H + Hadamard test accepts with probability exactly (1+Phi)/2
(machine-checked in the bqp project, quantum_algorithm_extracts.md §1). Classically, constant-advantage
estimation of Phi needs Omega(sqrt(N)/log N) queries (Aaronson–Ambainis).

Families: 'kloosterman' f = (-1)^{Tr(x^{-1})} over GF(2^n), g = sign(Walsh(f)) (Phi in [0.81, 0.85], not quadratic);
          'gold'        f = (-1)^{Tr(s3 x^3)} bent (n even, s3 non-cubic-residue), g = sign(Walsh(f)) (Phi = 1;
                        both are QUADRATIC Boolean functions, hence classically learnable in O(n^2) queries, §4).
NO instances: g translated by e != 0 (Phi(f, g o tau_e) ~ 0). All translation correlations come from two FWHTs
(S_e = H(f . Hg)(e), §3).
"""
import numpy as np

PRIM = {8: 0x11D, 10: 0x409, 12: 0x1053, 14: 0x4443, 16: 0x1100B, 18: 0x40081, 20: 0x100009, 22: 0x400003, 24: 0x1000087}


def gf_tables(n):
    """exp/log tables of GF(2^n) with a primitive polynomial; raises if the polynomial is not primitive."""
    poly = PRIM[n]; N = 1 << n
    exp = np.zeros(2 * N, dtype=np.int64); log = np.full(N, -1, dtype=np.int64)
    a = 1
    for i in range(N - 1):
        exp[i] = a
        if log[a] != -1:
            raise ValueError("polynomial not primitive")
        log[a] = i
        a <<= 1
        if a & N:
            a ^= poly
    exp[N - 1:2 * N - 2] = exp[:N - 1]
    return exp, log


def gf_trace_table(n, exp, log):
    """Tr(a) for all a in GF(2^n) as 0/1 (vectorised via log tables)."""
    N = 1 << n; a = np.arange(1, N); la = log[a]
    tr = np.zeros(N, dtype=np.int64)
    for i in range(n):
        tr[1:] ^= exp[(la * (1 << i)) % (N - 1)]
    # the sum of conjugates is in GF(2): element 0 or 1
    assert np.all((tr == 0) | (tr == 1)), "trace not in {0,1}"
    return tr


def fwht(v):
    """Unnormalised Walsh–Hadamard transform (in place on a copy)."""
    v = np.array(v, dtype=np.float64); N = len(v); h = 1
    while h < N:
        v = v.reshape(-1, 2, h)
        a, b = v[:, 0, :].copy(), v[:, 1, :].copy()
        v[:, 0, :] = a + b; v[:, 1, :] = a - b
        v = v.reshape(N); h *= 2
    return v


def phi_all_translations(f, g):
    """Phi(f, g o tau_e) for every e, via S_e = FWHT(f * FWHT(g))(e) / N^{3/2} (two transforms)."""
    N = len(f)
    return fwht(f * fwht(g)) / N ** 1.5


def kloosterman_pair(n):
    exp, log = gf_tables(n); N = 1 << n
    tr = gf_trace_table(n, exp, log)
    inv = np.zeros(N, dtype=np.int64); a = np.arange(1, N)
    inv[1:] = exp[(-log[a]) % (N - 1)]
    f = 1.0 - 2.0 * tr[inv]
    fh = fwht(f); g = np.where(fh >= 0, 1.0, -1.0)
    return f, g


def gold_pair(n, rng):
    """Bent Gold pair: Tr(s3 x^3) with s3 a non-cubic-residue (|Walsh| flat); resample s3 until bent."""
    exp, log = gf_tables(n); N = 1 << n
    tr = gf_trace_table(n, exp, log)
    for _ in range(50):
        s3 = int(rng.integers(1, N))
        cube = np.zeros(N, dtype=np.int64); a = np.arange(1, N)
        cube[1:] = exp[(3 * log[a] + log[s3]) % (N - 1)]
        f = 1.0 - 2.0 * tr[cube]
        fh = fwht(f)
        if np.allclose(np.abs(fh), np.sqrt(N)):
            return f, np.where(fh >= 0, 1.0, -1.0)
    raise RuntimeError("no bent Gold function found")


def is_quadratic(f, n):
    """True if the ±1 function f has algebraic degree <= 2 (checked exactly on the full table)."""
    return np.array_equal(anf2_reconstruct(anf2_learn(f, n), n), f)


def anf2_learn(f, n, query=None):
    """Degree-<=2 ANF of f from 1 + n + n(n-1)/2 queries at 0, e_i, e_i^e_j (Möbius inversion restricted
    to degree <= 2). `query(x)` returns f(x); defaults to table lookup. Returns (a0, a (n,), A (n,n) upper)."""
    q = (lambda x: f[x]) if query is None else query
    b = lambda x: int((1 - q(x)) // 2)
    a0 = b(0); a = np.array([b(1 << i) ^ a0 for i in range(n)], dtype=np.int64)
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for j in range(i + 1, n):
            A[i, j] = b((1 << i) | (1 << j)) ^ a0 ^ a[i] ^ a[j]
    return a0, a, A


def anf2_reconstruct(coef, n):
    a0, a, A = coef; N = 1 << n
    X = ((np.arange(N)[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int64)
    lin = (X @ a) & 1
    quad = ((X @ A) * X).sum(1) & 1
    return 1.0 - 2.0 * ((a0 ^ lin ^ quad) & 1)


ANF2_EXTRA = 32  # verification queries per oracle


def _parity(v):
    """Popcount parity of an int array as int64 0/1 (bitwise_count returns uint8: cast before arithmetic)."""
    return np.bitwise_count(np.asarray(v, dtype=np.int64)).astype(np.int64) & 1


def anf2_queries(n):
    return 2 * (1 + n + n * (n - 1) // 2 + ANF2_EXTRA)


def drift_stream(n=16, T_train=1000, T_test=500, seed=0):
    """Demo-A task as a map task: device g_t = ideal dual g with each entry flipped w.p. (1-p_t)/2, fidelity
    p_t in [0.3,1] follows an OU walk with jumps; E[Phi_t] = p_t * Phi_YES. Targets [p_t, Phi_t].
    u = exact Phi_t (full-information baselines). Carries f, g, flips for query-limited estimators."""
    from .tasks import _pack, WASHOUT
    rng = np.random.default_rng(seed)
    f, g = kloosterman_pair(n); N = 1 << n
    fh = fwht(f); phi_yes = float(np.dot(g, fh) / N ** 1.5)
    T = WASHOUT + T_train + T_test
    p = np.zeros(T); p[0] = 0.8
    for t in range(1, T):
        p[t] = p[t - 1] + 0.05 * (0.7 - p[t - 1]) + 0.03 * rng.standard_normal()
        if rng.uniform() < 0.02:
            p[t] = rng.uniform(0.3, 1.0)
        p[t] = np.clip(p[t], 0.3, 1.0)
    flips = rng.uniform(size=(T, N)) < ((1 - p) / 2)[:, None]
    phi = np.array([np.dot(np.where(flips[t], -g, g), fh) for t in range(T)]) / N ** 1.5
    out = _pack(f"drift_kloos_n{n}", phi, np.stack([p, phi], 1), T_train, T_test)
    out.update(f=f, g=g, flips=flips, n=n, phi=phi[:out["u"].shape[0]], p=p[:out["u"].shape[0]], phi_yes=phi_yes)
    return out


def mm_pair(n, seed):
    """Maiorana–McFarland bent pair on n = 2k bits from a seed: f(x,y) = (-1)^{x.pi(y) + h(y)}, exact dual
    g(a,b) = (-1)^{b.pi^{-1}(a) + h(pi^{-1}(a))}. Index convention: z = x + 2^k y (x = low k bits)."""
    assert n % 2 == 0
    k = n // 2; K = 1 << k; N = 1 << n
    rng = np.random.default_rng(seed)
    pi = rng.permutation(K); pinv = np.empty(K, dtype=np.int64); pinv[pi] = np.arange(K)
    hb = rng.integers(0, 2, K)
    z = np.arange(N); x = z & (K - 1); y = z >> k
    f = 1.0 - 2.0 * ((_parity(x & pi[y]) ^ hb[y]) & 1)
    a = x; b = y  # (a, b) use the same index convention
    g = 1.0 - 2.0 * ((_parity(b & pinv[a]) ^ hb[pinv[a]]) & 1)
    return f, g


def fresh_pair(task, t):
    """(f_t, g_t) tables of a fresh-pair task step, regenerated from the per-step seed (no persistence)."""
    N = 1 << task["n"]
    if task.get("family") == "mm":
        f, g = mm_pair(task["n"], int(task["fseed"][t]))
    else:
        f = 1.0 - 2.0 * np.random.default_rng(int(task["fseed"][t])).integers(0, 2, N)
        g = np.where(fwht(f) >= 0, 1.0, -1.0)
    return f, g[np.arange(N) ^ int(task["e"][t])]


def classical_estimates(task, variant, Q, rng):
    """Per-step classical estimate of Phi_t from Q oracle queries per step.
    'naive': Phi_hat = sqrt(N) * mean_{i<=Q} f_t(x_i) (-1)^{x_i.y_i} g_t(y_i), unbiased, variance ~ N/Q.
    'pairs': IMPLEMENTED sqrt(N)-query algorithm (Aaronson–Ambainis flavour): query Q/2 random x's and Q/2
             random y's and average f(x_i)(-1)^{x_i.y_j} g(y_j) over ALL Q^2/4 pairs (a U-statistic; the
             (-1)^{x.y} matrix is a bit-matmul, no extra queries). Var(Phi_hat) ≈ 4/Q + 4N/Q^2, so constant
             precision needs Q = Θ(sqrt(N)) queries.
    'opt'  : deprecated optimistic surrogate Phi + N(0, sqrt(N)/Q) (kept for reference only, not reported).
    'knownf': WHITE-BOX: f public (one FWHT, no queries); n+1 queries recover c_t, the rest importance-sample
             g_t at z ~ |f_hat(z)|. Unbiased, variance <= A^2/K, independent of N.
    'anf2' : learn degree-<=2 ANFs of f_t and g_t with anf2_queries(n) queries, verify on ANF2_EXTRA random
             points, and if both verify compute Phi_t exactly from the reconstructed tables (the §4
             dequantisation of quadratic phases); otherwise fall back to 'naive' with the same Q."""
    n, phi = task["n"], task["phi"]
    N = 1 << n; T = len(phi)
    if "fseed" in task:  # fresh random pair per step: only black-box estimators apply
        if variant not in ("naive", "pairs", "anf2"):
            return np.full(T, np.nan)
        out = np.zeros(T)
        for t in range(T):
            ft, gt = fresh_pair(task, t)
            if variant == "anf2":
                ok = True; tabs = []
                for tab_q in (ft, gt):
                    coef = anf2_learn(tab_q, n); tab = anf2_reconstruct(coef, n)
                    xs = rng.integers(0, N, ANF2_EXTRA)
                    if not np.array_equal(tab[xs], tab_q[xs]):
                        ok = False; break
                    tabs.append(tab)
                if ok:
                    out[t] = float(np.dot(tabs[1], fwht(tabs[0])) / N ** 1.5); continue
            if variant == "pairs":
                xs = rng.integers(0, N, Q // 2); ys = rng.integers(0, N, Q - Q // 2)
                sp = np.zeros(N); np.add.at(sp, xs, ft[xs])
                out[t] = np.sqrt(N) * float(np.dot(gt[ys], fwht(sp)[ys])) / (len(xs) * len(ys)); continue
            xs = rng.integers(0, N, Q); ys = rng.integers(0, N, Q)
            out[t] = np.sqrt(N) * np.mean(ft[xs] * (1 - 2 * _parity(xs & ys)) * gt[ys])
        return out
    f, g = task["f"], task["g"]
    if variant == "opt":
        return phi + rng.standard_normal(T) * np.sqrt(np.sqrt(N) / Q)
    bits = np.arange(n)

    def pairs_estimate(fx, gy, xs, ys):
        # sum_{i,j} f_i (-1)^{x_i.y_j} g_j = sum_j g_j * WHT[sparse f on {x_i}](y_j): one N-point FWHT of a
        # Q_x-sparse vector (classical post-processing O(N log N), still only Q queries)
        sp = np.zeros(N); np.add.at(sp, xs, fx)
        return np.sqrt(N) * float(np.dot(gy, fwht(sp)[ys])) / (len(xs) * len(ys))

    if "flips" in task:  # drift task: g_t = g with flipped entries
        flips = task["flips"]; out = np.zeros(T)
        for t in range(T):
            if variant == "wb":  # white-box control: knows the ideal g, samples g_t(y) g(y)
                ys = rng.integers(0, N, Q); out[t] = np.mean(np.where(flips[t, ys], -1.0, 1.0))
            elif variant == "pairs":
                xs = rng.integers(0, N, Q // 2); ys = rng.integers(0, N, Q - Q // 2)
                out[t] = pairs_estimate(f[xs].astype(np.float32), np.where(flips[t, ys], -g[ys], g[ys]).astype(np.float32), xs, ys)
            else:
                xs = rng.integers(0, N, Q); ys = rng.integers(0, N, Q)
                gy = np.where(flips[t, ys], -g[ys], g[ys])
                out[t] = np.sqrt(N) * np.mean(f[xs] * (1 - 2 * _parity(xs & ys)) * gy)
        return out
    c, e = task["c"], task["e"]
    out = np.zeros(T)
    if variant == "knownf":
        # WHITE-BOX estimator: the base function f is public, so f_hat (hence g = sign f_hat) costs no queries
        # (one FWHT per task). Per step: n+1 queries of f_t at 0 and the basis vectors recover c_t exactly
        # (f_t(e_i) f(e_i) = (-1)^{c_i}); the remaining K = Q-(n+1) queries sample z ~ |f_hat(z)| and read
        # g_t(z ^ c_t) = g(z ^ e_t). Phi_hat = A * mean(sign f_hat(z) g_t(z ^ c_t)), A = sum|f_hat| / N^{3/2},
        # is unbiased with variance <= A^2 / K (exact on YES steps). Proposed by the adversarial review panel.
        fh = fwht(f); A = float(np.abs(fh).sum() / N ** 1.5); prob = np.abs(fh) / np.abs(fh).sum(); sgn = np.sign(fh)
        K = max(1, Q - (n + 1))
        for t in range(T):
            zs = rng.choice(N, K, p=prob)
            out[t] = A * np.mean(sgn[zs] * g[zs ^ int(e[t])])  # g_t(z ^ c_t) = g(z ^ c_t ^ c_t ^ e_t)
        return out
    for t in range(T):
        ft = lambda x: f[x] * (1 - 2 * int(_parity(int(x) & int(c[t]))))             # chi_c . f
        gt = lambda y: g[int(y) ^ int(c[t]) ^ int(e[t])]                            # g o tau_{c+e}
        if variant == "anf2":
            ok = True
            tabs = []
            for orc in (ft, gt):
                coef = anf2_learn(None, n, query=orc); tab = anf2_reconstruct(coef, n)
                xs = rng.integers(0, N, ANF2_EXTRA)
                if not all(tab[x] == orc(x) for x in xs):
                    ok = False; break
                tabs.append(tab)
            if ok:
                out[t] = float(np.dot(tabs[1], fwht(tabs[0])) / N ** 1.5); continue
        if variant == "pairs":
            xs = rng.integers(0, N, Q // 2); ys = rng.integers(0, N, Q - Q // 2)
            fx = (f[xs] * (1 - 2 * _parity(xs & int(c[t])))).astype(np.float32); gy = g[ys ^ int(c[t]) ^ int(e[t])].astype(np.float32)
            out[t] = pairs_estimate(fx, gy, xs, ys); continue
        xs = rng.integers(0, N, Q); ys = rng.integers(0, N, Q)
        par = 1 - 2 * _parity(xs & ys)
        fx = f[xs] * (1 - 2 * _parity(xs & int(c[t])))
        gy = g[ys ^ int(c[t]) ^ int(e[t])]
        out[t] = np.sqrt(N) * np.mean(fx * par * gy)
    return out


class ForrelationQRC:
    """Fixed 2-query Forrelation circuit + Hadamard test as an untrained quantum feature map. Per step the
    feature is the acceptance frequency over m shots (mean exactly (1+Phi_t)/2, binomial shot noise). The
    stream p_hat_t then gets the SAME tuned classical readout families (readout_best) as the query-limited
    classical Phi_hat_t streams, so the comparison isolates the feature-extraction stage. Each shot costs 2
    oracle queries; the circuit is memoryless so no washout replay is needed (W = 1). K copies under random
    invariance-group elements have the same mean and are equivalent to K x m shots (K = 1 here)."""
    accepts = "task_shots"

    def __init__(self, seed=0):
        self.seed = seed
        self.F = 1  # one quantum feature per step; readout size is tuned identically for all sides

    def shot_curve_task(self, task, shots):
        from .baselines import readout_best
        rng = np.random.default_rng(self.seed + 99)
        p = (1 + task["phi"]) / 2
        out = {}
        for S in shots:
            p_hat = p if np.isinf(S) else rng.binomial(int(S), np.clip(p, 0, 1)) / S
            out[S] = readout_best(p_hat[:, None], task, self.seed)[0]
        return out
