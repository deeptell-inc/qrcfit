"""Quantum reservoir families, all simulated exactly (density matrix / covariance), returning
(X, V): exact feature expectations X (T,F) and single-shot variances V (T,F) for finite-shot emulation.

Families and the map axes they probe
  SpinReset   : Fujii-Nakajima qubit-reset encoding. Axes: N, Hamiltonian kind (chain = free-fermion /
                integrable, random = interacting), coupling J*tau (frozen / edge / scrambled),
                readout (z | xyz | +zz correlations), time multiplexing V, local dissipation.
  SpinHamEnc  : Hou-style rotation (Hamiltonian) encoding with natural T1/T2 relaxation as fading memory
                and time-multiplexed xyz readout.
  GaussianCV  : linear passive optics with squeezing+displacement encoding, covariance readout
                (Nokkala's Gaussian / linear-bottleneck limit).
  KerrCV      : single driven Kerr mode with loss (chi=0 recovers a Gaussian control).
"""
import numpy as np
from scipy.linalg import expm

I2 = np.eye(2); SX = np.array([[0, 1], [1, 0]], complex); SY = np.array([[0, -1j], [1j, 0]]); SZ = np.diag([1.0, -1.0]).astype(complex)


def _op(single, i, N):
    out = np.array([[1.0 + 0j]])
    for k in range(N):
        out = np.kron(out, single if k == i else I2)
    return out


def ham(N, kind, rng, J=1.0, h=1.0):
    H = sum(h * _op(SZ, i, N) for i in range(N))
    if kind == "chain":  # nearest-neighbour XX + Z field: free fermion (integrable)
        for i in range(N - 1):
            H = H + J * _op(SX, i, N) @ _op(SX, i + 1, N)
    elif kind == "random":  # all-to-all random XX couplings (Fujii-Nakajima), interacting
        Jm = rng.uniform(-1, 1, (N, N)); Jm = np.triu(Jm, 1)
        Jm *= J / np.abs(np.linalg.eigvalsh(Jm + Jm.T)).max()
        for i in range(N):
            for j in range(i + 1, N):
                H = H + Jm[i, j] * _op(SX, i, N) @ _op(SX, j, N)
    elif kind == "chaotic":  # random XX + ZZ + random fields: strongly non-integrable
        for i in range(N):
            for j in range(i + 1, N):
                H = H + rng.uniform(-1, 1) * J / N * (_op(SX, i, N) @ _op(SX, j, N) + _op(SZ, i, N) @ _op(SZ, j, N))
            H = H + rng.uniform(-1, 1) * h * _op(SX, i, N)
    return H


def _local_kraus(rho, Ks, i, N):
    """Apply Kraus ops Ks (list of 2x2) on qubit i of density matrix rho (2^N x 2^N)."""
    t = rho.reshape([2] * (2 * N))
    out = np.zeros_like(t)
    for K in Ks:
        a = np.tensordot(K, t, axes=([1], [i]))            # new axis 0 replaces axis i
        a = np.moveaxis(a, 0, i)
        b = np.tensordot(a, K.conj(), axes=([N + i], [1]))  # contract ket side: rho K^dagger
        b = np.moveaxis(b, -1, N + i)
        out += b
    return out.reshape(rho.shape)


def _relax_kraus(T1, T2, dt):
    """Amplitude damping (T1) composed with pure dephasing so that total coherence decay is 1/T2."""
    g = 1 - np.exp(-dt / T1) if T1 < np.inf else 0.0
    ad = [np.array([[1, 0], [0, np.sqrt(1 - g)]], complex), np.array([[0, np.sqrt(g)], [0, 0]], complex)]
    if T2 < np.inf:
        # pure dephasing rate: 1/T2 - 1/(2 T1)
        gphi = 1 / T2 - (0.5 / T1 if T1 < np.inf else 0)
        p = 0.5 * (1 - np.exp(-gphi * dt)) if gphi > 0 else 0.0  # coherence factor (1-2p)=exp(-gphi dt)
        ph = [np.sqrt(1 - p) * I2.astype(complex), np.sqrt(p) * SZ]
        return [P @ A for A in ad for P in ph]
    return ad


