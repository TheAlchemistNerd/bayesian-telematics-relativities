# Bayesian Relativities × Moove: pitch evidence and coverage map

**Checked:** 14 October 2026.  
**Purpose:** Verified public evidence and implementation guidance for the Moove article and pitch materials.  
**Source archive:** The supplied analyses are preserved beside this note as `SOURCE_BAYESIAN_RELATIVITIES_MOOVE_ANALYSIS.txt` and `SOURCE_MOOVE_MWENDO_APPLICATION_ANALYSIS.txt`.

## 1. Main proposition

The useful proposition is to connect exposure-adjusted insurance evidence to a full economic test of mobility operations. Bayesian Relativities estimates expected insured loss and uncertainty. Mwendo Pamoja links vehicle availability, repair and driver liquidity to contractual cash and financing outcomes. Underwrite for Collection supplies the evidence, intervention and evaluation discipline. A proposed Moove study would examine whether a governed insurance or service decision improves the joint economic result while preserving the distinct rights and obligations of driver, operator, insurer and funder.

Moove is already an established use case for productivity data. CGAP's June 2023 brief describes Moove's platform earnings, trips and telematics in underwriting and risk management, and its work-to-own arrangements. The proposal should present the research as an actuarial measurement and evaluation extension to that public precedent. It should not frame the company as lacking telematics, underwriting, insurance or repair practices.

## 2. Source-backed operating context

| Evidence | Verified public statement | How to use it |
|---|---|---|
| CGAP, June 2023 | The brief documents Moove's proprietary data collection, credit scoring and risk management; platform activity such as trips, ratings and cancellations; telemetry such as speed, braking, vehicle use and distance; work-to-own finance; repayment deduction at source; and support for driver repayment and income. | Historical reported practice. This motivates an evaluation design; it does not establish current data sharing or current contractual terms. Cite the brief as the empirical anchor. |
| Moove corporate site, checked 14 Oct 2026 | Moove currently describes capital, infrastructure and city-level operations across driver-led and autonomous mobility. It identifies asset finance/ownership, fleet readiness and operations as linked services. | Establishes a close commercial setting for Mwendo. Use current corporate positioning. |
| Moove Kenya Drive With Us page, checked 14 Oct 2026 | Kenya is a selectable operating market; the page presents an application, verification and driving route toward vehicle ownership through partner platforms. Current Kenya vehicle pages list insurance, maintenance/service and support elements, and say product availability/features depend on location. | Localises the pitch while keeping product specifics tied to the selected vehicle, market and contract. Do not generalise UK package terms to Kenya. |
| Moove UK Customer Hub and privacy policy | The UK pages describe weekly payments, insurance/service inclusions, telematics supporting insurance claims and approved payment breaks. The policy describes vehicle and telematics data for stated purposes. | Use only as a UK example and only after checking a current applicable contract. The policy is a data inventory, not permission for a new research purpose. |
| Moove AV Operations and partner form | Current official page describes vehicle financing/ownership, depot infrastructure, charging and 24/7 operations and separately offers a strategic partnership/fleet-deployment contact route. | Supports a separate AV extension around utilisation, charging, maintenance and service readiness. Keep it distinct from the driver-led insurance case. |

## 3. Bayesian actuarial application

The paper separates exposure, claim frequency, conditional claim severity and non-driving loss. Its simplified driving expected-loss identity is:

**Expected driving claims cost = exposure × claim rate per exposure unit × mean claim cost.**

This distinction matters when two drivers accumulate different distances: a high number of kilometres can raise expected claims through exposure even if expected claims per kilometre are unchanged. Frequency and severity relativities can then be estimated with hierarchical credibility, reporting posterior intervals for the persistent parameter and a separate predictive distribution for future claims. Exposure volume, claim maturity and data-quality indicators should accompany those outputs.

The supplied Bayesian Relativities paper already contains a hypothetical, pre-calibration example using 0.08 claims per 10,000 km and KES 180,000 average claim cost. It calculates expected driving claims costs of KES 2,325.60 for Amina and KES 6,082.56 for Kamau. These are expected claims costs under illustrative assumptions. They are not observed Moove losses, calibrated premium rates, customer prices, or profit results. The article/deck should label that distinction at the point where the numbers appear.

The paper’s exposure-normalisation is a key pricing control: the combined frequency-severity relativity is normalised within approved tariff cells so it redistributes the expected loss indication without silently shifting the aggregate expected-loss level. It does not promise that an intervention will reduce total claims. If a safety or service intervention is found to change losses, that effect should be estimated separately against a defined comparator and only then considered in pricing or benefit allocation.

## 4. Profit testing to add to the Moove application

