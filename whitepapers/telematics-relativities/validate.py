"""Structural validator for the canonical telematics actuarial white paper.

Run from the telematics-relativities directory:
    python validate.py paper.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "paper.md")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        fail("paper is empty")

    parts = re.split(r"(?m)^# References\s*$", text)
    if len(parts) != 2:
        fail("expected exactly one top-level References heading")
    body, reference_text = parts

    body_words = re.findall(r"\b[\w-]+\b", body, flags=re.UNICODE)
    if not 9_500 <= len(body_words) <= 12_500:
        fail(f"body word count {len(body_words)} is outside 9,500-12,500")

    refs = [int(n) for n in re.findall(r"(?m)^\[(\d+)\]\s", reference_text)]
    if refs != list(range(1, len(refs) + 1)):
        fail("reference numbers are not contiguous from 1")
    if not 45 <= len(refs) <= 65:
        fail(f"expected 45-65 references, found {len(refs)}")

    citations = [int(n) for n in re.findall(r"\[(\d+)\]", body)]
    distinct_first_appearance = list(dict.fromkeys(citations))
    if distinct_first_appearance != refs:
        fail(
            "citation first appearances do not match the reference sequence: "
            f"{distinct_first_appearance}"
        )
    if set(citations) != set(refs):
        fail("body citations and reference entries do not reconcile")

    numbered_sections = [
        int(n)
        for n in re.findall(r"(?m)^## (\d+)\.\s", body)
    ]
    if numbered_sections != list(range(1, 15)):
        fail(f"top-level numbered sections are inconsistent: {numbered_sections}")

    equation_tags = re.findall(r"\\tag\{([^}]+)\}", body)
    duplicates = sorted({tag for tag in equation_tags if equation_tags.count(tag) > 1})
    if duplicates:
        fail(f"duplicate equation tags: {duplicates}")

    mermaid_opens = len(re.findall(r"(?m)^```mermaid\s*$", body))
    all_fences = len(re.findall(r"(?m)^```", body))
    if mermaid_opens != 7:
        fail(f"expected seven Mermaid figures, found {mermaid_opens}")
    if all_fences % 2:
        fail("unbalanced fenced code blocks")

    required_phrases = [
        "exposure-normalised actuarial modulating variable",
        "Cross-fitted neural representation residualisation",
        "regularised horseshoe",
        "RBNS",
        "IBNR",
        "economic capital",
        "Risk-transfer pricing and monitoring",
        "IFRS 17 measurement interface",
    ]
    missing = [phrase for phrase in required_phrases if phrase.lower() not in text.lower()]
    if missing:
        fail(f"required concepts missing: {missing}")

    forbidden = [
        "Tabular Bypass",
        "strictly adhering to IFRS 17 standards",
        "This neutrality is enforced via the Double Machine Learning",
        "direct sensor writes to PostgreSQL",
        "SPV Monte Carlo Simulation Architecture",
    ]
    present = [phrase for phrase in forbidden if phrase in text]
    if present:
        fail(f"legacy or misleading phrases remain: {present}")

    if "\u2014" in text:
        fail("em dash detected; use sentence punctuation or a hyphen")

    print(f"PASS: {path}")
    print(f"  body words: {len(body_words):,}")
    print(f"  references: {len(refs)}")
    print(f"  equations: {len(equation_tags)}")
    print(f"  Mermaid figures: {mermaid_opens}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
