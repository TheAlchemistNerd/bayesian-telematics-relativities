# Bayesian Relativities × Moove: hypothetical insurance profit test

**Status:** reproducible research case, built from explicit synthetic assumptions. It contains no Moove, insurer, broker or driver portfolio data. All money amounts are Kenyan shillings (KES); the case is a Kenyan fleet illustration and is separate from any Moove UK fixed-subscription product.

## Purpose and result

This case takes the exposure-normalised frequency and severity relativities in the Bayesian Relativities work and asks a commercial question: what happens to the insurer, fleet operator and driver when expected claim costs are converted into premiums, claim cash flows, repair downtime and driver incentives? It uses one consistent hypothetical 100-vehicle portfolio for the insurance projection, then uses the separate 156-week Mwendo Pamoja financing model as an operating bridge. The bridge is not added to the portfolio projection.

The central result is that a posterior risk relativity and an intervention effect answer different questions. Normalised relativities allocate an approved portfolio premium across risk groups. A separately specified 10% reduction in volatile-group claim frequency changes expected losses only if a controlled pilot later supports that effect. In this synthetic case, risk differentiation changes the stable/volatile annual tariff to KES 113,988/KES 167,360 while preserving the KES 130,000 weighted premium. The assumed intervention reduces the weighted premium to KES 127,912 and increases simulated insurer profit after capital from KES 1.307 million to KES 1.442 million for the 100-vehicle annual portfolio.

These figures demonstrate a calculation pathway. They are not a Moove quote, forecast, observed result, recommended tariff or regulatory capital determination.

## 1. Evidence and scope

The supplied Moove analysis motivates a practical connection among telematics exposure, insured claims, repair operations, driver economics and insurance profitability. It describes Moove product materials and data categories, but those materials do not supply a claim-level insurance dataset for this exercise. This case therefore uses no purported Moove performance data. The synthetic history and all commercial terms below are author-selected inputs designed to exercise the statistical and financial logic.

The statistical construction follows the hierarchical frequency, severity, pure-premium and tariff-normalisation framework in the Bayesian Relativities manuscript. The fleet-level operating bridge reuses the existing Mwendo Pamoja 156-week case, whose assumptions and code remain unchanged. The three ledgers are:

1. **Insurer:** earned premium, operating expenses, reinsurance, ultimate claims, claim expenses, outstanding reserves, capital charge and cash timing.
2. **Moove/operator:** insurance premium, package receipts, routine maintenance and administration, repair retention, expedited repair charges and contribution before vehicle acquisition, debt, tax and depreciation.
3. **Driver:** fares after the platform share, energy, household requirement, package payments, claim excess, incentives and earnings lost during vehicle downtime.

The simulation assumes full collection of scheduled package cash in its expected-value fleet ledger. Delinquency, arrears, cure, sponsor equity and vehicle transfer remain in the separate Mwendo case.

## 2. Explicit assumptions

| Assumption | Hypothetical value |
|---|---:|
| Insured fleet and mix | 100 vehicles; 70% stable, 30% volatile |
| Annual driving exposure | 36,000 km per vehicle; 360-day model year |
| Base insured driving frequency | 0.08 claims per 10,000 km |
| Base insured severity | KES 180,000 per claim |
| Synthetic history | 3 vehicle-years per fleet vehicle; 88 fully developed claims |
| Stable-group history | 756 units of 10,000 km; 47 claims; KES 170,000 mean severity |
| Volatile-group history | 324 units of 10,000 km; 41 claims; KES 205,000 mean severity |
| Non-driving insured events | 0.04 per vehicle-year; KES 300,000 mean severity |
| Flat annual commercial premium | KES 130,000 per vehicle |
| Quota-share reinsurance | 20% ceded; 25% ceding commission |
| Insurer operating expense / claim expense | 26% of premium / 3% of gross ultimate claims |
| Cost of capital | 10% of illustrative economic capital |
| Common shock | 2% annual probability; frequency ×1.8 and severity ×1.25 |
| Claim reporting delay | 1, 2 or 3 months with probabilities 60%, 30% and 10% |
| Settlement after reporting | 1, 2, 3, 6 or 9 months with probabilities 35%, 30%, 20%, 10% and 5% |
| Reinsurance recovery delay | 2 months after insurer claim payment |
| Volatile-group intervention | Assumed 10% frequency reduction, subject to later empirical validation |
| Savings allocation | 75% to premium reduction; 25% to driver incentive |
| Driver premium pass-through | 50% of group premium change through the weekly package |
| Moove operating inputs | KES 70,000 weekly fares; 20% platform share; KES 16,000 energy; KES 12,000 household requirement; KES 25,000 package |
| Repair and retained loss | KES 30,000 operator retention per driving claim; 12-day standard or 2-day expedited repair; KES 5,000 expediting cost |
| Computation | 12,000 posterior draws; 8,000 predictive paths; random seed 20261014 |

