# Detailed Implementation Plan for Advancing `paper.md`
## 1. Intended outcome
The revision will develop `paper.md` into a publication-quality actuarial and Insurtech white paper with five reinforcing qualities:
- A relatable human and microeconomic narrative centred on gig-economy motor risk.
- A coherent actuarial framework for exposure, frequency, severity, credibility and premium relativities.
- A technically credible neural and Bayesian architecture with explicit feature ownership.
- An integrated treatment of loss emergence, claim development, reserves, economic capital and risk transfer.
- A well-sourced governance framework covering ratemaking, fairness, data protection, model validation and the IFRS 17 measurement interface.
The paper’s original contribution will remain the exposure-normalised actuarial modulating variable. The revision will strengthen that contribution by showing precisely how telematics signals become actuarial frequency and severity relativities, how neural representations contribute incremental information, how hierarchical credibility stabilises sparse experience, how those estimates develop into paid and outstanding claims, and how the resulting loss distribution supports reserves, capital and reinsurance decisions.
The intended length will be approximately 10,000 to 12,000 words excluding references. Expansion will come from deeper explanations, worked examples, mathematical clarification, diagrams and implementation detail rather than repetition.
The prose will use constructive, affirmative language. Boundaries will be expressed by stating what each layer contributes:
- The physical measure estimates expected insured losses.
- The telematics service measures exposure and behaviour.
- The hierarchical model produces frequency, severity and uncertainty estimates.
- The tariff-calibration layer converts estimates into stable relativities.
- The claims-development layer converts incurred losses into settlement cash flows and reserve estimates.
- The economic-capital layer measures adverse deviation across underwriting, reserve, catastrophe, operational, counterparty and financial risks.
- The risk-transfer layer prices and monitors reinsurance protection against the gross loss distribution.
- The insurer’s pricing process incorporates expenses, reinsurance, capital and commercial objectives.
- The IFRS 17 process consumes governed cash-flow distributions for accounting measurement.
- The intervention layer turns acute safety signals into operational actions.
## 2. Preservation and working controls
Before revising the paper, create a timestamped backup containing:
- paper.md
- paper.docx
- guide.md
- outline.md
- research-note.md
- Mathematical_Derivations.md
- Semantic_Comparison_Notes.md
- validate.py
The backup manifest will record file paths, sizes, modification dates and SHA-256 hashes.
paper.md will become the single authoritative source. paper.docx will be treated as a generated publication artifact and rebuilt only after the Markdown passes semantic, mathematical and citation validation.
Supporting documents will retain distinct authority levels:
- guide.md and outline.md: writing intent and scope.
- research-note.md: conceptually reviewed research baseline.
- Mathematical_Derivations.md: derivation source requiring reconciliation.
- Root conversation fragments: idea provenance.
- paper.md: canonical publication text.
A correction ledger will map every material change to its current section and the issue it resolves. This makes the work traceable without inserting editorial commentary into the paper.
## 3. Revised narrative structure
The paper will retain its current title and central argument while adopting the following structure.
### Abstract
The abstract will present the complete contribution in six moves:
1. Gig drivers produce highly variable exposure and risk conditions.
2. Raw telematics scores are difficult to use directly as actuarial prices.
3. The paper separates claim frequency, conditional severity and non-driving losses.
4. Cross-fitted neural residualisation contributes incremental sequence information.
5. Hierarchical credibility and explicit calibration translate those estimates into stable tariff relativities.
6. The posterior loss distribution flows into claim reserves, economic capital and risk-transfer decisions.
IFRS 17 will be described as an accounting-measurement interface rather than a ratemaking standard.
The abstract will end with the practical result: a framework that supports usage-based pricing, safety intervention, reserving, capital management and governed portfolio learning while maintaining stable actuarial tariff foundations.
### Section 1: The human and economic setting
The introduction will open with a relatable comparison between two gig drivers who may share the same vehicle class and territory but experience different:
- Distances driven.
- Operating hours.
- Road environments.
- Traffic density.
- Fatigue accumulation.
- Vehicle utilisation.
- Weather exposure.
- Claim-free experience.
This story will establish the distinction between:
- Exposure: how much the vehicle operates.
- Frequency risk: expected claims per exposure unit.
- Severity risk: expected cost when a claim occurs.
- Temporary safety state: an acute condition that may warrant intervention.
- Persistent actuarial risk: evidence that can support a future tariff adjustment.
- Claims development: the time between occurrence, reporting, case estimation and payment.
- Capital risk: the adverse loss variation the insurer must be able to absorb.
- Risk transfer: the contractual allocation of selected loss layers to reinsurers or capital-market counterparties.
The paper will position GLMs and established tariff cells as the starting foundation. Telematics will enrich that foundation through new exposure and behavioural evidence.
The objectives will become:
1. Define exposure-consistent claim frequency and severity models.
2. Construct transparent actuarial modulating variables.
3. connect hierarchical Bayes to actuarial credibility.
4. integrate explicit telematics variables and neural sequence representations.
5. establish dynamic updating, calibration and governance controls.
6. Extend the model from expected loss into claim development, reserves and capital.
7. Price and monitor risk-transfer structures against gross and net loss distributions.
8. Describe the production data architecture and controlled pilot pathway.
### Section 2: Actuarial foundations
This section will contain four foundations.
### 2.1 Physical-measure loss estimation
The paper will explicitly define \(\mathbb P\) as the real-world probability measure used for:
- Claim frequency.
- Claim severity.
- Exposure forecasting.
- Claims cash-flow projection.
- Reserve distributions.
- Reinsurance analysis.
- Operational underwriting.
- Portfolio stress testing.
- Economic-capital simulation.
The discussion of incomplete markets will remain concise and purposeful. It will explain why actual motor losses are estimated from insured experience and exposure rather than derived from a replicating financial portfolio.
### 2.2 Classical credibility
The Bühlmann and Bühlmann-Straub framework will be presented accurately as a variance-components credibility system.
The paper will explain:
\[
\widehat{\Theta}_i
=
Z_i\overline X_i+(1-Z_i)m,
\]

