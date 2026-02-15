"""Tests for the data loader."""

import os

from qq_bot.data_loader import (
    format_emv,
    format_payoff_matrix,
    format_summary,
    load_analysis,
)

CSV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Mosaic_Ceramics_Decision_Analysis.csv",
)


def test_load_analysis_probabilities():
    data = load_analysis(CSV_PATH)
    assert data["probabilities"]["Expand"] == 0.25
    assert data["probabilities"]["Remain Stable"] == 0.35
    assert data["probabilities"]["Decline"] == 0.40


def test_load_analysis_payoff_matrix():
    data = load_analysis(CSV_PATH)
    assert len(data["payoff_matrix"]) == 3
    assert data["payoff_matrix"][0]["decision"] == "Construct New Plant"
    assert data["payoff_matrix"][0]["expand"] == 45000.0
    assert data["payoff_matrix"][1]["decision"] == "Expand Existing Plant"
    assert data["payoff_matrix"][2]["decision"] == "Do Nothing"


def test_load_analysis_emv():
    data = load_analysis(CSV_PATH)
    assert len(data["emv_analysis"]) == 3
    assert data["emv_analysis"][0]["total_emv"] == -250.0
    assert data["emv_analysis"][1]["total_emv"] == 1500.0
    assert data["emv_analysis"][2]["total_emv"] == 50.0


def test_load_analysis_optimal_decision():
    data = load_analysis(CSV_PATH)
    assert data["optimal_decision"] == "Expand Existing Plant"
    assert data["maximum_emv"] == "1500"


def test_load_analysis_recommendations():
    data = load_analysis(CSV_PATH)
    assert len(data["recommendations"]) == 4
    assert "Expand the existing plant" in data["recommendations"][0]


def test_format_summary():
    data = load_analysis(CSV_PATH)
    text = format_summary(data)
    assert "Mosaic Ceramics" in text
    assert "Expand Existing Plant" in text
    assert "1500" in text


def test_format_payoff_matrix():
    data = load_analysis(CSV_PATH)
    text = format_payoff_matrix(data)
    assert "Construct New Plant" in text
    assert "45,000" in text


def test_format_emv():
    data = load_analysis(CSV_PATH)
    text = format_emv(data)
    assert "Expected Monetary Value" in text
    assert "Expand Existing Plant" in text
