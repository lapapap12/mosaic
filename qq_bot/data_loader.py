"""Load and parse the Mosaic Ceramics decision analysis CSV."""

import csv
import os

# Default path to the CSV relative to the repository root.
DEFAULT_CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Mosaic_Ceramics_Decision_Analysis.csv",
)


def load_analysis(path=None):
    """Load the decision analysis CSV and return structured data.

    Args:
        path: Optional path to the CSV file. Uses the default if not provided.

    Returns:
        A dict containing the parsed analysis sections.
    """
    if path is None:
        path = DEFAULT_CSV_PATH

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]

    return _parse_rows(rows)


def _parse_rows(rows):
    """Parse raw CSV rows into structured analysis data."""
    data = {
        "probabilities": {},
        "payoff_matrix": [],
        "emv_analysis": [],
        "optimal_decision": "",
        "maximum_emv": "",
        "sensitivity": [],
        "sensitivity_ranking": [],
        "recommendations": [],
    }

    i = 0
    while i < len(rows):
        row = rows[i]
        text = row[0].strip() if row else ""

        if text == "P(Expand)":
            data["probabilities"]["Expand"] = _to_float(row[1])
        elif text == "P(Remain Stable)":
            data["probabilities"]["Remain Stable"] = _to_float(row[1])
        elif text == "P(Decline)":
            data["probabilities"]["Decline"] = _to_float(row[1])
        elif text == "Decision/Outcome":
            # Next rows are payoff matrix entries until blank line
            i += 1
            while i < len(rows) and rows[i] and rows[i][0].strip():
                r = rows[i]
                data["payoff_matrix"].append(
                    {
                        "decision": r[0].strip(),
                        "expand": _to_float(r[1]),
                        "stable": _to_float(r[2]),
                        "decline": _to_float(r[3]),
                    }
                )
                i += 1
            continue
        elif text.startswith("Decision") and len(row) > 3 and "Contribution" in row[1]:
            # EMV analysis header row – read next rows
            i += 1
            while i < len(rows) and rows[i] and rows[i][0].strip():
                r = rows[i]
                if r[0].strip().startswith("OPTIMAL"):
                    break
                data["emv_analysis"].append(
                    {
                        "decision": r[0].strip(),
                        "expand_contribution": _to_float(r[1]),
                        "stable_contribution": _to_float(r[2]),
                        "decline_contribution": _to_float(r[3]),
                        "total_emv": _to_float(r[4]),
                    }
                )
                i += 1
            continue
        elif text.startswith("OPTIMAL DECISION"):
            data["optimal_decision"] = row[1].strip() if len(row) > 1 else ""
        elif text.startswith("MAXIMUM EMV"):
            data["maximum_emv"] = row[1].strip() if len(row) > 1 else ""
        elif text.startswith("1. PRIMARY"):
            data["recommendations"].append(row[1].strip() if len(row) > 1 else "")
        elif text.startswith("2. MOST CRITICAL"):
            data["recommendations"].append(row[1].strip() if len(row) > 1 else "")
        elif text.startswith("3. RISK"):
            data["recommendations"].append(row[1].strip() if len(row) > 1 else "")
        elif text.startswith("4. DECISION"):
            data["recommendations"].append(row[1].strip() if len(row) > 1 else "")

        i += 1

    return data


def _to_float(value):
    """Convert a string value to float, returning 0.0 on failure."""
    try:
        return float(value.strip().replace(",", ""))
    except (ValueError, AttributeError):
        return 0.0


def format_summary(data):
    """Format the analysis data into a human-readable summary string."""
    lines = ["📊 Mosaic Ceramics Decision Analysis", ""]

    lines.append("Probabilities:")
    for k, v in data["probabilities"].items():
        lines.append(f"  • {k}: {v:.0%}")
    lines.append("")

    lines.append("EMV Analysis (million UZS):")
    for entry in data["emv_analysis"]:
        lines.append(f"  • {entry['decision']}: {entry['total_emv']:,.0f}")
    lines.append("")

    lines.append(f"✅ Optimal Decision: {data['optimal_decision']}")
    lines.append(f"💰 Maximum EMV: {data['maximum_emv']} million UZS")
    lines.append("")

    if data["recommendations"]:
        lines.append("Recommendations:")
        for i, rec in enumerate(data["recommendations"], 1):
            lines.append(f"  {i}. {rec}")

    return "\n".join(lines)


def format_payoff_matrix(data):
    """Format the payoff matrix into a readable string."""
    lines = ["📋 Payoff Matrix (million UZS)", ""]
    header = f"{'Decision':<25} {'Expand':>10} {'Stable':>10} {'Decline':>10}"
    lines.append(header)
    lines.append("-" * len(header))
    for entry in data["payoff_matrix"]:
        lines.append(
            f"{entry['decision']:<25} {entry['expand']:>10,.0f} "
            f"{entry['stable']:>10,.0f} {entry['decline']:>10,.0f}"
        )
    return "\n".join(lines)


def format_emv(data):
    """Format the EMV analysis into a readable string."""
    lines = ["📈 Expected Monetary Value (EMV) Analysis", ""]
    for entry in data["emv_analysis"]:
        lines.append(
            f"  {entry['decision']}: {entry['total_emv']:,.0f} million UZS"
        )
    lines.append("")
    lines.append(f"✅ Optimal: {data['optimal_decision']} ({data['maximum_emv']}M UZS)")
    return "\n".join(lines)