where \(Z_i\) represents the weight attached to the risk’s own experience.
The distinction between credibility and uncertainty will be explicit:
- Credibility describes the degree of reliance on individual experience.
- Posterior intervals describe remaining uncertainty.
- Partial pooling produces credibility-like shrinkage.
- Posterior predictive distributions show the range of future outcomes.
### 2.3 Hierarchical credibility
Hierarchical Bayes will be presented as an extension of credibility into multiple interacting levels:
- Driver.
- Vehicle class.
- Geographic zone.
- Platform or fleet.
- Time period.
- Exposure regime.
This section will explain how partial pooling supports new drivers, sparse corridors and emerging vehicle classes.
### 2.4 Premium architecture
The paper will establish a controlled terminology ladder:

```text
Expected driving losses
+ Expected non-driving losses
= Pure risk cost

Pure risk cost
+ Expenses
+ Expected reinsurance cost
+ Capital and profit provision
+ Taxes and levies
= Commercial premium
```

The IFRS 17 risk adjustment, regulatory capital, internal economic capital and contractual service margin will remain distinct concepts.
## 4. Canonical mathematical model
### 4.1 Notation register
A notation table will be placed before the core model.
| Symbol | Meaning |
|---|---|
| \(i\) | Driver or insured vehicle |
| \(t\) | Observation and exposure period |
| \(k\) | Claim within a period |
| \(d\) | Claim-development or payment period |
| \(c(i)\) | Conventional tariff cell |
| \(g(i,t)\) | Geographic operating cluster |
| \(v(i)\) | Vehicle class |
| \(E_{it}\) | Validated exposure |
| \(N_{it}\) | Claim count |
| \(Y_{itk}\) | Ultimate cost of claim \(k\) |
| \(P_{itkd}\) | Payment on claim \(k\) in development period \(d\) |
| \(\lambda_{it}\) | Claim frequency per exposure unit |
| \(m_{it}\) | Conditional expected claim severity |
| \(\theta_i\) | Driver frequency frailty |
| \(\Omega_i\) | Driver severity multiplier |
| \(\widetilde{\mathbf h}_{it}\) | Residualised neural representation |
| \(M^{f}_{it}\) | Frequency relativity |
| \(M^{s}_{it}\) | Severity relativity |
| \(M^{pp}_{it}\) | Combined pure-premium relativity |
| \(R_t\) | Outstanding claims reserve at valuation time \(t\) |
| \(L^{G}\), \(L^{N}\) | Gross and net loss |
| \(EC_q\) | Economic capital at confidence level \(q\) |


This will eliminate the current reuse of \(\mu\), \(\lambda\), \(\nu\), \(\phi\) and related symbols.
### 4.2 Frequency model
The paper will use the Poisson-Gamma representation as the canonical hierarchical frequency model:
\[
N_{it}\mid\theta_i,\lambda_{it},E_{it}
\sim
\operatorname{Poisson}
\left(E_{it}\lambda_{it}\theta_i\right),
\]

with:
\[
\theta_i\sim\operatorname{Gamma}(a_\theta,b_\theta),
\qquad
\mathbb E[\theta_i]=\frac{a_\theta}{b_\theta}=1.
\]

