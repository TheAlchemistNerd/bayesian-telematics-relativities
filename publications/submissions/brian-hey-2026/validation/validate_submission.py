"""Validate the Brian Hey 2026 derived manuscript and evidence package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import pandas as pd


CANONICAL_HASH = "283AE8C7A96C362BC6B5E8224F91770C295CB2D4B3357D4AF3E758A58309FFFD"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def locate_canonical(start: Path, explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    for parent in [start, *start.parents]:
        candidate = parent / "whitepapers" / "telematics-relativities" / "paper.md"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("canonical paper.md was not found; pass --canonical")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manuscript", nargs="?", default="Bayesian_Credibility_Telematics_Brian_Hey_2026.md")
    parser.add_argument("--canonical")
    parser.add_argument("--write-hashes", action="store_true")
    args = parser.parse_args()

    manuscript = Path(args.manuscript).resolve()
    root = manuscript.parent
    text = manuscript.read_text(encoding="utf-8")
    require(text.strip() != "", "submission manuscript is empty")
    parts = re.split(r"(?m)^# References\s*$", text)
    require(len(parts) == 2, "expected one top-level References heading")
    body, reference_text = parts

    word_count = len(re.findall(r"\b[\w-]+\b", body, flags=re.UNICODE))
    require(12_000 <= word_count <= 15_500, f"body word count {word_count} is outside 12,000-15,500")

    sections = [int(n) for n in re.findall(r"(?m)^## (\d+)\.\s", body)]
    require(sections == list(range(1, 18)), f"section sequence is incorrect: {sections}")
    figures = [int(n) for n in re.findall(r"(?m)^\*\*Figure (\d+)\.", body)]
    require(figures == list(range(1, 10)), f"figure sequence is incorrect: {figures}")
    tables = [int(n) for n in re.findall(r"(?m)^\*\*Table (\d+)\.", body)]
    require(tables == [1, 2, 3], f"table sequence is incorrect: {tables}")
    require(body.count("```mermaid") == 7, "expected seven Mermaid architecture diagrams")

    tags = re.findall(r"\\tag\{([^}]+)\}", body)
    duplicates = sorted({tag for tag in tags if tags.count(tag) > 1})
    require(not duplicates, f"duplicate equation tags: {duplicates}")

    refs = [int(n) for n in re.findall(r"(?m)^\[(\d+)\]\s", reference_text)]
    cites = [int(n) for n in re.findall(r"\[(\d+)\]", body)]
    first = list(dict.fromkeys(cites))
    require(refs == list(range(1, 52)), f"expected references 1-51, found {refs}")
    require(first == refs, f"citation first appearances do not match references: {first}")
    require(set(cites) == set(refs), "body citations and reference entries do not reconcile")

    require("—" not in text, "em dash detected")
    require(not re.search(r"[A-Za-z]:\\", text), "absolute Windows path detected in manuscript")
    require("file://" not in text, "file URI detected in manuscript")
    require("synthetic" in body.lower(), "synthetic evidence is not labelled")
    require("AI-assisted tools" in body, "AI-assistance declaration is missing")

    image_links = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", body)
    require(len(image_links) == 2, f"expected two linked experiment figures, found {len(image_links)}")
    for link in image_links:
        clean = link.split(" ", 1)[0]
        require((root / clean).exists(), f"missing linked image: {clean}")

    expected_outputs = [
        "experiment/results/model_comparison.csv",
        "experiment/results/representation_and_balance.csv",
        "experiment/results/reserve_comparison.csv",
        "experiment/results/capital_and_risk_transfer.csv",
        "experiment/results/run_manifest.json",
        "experiment/results/synthetic_sample_250_rows.csv",
        "experiment/figures/model_comparison.png",
        "experiment/figures/representation_diagnostics.png",
    ]
    for relative in expected_outputs:
        path = root / relative
        require(path.exists() and path.stat().st_size > 0, f"missing experiment output: {relative}")

    comparison = pd.read_csv(root / "experiment/results/model_comparison.csv")
    require(comparison["model"].tolist() == ["M0", "M1", "M2", "M3", "M4"], "model comparison order is incorrect")
    require(abs(float(comparison.loc[comparison.model == "M4", "severity_deviance"].iloc[0]) - 0.438257) < 1e-5, "M4 severity result changed")
    balance = pd.read_csv(root / "experiment/results/representation_and_balance.csv")
    values = dict(zip(balance.metric, balance.value))
    require(abs(values["calibrated_expected_loss_weighted_mean_relativity"] - 1.0) < 1e-10, "calibrated relativity is not balanced")
    require(values["max_abs_explicit_residual_embedding_correlation"] < 0.01, "residual embedding correlation control failed")

    canonical = locate_canonical(root, args.canonical)
    canonical_hash = sha256(canonical)
    require(canonical_hash == CANONICAL_HASH, f"canonical paper hash changed: {canonical_hash}")

    hashes = {
        "canonical_paper_md": {"path": str(canonical), "sha256": canonical_hash},
        "submission_markdown": {"path": str(manuscript), "sha256": sha256(manuscript)},
    }
    docx = manuscript.with_suffix(".docx")
    if docx.exists():
        hashes["submission_docx"] = {"path": str(docx), "sha256": sha256(docx)}
    if args.write_hashes:
        output = root / "validation" / "final_hashes.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(hashes, indent=2), encoding="utf-8")

    print("PASS: Brian Hey 2026 submission package")
    print(f"  body words: {word_count:,}")
    print(f"  references: {len(refs)}")
    print(f"  equations: {len(tags)}")
    print(f"  figures: {len(figures)}")
    print(f"  tables: {len(tables)}")
    print(f"  canonical hash: {canonical_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
