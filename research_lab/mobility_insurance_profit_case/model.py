"""Reproducible hypothetical Bayesian mobility-insurance profit test.

No Moove, insurer, broker, or driver data are used. The code imports the existing
Mwendo fleet model only to create a dated, one-vehicle operating bridge.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import math
import os
import random
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MWENDO_CASE_RELATIVE = Path("research_lab") / "mobility_fleet_case"
MWENDO_SIBLING_NAMES = (
    "mwendo-pamoja-continuous-underwriting",
    "insuretech & embedded finance",
    "mwendo-pamoja",
)


def resolve_mwendo_case_dir():
    """Find the explicitly separate Mwendo repository without copying its model."""
    override = os.environ.get("MWENDO_PAMOJA_ROOT")
    candidates = ([Path(override).expanduser().resolve()] if override else
                  [ROOT.parent / name for name in MWENDO_SIBLING_NAMES])
    for repository in candidates:
        directory = repository / MWENDO_CASE_RELATIVE
        if all((directory / name).is_file() for name in ("model.py", "assumptions.json")):
            return directory.resolve()
    checked = "; ".join(str(repository / MWENDO_CASE_RELATIVE) for repository in candidates)
    raise FileNotFoundError(
        "The Mwendo bridge requires its sibling repository "
        "https://github.com/TheAlchemistNerd/mwendo-pamoja-continuous-underwriting. "
        "Set MWENDO_PAMOJA_ROOT to that checkout's root. Checked: " + checked
    )


def quantile(values, p):
    if not values or not 0 <= p <= 1:
        raise ValueError("quantile needs values and p in [0, 1]")
    values = sorted(values)
    x = p * (len(values) - 1)
    lo, hi = int(x), min(int(x) + 1, len(values) - 1)
    weight = x - lo
    return values[lo] * (1 - weight) + values[hi] * weight


def poisson(rng, mean):
    if mean < 0:
        raise ValueError("Poisson mean must be non-negative")
    if mean == 0:
        return 0
    threshold, product, count = math.exp(-mean), 1.0, 0
    while product > threshold:
        count += 1
        product *= rng.random()
    return count - 1


def weighted_choice(rng, values, probabilities):
    u, cumulative = rng.random(), 0.0
    for value, probability in zip(values, probabilities):
        cumulative += probability
        if u <= cumulative:
            return value
    return values[-1]


def validate(x):
    groups = x["synthetic_history"]["groups"]
    if not math.isclose(sum(g["share"] for g in groups.values()), 1.0, abs_tol=1e-10):
        raise ValueError("group shares must sum to one")
    n = x["portfolio"]["vehicles"]
    if not isinstance(n, int) or n <= 0:
        raise ValueError("vehicles must be a positive integer")
    if sum(round(n * g["share"]) for g in groups.values()) != n:
        raise ValueError("group shares must map to integer vehicle counts")
    for delay in x["insurer"].values():
        if isinstance(delay, dict) and "values" in delay:
            if len(delay["values"]) != len(delay["probabilities"]):
                raise ValueError("lag values and probabilities must align")
            if not math.isclose(sum(delay["probabilities"]), 1.0, abs_tol=1e-10):
                raise ValueError("lag probabilities must sum to one")
    insurer = x["insurer"]
    for key in ("quota_share", "ceding_commission", "operating_expense_ratio", "claim_expense_ratio"):
        if not 0 <= insurer[key] < 1:
            raise ValueError(f"{key} must lie in [0, 1)")
    if not 0 <= x["pricing"]["premium_pass_through_to_driver"] <= 1:
        raise ValueError("premium pass-through must lie in [0, 1]")
    if not 0 <= x["pricing"]["intervention_frequency_reduction_volatile"] < 1:
        raise ValueError("intervention effect must lie in [0, 1)")


def posterior_parameters(x):
    """Gamma–Poisson frequency and inverse-Gamma/Gamma severity posteriors.

    Frequency theta has Gamma(a,b) shape-rate convention and multiplies the
    base claim rate. Severity omega has InvGamma(a,b) shape-scale convention;
    individual severities are Gamma(k, mean=base_mean*omega).
    """
    validate(x)
    h, p = x["synthetic_history"], x["portfolio"]
    fp, sp, k = h["frequency_prior"], h["severity_prior"], h["severity_gamma_shape"]
    out = {}
    for name, g in h["groups"].items():
        n, e = g["claims"], g["exposure_units_10000_km"]
        if n <= 0 or e <= 0:
            raise ValueError("synthetic claims and exposure must be positive")
        fs, fr = fp["shape"] + n, fp["rate"] + e * p["base_claims_per_10000_km"]
        ss = sp["shape"] + k * n
        sb = sp["scale"] + k * n * g["mean_ultimate_insured_severity"] / p["base_insured_severity"]
        out[name] = {
            "share": g["share"], "claims": n, "exposure_units_10000_km": e,
            "frequency_shape": fs, "frequency_rate": fr,
            "frequency_mean_multiplier": fs / fr,
            "frequency_credibility_weight": e * p["base_claims_per_10000_km"] / fr,
            "severity_shape": ss, "severity_scale": sb,
            "severity_mean_multiplier": sb / (ss - 1),
        }
    return out


def draw_risks(rng, posterior):
    risks = {}
    for name, g in posterior.items():
        theta = rng.gammavariate(g["frequency_shape"], 1 / g["frequency_rate"])
        # Reciprocal-Gamma sampler for the inverse-Gamma severity multiplier.
        omega = 1 / rng.gammavariate(g["severity_shape"], 1 / g["severity_scale"])
        risks[name] = {"frequency": theta, "severity": omega}
    return risks


def posterior_summary(x, posterior):
    draws, seed = x["computation"]["posterior_draws"], x["computation"]["random_seed"]
    rng = random.Random(seed + 17)
    samples = {n: {k: [] for k in ("frequency", "severity", "raw_joint", "calibrated_joint", "driving_loss")}
               for n in posterior}
    km_factor = x["portfolio"]["annual_km_per_vehicle"] / 10000
    base_rate = x["portfolio"]["base_claims_per_10000_km"]
    base_severity = x["portfolio"]["base_insured_severity"]
    insurer = x["insurer"]
    shock_loss_factor = 1 + insurer["common_shock_probability"] * (
        insurer["common_shock_frequency_multiplier"] * insurer["common_shock_severity_multiplier"] - 1)
    for _ in range(draws):
        risks = draw_risks(rng, posterior)
        joint = {n: risks[n]["frequency"] * risks[n]["severity"] for n in posterior}
        aggregate = sum(posterior[n]["share"] * joint[n] for n in posterior)
        for n in posterior:
            samples[n]["frequency"].append(risks[n]["frequency"])
            samples[n]["severity"].append(risks[n]["severity"])
            samples[n]["raw_joint"].append(joint[n])
            samples[n]["calibrated_joint"].append(joint[n] / aggregate)
            samples[n]["driving_loss"].append(km_factor * base_rate * base_severity * joint[n] * shock_loss_factor)
    out = {}
    for name, g in posterior.items():
        out[name] = {
            "claims": g["claims"], "historical_exposure_10000_km": g["exposure_units_10000_km"],
            "frequency_posterior_mean": g["frequency_mean_multiplier"],
            "frequency_credibility_weight": g["frequency_credibility_weight"],
            "severity_posterior_mean": g["severity_mean_multiplier"],
        }
        for key, vals in samples[name].items():
            out[name][key + "_interval_90"] = [quantile(vals, .05), quantile(vals, .95)]
    return out


def pricing_summary(x, posterior):
    p, price = x["portfolio"], x["pricing"]
    insurer = x["insurer"]
    shock_loss_factor = 1 + insurer["common_shock_probability"] * (
        insurer["common_shock_frequency_multiplier"] * insurer["common_shock_severity_multiplier"] - 1)
    shock_frequency_factor = 1 + insurer["common_shock_probability"] * (
        insurer["common_shock_frequency_multiplier"] - 1)
    base_drive = p["annual_km_per_vehicle"] / 10000 * p["base_claims_per_10000_km"] * p["base_insured_severity"]
    raw = {n: g["frequency_mean_multiplier"] * g["severity_mean_multiplier"] for n, g in posterior.items()}
    normaliser = sum(posterior[n]["share"] * raw[n] for n in posterior)
    estimated_drive_loss = base_drive * normaliser * shock_loss_factor
    non_drive = price["non_driving_pure_premium_per_vehicle"] * shock_loss_factor
    total_pure_loss = estimated_drive_loss + non_drive
    fixed_commercial_layer = price["annual_commercial_premium_per_vehicle"] - total_pure_loss
    out_groups = {}
    for name, g in posterior.items():
        factor = raw[name] / normaliser
        group_drive = estimated_drive_loss * factor
        group_pure = group_drive + non_drive
        premium = fixed_commercial_layer + group_pure
        out_groups[name] = {
            "share": g["share"], "frequency_posterior_mean": g["frequency_mean_multiplier"],
            "severity_posterior_mean": g["severity_mean_multiplier"], "raw_joint_factor": raw[name],
            "calibrated_joint_factor": factor, "expected_driving_pure_premium": group_drive,
            "expected_non_driving_pure_premium": non_drive, "expected_total_pure_premium": group_pure,
            "flat_commercial_premium": price["annual_commercial_premium_per_vehicle"],
            "neutral_relativity_premium": premium, "intervention_commercial_premium": premium,
            "expected_claim_frequency_per_vehicle_year": p["annual_km_per_vehicle"] / 10000
                * p["base_claims_per_10000_km"] * g["frequency_mean_multiplier"] * shock_frequency_factor,
        }
    high = "volatile" if "volatile" in out_groups else max(out_groups, key=lambda n: raw[n])
    saving = out_groups[high]["expected_driving_pure_premium"] * price["intervention_frequency_reduction_volatile"]
    premium_reduction = saving * price["premium_share_of_validated_saving"]
    incentive = saving * price["driver_incentive_share_of_volatile_group_saving"]
    out_groups[high].update({
        "intervention_expected_driving_pure_premium": out_groups[high]["expected_driving_pure_premium"] - saving,
        "intervention_commercial_premium": out_groups[high]["neutral_relativity_premium"] - premium_reduction,
        "intervention_expected_claim_frequency_per_vehicle_year":
            out_groups[high]["expected_claim_frequency_per_vehicle_year"]
            * (1 - price["intervention_frequency_reduction_volatile"]),
        "expected_loss_saving_per_volatile_vehicle": saving,
        "premium_reduction_per_volatile_vehicle": premium_reduction,
        "driver_incentive_per_volatile_vehicle": incentive,
    })
    neutral_total = sum(g["share"] * g["neutral_relativity_premium"] for g in out_groups.values())
    intervention_total = sum(g["share"] * g["intervention_commercial_premium"] for g in out_groups.values())
    portfolio_saving = sum(g["share"] * (g["expected_driving_pure_premium"]
        - g.get("intervention_expected_driving_pure_premium", g["expected_driving_pure_premium"]))
        for g in out_groups.values())
    return {
        "base_driving_pure_premium": base_drive, "posterior_estimated_portfolio_driving_loss": estimated_drive_loss,
        "base_non_driving_pure_premium": price["non_driving_pure_premium_per_vehicle"],
        "expected_non_driving_loss_including_common_shock": non_drive,
        "common_shock_expected_loss_factor": shock_loss_factor,
        "common_shock_expected_frequency_factor": shock_frequency_factor,
        "posterior_estimated_total_pure_loss": total_pure_loss,
        "fixed_commercial_layer": fixed_commercial_layer,
        "portfolio_baseline_premium": price["annual_commercial_premium_per_vehicle"],
        "joint_normaliser": normaliser, "neutral_portfolio_premium": neutral_total,
        "intervention_portfolio_premium": intervention_total,
        "portfolio_expected_driving_loss_saving": portfolio_saving,
        "portfolio_premium_reduction": neutral_total - intervention_total,
        "premium_pass_through_to_driver": price["premium_pass_through_to_driver"],
        "groups": out_groups,
    }


def merge_intervals(intervals):
    merged = []
    for start, end in sorted(intervals):
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged


def _simulate_plan(x, posterior, prices, plan):
    p, ins, econ = x["portfolio"], x["insurer"], x["moove_driver_economics"]
    n_sim = x["computation"]["predictive_simulations"]
    n_months = p["calendar_days"] // p["days_per_month"]
    max_month = n_months + max(ins["reporting_delay_months"]["values"]) \
        + max(ins["settlement_delay_after_report_months"]["values"]) + ins["reinsurance_recovery_delay_months"]
    groups = list(posterior)
    n_by_group = {n: round(p["vehicles"] * posterior[n]["share"]) for n in groups}
    base_premium = x["pricing"]["annual_commercial_premium_per_vehicle"]
    high = "volatile" if "volatile" in groups else max(groups, key=lambda n: posterior[n]["frequency_mean_multiplier"])
    premium = {n: (base_premium if plan == "flat" else
                   prices["groups"][n]["intervention_commercial_premium"] if plan == "intervention" else
                   prices["groups"][n]["neutral_relativity_premium"]) for n in groups}
    gross_premium = sum(n_by_group[n] * premium[n] for n in groups)
    intervention = x["pricing"]["intervention_frequency_reduction_volatile"] if plan == "intervention" else 0.0
    incentive_per_vehicle = prices["groups"][high].get("driver_incentive_per_volatile_vehicle", 0) if plan == "intervention" else 0
    month_count = max_month
    daily_margin = (econ["weekly_gross_fares"] * (1 - econ["platform_fraction"])
                    - econ["weekly_energy_cash"]) / 7
    base_weekly_driver_cash = (econ["weekly_gross_fares"] * (1 - econ["platform_fraction"])
        - econ["weekly_energy_cash"] - econ["weekly_household_need"] - econ["weekly_package_due"])
    qs = ins["quota_share"]
    k = x["synthetic_history"]["severity_gamma_shape"]
    simulations = []
    for i in range(n_sim):
        rng = random.Random(x["computation"]["random_seed"] + 1000 + i * 7919)
        risks = draw_risks(rng, posterior)
        shock = rng.random() < ins["common_shock_probability"]
        freq_shock = ins["common_shock_frequency_multiplier"] if shock else 1.0
        sev_shock = ins["common_shock_severity_multiplier"] if shock else 1.0
        paid = [0.0] * month_count
        recovered = [0.0] * month_count
        moove_gross_retention = [0.0] * month_count
        driver_excess = [0.0] * month_count
        expedite = [0.0] * month_count
        intervals = {mode: {g: [[] for _ in range(n_by_group[g])] for g in groups}
                     for mode in ("standard", "expedited")}
        gross_claims = drive_claims = non_drive_claims = 0
        drive_loss = non_drive_loss = 0.0
        reported_os = ibnr = 0.0

        def register_claim(amount, event_day, is_driving, group=None, owner=None):
            nonlocal gross_claims, drive_claims, non_drive_claims, gross_claims_amount, reported_os, ibnr
            gross_claims += 1
            gross_claims_amount += amount
            occurrence_month = event_day // p["days_per_month"] + 1
            report = occurrence_month + weighted_choice(rng, ins["reporting_delay_months"]["values"],
                                                        ins["reporting_delay_months"]["probabilities"])
            payment = report + weighted_choice(rng, ins["settlement_delay_after_report_months"]["values"],
                                               ins["settlement_delay_after_report_months"]["probabilities"])
            if payment <= month_count:
                paid[payment - 1] += amount
                recovery_month = payment + ins["reinsurance_recovery_delay_months"]
                if recovery_month <= month_count:
                    recovered[recovery_month - 1] += qs * amount
            if payment > n_months:
                if report <= n_months:
                    reported_os += amount
                else:
                    ibnr += amount
            if is_driving:
                drive_claims += 1
                claim_retention = econ["operator_retention_per_driving_claim"]
                excess = min(econ["driver_excess_per_claim"], claim_retention)
                moove_gross_retention[occurrence_month - 1] += claim_retention
                driver_excess[occurrence_month - 1] += excess
                expedite[occurrence_month - 1] += econ["expedited_repair_surcharge_per_claim"]
                intervals["standard"][group][owner].append(
                    (event_day, event_day + econ["standard_repair_downtime_days"]))
                intervals["expedited"][group][owner].append(
                    (event_day, event_day + econ["expedited_repair_downtime_days"]))
            else:
                non_drive_claims += 1

        gross_claims_amount = 0.0
        for group in groups:
            theta, omega = risks[group]["frequency"], risks[group]["severity"]
            mean_n = (n_by_group[group] * p["annual_km_per_vehicle"] / 10000
                      * p["base_claims_per_10000_km"] * theta * freq_shock
                      * ((1 - intervention) if group == high else 1.0))
            for _ in range(poisson(rng, mean_n)):
                owner = rng.randrange(n_by_group[group])
                day = rng.randrange(p["calendar_days"])
                severity = rng.gammavariate(k, p["base_insured_severity"] * omega * sev_shock / k)
                drive_loss += severity
                register_claim(severity, day, True, group, owner)
            for _ in range(poisson(rng, n_by_group[group] * p["non_driving_claims_per_vehicle_year"] * freq_shock)):
                day = rng.randrange(p["calendar_days"])
                severity = rng.gammavariate(k, p["non_driving_mean_severity"] * sev_shock / k)
                non_drive_loss += severity
                register_claim(severity, day, False)

        # Ultimate, paid, reserve and ceded outstanding amounts reconcile.
        paid_year = sum(paid[:n_months])
        outstanding = gross_claims_amount - paid_year
        reserve_error = abs(gross_claims_amount - paid_year - outstanding)
        ceded_recoverable = max(0.0, qs * gross_claims_amount - sum(recovered[:n_months]))

        op_modes = {}
        for mode in ("standard", "expedited"):
            lost_days = {g: [0.0] * n_months for g in groups}
            total_days = {g: 0.0 for g in groups}
            for group in groups:
                for vehicle_intervals in intervals[mode][group]:
                    for start, end in merge_intervals(vehicle_intervals):
                        end = min(end, p["calendar_days"])
                        for day in range(start, end):
                            m = day // p["days_per_month"]
                            lost_days[group][m] += 1
                            total_days[group] += 1
            m_cash, d_cash = [0.0] * n_months, [0.0] * n_months
            package, premiums, maint = [0.0] * n_months, [0.0] * n_months, [0.0] * n_months
            loss_work, incentives = [0.0] * n_months, [0.0] * n_months
            for group in groups:
                count = n_by_group[group]
                pass_through = x["pricing"]["premium_pass_through_to_driver"] * (premium[group] - base_premium)
                incentive = incentive_per_vehicle if plan == "intervention" and group == high else 0.0
                package_per_month = (econ["weekly_package_due"] * 52 / 12 + pass_through / 12 - incentive / 12) * count
                prem_per_month = premium[group] * count / 12
                maint_per_month = (econ["weekly_routine_maintenance"] + econ["weekly_administration"]) * 52 / 12 * count
                for m in range(12):
                    package[m] += package_per_month
                    premiums[m] += prem_per_month
                    maint[m] += maint_per_month
                    incentives[m] += incentive * count / 12
                    loss_work[m] += lost_days[group][m] * daily_margin
                    # Driver cash uses per-group claim counts in the event month, reconstructed from intervals.
                    claim_events_by_month = [0] * 12
                    for vehicle_intervals in intervals[mode][group]:
                        for start, _ in vehicle_intervals:
                            claim_events_by_month[start // p["days_per_month"]] += 1
                    gross_ret = claim_events_by_month[m] * econ["operator_retention_per_driving_claim"]
                    exc = min(econ["driver_excess_per_claim"], econ["operator_retention_per_driving_claim"]) * claim_events_by_month[m]
                    net_ret = gross_ret - exc
                    expedite_cost = (claim_events_by_month[m] * econ["expedited_repair_surcharge_per_claim"]
                                     if mode == "expedited" else 0.0)
                    m_cash[m] += package_per_month - prem_per_month - maint_per_month - net_ret - expedite_cost
                    d_cash[m] += (base_weekly_driver_cash * 52 / 12 * count - pass_through * count / 12
                                  + incentive * count / 12 - lost_days[group][m] * daily_margin - exc)
            m_npv = sum(v / (1 + econ["operator_annual_discount_rate"]) ** ((m + 1) / 12)
                        for m, v in enumerate(m_cash))
            d_npv = sum(v / (1 + econ["driver_annual_discount_rate"]) ** ((m + 1) / 12)
                        for m, v in enumerate(d_cash))
            op_modes[mode] = {
                "fleet_downtime_days": sum(total_days.values()),
                "moove_gross_retention": sum(moove_gross_retention[:12]),
                "driver_excess_paid_to_moove": sum(driver_excess[:12]),
                "moove_net_retention": sum(moove_gross_retention[:12]) - sum(driver_excess[:12]),
                "expedited_repair_surcharge": sum(expedite[:12]) if mode == "expedited" else 0.0,
                "package_cash_assuming_full_collection": sum(package),
                "insurance_premium_cash": sum(premiums), "maintenance_and_admin_cash": sum(maint),
                "moove_contribution_before_vehicle_capex_debt_tax_depreciation": sum(m_cash),
                "moove_npv": m_npv,
                "driver_take_home_after_household_package_downtime_excess": sum(d_cash),
                "driver_npv": d_npv,
                "monthly": {"moove_cash": m_cash, "driver_cash": d_cash, "package": package,
                    "premium": premiums, "maintenance_admin": maint, "lost_work": loss_work,
                    "incentive": incentives},
            }

        monthly = {key: [0.0] * month_count for key in
                   ("premium", "operating_expense", "reinsurance_premium", "gross_claim_paid",
                    "claim_expense_paid", "reinsurance_recovery")}
        for m in range(month_count):
            prem = gross_premium / 12 if m < 12 else 0.0
            monthly["premium"][m] = prem
            monthly["operating_expense"][m] = prem * ins["operating_expense_ratio"]
            monthly["reinsurance_premium"][m] = prem * qs * (1 - ins["ceding_commission"])
            monthly["gross_claim_paid"][m] = paid[m]
            monthly["claim_expense_paid"][m] = paid[m] * ins["claim_expense_ratio"]
            monthly["reinsurance_recovery"][m] = recovered[m]
        simulations.append({
            "gross_ultimate": gross_claims_amount, "driving_ultimate": drive_loss,
            "non_driving_ultimate": non_drive_loss, "net_ultimate": gross_claims_amount * (1 - qs),
            "claim_count": gross_claims, "driving_claim_count": drive_claims,
            "non_driving_claim_count": non_drive_claims, "reported_outstanding": reported_os,
            "ibnr": ibnr, "total_outstanding": outstanding, "gross_paid_year_end": paid_year,
            "ceded_recoverable": ceded_recoverable, "reserve_reconciliation_error": reserve_error,
            "common_shock": shock, "monthly": monthly, "operations": op_modes,
        })

    gross_losses = [s["gross_ultimate"] for s in simulations]
    net_losses = [s["net_ultimate"] for s in simulations]
    mean_net = sum(net_losses) / n_sim
    mean_gross = sum(gross_losses) / n_sim
    q = ins["annual_economic_capital_quantile"]
    var_net = quantile(net_losses, q)
    tail = [v for v in net_losses if v >= var_net]
    tvar = sum(tail) / len(tail)
    capital = max(0.0, var_net - mean_net)
    capital_charge = capital * ins["cost_of_capital_rate"]
    net_reins_premium = gross_premium * qs * (1 - ins["ceding_commission"])
    op_expense = gross_premium * ins["operating_expense_ratio"]
    claim_expense = mean_gross * ins["claim_expense_ratio"]
    profits = [gross_premium - net_reins_premium - op_expense - s["net_ultimate"]
               - s["gross_ultimate"] * ins["claim_expense_ratio"] - capital_charge for s in simulations]
    denominator = 1 - ins["operating_expense_ratio"] - qs * (1 - ins["ceding_commission"])
    if denominator <= 0:
        raise ValueError("expense and reinsurance shares leave no premium for claims")
    break_even = (mean_net + claim_expense + capital_charge) / denominator

    monthly_rows, npv = [], 0.0
    for m in range(month_count):
        row = {k: sum(s["monthly"][k][m] for s in simulations) / n_sim for k in simulations[0]["monthly"]}
        cash = (row["premium"] - row["operating_expense"] - row["reinsurance_premium"]
                - row["gross_claim_paid"] - row["claim_expense_paid"] + row["reinsurance_recovery"])
        capital_accrual = capital_charge / 12 if m < 12 else 0.0
        row.update({"month": m + 1, "net_cash_before_capital": cash,
                    "capital_cost_accrual": capital_accrual, "economic_cash_after_capital": cash - capital_accrual})
        npv += (cash - capital_accrual) / (1 + ins["annual_discount_rate"]) ** ((m + 1) / 12)
        monthly_rows.append(row)

    def mean_op(mode):
        keys = ["fleet_downtime_days", "moove_gross_retention", "driver_excess_paid_to_moove",
            "moove_net_retention", "expedited_repair_surcharge", "package_cash_assuming_full_collection",
            "insurance_premium_cash", "maintenance_and_admin_cash",
            "moove_contribution_before_vehicle_capex_debt_tax_depreciation", "moove_npv",
            "driver_take_home_after_household_package_downtime_excess", "driver_npv"]
        out = {k: sum(s["operations"][mode][k] for s in simulations) / n_sim for k in keys}
        out["moove_contribution_per_vehicle_year"] = (
            out["moove_contribution_before_vehicle_capex_debt_tax_depreciation"] / p["vehicles"])
        out["driver_take_home_per_vehicle_year"] = (
            out["driver_take_home_after_household_package_downtime_excess"] / p["vehicles"])
        out["fleet_downtime_days_per_vehicle_year"] = out["fleet_downtime_days"] / p["vehicles"]
        out["monthly"] = [{"month": m + 1, **{key: sum(s["operations"][mode]["monthly"][key][m]
            for s in simulations) / n_sim for key in simulations[0]["operations"][mode]["monthly"]}}
            for m in range(n_months)]
        return out

    sensitivity = []
    for test_premium in x["computation"]["break_even_premium_sensitivity"]:
        total = test_premium * p["vehicles"]
        profit = total * denominator - mean_net - claim_expense - capital_charge
        sensitivity.append({"premium_per_vehicle": test_premium, "expected_profit_after_capital": profit})
    excess_sensitivity = {}
    for group in groups:
        expected_frequency = (p["annual_km_per_vehicle"] / 10000
            * p["base_claims_per_10000_km"] * posterior[group]["frequency_mean_multiplier"]
            * prices["common_shock_expected_frequency_factor"])
        excess_sensitivity[group] = [{
            "driver_excess_per_claim": excess,
            "expected_driver_excess_per_vehicle_year": expected_frequency * min(
                excess, econ["operator_retention_per_driving_claim"]),
            "expected_operator_net_retention_per_vehicle_year": expected_frequency * (
                econ["operator_retention_per_driving_claim"] - min(
                    excess, econ["operator_retention_per_driving_claim"])),
        } for excess in econ["driver_excess_sensitivity"]]
    summary = {
        "plan": plan, "portfolio_vehicles": p["vehicles"], "annual_gross_premium": gross_premium,
        "mean_gross_ultimate_claims": mean_gross,
        "mean_driving_ultimate_claims": sum(s["driving_ultimate"] for s in simulations) / n_sim,
        "mean_non_driving_ultimate_claims": sum(s["non_driving_ultimate"] for s in simulations) / n_sim,
        "mean_net_ultimate_claims": mean_net,
        "predictive_net_claims_interval_90": [quantile(net_losses, .05), quantile(net_losses, .95)],
        "predictive_net_claims_median": quantile(net_losses, .5), "net_claims_var_at_selected_quantile": var_net,
        "net_claims_tvar_at_selected_quantile": tvar, "economic_capital_var_minus_mean": capital,
        "annual_cost_of_capital": capital_charge, "mean_claim_expense": claim_expense,
        "annual_operating_expense": op_expense, "annual_net_reinsurance_premium": net_reins_premium,
        "mean_expected_profit_after_capital": sum(profits) / n_sim,
        "profit_after_capital_predictive_interval_90": [quantile(profits, .05), quantile(profits, .95)],
        "probability_profit_after_capital_below_zero": sum(v < 0 for v in profits) / n_sim,
        "break_even_annual_premium_per_vehicle": break_even / p["vehicles"],
        "mean_driving_claim_count": sum(s["driving_claim_count"] for s in simulations) / n_sim,
        "mean_non_driving_claim_count": sum(s["non_driving_claim_count"] for s in simulations) / n_sim,
        "mean_gross_claims_paid_by_year_end": sum(s["gross_paid_year_end"] for s in simulations) / n_sim,
        "mean_reported_outstanding_at_year_end": sum(s["reported_outstanding"] for s in simulations) / n_sim,
        "mean_ibnr_at_year_end": sum(s["ibnr"] for s in simulations) / n_sim,
        "mean_total_outstanding_at_year_end": sum(s["total_outstanding"] for s in simulations) / n_sim,
        "mean_ceded_recoverable_at_year_end": sum(s["ceded_recoverable"] for s in simulations) / n_sim,
        "max_claim_reconciliation_error": max(s["reserve_reconciliation_error"] for s in simulations),
        "simulated_common_shock_frequency": sum(s["common_shock"] for s in simulations) / n_sim,
        "driver_excess_sensitivity_by_group": excess_sensitivity,
        "insurer_cash_npv_after_capital": npv,
        "moove_driver_standard_repair_12_days": mean_op("standard"),
        "moove_driver_expedited_repair_2_days": mean_op("expedited"),
        "premium_sensitivity": sensitivity,
    }
    return {"summary": summary, "insurer_monthly": monthly_rows}


def _load_mwendo():
    mwendo_dir = resolve_mwendo_case_dir()
    path = mwendo_dir / "model.py"
    spec = importlib.util.spec_from_file_location("mwendo_fleet_model_read_only", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assumptions = json.loads((mwendo_dir / "assumptions.json").read_text(encoding="utf-8"))
    return module, assumptions


def mwendo_bridge(x, prices):
    """Reuse the 156-week case: update only dated annual premium and weekly fee."""
    module, base = _load_mwendo()
    base_premium = x["pricing"]["annual_commercial_premium_per_vehicle"]
    pass_through = x["pricing"]["premium_pass_through_to_driver"]
    high = "volatile" if "volatile" in prices["groups"] else max(
        prices["groups"], key=lambda n: prices["groups"][n]["frequency_posterior_mean"])
    plans = {
        "flat": {n: base_premium for n in prices["groups"]},
        "neutral_relativity": {n: prices["groups"][n]["neutral_relativity_premium"] for n in prices["groups"]},
        "validated_intervention": {n: prices["groups"][n]["intervention_commercial_premium"] for n in prices["groups"]},
    }
    scenarios = {s["id"]: s for s in base["scenarios"]
                 if s["id"] in {"uninterrupted", "scheduled_repair", "expedited_repair"}}
    out = {}
    for plan, group_premiums in plans.items():
        out[plan] = {}
        for group, annual_premium in group_premiums.items():
            incentive = prices["groups"][group].get("driver_incentive_per_volatile_vehicle", 0) \
                if plan == "validated_intervention" and group == high else 0
            adjustment = (pass_through * (annual_premium - base_premium) - incentive) / 52
            case = copy.deepcopy(base)
            case["insurance_cash_every_52_weeks"] = f"{annual_premium:.10f}"
            case["weekly_package_due"] = f"{float(base['weekly_package_due']) + adjustment:.10f}"
            out[plan][group] = {}
            for scenario_id, scenario in scenarios.items():
                summary = module.run_case(case, scenario)["summary"]
                fields = ["billed_fees", "collected_fees", "final_arrears", "peak_arrears",
                    "household_shortfall", "driver_cash_surplus", "equity_npv", "additional_equity",
                    "total_insurance_cash", "total_debt_interest", "vehicle_transferred",
                    "maximum_reconciliation_error"]
                out[plan][group][scenario_id] = {
                    **{f: (summary[f] if isinstance(summary[f], bool) else
                           float(summary[f]) if isinstance(summary[f], (int, float, Decimal)) else summary[f])
                       for f in fields}, "annual_premium_input": annual_premium,
                    "weekly_fee_adjustment_including_incentive": adjustment,
                }
    return out


def run_case(x):
    validate(x)
    posterior = posterior_parameters(x)
    post_summary = posterior_summary(x, posterior)
    prices = pricing_summary(x, posterior)
    simulations = {plan: _simulate_plan(x, posterior, prices, plan)
                   for plan in ("flat", "neutral_relativity", "intervention")}
    return {
        "status": x["case_status"], "currency": x["currency"], "assumption_snapshot": x,
        "posterior_parameters": posterior, "posterior_summary": post_summary,
        "pricing_and_normalisation": prices,
        "simulation_summaries": {n: v["summary"] for n, v in simulations.items()},
        "monthly_ledgers": {n: {"insurer": v["insurer_monthly"],
            "moove_driver_12_day_repair": v["summary"]["moove_driver_standard_repair_12_days"]["monthly"],
            "moove_driver_2_day_repair": v["summary"]["moove_driver_expedited_repair_2_days"]["monthly"]}
            for n, v in simulations.items()},
        "mwendo_156_week_bridge": mwendo_bridge(x, prices),
    }