def _weak_kraus(g):
    """Ensemble-averaged channel of a weak Gaussian measurement of sigma_z with strength g in (0,1]:
    dephasing with coherence factor sqrt(1-g^2) (g=1 projective). ponytail: Gaussian-pointer model, no
    conditional trajectories; signal variance per shot is (1-<O>^2) + (1-g^2)/g^2 (Mujal+ 2023 scaling)."""
    c = np.sqrt(1 - g ** 2)
    return [np.sqrt((1 + c) / 2) * I2.astype(complex), np.sqrt((1 - c) / 2) * SZ]


class _SpinBase:
    accepts = "u"

    def __init__(self, N, kind="random", jt=1.0, V=1, readout="z", T1=np.inf, T2=np.inf, seed=0, pm=None, weak=None):
        """weak: measurement strength g of an online weak-measurement readout of every measured qubit (z basis)
        after each sub-step; the readout then needs no experiment restarts (shot-ops S*T instead of S*T*W)."""
        self.weak = weak
        self.Kw = _weak_kraus(weak) if weak else None
        """pm: optional pseudomode dict(g=coupling, T1=damping) — one extra unmeasured, never-reset spin coupled
        by XX to every reservoir spin: an engineered non-Markovian environment (Sannia+ 2026 embedding)."""
        self.N, self.V, self.readout, self.pm = N, V, readout, pm
        rng = np.random.default_rng(seed)
        H = ham(N, kind, rng)
        Nt = N + (1 if pm else 0)
        self.Nt = Nt
        if pm:
            H = np.kron(H, I2) + sum(pm["g"] * _op(SX, i, Nt) @ _op(SX, N, Nt) for i in range(N)) + _op(SZ, N, Nt)
            self.Ks_pm = _relax_kraus(pm["T1"], np.inf, jt / V)
        self.U = expm(-1j * H * jt / V)
        self.obs = []
        self.obs_names = []
        for i in range(N):
            pauli = {"z": [("z", SZ)], "xyz": [("x", SX), ("y", SY), ("z", SZ)]}[readout.replace("+zz", "")]
            for nm, P in pauli:
                self.obs.append(_op(P, i, Nt)); self.obs_names.append(f"{nm}{i}")
        if readout.endswith("+zz"):
            for i in range(N):
                for j in range(i + 1, N):
                    self.obs.append(_op(SZ, i, Nt) @ _op(SZ, j, Nt)); self.obs_names.append(f"zz{i}{j}")
        self.obsT = np.array([o.T for o in self.obs])  # Tr(rho O) = sum(rho * O.T)
        self.Ks = _relax_kraus(T1, T2, jt / V) if (T1 < np.inf or T2 < np.inf) else None
        self.P = None
        if self.Ks is not None and N <= 4 and not pm:  # exact for small N; Trotter-Kraus (faster) above
            # exact Lindblad propagator on the 4^N Liouville space (no Trotter split between H and relaxation)
            d = 2 ** N; Id = np.eye(d)
            L = -1j * (np.kron(Id, H) - np.kron(H.T, Id))
            g1 = 1 / T1 if T1 < np.inf else 0.0
            gphi = (1 / T2 - 0.5 * g1) if T2 < np.inf else 0.0
            sm = np.array([[0, 1], [0, 0]], complex)  # |0><1| : decay to |0> (the +1 eigenstate of sigma_z)
            for i in range(N):
                for rate, A in [(g1, _op(sm, i, N)), (max(gphi, 0) / 2, _op(SZ, i, N))]:
                    if rate > 0:
                        AdA = A.conj().T @ A
                        L = L + rate * (np.kron(A.conj(), A) - 0.5 * np.kron(Id, AdA) - 0.5 * np.kron(AdA.T, Id))
            self.P = expm(L * jt / V)
        self.F = len(self.obs) * V

    def _measure(self, rho):
        e = np.real(np.einsum("ij,kij->k", rho, self.obsT))
        var = 1 - e ** 2  # Pauli single-shot variance
        if self.weak:
            var = var + (1 - self.weak ** 2) / self.weak ** 2
        return e, var

    def _evolve(self, rho):
        if self.P is not None:
            d = rho.shape[0]
            return (self.P @ rho.reshape(-1, order="F")).reshape(d, d, order="F")
        rho = self.U @ rho @ self.U.conj().T
        if self.Ks is not None:
            for i in range(self.N):
                rho = _local_kraus(rho, self.Ks, i, self.Nt)
        if self.pm:
            rho = _local_kraus(rho, self.Ks_pm, self.N, self.Nt)
        if self.Kw is not None:  # measurement back-action on every measured qubit
            for i in range(self.N):
                rho = _local_kraus(rho, self.Kw, i, self.Nt)
        return rho

    def run(self, u, rho_seq=None):
        T = len(u); d = 2 ** self.Nt
        rho = np.zeros((d, d), complex); rho[0, 0] = 1
        X = np.zeros((T, self.F)); Vv = np.zeros((T, self.F))
        for t in range(T):
            rho = self._encode(rho, u[t] if rho_seq is None else rho_seq[t])
            for v in range(self.V):
                rho = self._evolve(rho)
                e, var = self._measure(rho)
                k = len(self.obs)
                X[t, v * k:(v + 1) * k] = e; Vv[t, v * k:(v + 1) * k] = var
        return X, Vv


