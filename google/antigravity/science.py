# Copyright 2026 Google LLC & Gia Bao Huynh (Jun)
# Licensed under the Apache License, Version 2.0

"""Scientific & Queueing Theory Computational Engine for Google Antigravity."""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class QueueingModel(BaseModel):
    """
    M/G/1 Cybernetic Queueing Instability Model.
    Models exponential discovery arrival rates lambda(t) vs bounded service capacity mu.
    """
    lambda_0: float = Field(default=0.015, description="Initial discovery arrival rate (e.g. CVEs/day or mutations/day)")
    alpha: float = Field(default=0.18, description="Autonomous AI acceleration rate (growth per year)")
    mu: float = Field(default=0.052, description="Bounded remediation/repair capacity rate (patches/day)")
    service_variance: float = Field(default=100.0, description="Variance of service time distribution (days^2)")

    def arrival_rate(self, t_years: float) -> float:
        """Calculate lambda(t) = lambda_0 * exp(alpha * t)."""
        return self.lambda_0 * math.exp(self.alpha * t_years)

    def traffic_intensity(self, t_years: float) -> float:
        """Calculate traffic intensity rho(t) = lambda(t) / mu."""
        return self.arrival_rate(t_years) / self.mu

    def critical_horizon(self) -> float:
        """Calculate critical transition horizon t* = (1 / alpha) * ln(mu / lambda_0)."""
        if self.mu <= self.lambda_0:
            return 0.0
        return (1.0 / self.alpha) * math.log(self.mu / self.lambda_0)

    def expected_workload(self, t_years: float) -> float:
        """
        Calculate expected Pollaczek-Khinchine workload W(t).
        W(t) = (lambda(t) * E[S^2]) / (2 * (1 - rho(t)))
        Returns infinity if rho(t) >= 1.
        """
        rho = self.traffic_intensity(t_years)
        if rho >= 1.0:
            return float("inf")
        e_s = 1.0 / self.mu
        e_s2 = self.service_variance + (e_s ** 2)
        lam = self.arrival_rate(t_years)
        return (lam * e_s2) / (2.0 * (1.0 - rho))


class LongevitySimulator:
    """
    Gompertz-Makeham Longevity Divergence Model for ALRP (Accelerated Longevity Regimes).
    Models mortality hazard rate h(x) = A + B * exp(C * x).
    """

    @staticmethod
    def hazard_rate(age: float, a: float = 0.0005, b: float = 0.00005, c: float = 0.085) -> float:
        """Calculate mortality hazard rate at age x."""
        return a + b * math.exp(c * age)

    @staticmethod
    def survival_probability(age: float, a: float = 0.0005, b: float = 0.00005, c: float = 0.085) -> float:
        """Calculate survival probability S(x) from birth to age x."""
        integral = a * age + (b / c) * (math.exp(c * age) - 1.0)
        return math.exp(-integral)


class CNACensusAnalytics:
    """
    Statistical analyzer for CVE Assigning Authority (CNA) full-population census data.
    """

    @staticmethod
    def calculate_hhi(shares: List[float]) -> float:
        """
        Calculate Herfindahl-Hirschman Index (0 to 10,000 scale).
        shares: list of percentage shares (e.g. [50.0, 30.0, 20.0]).
        """
        return sum(s ** 2 for s in shares)

    @staticmethod
    def analyze_cna_distribution(counts: Dict[str, int]) -> Dict[str, float]:
        """
        Analyze distribution given a dictionary of {cna_name: count}.
        Returns total count, distinct count, top-1 share, top-10 share, and HHI.
        """
        total = sum(counts.values())
        if total == 0:
            return {"total": 0, "distinct": 0, "top1_share": 0.0, "top10_share": 0.0, "hhi": 0.0}
        
        sorted_counts = sorted(counts.values(), reverse=True)
        shares = [(c / total) * 100.0 for c in sorted_counts]
        
        top1_share = shares[0] if shares else 0.0
        top10_share = sum(shares[:10]) if len(shares) >= 10 else sum(shares)
        hhi = CNACensusAnalytics.calculate_hhi(shares)

        return {
            "total_records": float(total),
            "distinct_cnas": float(len(counts)),
            "top1_share_pct": round(top1_share, 2),
            "top10_share_pct": round(top10_share, 2),
            "hhi": round(hhi, 2)
        }