Profit testing is the commercial bridge between the actuarial model and a decision about renewal, retention, incentives, reinsurance or service investment. The current paper supplies the statistical and financial components—expected loss, posterior predictive outcomes, claims development, reserves, capital and risk-transfer cash flows—but does not contain a Moove-calibrated multi-party profit test. Treat this as a proposed worked-example extension, populated with permitted and matched exposure, claim, contract and operating data.

Compare three scenarios on the same eligible population and horizon:

1. **Current arrangement:** current contract, tariff, insurance, maintenance and servicing obligations.
2. **Exposure-informed actuarial view:** posterior frequency/severity estimates and approved within-cell normalisation, with prices and contract features held to the selected approved baseline for the comparison.
3. **Intervention and incentive view:** a defined safety or repair intervention with its cost, timing, effect on availability, claims and driver outcomes estimated from an appropriate causal evaluation.

Keep three ledgers and reconcile all inter-party transfers:

| Perspective | Inflows and value | Costs and risks to include | Primary test |
|---|---|---|---|
| Insurer / risk carrier | Earned premium and investment income; reinsurance recoveries | Paid and incurred claims, claim expenses, acquisition/administration, reinsurance premium, capital and liquidity cost, counterparty and reserve risk | Underwriting result, combined ratio, gross/net loss distribution, capital use, and multi-year shareholder cash flows/return under an explicit capital policy |
| Moove / fleet operator | Contractual vehicle receipts, platform or service income where contractually due, recoveries or service reimbursements | Vehicle acquisition/funding, insurance cost actually borne, maintenance/repair, replacement and downtime, operations, collections, loss retention, working capital and intervention expense | Contribution by agreement and cohort, vehicle uptime, collection cash, funding/liquidity profile, and risk-adjusted return on deployed capital |
| Driver | Settled platform earnings, approved benefits/incentives, contractual asset equity or ownership transfer | Fuel/energy, operating costs, household cash needs (as a resilience measure), weekly/periodic obligations, insurance excesses, repair costs and time unable to earn | Take-home cash, affordability, days able to earn, arrears/cure and end-of-term ownership/equity outcome |

For each scenario, use a dated cash-flow model, not just an accounting ratio. On the insurer side, calculate premium less claim cash, expense, reinsurance and capital costs over time, carrying reserve development and reinsurance settlement lags. A multi-year shareholder-return extension may simulate claim outcomes, dividends, capital distributions, capital floors/ceilings and terminal liquidation or insolvency. Robbin and Malhotra (CAS Forum, 2023) provide an actuarial reference for that specific long-term insurance-company perspective and for sensitivity to reinsurance and capital management. It is a modelling method to adapt, not evidence about Moove or its insurer.

On the Moove side, assign every payment according to the selected agreement. An insurance premium paid by Moove, a driver, or a lender changes different ledgers. Record repair cost, days offline, replacement-vehicle expense, contractual receipts foregone or delayed, subsequent collections and financing cost. The driver ledger should show both scheduled payments and residual income. Reconcile the operator ledger to the bank and servicing records.

The profit test should report posterior distributions and scenario sensitivities, including claim frequency/severity, exposure, claim reporting and payment development, inflation, repair duration, vehicle replacement, discounting, renewals, retention, insurer expense, reinsurance price/attachment/limits, capital cost, and intervention take-up. Report expected NPV and an uncertainty range, tail loss/capital measures, liquidity shortfall probability, driver cash outcomes and downside thresholds. The risk/return object depends on whose profit is being tested; do not collapse all three into one return number.

Evidence needed to calibrate it includes: covered distance or hours; policy and tariff cell; premium and who pays; claim occurrence/reporting/closure/payment dates; incurred and paid loss; expenses; excess and exclusions; treaty terms and settlement; driver platform settlements and activity; repair/service work orders and downtime; vehicle residual value and funding terms; contract receipts and deductions; intervention assignment and costs; and relevant consent, access and retention records. Establish comparability and causal assignment before estimating a claim-reduction benefit.

## 5. Fit of the existing Mwendo worked case

The current Mwendo example already offers a useful repair mechanism: under its hypothetical first-month assumptions, 12 days of vehicle downtime produces about KES 10,750 unpaid scheduled debt; an authorised KES 30,000 repair-finance scenario with two days of downtime meets scheduled first-month payments and also records additional borrowing cost. Those two durations are scenario inputs, not an estimated repair effect. For Moove, carry the mechanism across a full contract term with the selected contract's weekly cash schedule, insurance payer, repair duty, replacement provision, vehicle depreciation, end-of-term ownership, and portfolio funding. The profit test should show how much of any improvement accrues to driver, operator, insurer and funder under actual terms.

Keep general ring-fenced receivables analysis separate from the specific transaction vehicle. If the financing arrangement uses an SPV, model its eligible receivables, controlled collections, reserve and waterfall from the executed documents. A vehicle-specific contract is not implied by the generic application.

## 6. Source-by-source coverage of the supplied Moove texts

### Latest Bayesian Relativities × Moove attachment

