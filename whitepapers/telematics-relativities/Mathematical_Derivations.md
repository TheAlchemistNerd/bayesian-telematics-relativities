> **Historical draft — superseded as technical authority, 22 September 2026.** Retained for provenance. This text contains claims corrected by the [current paper/specification](<paper.md>). Read the [source-retirement ledger](<C:/Users/Nevo/Downloads/insuretech & embedded finance/output/coverage_retirement_audit_2026-09-22/02_SOURCE_RETIREMENT_LEDGER.md>) before reusing its equations, code, fairness or compliance claims. The original text below is preserved.

# Mathematical Derivations: Bayesian Telematics Pricing Architecture

This document provides the complete, rigorous mathematical derivations supporting the continuous underwriting architecture detailed in the white paper.

---

## 1. The Hierarchical Negative Binomial-Gamma Engine

To calculate the pure premium, the model separates expected claim frequency from conditional claim severity to prevent confounding variables.

### 1.1 Claim Frequency (Negative Binomial)
Let $Y_{it}$ be the claim count for driver $i$ in period $t$, and $E_{it}$ be the accumulated GNSS-validated exposure (e.g., kilometers driven).

To account for overdispersion (variance > mean) common in motor insurance, $Y_{it}$ is modeled using a Negative Binomial distribution, defined via a Poisson-Gamma mixture:
$$ Y_{it} \mid \lambda_{it} \sim \text{Poisson}(\lambda_{it}) $$
$$ \lambda_{it} = \mu_{it} E_{it} \theta_i $$

Where $\theta_i \sim \text{Gamma}(\alpha, \alpha)$ is the driver-specific frailty (random effect) with $E[\theta_i] = 1$ and $Var(\theta_i) = 1/\alpha$. Integrating out the latent $\theta_i$ yields the Negative Binomial marginal likelihood:
$$ P(Y_{it} = y \mid \mu_{it}, E_{it}, \alpha) = \frac{\Gamma(y + \alpha)}{y! \, \Gamma(\alpha)} \left( \frac{\alpha}{\alpha + \mu_{it} E_{it}} \right)^\alpha \left( \frac{\mu_{it} E_{it}}{\alpha + \mu_{it} E_{it}} \right)^y $$

The log-linear predictor for the baseline rate $\mu_{it}$ is:
$$ \log \mu_{it} = \alpha_{c(i)} + u_{geo} + \mathbf{X}_{it}^\top \boldsymbol{\beta} + \widetilde{\mathbf{h}}_{it}^\top \boldsymbol{\gamma}_{freq} $$

### 1.2 Claim Severity (Gamma)
Conditional on a claim occurring ($Y_{it} > 0$), the severity (cost) of the $k$-th claim, $Z_{itk}$, is modeled using a Gamma distribution to capture the heavy right tail:
$$ Z_{itk} \sim \text{Gamma}\left(\nu, \frac{\nu}{\mu^{sev}_{it} \Omega_i}\right) $$
Where $\nu$ is the shape parameter, $\mu^{sev}_{it}$ is the expected severity, and $\Omega_i \sim \text{InverseGamma}(\tau, \tau-1)$ is the driver-specific severity random effect ($E[\Omega_i]=1$).

The expected severity is linked logarithmically:
$$ \log \mu^{sev}_{it} = \delta_{c(i)} + v_{geo} + \mathbf{X}_{it}^\top \boldsymbol{\zeta} + \widetilde{\mathbf{h}}_{it}^\top \boldsymbol{\gamma}_{sev} $$

The total expected pure premium is thus:
$$ \mathbb{E}[PP_{it}] = \mathbb{E}[Y_{it}] \cdot \mathbb{E}[Z_{itk}] = (E_{it} \mu_{it} \theta_i) \cdot (\mu^{sev}_{it} \Omega_i) $$

---

## 2. Conjugate Bayesian Updating & Bühlmann-Straub Credibility

A primary advantage of this architecture is the ability to update the random effects ($\theta_i$ and $\Omega_i$) sequentially in real-time as new telematics data arrives, without retraining the entire MCMC graph.

### 2.1 Frequency Conjugacy (Gamma-Poisson)
Assume the global model learns a prior for the frailty term $\theta_i \sim \text{Gamma}(\alpha, \beta)$, where $\alpha = \beta$ to center the prior mean at 1.0. 
In a new observation window, driver $i$ accumulates exposure $\Delta E_i$ and generates $\Delta N_i$ claims. The baseline neural prediction for this window is $\mu_0$. 

The likelihood of the observed counts is Poisson: $P(\Delta N_i \mid \theta_i) \propto \theta_i^{\Delta N_i} e^{-\theta_i \mu_0 \Delta E_i}$.
By Bayes' Theorem, the posterior is proportional to the Prior $\times$ Likelihood:
$$ P(\theta_i \mid \Delta N_i) \propto \left( \theta_i^{\alpha - 1} e^{-\beta \theta_i} \right) \times \left( \theta_i^{\Delta N_i} e^{-\theta_i \mu_0 \Delta E_i} \right) $$
$$ P(\theta_i \mid \Delta N_i) \propto \theta_i^{(\alpha + \Delta N_i) - 1} e^{-\theta_i (\beta + \mu_0 \Delta E_i)} $$

This is exactly the kernel of a new Gamma distribution. Thus, the posterior update is closed-form:
$$ \theta_{i, \text{post}} \sim \text{Gamma}(\alpha + \Delta N_i, \beta + \mu_0 \Delta E_i) $$

