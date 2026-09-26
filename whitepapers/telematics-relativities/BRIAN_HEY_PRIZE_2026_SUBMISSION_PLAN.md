# Brian Hey Prize 2026 Submission Implementation Plan

## 1. Objective

Prepare a competition-specific edition of *Bayesian Credibility and Exposure-Normalised Telematics Relativities* for submission to the Institute and Faculty of Actuaries' Brian Hey Prize 2026.

The submission edition will be created as a separate Markdown manuscript and compiled into a separate Microsoft Word document. The current telematics white paper will remain unchanged and will continue to serve as the canonical long-form source.

The purpose of the submission pass is to sharpen, demonstrate and package the existing contribution for a general-insurance research audience. It will preserve the paper's actuarial architecture, mathematical development, human narrative and technical novelty while making its central contribution easier for a prize panel to identify and evaluate.

## 2. Preservation and isolation policy

The canonical source is:

whitepapers/telematics-relativities/paper.md

Its pre-submission SHA-256 hash is:

283AE8C7A96C362BC6B5E8224F91770C295CB2D4B3357D4AF3E758A58309FFFD

The following controls will apply:

- paper.md will be treated as read-only throughout the submission exercise.
- The current paper.docx will not be overwritten.
- Existing diagrams, derivations, references and supporting notes will remain available to the submission edition but will not be destructively edited.
- All competition-specific rewriting will occur in a newly created submission Markdown file.
- The Word submission will use a distinct filename.
- Build intermediates, rendered previews and validation output will be isolated from the canonical manuscript.
- A final hash check will confirm that paper.md is unchanged.

The proposed derived working structure is:

    publications/
    └── submissions/
        └── brian-hey-2026/
            ├── Bayesian_Credibility_Telematics_Brian_Hey_2026.md
            ├── Bayesian_Credibility_Telematics_Brian_Hey_2026.docx
            ├── submission_requirements.md
            ├── experiment/
            ├── figures/
            ├── tables/
            ├── references/
            └── validation/

The exact destination can be reconciled with the repository's publication conventions at implementation time. The separation principle is locked even if the final folder name changes.

## 3. Readiness assessment

### Verdict: Yes, with a final submission pass

The telematics paper has the characteristics of a credible Brian Hey submission:

- It addresses general insurance directly.
- It is actuarially grounded rather than merely presenting a machine-learning model.
- It connects pricing, credibility, reserving, economic capital and risk transfer.
- It contains a genuine methodological contribution: exposure-normalised actuarial modulation.
- It separates claim frequency, conditional severity and exposure.
- It introduces cross-fitted neural residualisation and regularised horseshoe shrinkage without abandoning actuarial interpretability.
- It connects predictive distributions to RBNS, IBNR, IBNER, capital and reinsurance.
- It addresses governance, fairness, point-in-time data and operational deployment.
- It tells a relatable story about gig-economy motor risk while remaining mathematically rigorous.