The history totals 1,080 exposure units: 756 stable plus 324 volatile, consistent with 100 vehicles × 36,000 km × three years. Claim severities are assumed developed to ultimate and expressed on the insurer-indemnity basis. For the posterior severity likelihood, individual amounts follow a Gamma distribution with shape κ = 2 and mean μ₀ω, where ω is the group severity multiplier.

## 3. Bayesian model and derivation

For group *g*, let *Eᵍ* be exposure in units of 10,000 km, λ₀ = 0.08 the base claim rate, and θᵍ the unknown frequency multiplier:

> Nᵍ | θᵍ ~ Poisson(Eᵍ λ₀ θᵍ),     θᵍ ~ Gamma(a₀, b₀)

The Gamma distribution uses shape–rate parameters. With prior a₀ = 2 and b₀ = 2, the conjugate posterior is:

> θᵍ | Nᵍ,Eᵍ ~ Gamma(a₀ + Nᵍ, b₀ + Eᵍ λ₀)

For stable, the posterior is Gamma(49, 62.48), mean 0.7843 and frequency credibility weight 0.9680. For volatile, it is Gamma(43, 27.92), mean 1.5401 and credibility weight 0.9284. The credibility weight is *Eᵍλ₀/(b₀+Eᵍλ₀)*: as exposure grows, the observed claim count contributes more weight than the prior.

Let *Y* be an insured driving-claim severity, μ₀ = KES 180,000 and κ = 2. Conditional on severity multiplier ωᵍ:

> Y | ωᵍ ~ Gamma(κ, mean = μ₀ωᵍ),     ωᵍ ~ InvGamma(c₀,d₀)

With prior c₀ = 4 and d₀ = 3, and group mean severity Ȳᵍ, the posterior is:

> ωᵍ | Y ~ InvGamma(c₀ + κNᵍ, d₀ + κNᵍȲᵍ/μ₀)

The posterior mean is *dᵍ/(cᵍ−1)*. It is 0.9462 for stable and 1.1340 for volatile. Frequency and severity parameter draws are taken independently under this illustrative model; each draw produces a joint driving-loss factor *Jᵍ = θᵍωᵍ*. A posterior draw’s portfolio normaliser is *A = Σᵍ wᵍJᵍ*, where *wᵍ* is the group’s fleet share.

Annual base driving pure premium per vehicle before the portfolio common-shock allowance is:

> L₀ = (36,000 / 10,000) × 0.08 × 180,000 = KES 51,840

The common shock has a 2% annual probability and multiplies frequency and severity by 1.8 and 1.25, respectively. Its expected aggregate loss factor is *s = 1 + 0.02 × (1.8 × 1.25 − 1) = 1.025*. Applying the same factor in both tariff and predictive loss calculations gives posterior expected portfolio driving loss *L₀ΣwᵍJᵍs = KES 55,440*, expected non-driving loss *12,000s = KES 12,300*, and total expected pure loss of KES 67,740 per vehicle-year. The commercial residual to the KES 130,000 baseline is KES 62,260; this residual is a pricing layer, not an assertion that every part of it is a particular expense or capital amount.

For a neutral differentiated tariff, the pure-loss allocation uses the posterior joint relativities:

> Rᵍ = Jᵍ/A,     Pᵍ = C + 12,000s + (L₀As)Rᵍ

where *C* is the KES 62,260 residual. Because ΣwᵍRᵍ = 1, weighted average premium remains KES 130,000. This is a portfolio-level tariff allocation. Predictive claims use the underlying frequency and severity draws, not the tariff normaliser: simulated frequency is *Eλ₀θᵍ*, and simulated severity has mean *μ₀ωᵍ*, with the stated shock draw applied to both. The tariff normaliser does not reduce actual loss.