Integrating out \(\theta_i\) produces the Negative-Binomial marginal distribution. This gives the paper both overdispersion and exact Gamma-Poisson updating without introducing a duplicate driver random effect.
The baseline frequency predictor will be:
\[
\log\lambda_{it}
=
\log\lambda_{0,c(i)}
+
f_f(\mathbf X_{it})
+
\boldsymbol{\beta}_{h,f}^{\top}\widetilde{\mathbf h}_{it}
+
u^{f}_{g(i,t)}
+
u^{f}_{v(i)}
+
\delta^f_t.
\]

Here:
- \(\lambda_{0,c(i)}\) is the conventional tariff-cell rate.
- \(f_f(\mathbf X_{it})\) contains explicit actuarial variables and splines.
- \(\widetilde{\mathbf h}_{it}\) contains residual neural information.
- Geographic and vehicle effects provide group-level pooling.
- \(\delta_t^f\) captures a governed temporal state.
The meaning of exposure will be fixed for each model deployment. Kilometres, insured hours and trips will not be mixed inside a single fitted offset without a formal conversion.
### 4.3 Severity model
Individual claim severity will be represented as:
\[
Y_{itk}\mid \Omega_i,m_{it}
\sim
\operatorname{Gamma}
\left(
\kappa,
\frac{\kappa}{m_{it}\Omega_i}
\right),
\]

where the second Gamma parameter is explicitly identified as a rate. Therefore:
\[
\mathbb E[Y_{itk}\mid\Omega_i,m_{it}]
=
m_{it}\Omega_i.
\]

The driver severity multiplier will use:
\[
\Omega_i
\sim
\operatorname{InverseGamma}(a_\Omega,b_\Omega),
\qquad
\mathbb E[\Omega_i]
=
\frac{b_\Omega}{a_\Omega-1}.
\]

Its prior will be calibrated to a mean of one.
The severity predictor will be:
\[
\log m_{it}
=
\log m_{0,c(i)}
+
f_s(\mathbf X_{it})
+
\boldsymbol{\beta}_{h,s}^{\top}\widetilde{\mathbf h}_{it}
+
u^{s}_{g(i,t)}
+
u^{s}_{v(i)}
+
\delta^s_t.
\]

The paper will describe the Gamma distribution as a practical positive, right-skewed baseline. Tail diagnostics will determine whether a lognormal, GB2, Pareto layer or large-loss mixture provides a stronger fit for high-severity claims.
### 4.4 Pure premium
The general posterior expected driving loss will be:
\[
PP^{\mathrm{drive}}_{it}
=
E_{it}
\,
\mathbb E_{\mathbb P}
\left[
\lambda_{it}\theta_i
m_{it}\Omega_i
\mid
\mathcal D_t
\right].
\]

When frequency and severity are conditionally independent given the modeled latent state and covariates, this expectation factorises into the product of expected frequency and expected severity.
The paper will add:
\[
PP_{it}
=
PP^{\mathrm{drive}}_{it}
+
PP^{\mathrm{non-drive}}_{it},
\]

where non-driving losses include relevant theft, fire, catastrophe, vandalism and stationary-vehicle exposures.
## 5. Actuarial modulating variables and neutrality
The separate diagnostic relativities will be:
\[
M^f_{it}
=
\frac{\lambda_{it}}{\lambda_{0,c(i)}},
\qquad
M^s_{it}
=
\frac{m_{it}}{m_{0,c(i)}}.
\]

Their uncalibrated combined relativity is:
\[
M^{pp}_{it}=M^f_{it}M^s_{it}.
\]

The final pure-premium calibration will use baseline expected-loss weights:
\[
w^{0}_{it}
=
E_{it}\lambda_{0,c(i)}m_{0,c(i)}.
\]

Within tariff cell \(c\), define:
\[
A_{c,t}
=
\frac{
\sum_{i\in c}w^0_{it}M^{pp}_{it}
}{
\sum_{i\in c}w^0_{it}
}.
\]

The calibrated relativity becomes:
\[
M^{pp,*}_{it}
=
\frac{M^{pp}_{it}}{A_{c,t}}.
\]

This produces:
\[
\frac{
\sum_{i\in c}w^0_{it}M^{pp,*}_{it}
}{
\sum_{i\in c}w^0_{it}
}
=
1.
\]