That combination aligns well with previous winning themes. Recent winners have included interpretable machine learning, dependency modelling, reserving and capital-modelling methodology. The IFoA describes the prize as recognising work that advances practical general-insurance practice. See the [official Brian Hey Prize page](https://actuaries.org.uk/about-us/prizes-and-awards/best-paper-prizes/brian-hey-prize/).

### Main competitive weakness

The paper's greatest remaining weakness is empirical demonstration.

It contains a comprehensive architecture and mathematical specification, but a judging panel may want to see the methodology operating on:

- an empirical dataset;
- a credible synthetic portfolio;
- a controlled simulation; or
- a numerical worked example comparing competing specifications.

The strongest final addition would be a compact experiment comparing:

1. Traditional tariff or GLM.
2. Explicit telematics hierarchical model.
3. Explicit plus unadjusted neural embedding.
4. Explicit plus residualised neural embedding.
5. Explicit plus residualised neural embedding with regularised horseshoe shrinkage.

The results could report:

- out-of-time frequency deviance;
- severity deviance;
- observed-to-expected loss;
- calibration slope;
- stability under covariate shift;
- portfolio balance before and after exposure-normalisation;
- posterior interval coverage; and
- changes in indicated capital or treaty-layer loss.

If actual data cannot be used before the deadline, a clearly labelled synthetic experiment would still demonstrate computational feasibility. It must be presented as an illustration rather than empirical evidence about Kenyan drivers.

### Required final submission work

The paper needs a competition-specific preparation pass:

- Sharpen the abstract around one principal contribution.
- State the original contribution in two or three explicit sentences.
- Add a practical numerical demonstration if feasible.
- Add a compact “Implications for general insurers” section.
- Ensure all equations and figures reproduce correctly.
- Confirm every citation and reference.
- Add author information, acknowledgements and relevant declarations.
- Check the official guidelines concerning originality, prior online publication, copyright and disclosure of AI-assisted drafting.
- Produce one clean anonymous or identified Word document according to the official submission instructions.

The readiness assessment is:

- **Thematic fit:** 9/10.
- **Technical substance:** 8.5/10.
- **Current competitive readiness:** 7/10.
- **Readiness after a focused final pass:** 8.5/10.

## 4. Submission positioning

The submission should be organised around one principal research question:

> How can high-frequency telematics contribute credible, explainable evidence to an actuarial tariff while the same predictive distribution supports claims reserving, economic capital and risk-transfer decisions?

The principal contribution should be stated in a compact form:

> The paper develops an exposure-normalised actuarial modulating variable that combines interpretable telematics features and residual neural representations within a hierarchical Bayesian frequency-severity model, then recalibrates the resulting relativities to preserve the approved portfolio expected-loss foundation.

The supporting contributions are:

1. Explicit separation of exposure, claim frequency and conditional severity.
2. Canonical ownership of engineered features and neural sequence information.
3. Cross-fitted residualisation to reduce redundant neural representation.
4. Regularised-horseshoe shrinkage for the remaining neural block.
5. Hierarchical Bayesian credibility for individual and group experience.
6. Portfolio-balanced calibration of actuarial relativities.
7. A continuous predictive path from pricing into reserving, capital and risk transfer.
8. A point-in-time production and governance architecture.

These contributions should appear prominently in the abstract, introduction and conclusion. The submission should avoid presenting all components as equally central. Exposure-normalised modulation is the lead contribution; the remaining components demonstrate its actuarial coherence and practical reach.

## 5. Submission manuscript architecture

The separate submission Markdown should use a tighter research-paper structure:

1. **Title and author information**
2. **Abstract**
3. **Keywords**
4. **Research question and contribution**
5. **Actuarial motivation and gig-economy context**
6. **Exposure, frequency and conditional severity**
7. **Exposure-normalised actuarial modulation**
8. **Explicit features and residual neural representation**
9. **Hierarchical credibility and prior structure**
10. **Empirical or synthetic demonstration**
11. **Calibration, validation and fairness**
12. **Reserving, economic capital and risk-transfer implications**
13. **Implementation and model governance**
14. **Implications for general insurers**
15. **Limitations and research extensions**
16. **Conclusion**
17. **References**
18. **Technical appendices**

The submission edition may abridge material that is valuable in the white paper but peripheral to the prize argument. Abridgement will occur only in the derived manuscript. Detailed derivations, state schemas and extended governance material can move to appendices rather than disappearing.

## 6. Empirical or synthetic demonstration

### 6.1 Demonstration purpose

The experiment should establish whether the proposed architecture:

- improves held-out predictive performance;
- preserves portfolio expected-loss calibration;
- reduces redundant neural contribution;
- produces stable hierarchical estimates for sparse drivers or groups;
- preserves interpretable actuarial quantities; and
- generates usable reserve, capital or risk-transfer outputs.

The experiment is evidence about the implementation, not a decorative example.

### 6.2 Dataset strategy

The preferred evidence hierarchy is:

1. A lawful, documented empirical telematics and claims dataset with suitable permissions.
2. A public motor-insurance or telematics dataset that supports a defensible subset of the experiment.
3. A calibrated synthetic portfolio designed to reproduce stated actuarial mechanisms.
4. A compact numerical worked example where computational time prevents a larger study.

Synthetic data must be labelled consistently in the abstract, methods, tables, figures and conclusion. Generated drivers must not be described as observations from Kenya or any other real population.

### 6.3 Synthetic portfolio design

If the synthetic route is used, the experiment should define:

- policy and driver count;
- exposure distribution;
- traditional tariff cells;
- kilometres, active hours or covered days;
- explicit telematics variables;
- latent sequence factors;
- geography, vehicle and calendar effects;
- frequency process;
- conditional-severity process;
- persistent driver heterogeneity;
- claims-development timing;
- catastrophe or common-shock scenarios; and
- reinsurance terms.

The data-generating process should include controlled overlap between explicit variables and the raw neural representation. This is necessary to test whether cross-fitted residualisation and horseshoe shrinkage reduce duplication as intended.

### 6.4 Candidate models

The comparison should be implemented on identical training and evaluation splits:

- **M0:** Traditional tariff or GLM benchmark.
- **M1:** Hierarchical model with explicit telematics features.
- **M2:** Hierarchical model with explicit features and unadjusted neural embedding.
- **M3:** Hierarchical model with explicit features and cross-fitted residual neural embedding.
- **M4:** M3 with regularised-horseshoe shrinkage.

Where computationally feasible, include:

- a frequency-only ablation;
- a severity-only ablation;
- residualised versus residualised-and-whitened embeddings; and
- calibrated versus uncalibrated relativities.

### 6.5 Evaluation

The principal evaluation set should be a future-period holdout grouped by driver. Validation should report:

- Poisson or negative-binomial frequency deviance;
- Gamma or selected severity-family deviance;
- aggregate pure-premium error;
- observed-to-expected claims and losses;
- calibration intercept and slope;
- Brier or log score where a binary target is used;
- interval coverage;
- coefficient and relativity stability;
- posterior correlation;
- effective neural dimension;
- portfolio expected-loss balance;
- capital quantiles;
- treaty attachment and exhaustion probability; and
- sensitivity under simulated covariate shift.

The results table should distinguish statistical improvement from financial relevance. A small predictive gain may still be valuable if it materially improves calibration, capital allocation or treaty monitoring; a large in-sample gain is insufficient if future-period stability deteriorates.

### 6.6 Reproducibility

The experiment package should contain:

- random seed;
- environment and dependency versions;
- data-generation parameters;
- split definitions;
- model specifications;
- prior specifications;
- convergence diagnostics;
- calibration procedure;
- table-generation code;
- figure-generation code; and
- a command or script that reproduces the final outputs.

## 7. Editorial method

The submission will use advancing, research-oriented language. It will present the architecture as a practical actuarial development rather than constructing the argument around defensive qualifications.

The writing should:

- begin with the human and commercial problem;
- define actuarial quantities before introducing computation;
- distinguish a methodological contribution from an implementation choice;
- connect each equation to an actuarial decision;
- use limitations to define the next validation step;
- state synthetic evidence positively and accurately;
- use restrained claims supported by the actual experiment;
- preserve technical depth in appendices; and
- conclude with practical implications for general insurers.

The final submission should read as a coherent research paper, not as a shortened technical specification.

## 8. References and evidence

The submission will retain primary actuarial, statistical and technical sources from the white paper. Every retained reference must support a claim that remains in the derived manuscript.

The reference pass will:

- verify titles, authors, publication details, DOI and URL;
- remove uncited entries;
- add any competition-guideline or methodological sources required by the experiment;
- preserve one consistent citation style;
- ensure each reference begins as its own paragraph;
- confirm first-appearance ordering if a numerical citation style is used; and
- check that tables, figures and equations cite the appropriate source or state that they are the author's construction.

## 9. Competition compliance

Before producing the final submission, download and freeze the official 2026 prize guidelines in the submission folder. Record:

- deadline and submission time;
- eligibility;
- accepted file format;
- length or page guidance;
- anonymisation requirements;
- author and affiliation format;
- prior-publication restrictions;
- copyright and licensing terms;
- originality declaration;
- use-of-AI disclosure requirements;
- supplementary-material rules; and
- submission-portal fields.

Where the guidelines require a declaration regarding drafting or analytical tools, the declaration should be accurate, concise and consistent with the author's responsibility for the work.

## 10. Word compilation

The derived Markdown manuscript will be compiled into a new .docx file using Pandoc. The build must not use the existing paper.docx as a writable target.

The Word workflow will:

1. Create or select a dedicated reference Word template.
2. Map headings to Word styles.
3. Convert LaTeX mathematics to native Word equations where supported.
4. Insert diagrams and figures at publication-quality resolution.
5. Preserve figure and table captions.
6. Keep equations, captions and associated discussion together where practical.
7. Generate page breaks for references and appendices where required.
8. Apply consistent margins, typography, spacing and page numbering.
9. Create accessible alt text or descriptive captions for substantive figures where practicable.
10. Produce a clean final Word document without tracked changes, comments or local filesystem links.

The Word output will be rendered to PDF or page images for visual quality assurance. The render is a checking artifact; the submitted format will follow the official guidelines.

## 11. Quality assurance

### Content checks

- The abstract states the research question, method, principal contribution, evidence and implication.
- The central contribution is visible in the introduction and conclusion.
- The experiment is reproducible.
- Synthetic evidence is labelled accurately.
- Every numerical result is traceable.
- Pricing, reserving, economic capital and risk transfer remain distinct.
- Exposure remains separate from the claim-rate parameter.
- Frequency and conditional severity remain distinct.
- Residualisation is not described as causal identification.
- Whitening is not described as complete independence.
- The regularised horseshoe is not described as feature ownership.
- IFRS 17 remains a governed accounting interface.

### Technical checks

- All equations compile.
- Symbols have one canonical meaning.
- Equation references resolve.
- Figure and table numbering is sequential.
- Cross-references resolve.
- References are complete and cited.
- No missing image or absolute local path remains.
- Statistical results tie to the experiment output.

### Word checks

- No clipping, overlap or orphaned caption appears.
- Tables fit within page margins.
- Equations remain legible and editable where possible.
- Headers, footers and page numbers behave consistently.
- References begin on a new page if required.
- Appendices begin on new pages.
- No tracked changes, comments or temporary text remains.

### Preservation check

At completion:

- recompute the SHA-256 hash of paper.md;
- compare it with 283AE8C7A96C362BC6B5E8224F91770C295CB2D4B3357D4AF3E758A58309FFFD;
- confirm that paper.docx was not overwritten; and
- record the hashes of the final submission Markdown and Word documents.

## 12. Implementation sequence

### Stage 1: Requirements and source freeze

- Download the official guidelines.
- Record submission requirements.
- Verify the canonical source hash.
- Create the isolated submission directory.

### Stage 2: Derived manuscript

- Copy the intellectual content into the new submission Markdown.
- Rewrite the abstract and contribution statement.
- Reorder material around the prize research question.
- Move extended derivations and controls to appendices.
- Add the implications section.

### Stage 3: Demonstration

- Select the evidence route.
- Implement the model comparison.
- Validate convergence and calibration.
- Generate final tables and figures.
- Insert results into the derived manuscript.

### Stage 4: Scholarly and compliance review

- Verify claims and references.
- Review originality and publication conditions.
- Add author, acknowledgement and disclosure material.
- Complete an actuarial peer review if time permits.

### Stage 5: Word compilation

- Compile the separate Markdown manuscript.
- Render and inspect every page.
- Correct Word-specific layout defects.
- Produce the final clean .docx.

### Stage 6: Submission

- Complete the official portal fields.
- Upload the final file and permitted supplements.
- Save the confirmation.
- Record submitted-file hashes and submission time.

## 13. Acceptance criteria

The Brian Hey submission package will be complete only when:

- the original paper.md hash is unchanged;
- a separate submission Markdown exists;
- a separate final Word document exists;
- the abstract identifies one principal contribution;
- the contribution is supported by a practical numerical demonstration or clearly documented alternative;
- every experiment result is reproducible;
- all synthetic evidence is labelled accurately;
- the paper demonstrates practical value for general insurers;
- equations, figures, tables and references are correct;
- competition instructions and declarations are satisfied;
- the Word document passes full visual inspection;
- no canonical source file has been overwritten; and
- the submission confirmation and final hashes are retained.

## 14. Locked decisions

- The current telematics Markdown white paper remains unchanged.
- The current Word edition remains unchanged.
- Competition-specific editing occurs only in the derived submission manuscript.
- Exposure-normalised actuarial modulation remains the lead contribution.
- Actuarial interpretation remains more important than algorithmic spectacle.
- Empirical or synthetic evidence will be described according to its actual status.
- The final deliverable will be a separate Word document compiled from the separate submission Markdown.