## 4. Posterior credibility and indicated tariff

| Group | Posterior frequency mean (90% interval) | Severity mean (90% interval) | Calibrated joint relativity (90% interval) | Expected driving loss / year | Neutral tariff / year |
|---|---:|---:|---:|---:|---:|
| Stable | 0.784 (0.606–0.980) | 0.946 (0.800–1.114) | 0.711 (0.561–0.859) | KES 39,428 | KES 113,988 |
| Volatile | 1.540 (1.184–1.953) | 1.134 (0.945–1.351) | 1.674 (1.329–2.023) | KES 92,800 | KES 167,360 |

Intervals are equal-tail 90% posterior intervals from the seeded 12,000-draw calculation. They describe uncertainty in group parameters/relativities, not a promise about an individual driver’s next claim. Predictive claim amounts and claim counts also include process variability and are reported separately.

The flat KES 130,000 tariff and neutral differentiated tariff have the same aggregate premium and the same portfolio claim distribution; risk differentiation reallocates the price by group. At the individual level, the stable tariff is KES 15,621 below the flat rate and the volatile tariff KES 36,449 above it. That difference must be evaluated against data sufficiency, customer treatment, applicable policy and the intended pricing authority before any use.

## 5. Separately modelled intervention and savings allocation

The 10% reduction in volatile-group frequency is an explicit scenario input. It is not inferred by the Bayesian relativity model and must not be presented as an observed Moove effect. In the hypothetical case, it reduces volatile driving pure loss by KES 9,280 per eligible vehicle-year. The scenario allocates 75% of this amount (KES 6,960) to a lower insurance tariff and 25% (KES 2,320) to the driver incentive. The volatile-group intervention premium becomes KES 160,400; stable remains KES 113,988. The weighted portfolio premium becomes KES 127,912 and expected driving loss falls by KES 2,784 per fleet vehicle-year.

Under the 50% package pass-through, the stable weekly package adjustment is −KES 153.96; the volatile adjustment after the incentive is +KES 247.70 relative to the KES 25,000 base fee. This reflects three separate flows: the insurer’s premium change, the portion passed through in the weekly package, and the additional performance incentive. For the volatile group, the driver receives half of the premium reduction plus the separate incentive; the operator retains the remaining savings after paying that incentive. The payment and eligibility rules would require explicit data definitions, review and audit in any real design.

## 6. Insurer profit test: annual 100-vehicle portfolio

Each simulation samples cohort risk parameters, applies an annual common-shock draw, generates driving and non-driving claims, samples occurrence/report/payment timing, and follows claim and reinsurance cash through the settlement tail. Premium is earned and collected evenly over 12 months for this portfolio ledger. Insurer cash is discounted monthly at 10% through the final reinsurance-recovery month.

| Annual portfolio measure | Flat / neutral relativity | Intervention scenario |
|---|---:|---:|
| Gross written/earned premium | KES 13.000m | KES 12.791m |
| Gross ultimate claims | KES 6.739m | KES 6.469m |
| — driving claims | KES 5.513m | KES 5.241m |
| — non-driving claims | KES 1.226m | KES 1.227m |
| Net ultimate claims after 20% quota share | KES 5.391m | KES 5.175m |
| Net reinsurance premium after ceding commission | KES 1.950m | KES 1.919m |
| Operating expenses | KES 3.380m | KES 3.326m |
| Claim expenses | KES 0.202m | KES 0.194m |
| 99.5% VaR of net claims | KES 13.093m | KES 12.533m |
| 99.5% TVaR of net claims | KES 14.491m | KES 14.001m |
| Illustrative economic capital (VaR − mean) | KES 7.702m | KES 7.358m |
| Cost of capital at 10% | KES 0.770m | KES 0.736m |
| Mean simulated profit after capital cost | KES 1.307m | KES 1.442m |
| 90% predictive interval for profit | −KES 1.158m to KES 3.434m | −KES 1.048m to KES 3.518m |
| Probability of negative profit in simulation | 15.8% | 13.41% |
| Break-even annual gross premium / vehicle | KES 107,852 | KES 103,473 |
| Insurer cash NPV after capital cost | KES 1.391m | KES 1.513m |