This calibration layer, rather than neural residualisation, will be identified as the mechanism producing tariff neutrality.
The paper will also discuss:
- Calibration on the training portfolio.
- Validation on out-of-time exposure.
- Stability corridors around one.
- Credibility-weighted blending for sparse cells.
- Caps on period-to-period premium movement.
- Treatment of emerging risk trends requiring an approved base-rate update.
## 6. Explicit features and neural representations
### 6.1 Feature ownership
The model will distinguish three feature families:
1. Contract and exposure variables.
2. Explicit telematics and contextual variables.
3. Neural sequence representations.
Explicit features will include interpretable measurements such as:
- Exposure duration and distance.
- Night-driving proportion.
- Hard-braking rate per 100 kilometres.
- Speed volatility.
- Cornering intensity.
- Fatigue accumulation.
- Road-class distribution.
- Vehicle-condition indicators.
- Data-quality and sensor-reliability flags.
Raw high-frequency sequences will feed the GRU. The explicit feature path will feed the actuarial model directly. The same engineered metric will have one canonical owner.
### 6.2 Cross-fitted representation residualisation
The paper will rename the current procedure “cross-fitted neural representation residualisation.”
For training fold \(k\):
\[
\widehat m_{-k}(\mathbf X)
=
\widehat{\mathbb E}_{-k}
[
\boldsymbol{\Phi}\mid\mathbf X
],
\]

and:
\[
\widetilde{\mathbf h}_{it}
=
\boldsymbol{\Phi}_{it}
-
\widehat m_{-k(i)}(\mathbf X_{it}).
\]

The paper will explain that this construction:
- Reduces information duplication.
- Makes the neural contribution more interpretable as incremental predictive content.
- Supports coefficient stability.
- Reduces sensitivity to correlations with explicit rating variables.
- Preserves a testable separation between model branches.
Diagnostics will include:
- Cross-covariance with explicit variables.
- Nonlinear predictability of the residual embedding from explicit features.
- Variance inflation and condition numbers.
- Out-of-time stability.
- Ablation tests.
- Incremental log score or deviance improvement.
- Group-level calibration.
Optional whitening will occur only after residualisation, using parameters estimated inside each training fold.
### 6.3 Horseshoe shrinkage
A regularised horseshoe prior will control the neural bottleneck:
\[
\beta_{h,j}
\sim
\mathcal N
\left(
0,
\tau_h^2\widetilde{\lambda}_j^2
\right),
\]

with:
\[
\widetilde{\lambda}_j^2
=
\frac{
c^2\lambda_j^2
}{
c^2+\tau_h^2\lambda_j^2
},
\qquad
\lambda_j\sim C^+(0,1).
\]

Separate global shrinkage parameters will be used for:
- Neural components.
- Explicit feature interactions.
- Spline components.
- Contextual effects.
This supports sparse incremental contributions while preserving large signals supported by the data. The paper will describe shrinkage, residualisation and optional whitening as complementary controls.
## 7. Temporal and dependence modeling
The temporal component will use a stationary AR(1) state:
\[
\delta_t-\mu_\delta
=
\rho_\delta
(\delta_{t-1}-\mu_\delta)
+
\epsilon_t,
\qquad
|\rho_\delta|<1.
\]

The paper will distinguish:
- Persistent driver risk.
- Temporary fatigue.
- Road and weather state.
- Vehicle deterioration.
- Platform operating conditions.
- Portfolio-wide calendar effects.
The dependence section will begin with shared latent states and hierarchical effects. These mechanisms can explain much of the observed relationship between claim frequency and severity.
An advanced extension will examine residual tail dependence after conditioning. Copula use will specify:
- The exact marginal variables.
- Treatment of discrete claim counts.
- Estimation method.
- Tail direction.
- Diagnostic evidence supporting the selected family.
- Comparison with shared-random-effect and marked point-process models.
SPV waterfall mechanics will leave this section. Insurance-oriented aggregate-loss simulation, reinsurance attachment, claim settlement timing and catastrophe accumulation may remain.
## 8. Sequential credibility updating
The dynamic updating equations will preserve posterior sufficient statistics.
Frequency:
\[
a^\theta_{i,t}
=
a^\theta_{i,t-1}
+
\Delta N_{it},
\]

\[
b^\theta_{i,t}
=
b^\theta_{i,t-1}
+
\sum_{s\in t}
E_{is}\lambda_{is}.
\]

The posterior mean is:
\[
\mathbb E[\theta_i\mid\mathcal D_t]
=
\frac{a^\theta_{i,t}}{b^\theta_{i,t}}.
\]

A claim-free exposure period contributes evidence gradually through the denominator. Pricing actions will respect minimum credibility, smoothing and approved review intervals.
Severity:
\[
a^\Omega_{i,t}
=
a^\Omega_{i,t-1}
+
\kappa\Delta N_{it},
\]

\[
b^\Omega_{i,t}
=
b^\Omega_{i,t-1}
+
\kappa
\sum_{k=1}^{\Delta N_{it}}
\frac{Y_{itk}}{m_{it}}.
\]

