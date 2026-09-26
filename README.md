# Bayesian telematics relativities

Authoritative standalone working repository, extracted on 26 September 2026 from Mwendo Pamoja. This is a recorded working-tree snapshot, including unpublished changes; earlier history remains in the originating repository and its local migration bundle.

## Start here

- [Canonical paper](whitepapers/telematics-relativities/paper.md)
- [Mathematical derivations](whitepapers/telematics-relativities/Mathematical_Derivations.md)
- [Implementation plan](whitepapers/telematics-relativities/DETAILED_IMPLEMENTATION_PLAN.md)
- [Correction ledger](whitepapers/telematics-relativities/IMPLEMENTATION_CORRECTION_LEDGER.md)
- [Brian Hey submission package](publications/submissions/brian-hey-2026/README.md)
- [Migration provenance](MIGRATION.md)

## Checks and builds

Run `python validate.py paper.md` from `whitepapers/telematics-relativities`. Build with `scripts/build_paper.ps1` from that directory; it requires Pandoc, Mermaid CLI and the Python document-processing dependencies. Existing relative paths are retained deliberately.

Run `python validation/validate_submission.py` from `publications/submissions/brian-hey-2026` (requires pandas). At extraction this passes the structural/result checks and fails its final canonical-paper hash gate: the working paper differs from the pinned submission baseline. That pre-existing issue remains open; the expected hash has not been reset to make the check pass.

The published PDF is a dated release. Submission outputs and guidelines are curated package assets; build intermediates stay outside version control. The IFRS 17 discussion remains a research interface, not a separate implemented accounting product. Mwendo's controlled specifications and SPV model remain owned by the Mwendo repository.
