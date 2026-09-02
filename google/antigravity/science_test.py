# Copyright 2026 Google LLC & Gia Bao Huynh (Jun)
# Licensed under the Apache License, Version 2.0

"""Unit tests for Scientific & Queueing Theory models."""

import unittest
from google.antigravity.science import QueueingModel, LongevitySimulator, CNACensusAnalytics


class TestScienceModels(unittest.TestCase):

    def test_queueing_model_critical_horizon(self):
        qm = QueueingModel(lambda_0=0.015, alpha=0.18, mu=0.052)
        t_star = qm.critical_horizon()
        # t* = (1 / 0.18) * ln(0.052 / 0.015) = 6.9066 years
        self.assertAlmostEqual(t_star, 6.907, places=2)

    def test_queueing_model_traffic_intensity(self):
        qm = QueueingModel(lambda_0=0.015, alpha=0.18, mu=0.052)
        rho_0 = qm.traffic_intensity(0.0)
        self.assertAlmostEqual(rho_0, 0.015 / 0.052, places=3)

    def test_longevity_hazard_rate(self):
        h_80 = LongevitySimulator.hazard_rate(80.0)
        self.assertGreater(h_80, 0.0)
        s_80 = LongevitySimulator.survival_probability(80.0)
        self.assertGreaterEqual(s_80, 0.0)
        self.assertLessEqual(s_80, 1.0)

    def test_cna_census_hhi(self):
        counts = {"MITRE": 100, "Cisco": 50, "RedHat": 50}
        stats = CNACensusAnalytics.analyze_cna_distribution(counts)
        self.assertEqual(stats["total_records"], 200.0)
        self.assertEqual(stats["distinct_cnas"], 3.0)
        self.assertEqual(stats["top1_share_pct"], 50.0)
        # HHI: 50^2 + 25^2 + 25^2 = 2500 + 625 + 625 = 3750
        self.assertEqual(stats["hhi"], 3750.0)


if __name__ == "__main__":
    unittest.main()