When no claim occurs, the previous severity posterior remains in force.
The paper will distinguish:
- Streaming exposure and safety-state updates.
- Claim-event credibility updates.
- Periodic tariff recalculation.
- Scheduled global-model refitting.
- Full posterior recalibration after material drift.

## 9. Loss emergence and reserve modeling

### 9.1 Gross loss architecture

The paper will extend the frequency-severity engine into a full aggregate-loss representation. For valuation period \(t\), gross ultimate loss will be:

\[
L_t^{G}
=
\sum_i\sum_{k=1}^{N_{it}}Y_{itk}
+
L_t^{\mathrm{cat}}
+
L_t^{\mathrm{expense}},
\]

where attritional claims, large individual losses, catastrophe accumulation and allocated claim expenses are separately identifiable.

The model will distinguish:

- Claim occurrence date.
- Claim reporting date.
- Case-estimate revisions.
- Partial payment dates.
- Closure and reopening.
- Salvage and subrogation.
- Legal and claims-handling expenses.
- Repair-cost and social inflation.

The telematics model estimates the occurrence process and conditional loss amount. A claims-development layer translates ultimate losses into reported, incurred and paid cash-flow patterns. This creates a common actuarial spine from exposure and behaviour through pricing, reserving, capital and risk transfer.

### 9.2 Reporting and settlement delays

For claim \(k\), the paper will introduce reporting delay \(D^{R}_{itk}\) and settlement delay \(D^{S}_{itk}\). These may use discrete-time survival, hazard or state-transition models conditioned on:

- Claim type and cause of loss.
- Injury involvement.
- Vehicle damage class.
- Repair network.
- Geographic area.
- Litigation indicator.
- Data completeness.
- Calendar and inflation effects.

The payment process will be represented through incremental payments \(P_{itkd}\), satisfying:

\[
Y_{itk}
=
\sum_{d\geq 0}P_{itkd}
-
\operatorname{Salvage}_{itk}
-
\operatorname{Subrogation}_{itk}.
\]

The model will preserve nominal and inflation-adjusted views so that severity trends and settlement timing remain identifiable. Reported, incurred and paid datasets will share stable claim identifiers and valuation timestamps.

### 9.3 Outstanding claim reserves

At valuation time \(T\), the outstanding claims reserve will be defined as the conditional expectation of future claim payments:

\[
R_T^{\mathrm{claims}}
=
\mathbb E_{\mathbb P}
\left[
\sum_{t\leq T}
\sum_i
\sum_{k=1}^{N_{it}}
\sum_{d:\,t+d>T}
P_{itkd}
\mid
\mathcal F_T
\right].
\]

The reserve decomposition will cover:

- Reported but not settled claims.
- Incurred but not reported claims.
- Incurred but not enough reported development.
- Claim-handling expenses.
- Reopened claims.
- Expected salvage, subrogation and reinsurance recoveries.

The individual-claim Bayesian model will be reconciled to established aggregate reserving benchmarks, including chain-ladder, Bornhuetter-Ferguson, expected-loss-ratio and overdispersed-Poisson approaches. This benchmark comparison will provide an interpretable bridge between granular telematics evidence and established reserving controls.

The paper will distinguish the liability for incurred claims from the liability for remaining coverage in the IFRS 17 measurement architecture. Pricing, reserve adequacy and accounting measurement will share reconciled data while retaining their respective purposes and governance.

### 9.4 Reserve uncertainty and validation

Reserve output will include:

- Central estimate.
- Predictive distribution.
- Process uncertainty.
- Parameter uncertainty.
- Model and assumption sensitivity.
- Calendar and inflation scenarios.
- Gross, ceded and net views.

Back-testing will compare successive valuations against emergence by accident period, report period, product, vehicle class and geographic cohort. The validation suite will track one-year reserve deterioration, ultimate runoff, paid-versus-incurred consistency and the stability of telematics-driven segmentation.

The paper will distinguish the actuarial reserve distribution from the IFRS 17 risk adjustment and economic capital. Each uses related loss information for a different decision purpose.

## 10. Economic capital modeling

### 10.1 Capital objective and horizon

Economic capital will be defined as the insurer’s internal assessment of capital required to absorb adverse deviation over a specified horizon and confidence level. The paper will state the selected horizon, loss definition and risk measure before presenting results.

For a one-year loss variable \(L_{1y}\), a value-at-risk representation may be written as:

\[
EC_q^{\mathrm{VaR}}
=
\operatorname{VaR}_q(L_{1y})
-
\mathbb E[L_{1y}],
\]

with a tail-value-at-risk view:

\[
EC_q^{\mathrm{TVaR}}
=
\operatorname{TVaR}_q(L_{1y})
-
\mathbb E[L_{1y}].
\]

The selected convention will remain consistent throughout the paper and its worked example. The paper will provide both one-year change-in-own-funds and ultimate-loss perspectives where they support different management questions.

