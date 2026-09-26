# Brian Hey Prize 2026 submission package

This directory contains the competition-specific edition of *Bayesian Credibility and Exposure-Normalised Telematics Relativities*. The canonical white paper in `whitepapers/telematics-relativities/paper.md` is not modified by this package.

## Primary deliverables

- `Bayesian_Credibility_Telematics_Brian_Hey_2026.md`: derived submission manuscript.
- `Bayesian_Credibility_Telematics_Brian_Hey_2026.docx`: clean Word submission edition.
- `submission_requirements.md`: official requirements, unresolved author actions and a covering-note draft.
- `2026-brian-hey-guidelines.docx`: frozen official IFoA guidance downloaded on 30 August 2026.

## Reproduce the synthetic comparison

Run from this directory:

```powershell
python experiment/run_synthetic_comparison.py
```

The script uses seed `260831` and writes the following evidence:

- `experiment/results/model_comparison.csv`
- `experiment/results/representation_and_balance.csv`
- `experiment/results/reserve_comparison.csv`
- `experiment/results/capital_and_risk_transfer.csv`
- `experiment/results/run_manifest.json`
- `experiment/results/synthetic_sample_250_rows.csv`
- `experiment/figures/model_comparison.png`
- `experiment/figures/representation_diagnostics.png`

The data are synthetic. No row represents an actual policyholder, claim, insurer or Kenyan driver.

The experiment and validator require Python with NumPy, pandas and Pillow.

## Rebuild the Word manuscript

The Word build requires Pandoc, Mermaid CLI and Python with `python-docx`:

```powershell
.\scripts\build_submission.ps1 -PythonPath "C:\path\to\python.exe"
```

The build renders the seven Mermaid diagrams, converts the derived Markdown manuscript with Pandoc and applies the documented Word styles, page breaks, table geometry, alternative text and headers and footers. It does not read from or modify the canonical `paper.md`.

## Validate the package

Run:

```powershell
python validation/validate_submission.py Bayesian_Credibility_Telematics_Brian_Hey_2026.md
```

The validator reconciles sections, figures, tables, equations, citations, references, experiment outputs and the canonical-paper preservation hash recorded in the submission plan.
