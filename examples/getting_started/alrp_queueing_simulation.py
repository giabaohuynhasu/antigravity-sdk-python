"""
Example: ALRP Queueing Instability & Longevity Divergence Simulation
Demonstrates the use of google.antigravity.science computational models.
"""

import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

from google.antigravity import QueueingModel, LongevitySimulator

# 1. Initialize Queueing Model with Empirical Parameters
qm = QueueingModel(
    lambda_0=0.015,  # 0.015 discoveries/day
    alpha=0.18,      # 18% annual autonomous acceleration
    mu=0.052         # 0.052 patches/day (MTTR ~19 days)
)

t_star = qm.critical_horizon()
print("=" * 65)
print("📊 ALRP QUEUEING INSTABILITY COMPUTATION")
print("=" * 65)
print(f"Initial Arrival Rate lambda(0) : {qm.arrival_rate(0):.4f} items/day")
print(f"Service Remediation Rate mu     : {qm.mu:.4f} items/day")
print(f"Critical Transition Horizon t*  : {t_star:.2f} years")
print("-" * 65)
print(f"{'Year (t)':<10} | {'Arrival lambda(t)':<18} | {'Traffic Intensity rho(t)':<25} | {'Workload W(t)':<15}")
print("-" * 65)

for t in [0.0, 2.0, 4.0, 6.0, 6.9, 7.0]:
    lam = qm.arrival_rate(t)
    rho = qm.traffic_intensity(t)
    w = qm.expected_workload(t)
    w_str = f"{w:.2f} days" if w != float("inf") else "DIVERGENT (inf)"
    print(f"{t:<10.1f} | {lam:<18.4f} | {rho:<25.4f} | {w_str:<15}")

print("\n" + "=" * 65)
print("🧬 GOMPERTZ-MAKEHAM LONGEVITY ASYMMETRY HAZARD RATES")
print("=" * 65)
for age in [30, 50, 70, 90, 110]:
    h = LongevitySimulator.hazard_rate(age)
    s = LongevitySimulator.survival_probability(age)
    print(f"Age {age:3d} -> Mortality Hazard h(x): {h:.6f} | Survival Prob S(x): {s*100:.2f}%")
print("=" * 65)
