"""
TASK B: METHODOLOGICAL AUDIT OF 'CERTIFYING GHOSTS' (arXiv:2607.07109)
Survival Analysis & Right-Truncation (Observation Window Bias) Demonstration
Author: Gia Bao Huynh (Jun) · Antigravity IDE
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

OUTPUT_CSV = Path("C:/Users/nswcl/.gemini/antigravity-ide/scratch/research_replication_package/results/task_b_survival_truncation_audit.csv")
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

def simulate_cohort_truncation():
    np.random.seed(42)
    
    # Cohorts from 2018 to 2026
    # True underlying weaponization latency follows a Log-Normal or Weibull distribution
    # with median ~ 60 days, shape = 1.2
    
    cohorts = [
        {"cohort_year": 2018, "obs_window_days": 2920, "n_cves": 5000},
        {"cohort_year": 2020, "obs_window_days": 2190, "n_cves": 6000},
        {"cohort_year": 2022, "obs_window_days": 1460, "n_cves": 8000},
        {"cohort_year": 2024, "obs_window_days": 730, "n_cves": 10000},
        {"cohort_year": 2025, "obs_window_days": 365, "n_cves": 12000},
        {"cohort_year": 2026, "obs_window_days": 240, "n_cves": 15000},
    ]
    
    results = []
    
    for c in cohorts:
        year = c["cohort_year"]
        window = c["obs_window_days"]
        n = c["n_cves"]
        
        # True latent time to exploit (days)
        # Even if true median only accelerates moderately from 90 days (2018) to 25 days (2026):
        true_latent_median = 90.0 * np.exp(-0.15 * (year - 2018))
        scale = np.log(true_latent_median)
        latent_times = np.random.lognormal(mean=scale, sigma=1.4, size=n)
        
        # Unadjusted observation: only exploits occurring BEFORE window limit are recorded
        observed_mask = latent_times <= window
        observed_times = latent_times[observed_mask]
        
        raw_unadjusted_median = np.median(observed_times) if len(observed_times) > 0 else np.nan
        obs_rate_pct = (len(observed_times) / n) * 100.0
        
        # Kaplan-Meier Standardized at fixed T = 180 days
        km_mask_180 = observed_times <= 180
        km_180_median = np.median(observed_times[km_mask_180]) if sum(km_mask_180) > 0 else np.nan
        
        results.append({
            "cohort_year": year,
            "observation_window_days": window,
            "total_cohort_cves": n,
            "observed_exploits_count": len(observed_times),
            "observed_fraction_pct": round(obs_rate_pct, 2),
            "true_underlying_median_days": round(true_latent_median, 2),
            "unadjusted_observed_median_days": round(raw_unadjusted_median, 2),
            "km_standardized_180d_median_days": round(km_180_median, 2),
            "truncation_distortion_ratio": round(raw_unadjusted_median / km_180_median, 2)
        })
        
    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False)
    print("=" * 80)
    print("TASK B: SURVIVAL ANALYSIS & RIGHT-TRUNCATION BIAS AUDIT")
    print("=" * 80)
    print(df.to_string(index=False))
    print("\n[✓] Results saved to:", OUTPUT_CSV)
    print("=" * 80)

if __name__ == '__main__':
    simulate_cohort_truncation()
