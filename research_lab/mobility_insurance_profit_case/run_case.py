"""Run the hypothetical profit test and write machine-readable outputs."""
import csv
import json
from pathlib import Path

from model import run_case

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"


def main():
    inputs = json.loads((HERE / "assumptions.json").read_text(encoding="utf-8"))
    result = run_case(inputs)
    OUT.mkdir(exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    for plan, ledgers in result["monthly_ledgers"].items():
        for ledger, rows in ledgers.items():
            path = OUT / f"{plan}_{ledger}.csv"
            if not rows:
                continue
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
    summary = {plan: data for plan, data in result["simulation_summaries"].items()}
    (OUT / "summary.json").write_text(json.dumps({
        "currency": result["currency"], "status": result["status"],
        "posterior_summary": result["posterior_summary"],
        "pricing_and_normalisation": result["pricing_and_normalisation"],
        "simulation_summaries": summary,
        "mwendo_156_week_bridge": result["mwendo_156_week_bridge"],
    }, indent=2), encoding="utf-8")
    print(f"Wrote results to {OUT}")
    for name, item in summary.items():
        print(name, "profit after capital", round(item["mean_expected_profit_after_capital"]),
              "break-even/vehicle", round(item["break_even_annual_premium_per_vehicle"]))


if __name__ == "__main__":
    main()