**Proof of equivalence to Bühlmann-Straub Credibility:**
The expected value of the posterior is:
$$ \mathbb{E}[\theta_{i, \text{post}}] = \frac{\alpha + \Delta N_i}{\beta + \mu_0 \Delta E_i} $$
Rearranging this fraction yields:
$$ \mathbb{E}[\theta_{i, \text{post}}] = \left( \frac{\mu_0 \Delta E_i}{\beta + \mu_0 \Delta E_i} \right) \left( \frac{\Delta N_i}{\mu_0 \Delta E_i} \right) + \left( \frac{\beta}{\beta + \mu_0 \Delta E_i} \right) \left( \frac{\alpha}{\beta} \right) $$

Let the credibility factor $Z = \frac{\mu_0 \Delta E_i}{\beta + \mu_0 \Delta E_i}$. 
Substituting $Z$, we recover the exact classical Bühlmann-Straub linear credibility formula:
$$ \mathbb{E}[\theta_{i, \text{post}}] = Z \cdot (\text{Observed Risk Ratio}) + (1 - Z) \cdot (\text{Prior Mean}) $$

### 2.2 Severity Conjugacy (Inverse Gamma-Gamma)
For severity, the prior on the multiplier is $\Omega_i \sim \text{InverseGamma}(\tau, \lambda)$.
Given $\Delta N_i$ new claims with costs $\{Z_1, \dots, Z_{\Delta N_i}\}$, the posterior shape and scale parameters update analytically:
$$ \tau_{\text{post}} = \tau + \Delta N_i \cdot \nu $$
$$ \lambda_{\text{post}} = \lambda + \sum_{k=1}^{\Delta N_i} \left( \frac{\nu \cdot Z_k}{\mu^{sev}_0} \right) $$
If $\Delta N_i = 0$, the parameters do not change, mathematically preserving severity risk until physical damage actually occurs.

---

## 3. Tariff Neutrality and Modulating Variables

To deploy deep learning safely, the neural network cannot act as a "stealth base rate increase". The modulating variables must redistribute risk within a given tariff cell $c(i)$ strictly around an exposure-weighted mean of 1.0.

Let the frequency modulator be $M^{\mathrm{freq}}_{it} = \frac{\mu_{it}}{\mu_{0,c(i)}}$. 
The exposure-weighted average within cell $c(i)$ must evaluate to 1:
$$ \frac{\sum_{i \in c} E_{it} M^{\mathrm{freq}}_{it}}{\sum_{i \in c} E_{it}} = 1 $$

Since $\mu_{it} = \mu_{0,c(i)} \exp(\widetilde{\mathbf{h}}_{it}^\top \boldsymbol{\gamma})$, this strictly requires:
$$ \sum_{i \in c} E_{it} \exp(\widetilde{\mathbf{h}}_{it}^\top \boldsymbol{\gamma}) = \sum_{i \in c} E_{it} $$

This neutrality is enforced via the Double Machine Learning orthogonalization in the preceding layer.

---

## 4. Neural Residualization (Double Machine Learning)

To satisfy Equalized Odds and prevent proxy discrimination, the raw GRU embedding $\boldsymbol{\Phi}_{it}$ must be made strictly orthogonal to the traditional actuarial covariates $\mathbf{X}_{it}$ (e.g., geographic zone, age, vehicle class).

We define an adversarial projection network $P(\mathbf{X}_{it})$ that attempts to predict the telematics embedding solely from the traditional covariates:
$$ \widehat{\boldsymbol{\Phi}}_{it} = \mathbb{E}[\boldsymbol{\Phi}_{it} \mid \mathbf{X}_{it}] $$

The true behavioral risk is isolated by extracting the residual:
$$ \widetilde{\mathbf{h}}_{it} = \boldsymbol{\Phi}_{it} - \widehat{\boldsymbol{\Phi}}_{it} $$

By construction, $\text{Cov}(\widetilde{\mathbf{h}}_{it}, \mathbf{X}_{it}) = 0$. Therefore, if the log-linear predictor is evaluated, the neural term $\widetilde{\mathbf{h}}_{it}^\top \boldsymbol{\gamma}$ can only modulate the premium based on highly-specific individual driving kinematics that are mathematically uncorrelated with protected socioeconomic classes, ensuring absolute regulatory compliance.

---

## 5. Non-Centered Parameterization (Resolving Neal's Funnel)

In geographic or vehicle-class random effects ($u_{geo}$), sparse data leads to a pathological geometry where the variance collapses toward zero, trapping MCMC Hamiltonian transitions in an infinitely dense "funnel."

A centered parameterization is defined as:
$$ u_{geo, j} \sim \mathcal{N}(\mu_{geo}, \sigma_{geo}^2) $$
When $\sigma_{geo} \to 0$, the density of $u_{geo, j}$ becomes a delta function, which gradient-based samplers cannot traverse.

To resolve this, we map the geometry to an isotropic standard normal space (non-centered):
$$ \tilde{u}_{geo, j} \sim \mathcal{N}(0, 1) $$
$$ u_{geo, j} = \mu_{geo} + \sigma_{geo} \cdot \tilde{u}_{geo, j} $$

The gradient of the log-probability with respect to the raw sample $\tilde{u}_{geo, j}$ is now completely independent of $\sigma_{geo}$, decoupling the hierarchical layers and enabling highly efficient exploration of the posterior manifold regardless of cohort sparsity.