### 10.2 Risk modules

The economic-capital model will cover:

- Premium and underwriting risk.
- Reserve deterioration risk.
- Catastrophe and geographic accumulation risk.
- Reinsurance counterparty credit risk.
- Market risk affecting invested assets and discounting.
- Liquidity risk arising from claim-payment timing.
- Operational, cyber, data and model risk.
- Concentration in platforms, fleets, vehicle technology and repair networks.

The paper will show how the telematics posterior contributes to underwriting-risk distributions while the reserve model contributes runoff and one-year deterioration. Common economic, geographic and event states will preserve dependence across modules.

### 10.3 Aggregation and diversification

Risk aggregation will use a transparent dependency architecture supported by historical evidence, scenario analysis and expert review. The paper will compare:

- Variance-covariance aggregation for initial management views.
- Copula or common-shock simulation where tail dependence is material.
- Scenario aggregation for catastrophe, cyber and operational events.
- Nested simulation where future management actions and reserve revaluation materially affect the one-year result.

Diversification will be recognised after dependencies are calibrated. Concentration stresses will show how the benefit changes when drivers share roads, platforms, vehicle types, repair networks or weather systems.

### 10.4 Capital allocation and pricing use

Portfolio economic capital will be allocated to product and cohort levels using a governed method such as Euler allocation under a differentiable risk measure. The allocated capital will support:

- Risk-adjusted return on capital.
- Product and corridor profitability.
- Reinsurance optimisation.
- Growth and concentration limits.
- Pricing margins.
- Management-action thresholds.

The paper will distinguish:

- Regulatory capital: the legally prescribed solvency requirement.
- Economic capital: the insurer’s internal risk assessment.
- IFRS 17 risk adjustment: compensation for non-financial uncertainty in contract measurement.
- Commercial capital provision: the amount incorporated into pricing and business planning.

## 11. Risk-transfer pricing and monitoring

### 11.1 Reinsurance structures

The paper will assess risk transfer through structures suited to the modeled portfolio:

- Quota-share reinsurance.
- Per-risk excess of loss.
- Per-event catastrophe excess of loss.
- Aggregate excess of loss or stop loss.
- Adverse-development protection for reserve risk.
- Facultative cover for exceptional vehicles or limits.

Each structure will be linked to the underlying risk it addresses. Attritional volatility, large claims, catastrophe accumulation and reserve deterioration will use distinct attachment and exhaustion analyses.

### 11.2 Layer loss and technical price

For an occurrence loss \(L^G\), a simple excess-of-loss recovery with attachment \(A\) and limit \(U\) will be:

\[
L^{\mathrm{ceded}}
=
\min\left((L^G-A)^+,U\right).
\]

Net loss will be:

\[
L^N
=
L^G
-
L^{\mathrm{ceded}}
+
L^{\mathrm{counterparty\ shortfall}}.
\]

The technical reinsurance price will be decomposed into:

\[
\Pi^{RI}
=
\mathbb E[L^{\mathrm{ceded}}]
+
\operatorname{RiskLoad}
+
\operatorname{ExpenseLoad}
+
\operatorname{Brokerage}
+
\operatorname{ReinstatementCost}
+
\operatorname{CapitalMargin}.
\]

The analysis will compare experience rating, exposure rating and catastrophe-model output where applicable. Pricing will use the same versioned gross loss distribution that supports reserves and economic capital.

### 11.3 Capital efficiency and retained risk

The economic value of a treaty will be assessed through:

- Expected ceded loss.
- Reduction in gross loss volatility.
- Reduction in VaR or TVaR capital.
- Counterparty credit cost.
- Basis risk.
- Liquidity benefit.
- Reinstatement exposure.
- Ceding commission and profit commission.
- Net risk-adjusted return.

A capital-efficiency measure may be expressed as:

\[
\operatorname{CapitalEfficiency}
=
\frac{
EC_q^{G}-EC_q^{N}
}{
\Pi^{RI}-\mathbb E[L^{\mathrm{ceded}}]
},
\]

subject to consistent treatment of expenses, commissions and counterparty risk.

### 11.4 Continuous treaty monitoring

The monitoring framework will track:

- Attachment probability.
- Expected and realised layer loss.
- Limit utilisation and exhaustion probability.
- Reinstatement count and cost.
- Aggregate deductible erosion.
- Ceded and net loss ratios.
- Claims recoverable ageing and disputed balances.
- Reinsurer credit quality, collateral and concentration.
- Treaty exclusions and data-reporting compliance.
- Premium and exposure drift.
- Changes in geographic, platform and vehicle concentration.
- Model-versus-treaty basis risk.

