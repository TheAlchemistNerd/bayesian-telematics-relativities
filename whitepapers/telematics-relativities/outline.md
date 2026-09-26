# Outline: Bayesian Credibility and Exposure-Normalised Telematics Relativities for Usage-Based Motor Insurance

**Target Length:** ~6,000 Words
**Target Audience:** Actuarial scientists, quantitative researchers, insurance technologists.

---

## 1. Introduction (approx. 500 words)
*   **The Evolution of Usage-Based Insurance (UBI):** Transition from static pricing variables (age, vehicle class, geography) to high-frequency telematics and gig-economy contexts.
*   **Limitations of Current Approaches:** The failure of raw neural network outputs to function as interpretable actuarial relativities. 
*   **Proposed Framework:** A hybrid architecture combining Hierarchical Bayesian models, explicit actuarial variables, and residualised neural embeddings.
*   **Paper Objectives:** Formally define the modulating variable, explain the separation of frequency and severity, and map Bayesian partial pooling to classical credibility theory.

## 2. Theoretical Foundations and Actuarial Principles (approx. 800 words)
*   **The Measure Conundrum in Insurance Pricing:** 
    *   Why the physical measure ($\mathbb{P}$) is the only valid basis for estimating actual accident frequency, severity, and cash-flow risk.
*   **Revisiting Credibility Theory:** 
    *   Bühlmann-Straub classical credibility and its limitations with highly heterogeneous, sparse gig-economy data.
    *   Hierarchical Bayes as a mathematically rigorous generalization of actuarial credibility (shrinkage, borrowing strength, and partial pooling).
*   *Key Sources: CAS Literature on Insurance vs. Financial Pricing; Foundations of Bayesian Data Analysis.*

## 3. The Actuarial Modulating Variable Framework (approx. 1,200 words)
*   **Defining the Baseline:** Setting the conventional tariff cell ($c(i)$) and exposure base ($E_{it}$, e.g., kilometers, insured hours).
*   **Frequency and Severity Separation:**
    *   **Frequency Model:** Negative Binomial formulation ($N_{it}\sim\operatorname{NegBin}(\mu_{it},\phi)$) with exposure entering strictly as an offset to avoid confusing "drives more" with "is more dangerous per kilometer."
    *   **Conditional Severity Model:** Gamma formulation ($Y_{itk}\mid N_{it}>0 \sim \operatorname{Gamma}\left(\mu^{\mathrm{sev}}_{it},\kappa\right)$) representing claim costs given a claim occurs.
*   **Constructing the Modulating Variables:**
    *   Deriving explicit behavioral relativities ($M^{\mathrm{freq}}_{it}$ and $M^{\mathrm{sev}}_{it}$) relative to the conventional base class.
*   **Tariff Neutrality:** Mathematical constraints to ensure the exposure-weighted average of the modulator approximates 1.0, redistributing risk without silently inflating the aggregate base tariff.
*   **From Pure Premium to Commercial Premium:** Adding non-driving baseline risks ($B_{it}$), expenses, reinsurance, and capital margins.

## 4. Integrating Neural Representations: The Residualisation Strategy (approx. 900 words)
*   **The Redundancy Problem:** The danger of a deep learning model (e.g., GRU/Transformer) implicitly memorizing and double-counting explicit actuarial metrics (like liquidity or mileage).
*   **Cross-Fitted Residualisation:** 
    *   Projecting the raw neural representation ($\mathbf{h}_{it}$) orthogonally against explicit B-spline features.
    *   Using the residual ($\widetilde{\mathbf{h}}_{it}$) to capture only the *incremental* predictive value of complex telematics sequences (e.g., cornering rhythms, fatigue markers).
*   *Key Sources: Literature on Double Machine Learning and Orthogonalized Regression.*

## 5. Spatio-Temporal Dynamics and State-Space Modeling (approx. 800 words)
*   **Latent-Risk State-Space Models:** Distinguishing persistent underlying driver risk from transient states (e.g., temporary fatigue, severe weather, urban congestion).
*   **Time-Varying Coefficients:** Implementing Autoregressive (AR(1)) priors to handle structural regime changes (e.g., platform algorithm updates, new ZEV mandates, fuel price shocks).
*   **Avoiding Causal Confusion:** Differentiating between intrinsic dangerous driving and environmentally forced kinematics (e.g., hard braking due to road quality or dispatch pressure).
*   **Dynamic Pricing vs. Interventions:** Why an immediate kinematic alert (fatigue warning) should trigger a behavioral intervention (rest mandate) rather than an instantaneous premium spike.

## 6. Computational Architecture and Bayesian Inference (approx. 700 words)
*   **Scaling Hierarchical Models:** The computational bottleneck of MCMC on massive telematics portfolios.
*   **Taming the Geometry:** Utilizing non-centered parameterizations and Half-Student-t priors to resolve Neal's Funnel and ensure stable sampling of variance components.
*   **Production Inference:** Strategies for scalability, including Bernoulli-to-Binomial exact aggregation for identical cohorts and leveraging compiled JAX/BlackJAX on hardware accelerators.
*   **Validation:** Posterior Predictive Checks (PPCs), out-of-time calibration, and handling posterior uncertainty (HDIs).

## 7. Regulatory, Accounting, and Fairness Governance (approx. 800 words)
*   **IFRS 17 Alignment:** Conceptually distinguishing the pure premium cash-flow estimates from the risk adjustment for non-financial risk, preventing double-counting of uncertainty.
*   **Policy States and Cash-Flow Isolation:** Modeling active, grace, and lapse states, and separating insurance cash from lender-owned premium finance (IPF) receivables.
*   **Fairness and Proxy Testing:** Ensuring telematics variables do not act as proxies for protected or socioeconomically sensitive characteristics (e.g., late-night driving penalties disproportionately affecting lower-income segments).
*   **Feedback Loops:** Acknowledging that higher premiums can alter driver behavior, reduce liquidity, and change the very risk profile being measured.

## 8. Conclusion (approx. 300 words)
*   Synthesis of the exposure-normalized Bayesian framework.
*   The path forward: Designing controlled pilots to measure causal claims reduction rather than relying solely on observational predictive accuracy.

---

## Proposed Bibliography and Source Integration
1.  **Casualty Actuarial Society (CAS):** "Credibility Theory and Generalized Linear Models" – *For linking Hierarchical Bayes to classical actuarial standards.*
2.  **IFRS Foundation:** "IFRS 17 Insurance Contracts" – *For the explicit separation of expected cash flows, non-financial risk adjustments, and commercial margins.*
3.  **Gelman, A., et al.:** "Bayesian Data Analysis" (3rd Ed.) – *For the theoretical foundation of partial pooling, AR(1) priors, and non-centered hierarchical geometries.*
4.  **McNeil, A. J., Frey, R., & Embrechts, P.:** "Quantitative Risk Management" – *For establishing the physical measure ($\mathbb{P}$) as the appropriate basis for real-world loss estimation.*
5.  **Recent UBI/Telematics Literature:** Case studies on frequency-severity modeling and the impact of kinematics on motor risk.