class SpinReset(_SpinBase):
    """Qubit-reset encoding: rho -> |psi_u><psi_u| (x) Tr_0 rho, |psi_u> = sqrt(1-u)|0> + sqrt(u)|1>."""

    def _encode(self, rho, u):
        u = float(np.clip(np.mean(u), 0, 1))
        N = self.Nt
        t = rho.reshape([2] * (2 * N))
        red = np.trace(t, axis1=0, axis2=N)  # partial trace over qubit 0
        psi = np.array([np.sqrt(1 - u), np.sqrt(u)], complex)
        pp = np.outer(psi, psi.conj())
        new = np.einsum("ab,...->ab...", pp, red)  # indices: a, b, rest_bra..., rest_ket...
        # reorder to (a, rest_bra..., b, rest_ket...)
        new = np.moveaxis(new, 1, N)
        return new.reshape(rho.shape)


class SpinQInput(_SpinBase):
    """Quantum-input reservoir: the 2-qubit input state replaces reservoir qubits 0,1 each step
    (rho -> rho_in (x) Tr_{01} rho); the remaining N-2 qubits carry memory. Readout on all N qubits.
    hybrid=True appends a fixed classical ESN(100) driven by the quantum features (Coll-Comas+ 2026 HRC):
    the only way a linear readout can reach functionals nonlinear in a single input state (purity, negativity)."""
    accepts = "rho"

    def __init__(self, *a, hybrid=False, **k):
        super().__init__(*a, **k)
        self.hybrid = hybrid
        if hybrid:
            self.F += 100

    def run(self, u, rho_seq=None):
        X, V = super().run(u, rho_seq)
        if not self.hybrid:
            return X, V
        from .baselines import esn_features
        Xs = (X - X.mean(0)) / np.maximum(X.std(0), 1e-10)
        E = esn_features(Xs, 100, 0.9, 0.3, 0.5, 0)
        # ponytail: shot noise on ESN-post-processed features approximated by the mean input-feature variance
        return np.hstack([X, E]), np.hstack([V, np.full(E.shape, V.mean())])

    def _encode(self, rho, rho_in):
        N = self.Nt
        t = rho.reshape([2] * (2 * N))
        red = np.trace(t, axis1=0, axis2=N)
        red = np.trace(red, axis1=0, axis2=N - 1)
        return np.kron(rho_in, red.reshape(2 ** (N - 2), 2 ** (N - 2)))


class SpinHamEnc(_SpinBase):
    """Hou-style encoding: global y-rotation by angle pi*u on every spin (multi-input: spin i gets input i mod d)."""

    def __init__(self, *a, amp=np.pi, **k):
        super().__init__(*a, **k)
        self.amp = amp
        self._cache = {}

    def _encode(self, rho, u):
        u = np.atleast_1d(u)
        key = tuple(np.round(u, 3))
        if key not in self._cache:
            Ug = np.array([[1.0 + 0j]])
            for i in range(self.N):
                th = self.amp * float(u[i % len(u)])
                Ug = np.kron(Ug, expm(-0.5j * th * SY))
            self._cache[key] = Ug
        Ug = self._cache[key]
        return Ug @ rho @ Ug.conj().T


