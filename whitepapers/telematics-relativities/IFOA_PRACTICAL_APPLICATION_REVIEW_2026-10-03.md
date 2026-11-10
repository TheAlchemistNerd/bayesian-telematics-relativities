# Bayesian Relativities: practical pricing, reserving and capital depth

**3 October 2026 — assessment of the current paper and executable submission evidence.**

## What is already substantial

The [paper](paper.md), [derivations](Mathematical_Derivations.md) and [implementation plan](DETAILED_IMPLEMENTATION_PLAN.md) cover much more than Gamma/negative-binomial introductions. They develop exposure, credibility, nonlinear rating, representation overlap, shrinkage, reserving, capital, risk transfer, validation and an IFRS 17 interface.

The [submission experiment](../../publications/submissions/brian-hey-2026/experiment/run_synthetic_comparison.py) supplies executable comparisons on 2,800 synthetic drivers and 18 months. It includes a future holdout, five model variants, a reserve illustration and capital/treaty outputs. The conditional-mode shrinkage approximation and synthetic representations should keep those accurate labels.

The relevant distinction is **SP8 pricing** versus **SP7 reserving and capital**. These applications share data and assumptions but have different targets and validation. [SP8 2026](https://actuaries.org.uk/media/wd5dljtc/sp8_syllabus-2026-_final-proof.pdf), [SP7 2026](https://actuaries.org.uk/media/2dinpmq4/sp7_syllabus-2026-_final-proof.pdf). [SA3](https://actuaries.org.uk/media/uekpxxaj/sa3_syllabus-2026-_final-proof.pdf) also motivates a coherent insurer business decision. The following work builds on current evidence rather than repeating the distribution theory.

## B1 — Choose complexity using calibration and business value

**Owner roles:** pricing analyst and model validation.

The [saved comparison](../../publications/submissions/brian-hey-2026/experiment/results/model_comparison.csv) gives M4 pure-premium error of about 14.51%, compared with 14.30% for M3. M4 severity deviance improves, while loss observed/expected remains about 1.170. The 90% predictive interval covers 9 of 12 region-quarter groups. Thus performance is mixed; the most complex model is not a uniform winner.

**Deliverables:** repeated time-based evaluations, grouped uncertainty intervals, cold-start and returning-driver comparisons, temporal calibration, ablations and an explicit decision on retaining each model component. Separate representation training from downstream fitting. Add full posterior computation only where it has a demonstrable uncertainty/decision benefit and supply diagnostics when used.

**Completion evidence:** no future information enters training or feature preparation; simpler challengers are evaluated on the same exposure and target; process and parameter uncertainty are reported separately; complexity earns a place through decision value and maintainable inputs. Twelve correlated portfolio groups alone are insufficient evidence of stable interval calibration.

## B2 — Reserving across valuation dates

**Owner roles:** reserving and claims-data teams.

The [reserve output](../../publications/submissions/brian-hey-2026/experiment/results/reserve_comparison.csv) shows absolute relative error falling from 12.37% for M0 to 3.73% for M4. In `reserve_estimate`, report/payment lag parameters match those used by the synthetic data generator. This is a useful internally consistent illustration; independently estimated development remains to be demonstrated.

**Deliverables:** dated paid/incurred claim histories and development triangles; information available at each valuation; granular reserve estimates and suitable aggregate challengers; gross, ceded and net reserve movements; run-off backtests under inflation and reporting/settlement changes. Distinguish reported outstanding claims, incurred-but-not-reported claims and later development on reported claims.

**Completion evidence:** delay parameters are fitted using only available historical observations; unresolved claims are handled explicitly; multiple valuation dates are reconciled. Provide uncertainty decomposition and empirical coverage, including a structural change in claims handling. The central estimate and its movement must explain actual emerging payments.

## B3 — Capital and treaty decision with tail uncertainty

**Owner roles:** capital modelling, reinsurance and independent validation.

The current `capital_and_treaty` uses 8,000 draws. A 99.5% tail then contains approximately 40 observations, so the estimate needs simulation-error analysis before it supports a material treaty or capital choice. Its assumed frequency/severity shocks also need an evidence basis and dependence challenge.

**Deliverables:** repeat-seed and increasing-simulation convergence; uncertainty intervals; several attachment/limit/retention choices; treaty price, reinstatement and recovery timing where relevant; counterparty/default stress and gross/net capital attribution.

**Completion evidence:** define the risk measure and horizon; quantify simulation error at the proposed decision tolerance; compare expected cost, tail retention and liquidity need. Distinguish aggregate stop-loss from per-occurrence cover. Include treaty premium and recoverability before concluding that a ceded expected loss is an economic benefit. Match any regulatory capital claim to an applicable authorised methodology.

## B4 — From loss cost to offered premium

**Owner roles:** pricing/product, distribution and conduct functions.

Add expenses, commission, reinsurance, capital remuneration and applicable tax assumptions to the technical loss estimate. Compare renewal prices with expected retention and selection under stated evidence, avoiding unsupported demand precision. Assess sparse segments, missing telematics, affordability and permitted rating factors.

**Deliverables:** premium bridge, target-market definition, constrained price alternatives, fairness/complaint review and a renewal scorecard.

**Completion evidence:** exposure is consistent across numerator and denominator; pricing factors have known ownership; a price change can be explained to the intended customer; proposed commercial margins reconcile to projected cash and claims. Monitor experience by cohort and explain changes in mix as well as changes in risk.

## B5 — One insurer planning and accounting handoff case

**Owner roles:** actuarial, Finance and the board decision maker.

Connect B1–B4 through new business, renewal, claims emergence, reinsurance, reserves, capital resources and distributions. Compare growth, repricing and treaty changes under a common scenario. Carry the measurement interface into a scoped IFRS 17 case only after contract grouping and the applicable measurement approach are defined; an expected-loss output is one input to that process.

**Deliverables:** multi-period insurer plan, decision memo, accounting input dictionary and actual-versus-expected bridge. Use [CP2](https://actuaries.org.uk/media/ujbbaef3/cp2_syllabus-2026-_final-proof.pdf) as a handover benchmark and [CP3](https://actuaries.org.uk/media/vsnpg4zm/cp3_syllabus-2026-_final-proof.pdf) for the board/customer communication exercise.

**Completion evidence:** cash, reserve, reinsurance asset and capital-resource movements reconcile; adverse inflation or delayed recoveries alter the recommendation; accounting outputs distinguish measurement components and business cash. SokoIntel can consume declared outputs and evidence metadata while this repository owns estimation methods.

## Release integrity and status

The [repository README](../../README.md) records an existing canonical-paper hash mismatch in the submission validator. Resolve it through an explained version reconciliation before describing the submission as a fully validated release; do not reset the expected hash merely to remove a failure.

This review inspected source and saved results; it did not rerun the experiment or validator. B1–B5 are **proposed developments**. The current synthetic results remain useful evidence with their stated limits. No guest repository or workbook was changed.