Mean profit is computed as gross premium less net reinsurance premium, operating expenses, net ultimate claims, claim expenses and the capital charge. The intervention scenario reduces premium because of the specified 75% premium-saving share; it improves expected profit in these draws because the assumed frequency reduction lowers retained claims and associated risk capital as well. It is a scenario comparison, not causal evidence.

The 99.5% VaR and TVaR use 8,000 predictive paths, giving only about 40 observations above the 99.5% empirical quantile. The tail metrics are therefore coarse simulation estimates and should be interpreted with Monte Carlo uncertainty. They are not local solvency, regulatory or economic-capital requirements. Sensitivity to a larger simulation count, alternative severity tails, common-shock assumptions and reinsurance terms is appropriate before drawing commercial conclusions.

## 7. Claim timing, reserves and liquidity

For the flat/neutral case, simulated mean gross claims paid by the end of month 12 are KES 4.437m, against KES 6.739m of ultimate incurred claims. Mean outstanding claims are KES 2.302m, comprising KES 1.462m reported outstanding and KES 0.840m IBNR. The incurred-to-date reserve identity reconciles exactly on every simulated path:

> Gross ultimate claims − gross paid by year-end − outstanding claims = KES 0

Mean ceded recoverable at year-end is KES 0.683m, including the quota-share share on incurred amounts not yet received. The payment and recovery lag creates liquidity pressure even when ultimate underwriting profit is positive. Insurer monthly cash flows are in the result CSVs, with claim payments extending beyond the 12-month exposure period.

## 8. Moove and driver operating ledgers

The portfolio operating ledger assumes 100 active vehicles, scheduled package collection, and the same fare, energy, household and maintenance inputs as the Mwendo operating case. The driver retains KES 56,000 of weekly fares after the platform share and pays KES 16,000 weekly energy cost. After household requirement of KES 12,000 and package payment of KES 25,000, pre-claim residual cash is KES 3,000 per week, or KES 156,000 per vehicle-year. The net contribution lost per day off road is (KES 56,000 − KES 16,000)/7 = KES 5,714.

| Portfolio operating measure, per 100 vehicles | Standard 12-day repairs | Expedited 2-day repairs |
|---|---:|---:|
| Mean fleet downtime (flat/neutral) | 344.95 days | 58.61 days |
| Mean downtime per vehicle | 3.45 days | 0.59 days |
| Operator gross retained repair cash | KES 881,228 | KES 881,228 |
| Expediting cash | KES 0 | KES 146,871 |
| Moove contribution before vehicle capex/debt/tax/depreciation | KES 102.599m | KES 102.452m |
| Moove contribution / vehicle-year | KES 1,025,988 | KES 1,024,519 |
| Driver take-home after household, package and downtime | KES 13.629m | KES 15.265m |
| Driver take-home / vehicle-year | KES 136,289 | KES 152,651 |
| Moove NPV for 12-month operating cash flow at 18% | KES 93.907m | KES 93.772m |
| Driver NPV for 12-month take-home at 10% | KES 12.949m | KES 14.502m |

Expedited repair is a trade-off in this case: the operator pays KES 5,000 per claim, while faster return to work improves driver take-home. It reduces average fleet downtime from 344.95 to 58.61 vehicle-days. The intervention scenario’s standard-repair figures are 329.61 fleet downtime days, KES 102.673m operator contribution and KES 138,905 driver take-home per vehicle-year. Its 12-month Moove and driver NPVs are KES 93.975m and KES 13.198m, respectively. These scenario projections use the claim count generated by the insurance simulation; they do not also add Mwendo’s single-claim repair case.

The Moove and driver NPVs discount month-end annual operating cash at the rates in the assumption file; insurer NPV discounts its monthly cash through the claim/reinsurance settlement tail. They exclude vehicle acquisition, debt service, tax and terminal asset value, which belong to the separate Mwendo financing ledger.

Driver-excess sensitivity is modelled as a transfer from the driver to Moove that reduces Moove’s KES 30,000 assumed retention per driving claim. Including the common-shock expected frequency factor, a KES 5,000 excess produces expected annual driver payments of KES 1,147 stable / KES 2,253 volatile per vehicle; a KES 10,000 excess produces KES 2,295 / KES 4,506. Corresponding expected operator retention becomes KES 5,737 / KES 11,266 at KES 5,000 excess, or KES 4,590 / KES 9,013 at KES 10,000. The base simulation uses zero excess; those alternatives are sensitivities, not recommended terms.