class GaussianCV:
    """N-mode Gaussian reservoir. Per step: mode 0 is re-prepared (traced out and replaced) in a
    squeezed-displaced state set by the input, then a fixed random passive interferometer mixes all
    modes and uniform loss eta provides fading memory. Readout: all first moments and second moments."""

    def __init__(self, N=8, eta=0.8, r0=1.0, d0=2.0, seed=0, readout="cov"):
        rng = np.random.default_rng(seed)
        self.N, self.eta, self.r0, self.d0 = N, eta, r0, d0
        A = rng.standard_normal((N, N)); Q, _ = np.linalg.qr(A + 1j * rng.standard_normal((N, N)))
        self.S = np.block([[Q.real, -Q.imag], [Q.imag, Q.real]])  # passive symplectic
        self.readout = readout
        iu = np.triu_indices(2 * N)
        self.iu = iu
        self.F = 2 * N + len(iu[0])

    def run(self, u):
        N = self.N; T = len(u)
        m = np.zeros(2 * N); Vm = np.eye(2 * N)
        X = np.zeros((T, self.F)); Var = np.zeros((T, self.F))
        for t in range(T):
            x = float(np.clip(np.mean(u[t]), 0, 1))
            # replace mode 0 by a fresh squeezed displaced state
            r = self.r0 * (x - 0.5); d = self.d0 * x
            m[[0, N]] = [d, 0.0]
            Vm[0, :] = 0; Vm[:, 0] = 0; Vm[N, :] = 0; Vm[:, N] = 0
            Vm[0, 0] = np.exp(-2 * r); Vm[N, N] = np.exp(2 * r)
            m = self.S @ m; Vm = self.S @ Vm @ self.S.T
            m = np.sqrt(self.eta) * m; Vm = self.eta * Vm + (1 - self.eta) * np.eye(2 * N)
            sec = Vm + np.outer(m, m)  # second moments <q_i q_j>
            X[t, :2 * N] = m; X[t, 2 * N:] = sec[self.iu]
            dv = np.diag(Vm)
            Var[t, :2 * N] = dv
            Var[t, 2 * N:] = (dv[self.iu[0]] * dv[self.iu[1]] + Vm[self.iu] ** 2
                              + dv[self.iu[0]] * m[self.iu[1]] ** 2 + dv[self.iu[1]] * m[self.iu[0]] ** 2)
        return X, Var


class KerrCV:
    """Single driven Kerr mode, H = chi a^dag^2 a^2 + i eps(u) (a^dag - a), loss kappa. Exact Lindblad via
    precomputed propagators on a quantized input grid. Readout at V sub-times: <x>,<p>,<n>,<n^2>."""

    def __init__(self, chi=0.5, kappa=0.3, eps0=1.5, tau=1.0, V=1, dim=20, levels=32, seed=0):
        self.V, self.dim, self.levels = V, dim, levels
        a = np.diag(np.sqrt(np.arange(1, dim)), 1)
        ad = a.T
        n = ad @ a
        x = (a + ad) / np.sqrt(2); p = (a - ad) / (1j * np.sqrt(2))
        self.obs = [x, p, n, n @ n]
        self.obs2 = [x @ x, p @ p, n @ n, n @ n @ n @ n]
        self.obsT = np.array([o.T for o in self.obs]); self.obs2T = np.array([o.T for o in self.obs2])
        Id = np.eye(dim)
        D = np.kron(a.conj(), a) - 0.5 * np.kron(Id, n) - 0.5 * np.kron(n.T, Id)  # vec(rho) column-stacking: vec(A rho B) = (B^T kron A) vec(rho)
        self.props = []
        for lv in range(levels):
            eps = eps0 * lv / (levels - 1)
            H = chi * ad @ ad @ a @ a + 1j * eps * (ad - a)
            L = -1j * (np.kron(Id, H) - np.kron(H.T, Id)) + kappa * D
            self.props.append(expm(L * tau / V))
        self.F = 4 * V

    def run(self, u):
        T = len(u); d = self.dim
        rho = np.zeros((d, d), complex); rho[0, 0] = 1
        X = np.zeros((T, self.F)); Var = np.zeros((T, self.F))
        for t in range(T):
            lv = int(round(float(np.clip(np.mean(u[t]), 0, 1)) * (self.levels - 1)))
            P = self.props[lv]
            for v in range(self.V):
                rho = (P @ rho.reshape(-1, order="F")).reshape(d, d, order="F")
                e = np.real(np.einsum("ij,kij->k", rho, self.obsT))
                e2 = np.real(np.einsum("ij,kij->k", rho, self.obs2T))
                X[t, 4 * v:4 * v + 4] = e; Var[t, 4 * v:4 * v + 4] = np.maximum(e2 - e ** 2, 0)
        return X, Var


