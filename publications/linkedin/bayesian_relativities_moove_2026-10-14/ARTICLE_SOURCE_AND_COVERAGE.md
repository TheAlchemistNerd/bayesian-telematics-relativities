# Bayesian Relativities × Moove: Source and Coverage Record

**Prepared:** 14 October 2026

## Pasted analysis coverage

The attachment `Pasted text.txt` was read in full, line by line. Its six numbered sections are represented in the article as follows.

| Pasted section | Analysis carried into the article |
|---|---|
| 1. Moove’s operating setting | The article begins with the CGAP 2023 gig-data study and Moove’s UK Driver Hub and privacy-policy descriptions. It treats the UK materials as a public illustration of operations and data classes, then defines a market-specific product and insurer as necessary inputs to any calibrated application. |
| 2. Insurance quantities and existing Amina/Kamau illustration | The article defines exposure, frequency, severity and non-driving losses, then reproduces the paper’s hypothetical KES 2,325.60 and KES 6,082.56 expected-driving-loss calculations. It separates those expected claims costs from a customer premium. |
| 3. Bayesian credibility | The article explains hierarchical partial pooling, posterior credible intervals, future-loss prediction intervals, recursive Gamma–Poisson and inverse-Gamma–Gamma updates, and the model artefacts needed for review. |
| 4. Commercial uses | The article carries forward renewal, driver rewards, safety support, retained risk, reserving, reinsurance, vehicle economics and customer cash. It assigns each quantity to the actor whose contract or balance sheet bears it. |
| 5. Profit testing | The article develops insurer, operator and driver ledgers; multi-period incurred and paid claims; reserve development; reinsurance cash, capital and counterparty timing; common shocks; sensitivities; and a hypothetical 100-vehicle KES case. It explicitly distinguishes neutral tariff allocation from an assumed intervention effect. |
| 6. Project connection | The article connects Bayesian Relativities to insurance estimates, Mwendo Pamoja to operations and financing, and Underwrite for Collection to governed decisions and evaluation. |

## Source verification and use

The article’s source order follows first citation in the body. The key publisher and primary-source pages were checked during preparation.

| Ref. | Source | Claim supported |
|---|---|---|
| [1] | Anand and Murthy, CGAP, *Putting Gig Data to Work* (2023), https://documents1.worldbank.org/curated/en/099063023143011873/pdf/P17436207747210ff096970c02a59ed1daf.pdf | CGAP’s discussion of Moove, platform work data and gig-worker finance. |
| [2] | Moove UK Customer Hub, https://uk.moove.io/customer-hub/ | Published UK vehicle package, weekly payment and service descriptions. |
| [3] | Moove UK Privacy Policy, https://uk.moove.io/privacy-policy/ | Publicly described UK driver/vehicle telematics fields and purposes. |
| [4] | Lee and Shi (2019), *Insurance: Mathematics and Economics*, https://doi.org/10.1016/j.insmatheco.2019.04.004 | Longitudinal dependence between claim frequency and severity. |
| [5] | Maloba, *Bayesian Credibility and Exposure-Normalised Telematics Relativities*, https://github.com/TheAlchemistNerd/bayesian-telematics-relativities/blob/main/whitepapers/telematics-relativities/paper.md | Exposure, frequency and severity methods; credibility, draw-wise tariff calibration, posterior uncertainty, claims development, capital and risk transfer. |
| [6] | Belhadj, Goulet, and Ouellet (2009), “On parameter estimation in hierarchical credibility,” *ASTIN Bulletin*, https://doi.org/10.2143/AST.39.2.2044645 | Peer-reviewed hierarchical credibility estimation. |
| [7] | Bühlmann (1967), *ASTIN Bulletin*, https://doi.org/10.1017/S0515036100008989 | Classical credibility foundation. |
| [8] | Actuarial Standards Board, ASOP No. 43, https://www.actuarialstandardsboard.org/asops/propertycasualty-unpaid-claim-estimates/ | Unpaid-claim estimate considerations. |
| [9] | IFRS Foundation, IFRS 17 reinsurance contracts-held guide, https://www.ifrs.org/content/dam/ifrs/supporting-implementation/ifrs-17/ifrs-17-pocket-guide-on-reinsurance-contracts-held.pdf | Separate measurement of reinsurance contracts held and reinsurer non-performance. |
| [10] | IAIS, Insurance Core Principles and ComFrame (December 2024), https://www.iais.org/uploads/2024/12/IAIS-ICPs-and-ComFrame-adopted-in-December-2024.pdf | Risk appetite, reinsurance strategy, capital, liquidity and counterparty risk. |
| [11] | Robbin and Malhotra (2023), CAS Forum, https://forum.casact.org/article/83958-modeling-the-impact-of-capital-management-and-reinsurance-on-long-term-profitability | Multi-year insurer capital sequences and shareholder-return perspective on reinsurance. |

**Bibliographic correction:** the DOI used in the source paper’s reference for “A dependent frequency–severity approach to modeling longitudinal insurance claims” resolves to Gee Y. Lee and Peng Shi (2019). The article cites those verified authors. The source paper’s bibliography was not edited as part of this task.

## Numerical scope

The 100-vehicle annual insurance profit test is its own hypothetical KES research case. It uses synthetic exposure and claim sufficient statistics and elected model, treaty, timing, capital, cost and intervention assumptions. It contains no data supplied by Moove, an insurer, broker or driver and is not a market quotation. A 2% shared common shock with frequency and severity multipliers 1.8 and 1.25 contributes the factor 1.025 to both expected-loss indications and simulated losses. The 156-week Mwendo operating and financing case remains a separate illustration; it supplies context on how insurance premium and repair timing can connect to a weekly package, with the repair event counted once. The profit case uses 12,000 posterior draws and 8,000 predictive paths; eight automated checks passed, seeded reproducibility was checked and gross-to-net claim reconciliation error was zero. Only about 40 predictive paths support the upper 0.5% tail, so VaR/TVaR are coarse illustrative economic-capital estimates, not regulatory capital results.

The 10% volatile-group frequency reduction is a stipulated intervention sensitivity. The model allocates 75% of its expected saving to premium reduction and 25% to an operator-funded driver incentive. These parameters describe benefit-sharing assumptions; the frequency effect becomes an empirical result only after a suitable pilot produces mature, comparable exposure and claim outcomes.

## Article checks

- IEEE citations appear in first-citation order [1]–[11] and match the references list.
- Displayed Unicode formulas are separate lines; every symbol in the article is defined in its equation or surrounding text.
- The profit test separates insurer underwriting/capital profit, operator cash and driver cash. Pure-loss relativities are calibrated within the selected portfolio; they change group allocation while preserving its weighted commercial premium. The 10% frequency intervention is a separate assumed effect that changes total expected claims.
- The companion LinkedIn post is 1,969 characters excluding its final newline and 1,970 including it; see `ARTICLE_VERIFICATION.json` for the exact counting rules.
