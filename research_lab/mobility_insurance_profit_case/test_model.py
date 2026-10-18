"""Invariant tests for the hypothetical Bayesian insurance profit case."""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model


def assumptions():
    return json.loads((HERE / "assumptions.json").read_text(encoding="utf-8"))


class ProfitTest(unittest.TestCase):
    def test_quantile_interpolates_and_handles_endpoints(self):
        self.assertEqual(model.quantile([2, 4, 8], 0), 2)
        self.assertEqual(model.quantile([2, 4, 8], 1), 8)
        self.assertEqual(model.quantile([2, 4, 8], .5), 4)

    def test_conjugate_frequency_and_severity_updates(self):
        x = assumptions()
        p = model.posterior_parameters(x)
        g = x["synthetic_history"]["groups"]["stable"]
        fp, sp, k = (x["synthetic_history"]["frequency_prior"],
                     x["synthetic_history"]["severity_prior"],
                     x["synthetic_history"]["severity_gamma_shape"])
        expected_shape = fp["shape"] + g["claims"]
        expected_rate = fp["rate"] + g["exposure_units_10000_km"] * x["portfolio"]["base_claims_per_10000_km"]
        expected_sev_shape = sp["shape"] + k * g["claims"]
        expected_sev_scale = sp["scale"] + k * g["claims"] * g["mean_ultimate_insured_severity"] / x["portfolio"]["base_insured_severity"]
        self.assertAlmostEqual(p["stable"]["frequency_shape"], expected_shape)
        self.assertAlmostEqual(p["stable"]["frequency_rate"], expected_rate)
        self.assertAlmostEqual(p["stable"]["severity_shape"], expected_sev_shape)
        self.assertAlmostEqual(p["stable"]["severity_scale"], expected_sev_scale)

    def test_neutral_tariff_is_premium_normalised(self):
        x = assumptions()
        prices = model.pricing_summary(x, model.posterior_parameters(x))
        self.assertAlmostEqual(prices["neutral_portfolio_premium"], 130000, places=6)
        weighted = sum(g["share"] * g["calibrated_joint_factor"] for g in prices["groups"].values())
        self.assertAlmostEqual(weighted, 1.0, places=12)
        self.assertLess(prices["groups"]["stable"]["neutral_relativity_premium"],
                        prices["groups"]["volatile"]["neutral_relativity_premium"])

    def test_intervention_is_separate_from_tariff_normalisation(self):
        x = assumptions()
        prices = model.pricing_summary(x, model.posterior_parameters(x))
        high = prices["groups"]["volatile"]
        expected_saving = high["expected_driving_pure_premium"] * .10
        self.assertAlmostEqual(high["expected_loss_saving_per_volatile_vehicle"], expected_saving)
        self.assertAlmostEqual(high["driver_incentive_per_volatile_vehicle"], expected_saving * .25)
        self.assertAlmostEqual(prices["intervention_portfolio_premium"],
                               130000 - .75 * prices["portfolio_expected_driving_loss_saving"], places=6)
        self.assertLess(prices["intervention_portfolio_premium"], prices["neutral_portfolio_premium"])

    def test_simulation_reconciles_claims_and_keeps_cash_ledgers_distinct(self):
        x = assumptions()
        x["computation"]["predictive_simulations"] = 100
        posterior = model.posterior_parameters(x)
        prices = model.pricing_summary(x, posterior)
        result = model._simulate_plan(x, posterior, prices, "flat")["summary"]
        self.assertEqual(result["max_claim_reconciliation_error"], 0)
        self.assertGreater(result["mean_total_outstanding_at_year_end"], 0)
        self.assertLess(result["mean_gross_claims_paid_by_year_end"], result["mean_gross_ultimate_claims"])
        self.assertAlmostEqual(result["mean_reported_outstanding_at_year_end"]
                               + result["mean_ibnr_at_year_end"],
                               result["mean_total_outstanding_at_year_end"], places=6)
        self.assertGreater(result["annual_cost_of_capital"], 0)
        self.assertEqual(len(result["moove_driver_standard_repair_12_days"]["monthly"]), 12)
        self.assertGreaterEqual(result["moove_driver_standard_repair_12_days"]["fleet_downtime_days"],
                                result["moove_driver_expedited_repair_2_days"]["fleet_downtime_days"])

    def test_seeded_predictive_run_is_reproducible(self):
        x = assumptions()
        x["computation"]["predictive_simulations"] = 25
        posterior = model.posterior_parameters(x)
        prices = model.pricing_summary(x, posterior)
        first = model._simulate_plan(x, posterior, prices, "intervention")["summary"]
        second = model._simulate_plan(x, posterior, prices, "intervention")["summary"]
        self.assertEqual(first["mean_gross_ultimate_claims"], second["mean_gross_ultimate_claims"])
        self.assertEqual(first["mean_expected_profit_after_capital"],
                         second["mean_expected_profit_after_capital"])

    def test_zero_intervention_changes_neither_loss_nor_tariff(self):
        x = assumptions()
        x["pricing"]["intervention_frequency_reduction_volatile"] = 0
        prices = model.pricing_summary(x, model.posterior_parameters(x))
        self.assertAlmostEqual(prices["intervention_portfolio_premium"], prices["neutral_portfolio_premium"])
        self.assertAlmostEqual(prices["portfolio_expected_driving_loss_saving"], 0)

    def test_mwendo_bridge_uses_annual_insurance_cash_and_weekly_pass_through(self):
        x = assumptions()
        prices = model.pricing_summary(x, model.posterior_parameters(x))
        bridge = model.mwendo_bridge(x, prices)
        stable = bridge["neutral_relativity"]["stable"]["uninterrupted"]
        expected = .5 * (prices["groups"]["stable"]["neutral_relativity_premium"] - 130000) / 52
        self.assertAlmostEqual(stable["annual_premium_input"], prices["groups"]["stable"]["neutral_relativity_premium"])
        self.assertAlmostEqual(stable["weekly_fee_adjustment_including_incentive"], expected)
        self.assertLessEqual(stable["maximum_reconciliation_error"], 1e-6)


if __name__ == "__main__":
    unittest.main()
