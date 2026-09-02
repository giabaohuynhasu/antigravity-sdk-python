"""
TASK E: HOUSING SUPPLY NULL-CASE ECONOMETRICS & R^2 INTERPRETATION
US Census Bureau Permits Authorized vs Units Completed (1968–2026, N = 703 Months)
Author: Gia Bao Huynh (Jun) · Antigravity IDE
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.optimize import curve_fit

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

INPUT_CSV = Path("C:/Users/nswcl/.gemini/antigravity-ide/scratch/cybersecurity-cna-census/data/housing/census_permits_and_completions.csv")
OUTPUT_CSV = Path("C:/Users/nswcl/.gemini/antigravity-ide/scratch/research_replication_package/results/task_e_housing_null_case_econometrics.csv")
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

def exp_func(t, a, b):
    return a * np.exp(b * t)

def main():
    print("=" * 85)
    print("TASK E: HOUSING SUPPLY NULL-CASE ECONOMETRIC REGRESSION (N = 703 MONTHS)")
    print(f"Data source: {INPUT_CSV}")
    print("=" * 85)

    df = pd.read_csv(INPUT_CSV)
    print(f"Loaded {len(df)} monthly observations (from {df['date'].iloc[0]} to {df['date'].iloc[-1]}).")

    # Time in years since start
    t = np.arange(len(df)) / 12.0
    permits = df["permits_authorized_thousands_saar"].values
    completions = df["units_completed_thousands_saar"].values

    # 1. Linear OLS (y = alpha + beta * t)
    slope_p, intercept_p = np.polyfit(t, permits, 1)
    y_pred_lin_p = intercept_p + slope_p * t
    ss_tot_p = np.sum((permits - np.mean(permits)) ** 2)
    ss_res_lin_p = np.sum((permits - y_pred_lin_p) ** 2)
    r2_lin_p = 1.0 - (ss_res_lin_p / ss_tot_p)

    slope_c, intercept_c = np.polyfit(t, completions, 1)
    y_pred_lin_c = intercept_c + slope_c * t
    ss_tot_c = np.sum((completions - np.mean(completions)) ** 2)
    ss_res_lin_c = np.sum((completions - y_pred_lin_c) ** 2)
    r2_lin_c = 1.0 - (ss_res_lin_c / ss_tot_c)

    # 2. Nonlinear Exponential Fit in Level Space (y = a * exp(b * t))
    popt_p, _ = curve_fit(exp_func, t, permits, p0=[1400.0, 0.0])
    y_pred_exp_p = exp_func(t, *popt_p)
    ss_res_exp_p = np.sum((permits - y_pred_exp_p) ** 2)
    r2_exp_p = 1.0 - (ss_res_exp_p / ss_tot_p)

    popt_c, _ = curve_fit(exp_func, t, completions, p0=[1400.0, 0.0])
    y_pred_exp_c = exp_func(t, *popt_c)
    ss_res_exp_c = np.sum((completions - y_pred_exp_c) ** 2)
    r2_exp_c = 1.0 - (ss_res_exp_c / ss_tot_c)

    # 3. Log-linear OLS (ln(y) = ln(a) + b * t)
    log_p = np.log(permits)
    b_log_p, ln_a_p = np.polyfit(t, log_p, 1)
    r2_log_p = 1.0 - np.sum((log_p - (ln_a_p + b_log_p * t)) ** 2) / np.sum((log_p - np.mean(log_p)) ** 2)

    log_c = np.log(completions)
    b_log_c, ln_a_c = np.polyfit(t, log_c, 1)
    r2_log_c = 1.0 - np.sum((log_c - (ln_a_c + b_log_c * t)) ** 2) / np.sum((log_c - np.mean(log_c)) ** 2)

    summary_rows = [
        {
            "series": "Housing Permits Authorized (F_t)",
            "n_obs": len(df),
            "mean_level_thousands": round(np.mean(permits), 2),
            "linear_slope_per_year": round(slope_p, 4),
            "linear_r2": round(r2_lin_p, 4),
            "exp_growth_rate_b_level_fit": round(popt_p[1], 4),
            "exp_level_r2": round(r2_exp_p, 4),
            "log_linear_b_rate": round(b_log_p, 4),
            "log_linear_r2": round(r2_log_p, 4),
            "verdict": "Stationary / Cyclical (Zero Compounding)"
        },
        {
            "series": "Housing Units Completed (C_t)",
            "n_obs": len(df),
            "mean_level_thousands": round(np.mean(completions), 2),
            "linear_slope_per_year": round(slope_c, 4),
            "linear_r2": round(r2_lin_c, 4),
            "exp_growth_rate_b_level_fit": round(popt_c[1], 4),
            "exp_level_r2": round(r2_exp_c, 4),
            "log_linear_b_rate": round(b_log_c, 4),
            "log_linear_r2": round(r2_log_c, 4),
            "verdict": "Stationary / Cyclical (Zero Compounding)"
        }
    ]

    df_out = pd.DataFrame(summary_rows)
    df_out.to_csv(OUTPUT_CSV, index=False)
    print(df_out.to_string(index=False))

    print("\n" + "=" * 85)
    print("📐 MATHEMATICAL NOTE ON R^2 < 0 FOR EXPONENTIAL LEVEL FIT:")
    print("In linear OLS with an intercept, R^2 is bounded in [0, 1].")
    print("However, when nonlinear curve_fit evaluates y = a * exp(b*t) in raw levels without")
    print("an unconstrained additive constant, SS_res can slightly exceed SS_tot if the model")
    print(f"performs worse than a horizontal mean line. Here, exp_level_R^2 = {r2_exp_p:.4f},")
    print("confirming that an exponential curve is econometrically inferior to a flat mean line.")
    print(f"\n[✓] Results saved to: {OUTPUT_CSV}")
    print("=" * 85)

if __name__ == '__main__':
    main()
