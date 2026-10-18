# Rebuild the Bayesian Relativities Moove deck

These scripts resolve publication and temporary build paths from their own location in the Bayesian Relativities repository. The 156-week operating bridge is the explicitly documented sibling-repository dependency in `research_lab/mobility_insurance_profit_case/README.md`.

Use the configured Codex workspace Node and Python runtimes, with `@oai/artifact-tool`, Pillow and Arial available. Run `make_charts.py`, `generate_deck_v3.mjs`, `render_deck_v3.mjs`, then `make_pdf_v3.py`. The deck generator reads the stored insurance-case `output/summary.json`; rerun that case first when numerical assumptions change.

`PRESENTATIONS_SKILL_DIR` can override the local presentation helper location, and `CODEX_PYTHON_EXECUTABLE` can override the Python executable used by validation. The defaults resolve from the current user's home directory. Generated deck files remain in this publication folder, while intermediate rendering files go under the repository `.build` directory.