class KerrDelayQ:
    """Quantum Kerr delay-line reservoir with feedback depth set by the round-trip loss (Soh 2026 geometry).
    D pulses circulate in a loop; each pass through the single Kerr element applies, to that pulse alone,
    the exact single-mode Lindblad map  Kerr(chi) + loss(kappa) + coherent drive eps0*u_t*mask_j  for one
    round-trip time. Pulses never overlap, so the state is D independent single-mode density matrices; the
    ring shift (pulse in slot j came from slot j-1) is the standard virtual-node coupling. Loss eta=exp(-kappa)
    per pass gives depth D_eff ~ 1/(1-eta). Readout <x>,<p>,<n> per pulse: the same three features per
    virtual node as the semiclassical kerr_delay baseline, so the two are compared at equal readout cost."""
    accepts = "u"

    def __init__(self, D=30, chi=0.3, kappa=0.05, eps0=0.5, dim=16, levels=33, seed=0):
        rng = np.random.default_rng(seed)
        self.D, self.dim, self.levels = D, dim, levels
        self.mask = rng.uniform(-1, 1, D)
        a = np.diag(np.sqrt(np.arange(1, dim)), 1); ad = a.T; n = ad @ a; Id = np.eye(dim)
        x = (a + ad) / np.sqrt(2); p = (a - ad) / (1j * np.sqrt(2))
        self.obs = [x, p, n]; self.obs2 = [x @ x, p @ p, n @ n]
        self.obsT = np.array([o.T for o in self.obs]); self.obs2T = np.array([o.T for o in self.obs2])
        Dis = np.kron(a.conj(), a) - 0.5 * np.kron(Id, n) - 0.5 * np.kron(n.T, Id)
        self.grid = np.linspace(-eps0, eps0, levels)  # signed drive: mask*u in [-1,1]*eps0
        self.props = []
        for eps in self.grid:
            H = chi * ad @ ad @ a @ a + 1j * eps * (ad - a)
            L = -1j * (np.kron(Id, H) - np.kron(H.T, Id)) + kappa * Dis
            self.props.append(expm(L))
        self.F = 3 * D

    def run(self, u):
        T = len(u); d = self.dim; D = self.D
        vec = np.zeros((D, d * d), complex); vec[:, 0] = 1  # vacuum in every slot (vec index 0 = |0><0|)
        X = np.zeros((T, self.F)); Var = np.zeros((T, self.F))
        for t in range(T):
            inp = float(np.clip(np.mean(u[t]), 0, 1))
            vec = np.roll(vec, 1, axis=0)  # ring shift of the circulating pulses
            for j in range(D):
                lv = int(round((inp * self.mask[j] + 1) / 2 * (self.levels - 1)))
                vec[j] = self.props[lv] @ vec[j]
            rho = vec.reshape(D, d, d).transpose(0, 2, 1)  # column-stacking vec -> matrix
            e = np.real(np.einsum("jik,oik->jo", rho, self.obsT)); e2 = np.real(np.einsum("jik,oik->jo", rho, self.obs2T))
            X[t] = e.reshape(-1); Var[t] = np.maximum(e2 - e ** 2, 0).reshape(-1)
        return X, Var


