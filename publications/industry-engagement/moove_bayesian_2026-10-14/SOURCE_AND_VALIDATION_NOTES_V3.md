# Sources, assumptions and validation record

**Deck:** *Bayesian Relativities × Moove: Mobility Insurance Profit Testing*  
**Prepared:** 14 October 2026  
**Status:** Research-partnership proposal built from public material and a reproducible hypothetical case.

## Source references

[1] M. Anand and G. Murthy, “Putting Gig Data to Work: Innovations in Expanding Credit Access,” CGAP Brief, June 2023. [Online]. Available: https://documents1.worldbank.org/curated/en/099063023143011873/pdf/P17436207747210ff096970c02a59ed1daf.pdf

[2] Moove, “Customer Hub,” United Kingdom. Accessed October 14, 2026. [Online]. Available: https://uk.moove.io/customer-hub/

[3] Moove, “Privacy Policy,” United Kingdom. Accessed October 14, 2026. [Online]. Available: https://uk.moove.io/privacy-policy/

[4] G. Y. Lee and P. Shi, “A dependent frequency–severity approach to modeling longitudinal insurance claims,” *Insurance: Mathematics and Economics*, vol. 87, pp. 115–129, 2019, doi: 10.1016/j.insmatheco.2019.04.004. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0167668718301951

[5] N. Maloba, *Bayesian Credibility and Exposure-Normalised Telematics Relativities*, technical white paper, 2026. [Online]. Available: https://github.com/TheAlchemistNerd/bayesian-telematics-relativities/blob/main/whitepapers/telematics-relativities/paper.md

[6] H. Belhadj, V. Goulet, and T. Ouellet, “On parameter estimation in hierarchical credibility,” *ASTIN Bulletin*, vol. 39, no. 2, pp. 495–514, 2009, doi: 10.2143/AST.39.2.2044645. [Online]. Available: https://www.cambridge.org/core/journals/astin-bulletin-journal-of-the-iaa/article/abs/on-parameter-estimation-in-hierarchical-credibility/630A49D6B48A8FE019222FC50014DCB1

[7] H. Bühlmann, “Experience rating and credibility,” *ASTIN Bulletin*, vol. 4, no. 3, pp. 199–207, 1967, doi: 10.1017/S0515036100008989. [Online]. Available: https://www.cambridge.org/core/journals/astin-bulletin-journal-of-the-iaa/article/experience-rating-and-credibility/B9A879CE4A73397C653963B474A7F954

[8] Actuarial Standards Board, “ASOP No. 43: Property/Casualty Unpaid Claim Estimates,” adopted 2007, revised 2011. [Online]. Available: https://www.actuarialstandardsboard.org/asops/propertycasualty-unpaid-claim-estimates/

[9] IFRS Foundation, *IFRS 17 Insurance Contracts: Pocket Guide on Reinsurance Contracts Held*. London, U.K., 2018. [Online]. Available: https://www.ifrs.org/content/dam/ifrs/supporting-implementation/ifrs-17/ifrs-17-pocket-guide-on-reinsurance-contracts-held.pdf

[10] International Association of Insurance Supervisors, *Insurance Core Principles and Common Framework for the Supervision of Internationally Active Insurance Groups*, December 2024. [Online]. Available: https://www.iais.org/uploads/2024/12/IAIS-ICPs-and-ComFrame-adopted-in-December-2024.pdf

[11] I. Robbin and A. Malhotra, “Modeling the impact of capital management and reinsurance on long-term profitability,” *CAS Forum*, Summer 2023. [Online]. Available: https://forum.casact.org/article/83958-modeling-the-impact-of-capital-management-and-reinsurance-on-long-term-profitability

## Numerical inputs and interpretation

The KES case is a **synthetic research illustration**, not Moove, insurer, broker or driver portfolio experience. It is not a quote. It does not describe a Moove contract. Public UK product material [2] and privacy material [3] are used only to motivate relevant operational and data questions; CGAP [1] supplies the gig-work data and credit-access context.

The case uses a 100-vehicle annual portfolio with a synthetic 70% stable / 30% volatile mix, a three-year synthetic claim history, Gamma–Poisson frequency, inverse-Gamma/Gamma severity, 12,000 posterior draws, 8,000 predictive paths, and fixed seed 20261014. The 2% shared-shock scenario uses frequency ×1.8 and severity ×1.25, with expected-loss factor 1.025. The annual 100-vehicle insurance portfolio and the separate 156-week Mwendo financing illustration remain separate ledgers.

The 10% volatile-cohort frequency reduction is an assumed sensitivity. Its modelled expected saving is allocated 75% to premium reduction and 25% to an operator-funded driver incentive. An empirical intervention effect would need a suitable pilot with exposure-linked and sufficiently mature claims.

The 99.5% VaR and TVaR are coarse Monte Carlo illustrations. With 8,000 paths, approximately 40 paths lie beyond the 99.5th percentile. They are not regulatory capital calculations. More simulations, convergence checks and parameter, reinsurance, common-shock and claim-maturity sensitivity are needed before decision use.

## Reproducibility

Case source is in `research_lab/mobility_insurance_profit_case/`:

- `assumptions.json`, `model.py`, `run_case.py`, `test_model.py`
- `output/summary.json` and `output/results.json`
- `README.md` gives commands for reproducing the case.

The article and its checked references are in `publications/linkedin/bayesian_relativities_moove_2026-10-14/`. Four Python-generated standalone charts are under `charts/` and are embedded in the deck. The complete slide speaker notes, including slide-specific citations and interpretation, are in `SPEAKER_NOTES.md` and embedded in the editable PPTX.

## Final V3 validation

- Deliverable: `BAYESIAN_RELATIVITIES_X_MOOVE_RESEARCH_PARTNERSHIP_DECK_2026-10-14_V3.pptx` and matching PDF. V3 removes a crowded in-chart label while retaining exact posterior values and 90% intervals in the slide callouts.
- Package integrity validator: **pass**, 19 slides, 0 findings.
- Slide geometry / heading-fit validator: **pass**, 19 slides, 0 findings and 0 warnings; 13.3333 × 7.5 inch canvas.
- PNG render QA: all 19 slides rendered from the exported V3 PPTX at 2× (2560 × 1440). The full contact sheet and key slides were reviewed; the chart values, captions, titles and slide boundaries are legible.
- PDF QA: 19 pages at 960 × 540 points (16:9). Poppler `pdfinfo` confirmed the page count and size; pages 1, 7, 12 and 19 were rendered back to PNG and visually checked. The PDF is image-based from the reviewed PNG renders to preserve slide layout.
- The presentation skill’s automated finalizer classified the package-integrity check as a failure. The underlying package validator was rerun directly against the final V3 PPTX and returned **pass**, 0 findings; the layout validator also passed directly. The automated finalizer could not launch its Python child process in this restricted workspace. Artifact-tool’s native PDF export could not load its bundled Helvetica module, so the verified PNG renders were used for PDF output.
- Build scripts are preserved under `BUILD_SOURCE/`; reusable Python-generated figures are in `charts/`.
