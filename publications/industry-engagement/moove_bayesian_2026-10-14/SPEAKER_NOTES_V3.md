# Speaker notes — Bayesian Relativities × Moove

## Slide 01

Opening: this is a research partnership proposal, not an offer, quote, or claim about Moove’s own performance. All KES results are synthetic. The public Moove context is cited in the notes and in the source slide.

## Slide 02

These three questions structure the article and proposed collaboration. They separate estimation, intervention evaluation and commercial sustainability. Sources: [1]–[7] in the source notes.

## Slide 03

The public sources establish the business context and publicly described data classes. They do not establish current terms for a different market, insured portfolio results, pricing, driver outcomes or causal effects. A partner would select the target market and appropriate insurer/product. [1] M. Anand and G. Murthy, CGAP, 2023. [2] Moove UK Customer Hub. [3] Moove UK Privacy Policy.

## Slide 04

This is a proposed research architecture. Bayesian Relativities estimates risk distributions; Mwendo Pamoja connects financing and vehicle operating flows; Underwrite for Collection contributes evidence governance and intervention evaluation. The Moove lane denotes a possible application, subject to partnership and local terms. Sources: Bayesian Relativities paper [5]; Underwrite for Collection and Mwendo materials supplied in the shared project corpus.

## Slide 05

Equation terms: E is insured exposure; λ₀ is base claim frequency; θ is a frequency relativity; μ₀ is base severity; ω is severity relativity; L(non-drive) represents separately modelled non-driving expected losses. The specific model permits frequency–severity dependence, so joint posterior draws are used where appropriate. [4] Lee and Shi, 2019; [5] Bayesian Relativities paper.

## Slide 06

The frequency illustration uses Gamma–Poisson conjugacy. Severity updates use the case’s inverse-Gamma/Gamma model. Partial pooling links individual experience to group-level information; the credible interval describes uncertainty in underlying expected loss, while a predictive interval additionally includes random future claims. This supports human review with distributions, not just a point score. [5]–[7].

## Slide 07

The posterior means are frequency factors 0.7843 / 1.5401 and severity factors 0.9462 / 1.1340. Joint factors are calibrated draw-wise to a portfolio mean of one. Reported 90% intervals: stable 0.561–0.859; volatile 1.329–2.023. These are synthetic case results based on selected priors and claim summaries; they are not Moove pricing indicators. Sources: Bayesian Relativities paper [5], Belhadj et al. [6], Bühlmann [7].

## Slide 08

Group premiums are KES 113,988 and KES 167,360, weighted 70/30 to KES 130,000. In the profit test, flat and neutral designs have identical aggregate premium and claims distributions: neutral differentiation reallocates expected loss, not portfolio risk. It may affect participation, retention or selection in practice, which should be tested separately. [5]–[7].

## Slide 09

Do not interpret the 10% frequency change as an observed or promised outcome. A lower premium or changed tariff does not itself reduce loss. The simulation separately stipulates a 10% reduction in volatile-group frequency, and allocates the expected loss saving 75% to premium reduction and 25% to an operator-funded incentive. Estimate the intervention effect from a pre-specified design. [5], [11].

## Slide 10

Insurer profit after capital is a distinct result from operator contribution and driver take-home. Insurance pricing allocation belongs to the insurer-product terms; operator economics include contracted insurance costs and retention; driver economics include fees, costs, working days, incentives and take-home. Avoid adding the 156-week Mwendo financing illustration to the separate annual 100-vehicle insurance portfolio. [5], [8]–[11].

## Slide 11

The simulation uses a three-year synthetic history. Stable cohort: 756 10,000-km exposure units, 47 claims, KES 170,000 mean severity. Volatile: 324 units, 41 claims, KES 205,000 mean severity. Posterior draws: 12,000; predictive paths: 8,000; fixed seed: 20261014. A 2% common-shock probability with frequency 1.8 and severity 1.25 yields an expected shock load of 1.025, used consistently in indication and simulation. See case README and assumptions.json.

## Slide 12

Flat and neutral have identical aggregate insurer P&L. Intervention is a synthetic frequency sensitivity. Flat/neutral: mean after-capital profit KES 1.307m; 90% predictive interval −KES 1.158m to KES 3.434m; probability below zero 15.8%; break-even gross annual premium KES 107,852/vehicle. Intervention: KES 1.442m; interval −KES 1.048m to KES 3.518m; loss probability 13.4125%; break-even KES 103,473. Predictive intervals include parameter and process variation. [11] for capital/reinsurance profit-testing context; underlying case files for figures.

## Slide 13

Baseline: gross ultimate claims KES 6.739m; net claims after the 20% quota share KES 5.391m. By year-end, gross claims paid KES 4.437m, reported outstanding KES 1.462m, IBNR KES 0.840m, total outstanding KES 2.302m, ceded recoverable KES 0.683m. The model reconciles paid plus outstanding to ultimate claims (maximum error KES 0). Reporting and settlement delays are elected assumptions. Model incurred, paid and recoverable cash separately. Sources: ASOP 43 [8], IFRS 17 reinsurance guide [9], IAIS [10].

## Slide 14

Flat standard 12-day repair case: 344.95 total fleet downtime days (3.45/vehicle); operator contribution before vehicle capex, debt, tax and depreciation KES 102.599m across the portfolio; driver take-home KES 136,289/vehicle-year. Intervention standard repair: 329.61 fleet days; contribution KES 102.673m; driver take-home KES 138,905. Flat 2-day repair scenario: 58.61 fleet downtime days; take-home KES 152,651; fleet expedite cash KES 146,871 and contribution KES 102.452m. This is a separate 100-vehicle annual case. [2] gives public package context; numbers are entirely synthetic.

## Slide 15

Baseline empirical 99.5% net-loss VaR: KES 13.093m; TVaR: KES 14.491m; economic capital VaR minus mean net claims: KES 7.702m. The case has 8,000 predictive paths, so only about 40 paths support the upper 0.5% tail. These are coarse illustrative economic-capital estimates, not a regulatory capital result. Required next steps include larger-run convergence checks and scenario sensitivity over common shocks, treaty terms/recovery delays, claim maturity and capital cost. [8]–[10].

## Slide 16

A future pilot should estimate the intervention effect rather than reusing the assumed 10%. Define eligibility, intervention, treatment fidelity, exposure, claims development, comparison group and primary endpoints before launch. If driver-level randomisation is unsuitable, consider depot or time-based cluster assignment with appropriate design. Report intention-to-treat effects and uncertainty; claims must have sufficient maturity. Include customer outcomes, complaints and operational costs. [11].

## Slide 17

This slide describes a proposed data contract, not a production architecture or legal opinion. Specify permitted purpose, minimum necessary fields, access roles, retention, linkage, security, data quality, model/version lineage, approver and event outcome. Establish integration with the selected insurer and operator systems through documented interfaces. Data-protection review and a human review route are part of pilot design.

## Slide 18

Suggested first engagement: a scoping workshop with actuarial/pricing, claims, fleet operations, driver support, data and legal teams. The concrete output can be a market-specific data dictionary, baseline reconstruction plan, pre-analysis plan and pilot-readiness decision. The case makes no assertion that Moove has agreed to share data or run a pilot.

## Slide 19

Full source details and direct URLs are listed in SOURCE_AND_VALIDATION_NOTES.md. Model files: research_lab/mobility_insurance_profit_case/assumptions.json, model.py, run_case.py, test_model.py, output/summary.json and output/results.json. The 12,000 posterior / 8,000 predictive run passed eight unit tests and seeded reproducibility checks; claim reconciliation maximum error is zero.

