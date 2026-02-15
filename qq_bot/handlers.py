"""Command handlers for the QQ bot."""

from qq_bot.data_loader import (
    format_emv,
    format_payoff_matrix,
    format_summary,
    load_analysis,
)

HELP_TEXT = (
    "🤖 Mosaic Ceramics Bot Commands:\n"
    "  /help      - Show this help message\n"
    "  /summary   - Full decision analysis summary\n"
    "  /emv       - Expected Monetary Value analysis\n"
    "  /payoff    - Payoff matrix\n"
    "  /recommend - Key recommendations"
)

_analysis_cache = {}


def _get_analysis(csv_path=None):
    """Return cached analysis data, loading from disk on first call."""
    key = csv_path or "__default__"
    if key not in _analysis_cache:
        _analysis_cache[key] = load_analysis(csv_path)
    return _analysis_cache[key]


def handle_command(content, csv_path=None):
    """Process a command string and return the appropriate response.

    Args:
        content: The message content (command string).
        csv_path: Optional path to the CSV data file.

    Returns:
        A response string, or None if the content is not a recognized command.
    """
    cmd = content.strip().split()[0].lower() if content.strip() else ""

    if cmd == "/help":
        return HELP_TEXT

    if cmd == "/summary":
        return format_summary(_get_analysis(csv_path))

    if cmd == "/emv":
        return format_emv(_get_analysis(csv_path))

    if cmd == "/payoff":
        return format_payoff_matrix(_get_analysis(csv_path))

    if cmd == "/recommend":
        data = _get_analysis(csv_path)
        if not data["recommendations"]:
            return "No recommendations available."
        lines = ["💡 Key Recommendations:"]
        for i, rec in enumerate(data["recommendations"], 1):
            lines.append(f"  {i}. {rec}")
        return "\n".join(lines)

    return None
