# Bayesian mobility-insurance profit test

This is a reproducible **hypothetical** KES insurance and fleet case. Every claim count, severity, price, reinsurance term, intervention effect and operating assumption is synthetic. No Moove, insurer, broker or driver data were used, and the output is not a quote or observed business result.

The case uses Gamma–Poisson frequency and inverse-Gamma/Gamma severity posteriors, exposure-normalised pure-premium relativities, a separate intervention scenario, and annual profit, reserve, capital and cashflow projections for a 100-vehicle portfolio. Its separate Mwendo Pamoja bridge runs the existing 156-week financing model with only its dated insurance premium and weekly package changed; the two ledgers must not be added together.

## Repository dependency

The insurance case belongs to [Bayesian Relativities](https://github.com/TheAlchemistNerd/bayesian-telematics-relativities/tree/main/research_lab/mobility_insurance_profit_case). Its 156-week operating bridge imports `model.py` and `assumptions.json` from the separate [Mwendo Pamoja fleet case](https://github.com/TheAlchemistNerd/mwendo-pamoja-continuous-underwriting/tree/main/research_lab/mobility_fleet_case).

Keep the repositories side by side. The resolver checks sibling folder names `mwendo-pamoja-continuous-underwriting`, `insuretech & embedded finance`, and `mwendo-pamoja`. For another location, set the repository root explicitly:

```powershell
$env:MWENDO_PAMOJA_ROOT = 'C:\path\to\mwendo-pamoja-continuous-underwriting'
```

The override must contain `research_lab/mobility_fleet_case/model.py` and `assumptions.json`. An invalid override reports the checked path rather than silently selecting another checkout. The input field `existing_mwendo_case_path` records the conventional sibling layout; `MWENDO_PAMOJA_ROOT` controls an alternative layout. The insurance calculations remain in this repository, while the operating bridge reads the Mwendo inputs without modifying them.

## Reproduce

From the project root:

```powershell
python -m unittest research_lab.mobility_insurance_profit_case.test_model -v
python research_lab/mobility_insurance_profit_case/run_case.py
```

The runner uses `assumptions.json` and fixed seed `20261014`, then writes `output/results.json`, `output/summary.json` and monthly CSV ledgers. The full run uses 12,000 posterior draws and 8,000 predictive paths.

## Interpretation of tail outputs

The reported 99.5% VaR and TVaR are empirical Monte Carlo estimates from 8,000 synthetic portfolio paths, so approximately 40 paths inform the upper 0.5% tail. They are illustrative economic-capital calculations, not a regulatory capital requirement. Treat them as coarse tail estimates, and rerun with more paths and alternative tail, common-shock and reinsurance assumptions before using the values for decisions.

For equations, assumptions, results, accounting boundaries, the reserve reconciliation and the Mwendo bridge, read [the research note](../../docs/research/MOOVE_BAYESIAN_INSURANCE_PROFIT_TESTING_CASE_2026-10-14.md).