class TunedKerrDelayQ:
    """Quantum Kerr delay line with (chi, kappa, eps0) chosen per task by the same 20-draw random search and
    validation selection the classical baselines get (equal tuning effort). Needs the task, not just u."""
    accepts = "task"

    def __init__(self, D=30, budget=20, seed=0):
        self.D, self.budget, self.seed = D, budget, seed
        self.F = 3 * D

    def run_task(self, task):
        from .evaluate import val_test
        rng = np.random.default_rng(self.seed + 777)
        best = (np.inf, None)
        for b in range(self.budget):
            chi, kappa, eps0 = 10 ** rng.uniform(-1.5, 0.5), 10 ** rng.uniform(-1.7, -0.3), 10 ** rng.uniform(-0.7, 0.3)
            R = KerrDelayQ(D=self.D, chi=chi, kappa=kappa, eps0=eps0, dim=16, seed=self.seed * 100 + b)
            X, V = R.run(task["u"])
            if not np.all(np.isfinite(X)) or X[:, 2::3].max() > 9:
                continue
            val = val_test(X, task)[0]
            if val < best[0]:
                best = (val, (X, V))
        return best[1]


class TwoModeCV:
    """Two bosonic modes a -> b, exact Lindblad in truncated Fock space (dim D each) propagated with sparse
    expm_multiply. Mode a is driven by eps(u); 'cascade' coupling is the unidirectional Carmichael/Gardiner
    master equation (quantum stand-in for Soh's Kerr feedback with depth 2), 'bs' is a beam splitter.
    chi=0 gives Gaussian dynamics; readout 'moments' (x,p,n,n^2 per mode) vs 'fock' (joint photon-number
    probabilities P(na,nb), na,nb<nmax: a non-Gaussian measurement of the same state)."""
    accepts = "u"

    def __init__(self, chi=0.5, kappa=0.3, g=0.3, eps0=1.5, tau=1.0, V=1, dim=8, levels=32, coupling="cascade",
                 readout="moments", nmax=4, seed=0):
        import scipy.sparse as sp
        self.V, self.dim, self.levels, self.readout = V, dim, levels, readout
        a1 = np.diag(np.sqrt(np.arange(1, dim)), 1); Id = np.eye(dim)
        a = np.kron(a1, Id); b = np.kron(Id, a1)
        D2 = dim * dim; I2m = np.eye(D2)
        na, nb = a.T @ a, b.T @ b
        H0 = chi * (a.T @ a.T @ a @ a + b.T @ b.T @ b @ b)
        def lind(A, rate):
            AdA = A.conj().T @ A
            return rate * (np.kron(A.conj(), A) - 0.5 * np.kron(I2m, AdA) - 0.5 * np.kron(AdA.T, I2m))
        L0 = -1j * (np.kron(I2m, H0) - np.kron(H0.T, I2m)) + lind(a, kappa) + lind(b, kappa)
        if coupling == "cascade":
            c1, c2 = a, b; k = kappa
            L0 = L0 - k * (np.kron(I2m, c2.conj().T @ c1) - np.kron(c2.conj(), c1)
                           + np.kron((c1.conj().T @ c2).T, I2m) - np.kron(c1.conj(), c2))
        else:
            Hc = g * (a.T @ b + b.T @ a)
            L0 = L0 - 1j * (np.kron(I2m, Hc) - np.kron(Hc.T, I2m))
        Hd = 1j * (a.T - a)  # drive generator, multiplied by eps(u)
        Ld = -1j * (np.kron(I2m, Hd) - np.kron(Hd.T, I2m))
        self.L0 = sp.csr_matrix(L0 * tau / V); self.Ld = sp.csr_matrix(Ld * tau / V); self.eps0 = eps0
        x = (a + a.T) / np.sqrt(2); pa = (a - a.T) / (1j * np.sqrt(2)); xb = (b + b.T) / np.sqrt(2); pb = (b - b.T) / (1j * np.sqrt(2))
        if readout == "moments":
            self.obs = [x, pa, na, na @ na, xb, pb, nb, nb @ nb]
            self.obs2 = [o @ o for o in self.obs]
        else:
            idx = [i * dim + j for i in range(nmax) for j in range(nmax)]
            self.obs = [np.diag((np.arange(D2) == k).astype(complex)) for k in idx]
            self.obs2 = self.obs  # projectors: P^2 = P
        self.obsT = np.array([o.T for o in self.obs]); self.obs2T = np.array([o.T for o in self.obs2])
        self.F = len(self.obs) * V

    def run(self, u):
        from scipy.sparse.linalg import expm_multiply
        T = len(u); d = self.dim ** 2
        rho = np.zeros((d, d), complex); rho[0, 0] = 1
        X = np.zeros((T, self.F)); Var = np.zeros((T, self.F)); k = len(self.obs)
        vec = rho.reshape(-1, order="F")
        for t in range(T):
            lv = round(float(np.clip(np.mean(u[t]), 0, 1)) * (self.levels - 1)) / (self.levels - 1)
            L = self.L0 + (self.eps0 * lv) * self.Ld
            for v in range(self.V):
                vec = expm_multiply(L, vec)
                rho = vec.reshape(d, d, order="F")
                e = np.real(np.einsum("ij,kij->k", rho, self.obsT)); e2 = np.real(np.einsum("ij,kij->k", rho, self.obs2T))
                X[t, k * v:k * (v + 1)] = e; Var[t, k * v:k * (v + 1)] = np.maximum(e2 - e ** 2, 0)
        return X, Var


