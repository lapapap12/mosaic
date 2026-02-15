"""Tests for command handlers."""

import os

from qq_bot.handlers import HELP_TEXT, handle_command

CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Mosaic_Ceramics_Decision_Analysis.csv",
)


def test_help_command():
    result = handle_command("/help", csv_path=CSV_PATH)
    assert result == HELP_TEXT
    assert "/summary" in result


def test_summary_command():
    result = handle_command("/summary", csv_path=CSV_PATH)
    assert "Mosaic Ceramics" in result
    assert "Expand Existing Plant" in result


def test_emv_command():
    result = handle_command("/emv", csv_path=CSV_PATH)
    assert "Expected Monetary Value" in result


def test_payoff_command():
    result = handle_command("/payoff", csv_path=CSV_PATH)
    assert "Payoff Matrix" in result
    assert "Construct New Plant" in result


def test_recommend_command():
    result = handle_command("/recommend", csv_path=CSV_PATH)
    assert "Recommendations" in result
    assert "Expand the existing plant" in result


def test_unknown_command():
    result = handle_command("/unknown", csv_path=CSV_PATH)
    assert result is None


def test_empty_command():
    result = handle_command("", csv_path=CSV_PATH)
    assert result is None
