# Writing Guide: Bayesian Credibility and Exposure-Normalised Telematics Relativities

## Objective
The goal is to draft a 6,000-word standalone research paper that builds upon the foundations laid out in the Mwendo Pamoja white paper (Parts 2a and 2b) and the initial Research Note. The paper will formalize the actuarial, statistical, and financial mechanisms of a continuous underwriting system for usage-based motor insurance (UBI) in the gig economy.

## Target Audience
Actuaries, data scientists, quantitative risk managers, and insurance regulators. The tone must be rigorous, academically grounded, and practical for production deployment.

## Key Principles
1. **Actuarial Rigor:** Emphasize that raw machine learning predictions are insufficient for insurance pricing. Telematics outputs must be mapped to formal actuarial relativities (modulating variables).
2. **Proper Uncertainty Treatment:** Use hierarchical Bayesian models as a modern extension of credibility theory. Emphasize that posterior Highest Density Intervals (HDIs) report uncertainty but are not credibility factors themselves.
3. **Orthogonality & Residualization:** Clearly differentiate between explicit financial/actuarial features and deep neural representations. Use cross-fitted residualization to prevent double-counting of risk signals.
4. **Financial Soundness:** Focus on the physical measure ($\mathbb{P}$) for actual expected claims and operational underwriting, avoiding unrelated detours.
5. **Regulatory Alignment:** Adhere to IFRS 17 standards, clearly separating pure premium, risk adjustment for non-financial risk, and commercial margins.

## Drafting Strategy by Section

### Phase 1: Foundations and Literature Review (Outline Sections 1 & 2)
Focus on establishing the mathematical inadequacy of raw neural networks for insurance pricing. Cite authoritative sources on generalized linear models (GLMs), credibility theory (Bühlmann-Straub), and incomplete markets in quantitative finance.

### Phase 2: Core Methodology (Outline Sections 3 & 4)
This is the mathematical heart of the paper. Clearly define the exposure-offset frequency and conditional severity models. Provide the exact mathematical formulation for the modulating variables ($M^{\mathrm{freq}}_{it}$, $M^{\mathrm{sev}}_{it}$) and the calibration mechanism that ensures exposure-weighted averages remain neutral within base tariff cells. Introduce the residualized neural component ($\widetilde{h}_{it}$) here.

### Phase 3: Advanced Modeling & Computation (Outline Sections 5 & 6)
Address the complexities discussed in Part 2b: partial pooling for sparse data geometries, time-varying AR(1) effects, and the MCMC sampling strategy (non-centered parameterizations, BlackJAX). Keep the focus on how these techniques solve real-world UBI challenges (e.g., new drivers, changing platform algorithms).

### Phase 4: Implementation and Governance (Outline Sections 7 & 8)
Address practical concerns: fairness, preventing causal confusion (e.g., hard braking caused by road conditions vs. driver behavior), separating pricing from immediate behavioral interventions, and IFRS 17 compliance. 

## Source Material Integration
- **Mwendo Pamoja White Paper (Parts 2a & 2b):** Use the dual-regime neural architecture (GRU/Transformer) and Bayesian underwriting methodologies as the technical baseline.
- **Research Note:** Expand upon the functional forms for frequency (Negative Binomial) and severity (Gamma), the definition of the modulating variables, and the alignment with credibility theory.
- **External Citations:** Integrate references from the Casualty Actuarial Society (CAS), IFRS 17 guidelines, and foundational texts on Bayesian Data Analysis (e.g., Gelman et al.).