The telematics architecture will provide early evidence of portfolio-mix and exposure changes. Treaty repricing and renewal analysis will use governed exposure snapshots and reconciled gross-to-net loss data.

## 12. Validation and governance
Validation will be organised by modeled quantity.
Frequency validation:
- Count calibration.
- Exposure-adjusted residuals.
- Negative-Binomial deviance.
- Zero-count reproduction.
- Tail count reproduction.
- Out-of-time and cohort calibration.
Severity validation:
- Conditional mean calibration.
- Quantile calibration.
- Tail exceedance plots.
- Proper continuous scores.
- Large-loss sensitivity.
- Inflation and repair-cost drift.
Aggregate validation:
- Posterior predictive aggregate losses.
- Frequency-severity composition.
- Reinsurance-layer losses.
- Geographic accumulation.
- Calendar-period stress.

Reserve and aggregate-loss validation will add:

- Paid and incurred emergence by development period.
- Reserve runoff and one-year deterioration.
- Gross-to-net and ceded-recovery reconciliation.
- Reinsurance-layer loss reproduction.
- Large-loss and catastrophe accumulation tests.

Capital and risk-transfer validation will add:

- VaR and TVaR stability.
- Sensitivity to dependency assumptions.
- Reverse stress tests.
- Treaty attachment, erosion and exhaustion tests.
- Reinsurer-default and collateral scenarios.
- Capital-allocation reconciliation.
Bayesian computation:
- Rank-normalised split \(\widehat R\).
- Bulk and tail effective sample size.
- Divergent transitions.
- Energy diagnostics.
- Prior-to-posterior sensitivity.
- Centred versus non-centred parameterisation tests.
Fairness governance will use measures suitable for insurance pricing and count outcomes. Equalized odds will be reserved for an explicitly defined classification decision. Pricing assessment will include:
- Calibration by relevant group.
- Relative-error and residual analysis.
- Distribution of premium changes.
- Proxy and feature-provenance review.
- Geographic infrastructure effects.
- Intersectional stability.
- Appeal and human-review pathways.
- Controlled intervention trials.
Acute safety signals will lead to supportive, contractually governed actions such as warnings, rest recommendations, routing assistance or human review. Premium revisions will follow the insurer’s approved pricing cycle.
## 13. IFRS 17 and insurance-finance interface
The accounting section will explain that the model supplies:
- Expected claim amounts.
- Claim timing distributions.
- Exposure projections.
- Lapse and policy-state assumptions.
- Uncertainty distributions.
- Scenario outputs.
- Gross, ceded and net claim cash flows.
- Data and model lineage.
The insurer’s IFRS 17 process will then combine these with:
- Contract boundaries.
- Directly attributable expenses.
- Discount rates.
- Risk adjustment methodology.
- Grouping and onerous-contract assessment.
- Contractual service margin mechanics.
The posterior HDI will be presented as model information that can inform risk analysis. The selected IFRS 17 risk-adjustment technique will remain an entity-governed accounting decision consistent with the IFRS Foundation’s measurement framework.
IPF content will be limited to the operational interface between policy status, premium payment and insurer cash. Lender-owned finance receivables will remain outside the insurance pure-premium, reserve and economic-capital calculations unless counterparty exposure is expressly modeled.

## 14. Production architecture
Appendix B will be reorganised around two ingestion paths:

```text
Vehicle sensors
      ↓
Device gateway and event streaming
      ↓
Flink event-time processing
  ↙                     ↘
Sequence windows       Explicit actuarial features
  ↓                     ↓
GRU encoder            Feature store
  ↘                     ↙
Cross-fitted residual representation
             ↓
Hierarchical frequency-severity engine
             ↓
Loss, reserve and capital simulation
             ↓
Calibration, risk transfer, governance and intervention
```

