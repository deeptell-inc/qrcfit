"""Physical-unit conversion of the map's dimensionless parameters for the experimental-feasibility section.
All values are ESTIMATES derived from the stated reference frequencies (not measured); asserts guard the arithmetic.
Writes paper/feasibility_units.json. Sources for the reference numbers are the manuscript's own references
(superconducting QRC: senanian2024, yasuda2023; NMR: hou2026; delay-line RC: appeltant2011)."""
import json, math, os
out = {}
# --- spin reservoirs: J*tau = 1 per step (H = h sigma_z + J XX, U = exp(-i H J tau)); tau = (J tau)/J
for name, J_over_2pi_Hz in [("superconducting_qubits", 10e6), ("nmr_spins", 100.0)]:
    J = 2 * math.pi * J_over_2pi_Hz
    tau = 1.0 / J  # J tau = 1
    out[name] = dict(J_over_2pi_Hz=J_over_2pi_Hz, step_time_s=tau, T1_5_steps_s=5 * tau, T1_3_steps_s=3 * tau,
                     per_step_decay_at_T1_100us=1 - math.exp(-tau / 100e-6), per_step_decay_at_T1_1s=1 - math.exp(-tau / 1.0))
assert abs(out["superconducting_qubits"]["step_time_s"] - 15.9e-9) < 0.2e-9
assert abs(out["nmr_spins"]["step_time_s"] - 1.59e-3) < 0.02e-3
# --- shot budget: 3e5 shot-ops per step; projective W = 30 replays of S = 1e4 shots, or online W = 1 with S = 1e5
T_steps = 1600  # washout 100 + train 1000 + test 500 (qrcfit/tasks.py)
for name, cycle_s in [("superconducting_1us_cycle", 1e-6), ("nmr_1s_cycle", 1.0)]:
    per_step = 3e5 * cycle_s
    out[f"budget_{name}"] = dict(shot_cycle_s=cycle_s, wallclock_per_step_s=per_step, wallclock_per_task_s=per_step * T_steps,
                                 wallclock_per_task_at_S1e6_W30_s=1e6 * 30 * cycle_s * T_steps)
assert abs(out["budget_superconducting_1us_cycle"]["wallclock_per_task_s"] - 480) < 1
assert abs(out["budget_superconducting_1us_cycle"]["wallclock_per_task_at_S1e6_W30_s"] / 3600 - 13.33) < 0.01
# --- quantum Kerr delay line: chi = 0.3, kappa = 0.05 per round trip (H = chi a^dag^2 a^2, loss kappa, drive eps0 = 0.5)
for name, K_over_2pi_Hz in [("superconducting_kerr_resonator", 1e6)]:
    K = 2 * math.pi * K_over_2pi_Hz
    tau_rt = 0.3 / K                      # chi = K * tau_rt = 0.3
    kappa = 0.05 / tau_rt                 # kappa * tau_rt = 0.05
    out[name] = dict(K_over_2pi_Hz=K_over_2pi_Hz, round_trip_s=tau_rt, kappa_over_2pi_Hz=kappa / (2 * math.pi),
                     Q_at_5GHz=5e9 / (kappa / (2 * math.pi)), loop_time_D100_s=100 * tau_rt, loop_time_D30_s=30 * tau_rt,
                     drive_eps0_over_2pi_Hz=0.5 / tau_rt / (2 * math.pi), mean_photons=(1.2, 1.6))
assert abs(out["superconducting_kerr_resonator"]["round_trip_s"] - 47.7e-9) < 0.2e-9
assert abs(out["superconducting_kerr_resonator"]["kappa_over_2pi_Hz"] - 167e3) < 2e3
# --- Forrelation circuit: n+1 qubits (control for the Hadamard test) or n qubits with the |0^n> test; 2 oracle calls per shot
for n in (10, 16, 20):
    out[f"forrelation_n{n}"] = dict(qubits_hadamard_test=n + 1, qubits_zero_test=n, oracle_calls_per_step_m100=200, hadamard_layers=3,
                                    shots_per_step_m100=100, phi_squared_YES_random=0.798 ** 2, phi_squared_YES_mm=1.0)
assert abs(out["forrelation_n16"]["phi_squared_YES_random"] - 0.637) < 0.001
json.dump(out, open(os.path.join(os.path.dirname(__file__), "..", "paper", "feasibility_units.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