def quantum_configs(quick=False):
    """The enumerated quantum map axis. name -> factory(seed)."""
    C = {}
    Ns = [4, 6] if quick else [4, 6, 8]
    for N in Ns:
        C[f"spin_reset_chain_N{N}_z"] = lambda s, N=N: SpinReset(N, "chain", 1.0, 1, "z", seed=s)
        C[f"spin_reset_rand_N{N}_z"] = lambda s, N=N: SpinReset(N, "random", 1.0, 1, "z", seed=s)
    N = 6
    for jt, tag in [(0.1, "frozen"), (1.0, "edge"), (10.0, "scrambled")]:
        C[f"spin_reset_rand_N6_z_{tag}"] = lambda s, jt=jt: SpinReset(N, "random", jt, 1, "z", seed=s)
    C["spin_reset_chaotic_N6_z"] = lambda s: SpinReset(N, "chaotic", 1.0, 1, "z", seed=s)
    C["spin_reset_rand_N6_zz"] = lambda s: SpinReset(N, "random", 1.0, 1, "z+zz", seed=s)
    C["spin_reset_rand_N6_xyz"] = lambda s: SpinReset(N, "random", 1.0, 1, "xyz", seed=s)
    C["spin_reset_rand_N6_z_V5"] = lambda s: SpinReset(N, "random", 1.0, 5, "z", seed=s)
    C["spin_reset_rand_N6_z_T1"] = lambda s: SpinReset(N, "random", 1.0, 1, "z", T1=5.0, T2=5.0, seed=s)
    C["spin_hamenc_rand_N6_xyz_V5"] = lambda s: SpinHamEnc(N, "random", 1.0, 5, "xyz", T1=3.0, T2=2.0, seed=s)
    C["spin_hamenc_chain_N6_xyz_V5"] = lambda s: SpinHamEnc(N, "chain", 1.0, 5, "xyz", T1=3.0, T2=2.0, seed=s)
    C["spin_hamenc_rand_N6_xyz_V5_noT"] = lambda s: SpinHamEnc(N, "random", 1.0, 5, "xyz", seed=s)
    C["spin_hamenc_rand_N6_xyz_V10_weakT"] = lambda s: SpinHamEnc(N, "random", 1.0, 10, "xyz", T1=30.0, T2=10.0, amp=np.pi / 4, seed=s)
    C["spin_hamenc_rand_N6_xyz_V10_weakT_amp1"] = lambda s: SpinHamEnc(N, "random", 1.0, 10, "xyz", T1=30.0, T2=10.0, amp=np.pi, seed=s)
    C["spin_reset_rand_N6_z_V10"] = lambda s: SpinReset(N, "random", 1.0, 10, "z", seed=s)
    C["spin_reset_rand_N6_zz_V10"] = lambda s: SpinReset(N, "random", 1.0, 10, "z+zz", seed=s)
    C["cv_gauss_N4"] = lambda s: GaussianCV(4, seed=s)
    C["cv_gauss_N12"] = lambda s: GaussianCV(12, seed=s)
    C["cv_kerr_chi0"] = lambda s: KerrCV(chi=0.0, seed=s)
    C["cv_kerr_chi0.3"] = lambda s: KerrCV(chi=0.3, seed=s)
    C["cv_kerr_chi1_V4"] = lambda s: KerrCV(chi=1.0, V=4, seed=s)
    # ---- wave 2
    C["spin_reset_rand_N6_z_pm"] = lambda s: SpinReset(N, "random", 1.0, 1, "z", seed=s, pm=dict(g=0.5, T1=5.0))
    C["spin_reset_rand_N6_zz_pm"] = lambda s: SpinReset(N, "random", 1.0, 1, "z+zz", seed=s, pm=dict(g=0.5, T1=5.0))
    C["spin_reset_rand_N6_z_pm_slow"] = lambda s: SpinReset(N, "random", 1.0, 1, "z", seed=s, pm=dict(g=0.5, T1=50.0))
    C["spin_qin_rand_N6_zz"] = lambda s: SpinQInput(N, "random", 1.0, 1, "z+zz", seed=s)
    C["spin_qin_rand_N6_xyz_V5"] = lambda s: SpinQInput(N, "random", 1.0, 5, "xyz", seed=s)
    C["spin_qin_rand_N6_zz_T1"] = lambda s: SpinQInput(N, "random", 1.0, 1, "z+zz", T1=5.0, T2=5.0, seed=s)
    C["spin_qin_rand_N6_zz_hybrid"] = lambda s: SpinQInput(N, "random", 1.0, 1, "z+zz", seed=s, hybrid=True)
    C["cv2_cascade_kerr0.5_moments"] = lambda s: TwoModeCV(chi=0.5, coupling="cascade", readout="moments", seed=s)
    C["cv2_cascade_kerr0.5_fock"] = lambda s: TwoModeCV(chi=0.5, coupling="cascade", readout="fock", seed=s)
    C["cv2_cascade_chi0_moments"] = lambda s: TwoModeCV(chi=0.0, coupling="cascade", readout="moments", seed=s)
    C["cv2_cascade_chi0_fock"] = lambda s: TwoModeCV(chi=0.0, coupling="cascade", readout="fock", seed=s)
    C["cv2_bs_chi0_fock"] = lambda s: TwoModeCV(chi=0.0, coupling="bs", readout="fock", seed=s)
    if not quick:
        C["spin_reset_rand_N10_zz"] = lambda s: SpinReset(10, "random", 1.0, 1, "z+zz", seed=s)
    # ---- wave 3
    for Dd in (30, 100):
        C[f"qkerr_delay_D{Dd}_chi0.3"] = lambda s, Dd=Dd: KerrDelayQ(D=Dd, chi=0.3, kappa=0.05, eps0=0.5, seed=s)
        C[f"qkerr_delay_D{Dd}_chi1"] = lambda s, Dd=Dd: KerrDelayQ(D=Dd, chi=1.0, kappa=0.05, eps0=0.5, seed=s)
        C[f"qkerr_delay_D{Dd}_chi0"] = lambda s, Dd=Dd: KerrDelayQ(D=Dd, chi=0.0, kappa=0.05, eps0=0.5, seed=s)
    C["qkerr_delay_D30_chi0.3_bright"] = lambda s: KerrDelayQ(D=30, chi=0.1, kappa=0.05, eps0=1.5, dim=24, seed=s)
    C["qkerr_delay_D30_chi1_lossy"] = lambda s: KerrDelayQ(D=30, chi=1.0, kappa=0.3, eps0=0.5, seed=s)
    for g in (0.1, 0.3, 0.6):
        C[f"spin_reset_rand_N6_zz_weak{g}"] = lambda s, g=g: SpinReset(N, "random", 1.0, 1, "z+zz", seed=s, weak=g)
        C[f"spin_reset_rand_N6_z_weak{g}"] = lambda s, g=g: SpinReset(N, "random", 1.0, 1, "z", seed=s, weak=g)
    C["spin_qin_rand_N6_zz_weak0.3"] = lambda s: SpinQInput(N, "random", 1.0, 1, "z+zz", seed=s, weak=0.3)
    from .forrelation import ForrelationQRC
    C["forr_qrc"] = lambda s: ForrelationQRC(seed=s)
    C["qkerr_delay_D30_tuned"] = lambda s: TunedKerrDelayQ(D=30, seed=s)
    C["qkerr_delay_D100_tuned"] = lambda s: TunedKerrDelayQ(D=100, seed=s)
    return C