Transactional CDC will serve policy, billing, claims and reference-data events. Raw 10 Hz telemetry will enter through a device ingestion service rather than first being persisted as ordinary transactional rows.
The appendix will add:
- Device orientation correction.
- Clock synchronisation.
- GPS accuracy controls.
- Map matching.
- Missingness indicators.
- Sensor calibration.
- Duplicate and late-event handling.
- Event-time watermarks.
- Consent and retention controls.
- Point-in-time feature reconstruction.
- Training-serving consistency.
- Exposure-ledger reconciliation.
- Claim-event and payment-ledger reconciliation.
- Treaty and recoverable master-data controls.
- Valuation-date snapshots for reserves and capital.
Thresholds such as hard braking, jerk and fatigue duration will be described as configurable pilot parameters supported by empirical calibration and local safety policy.
## 15. Citation reconstruction
The existing seven-entry reference list will be rebuilt after the prose stabilises.
The new source hierarchy will prioritise:
1. Standards, regulators and legislation.
2. Foundational actuarial and statistical literature.
3. Peer-reviewed telematics research.
4. Official technical documentation.
5. Carefully selected professional implementation material.
The bibliography should contain approximately 45 to 65 substantive sources covering:
- Bühlmann and Bühlmann-Straub credibility.
- Hierarchical actuarial models.
- Frequency-severity and aggregate-loss modeling.
- UBI and telematics ratemaking.
- Cross-fitting and orthogonal scores.
- Representation residualisation.
- Regularised horseshoe priors.
- Bayesian computation and \(\widehat R\).
- Claim development and stochastic reserving.
- Chain-ladder, Bornhuetter-Ferguson and granular reserving.
- Economic capital, VaR, TVaR and capital allocation.
- Reinsurance pricing, exposure rating and treaty monitoring.
- Fairness in regression and insurance pricing.
- IFRS 17.
- Kenyan insurance and data-protection requirements.
- Kafka, Flink and streaming correctness.
IEEE references will be numbered by first appearance. Every number will resolve to one source, every source will support its adjacent claim, and every retained reference will be cited in the body.
## 16. Editorial and structural refinement
The revision will:
- Repair broken mathematical expressions and code fences.
- Consolidate the duplicated conjugacy sections.
- Correct section numbering.
- Introduce Appendix A before Appendix B.
- Add Appendix C for loss, reserve, capital and risk-transfer formulas.
- Standardise British spelling, including “normalised,” “behavioural” and “residualisation.”
- Restore “Bühlmann-Straub” throughout.
- Define every symbol before use.
- Replace repeated intensifiers with precise technical verbs.
- Add short transitions between actuarial, computational and governance sections.
- Keep equations close to their interpretation.
- Add a worked driver example carried through exposure, frequency, severity, credibility, reserve development, economic capital and net retained loss.
- Add five publication-quality diagrams:
  - Model and feature architecture.
  - Actuarial premium construction.
  - Sequential credibility and intervention cycle.
  - Claims development and reserve emergence.
  - Gross loss, reinsurance recovery and net capital flow.

The conclusion will return to the opening driver narrative and explain how the framework converts continuous observation into proportionate, credible and governable insurance decisions across pricing, safety, claims, reserves, capital and risk transfer.

## 17. Implementation sequence

The work will proceed in controlled phases:

1. Create the source backup and correction ledger.
2. Freeze the notation and feature-ownership registers.
3. Repair the frequency, severity and pure-premium equations.
4. Implement explicit tariff-neutrality calibration.
5. Reconstruct neural residualisation and horseshoe shrinkage.
6. Reframe temporal states and dependence modeling.
7. Correct sequential credibility updating.
8. Add claim-development and reserve modeling.
9. Add economic-capital aggregation and allocation.
10. Add risk-transfer pricing and monitoring.
11. Rebuild validation, fairness and IFRS 17 interfaces.
12. Reconstruct the production architecture and diagrams.
13. Rebuild IEEE citations in order of appearance.
14. Perform semantic, mathematical and visual quality assurance.
15. Regenerate `paper.docx` from the approved Markdown.

## 18. Verification and definition of done
The revision will be complete when:
- Exposure is applied exactly once.
- Frequency rate and expected count use distinct notation.
- Driver frailty has one canonical representation.
- Severity-prior parameters are unambiguous.
- Zero-claim periods retain the previous severity posterior.
- Tariff neutrality is enforced by an explicit calibration formula.
- Residualisation, whitening and shrinkage have distinct purposes.
- Horseshoe priors are fully specified.
- Fairness claims correspond to measured fairness criteria.
- IFRS 17 is presented as an accounting interface.
- Insurance losses and finance receivables remain conceptually separate.
- Gross ultimate, reported, incurred, paid and outstanding losses reconcile.
- The reserve model distinguishes process, parameter and model uncertainty.
- Granular reserve results reconcile to recognised aggregate benchmarks.
- Economic capital states its horizon, risk measure and included risks.
- Regulatory capital, economic capital, commercial capital and the IFRS 17 risk adjustment remain distinct.
- Gross, ceded and net loss distributions reconcile under every treaty scenario.
- Reinsurance pricing identifies expected loss, loads, commissions, reinstatements and counterparty effects.
- Treaty monitoring covers attachment, erosion, exhaustion, recoverables, credit quality and basis risk.
- Every validation metric matches its response variable.
- Every citation supports its adjacent claim.
- IEEE numbering follows first appearance.
- All Markdown and LaTeX render correctly.
- The regenerated DOCX matches the canonical Markdown.
- The final paper retains its narrative warmth, mathematical ambition and original actuarial contribution.