| Attachment lines | Content read | Destination / treatment |
|---|---|---|
| 1–5 | Connect Bayesian Relativities, Mwendo, Moove UK telematics/insurance and claims outcomes. | Sections 1–3; CGAP and current Moove facts are explicitly dated and kept separate. |
| 6–14 | Exposure, frequency, severity, non-driving loss, expected-loss equation and exposure-versus-risk interpretation. | Section 3; formula preserved, with tariff-cell normalization and no causal claim. |
| 15–25 | Amina/Kamau pre-calibration example and premium layers. | Section 3; values are identified as hypothetical claims costs, not premium or profit. |
| 26–34 | Hierarchical credibility, posterior interval, predictive distribution, data maturity and recursive conjugate updates. | Section 3; interval and predictive distribution retain their distinct meaning. |
| 35–45 | Commercial uses for renewal, incentives, safety support, retained risk, reserving/reinsurance and vehicle economics. | Sections 4–5; responsibilities allocated by contract and risk-bearing entity. |
| 46–54 | Three-scenario profit testing; insurer/Moove/driver ledgers; tariff neutrality; long-term reinsurance/capital literature. | Section 4 expands into a proposed multi-party test with separate cashflows, uncertainty and outcome identification. |
| 55–62 | Cross-project connection and matched operational evidence. | Sections 1, 4 and 5; requires matched claims, exposure, contract and operations data. |

### Earlier Moove–Mwendo attachment

| Attachment lines | Content read | Destination / treatment |
|---|---|---|
| 1–7 | Moove fit, CGAP precedent, distinguish application from claims about Moove gaps. | Sections 1–2 preserve that framing. |
| 8–15 | Cash affordability, deterioration, intervention, thin-data decisions, insurance and receivables, auditable decision history. | Sections 3–5 carry the applications into a full-term contract and cost test. |
| 18–28 | Existing repair example and causal evidence requirements. | Section 5 preserves the exact hypothetical values and states the two downtime assumptions do not establish causal impact. |
| 29–35 | UK contract package, full horizon and jurisdiction, ring-fenced receivables and SPV. | Sections 2 and 5 localise UK facts and separate a generic cash stream from a specific SPV. |
| 36–44 | Autonomous fleet extension, value proposition and bounded pilot. | Section 2 notes official current AV infrastructure; section 4 keeps driver-led profit test distinct. |

## 7. Current public contact routes

- **Moove corporate contact form:** https://www.moove.io/drive-to-own/contact-us
- **Moove AV partnerships and deployment:** https://www.moove.io/autonomous-vehicles (choose its “Partner with us” route).
- **Published corporate mailboxes:** cs@moove.io (technical/customer support) and press@moove.io (PR/marketing). These are not labelled as dedicated partnerships mailboxes. The corporate form is the stronger route for a driver-led research proposal; the AV partnerships form fits an autonomous-fleet proposal.
- **UK customer contact:** ukonboarding@moove.io is published for UK onboarding/customer support, not research partnerships.

No message was sent. No named person's email is inferred.

## 8. Public source register (primary sources first)

1. Malika Anand and Gayatri Murthy, “Putting Gig Data to Work: Innovations in Expanding Credit Access,” CGAP Brief, June 2023: https://www.cgap.org/research/publication/putting-gig-data-to-work-innovations-in-expanding-credit-access ; PDF: https://documents1.worldbank.org/curated/en/099063023143011873/pdf/P17436207747210ff096970c02a59ed1daf.pdf
2. Moove corporate site: https://www.moove.io/ ; Kenya Drive With Us: https://www.moove.io/en-KE/drive-to-own/drive-with-us ; Drive to Own: https://www.moove.io/drive-to-own
3. Moove AV Operations: https://www.moove.io/autonomous-vehicles ; corporate contact: https://www.moove.io/drive-to-own/contact-us
4. Moove UK Customer Hub: https://uk.moove.io/customer-hub/ ; UK privacy policy: https://uk.moove.io/privacy-policy/
5. Nevil Maloba, “Bayesian Credibility and Exposure-Normalised Telematics Relativities,” August 2026, local project manuscript: C:\Users\Nevo\Downloads\bayesian-telematics-relativities\whitepapers\telematics-relativities\paper.md
6. Ira Robbin and Atul Malhotra, “Modeling the Impact of Capital Management and Reinsurance on Long-Term Profitability,” CAS Forum, Summer 2023: https://forum.casact.org/article/83958-modeling-the-impact-of-capital-management-and-reinsurance-on-long-term-profitability
7. Waymo, “Next stop: Miami,” 5 December 2024, historical partnership announcement: https://waymo.com/blog/2024/12/next-stop-miami/

**Limits:** Moove-specific claim, policy, expense, contract and intervention data are not public in these sources. The public material supports the application and pilot design, while model parameters and profitability remain to be estimated with approved data.