## 9. Separate bridge to the Mwendo 156-week case

The annual insurance projection above is a 100-vehicle risk and profit test. The Mwendo bridge asks a different question: how would the illustrative premium and weekly package pass-through interact with the existing financed-vehicle case over 156 weeks? It retains Mwendo’s own loan, household, package, collection, arrears, terminal transfer and dated annual insurance mechanics.

At the KES 130,000 flat rate, the 156-week case pays KES 390,000 total insurance cash. It reports driver cash surplus KES 468,000 uninterrupted, KES 399,429 with the scheduled repair case, and KES 456,571 with the expedited-repair case. Under neutral relativities, the stable profile uses KES 113,988 annual premium (KES 341,965 over 156 weeks) and weekly package adjustment −KES 153.96; the volatile profile uses KES 167,360 annual premium (KES 502,081 total) and +KES 359.23 weekly. Under the intervention tariff, the volatile profile’s annual premium is KES 160,400 (KES 481,201 total), with +KES 247.70 weekly package adjustment after the incentive.

Those 156-week figures are a bridge from premium assumptions into the existing financing and collections ledger. The annual 100-vehicle simulation separately projects claim frequency, ultimate costs, claim settlement and fleet downtime. Combining a Mwendo scheduled/expedited one-repair scenario with the portfolio’s simulated repair events would count downtime and repair cash twice.

## 10. Interpretation, model controls and next empirical step

This case shows how to move from exposure-normalised frequency and severity posteriors to a tariff allocation, predictive loss distribution, insurer profit test, reserve and cash schedule, fleet downtime, operator contribution and driver take-home. It also makes the key economic distinction explicit: a relativity changes who bears the existing portfolio cost; a measured intervention effect can change the portfolio cost. The intervention assumption should be tested separately through an approved, pre-specified design with eligible comparison groups, exposure offsets, collision/claim definitions, repair outcomes and stable follow-up.

Before an applied pricing or service decision, a real dataset would require exposure and event validation; claim-to-telematics matching; late-reporting development; severity trend and inflation; coverage, deductible and salvage terms; expense allocation; reinsurance treaty terms; vehicle and driver turnover; repair-network capacity; selection and attrition; customer affordability; subgroup uncertainty; calibration; and independent actuarial/model validation. Pilot results should report posterior credible intervals and predictive claim intervals, not only point estimates. Claims, policy and service decisions would require documented approval, data access, purpose limitation and human review under the institution’s governance and applicable rules.

## 11. Reproduction and files

From this project root, execute:

```powershell
python -m unittest research_lab.mobility_insurance_profit_case.test_model -v
python research_lab/mobility_insurance_profit_case/run_case.py
```

The first command runs eight tests covering conjugate updates, quantile calculation, weighted tariff normalisation, the separate intervention effect, claim/reserve reconciliation, downtime comparison, seeded reproducibility and the Mwendo annual-premium/weekly-fee bridge. The second command regenerates seeded results and monthly ledger CSVs. The 14 October 2026 run completed with all eight tests passing and zero claim-reserve reconciliation error.

Files:

- `research_lab/mobility_insurance_profit_case/assumptions.json` — complete parameter set and simulation seed.
- `research_lab/mobility_insurance_profit_case/model.py` — posterior, premium, claim, reserve, capital, cash-flow and Mwendo-bridge calculations.
- `research_lab/mobility_insurance_profit_case/test_model.py` — executable invariant tests.
- `research_lab/mobility_insurance_profit_case/run_case.py` — reproducible output builder.
- `research_lab/mobility_insurance_profit_case/output/summary.json` — compact results, posterior intervals and Mwendo bridge.
- `research_lab/mobility_insurance_profit_case/output/results.json` — full assumptions, results and monthly ledgers.
- `research_lab/mobility_insurance_profit_case/output/*.csv` — monthly insurer cash and Moove/driver operating ledgers by tariff scenario.

The result can inform the Bayesian Relativities × Moove article and pitch materials as a worked illustration. It should be kept explicitly hypothetical and should not be described as Moove’s observed experience or a validated intervention.
