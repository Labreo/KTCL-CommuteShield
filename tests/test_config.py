"""Tests for configuration and privacy-preserving masking."""

from commuteshield.config import Config, mask_card_number


def test_card_masking():
    """Verify that card numbers are properly masked for privacy."""
    assert mask_card_number("ST2512345678") == "ST25****5678"
    assert mask_card_number("1234567890") == "1234**7890"
    assert mask_card_number("1234") == "****"
    assert mask_card_number("") == "UNKNOWN_CARD"
    assert mask_card_number(None) == "UNKNOWN_CARD"


def test_config_defaults():
    """Verify configuration defaults are sensible."""
    assert len(Config.COMMUTER_NAME) > 0
    assert Config.HOME_HUB == "Margao"
    assert Config.CAMPUS_HUB == "Farmagudi"
    assert Config.RISK_THRESHOLD == 0.60
    assert Config.COMMUTE_HISTORY_PATH.exists()


def test_masked_summary_does_not_leak_full_card():
    """Ensure summary dict hides the full card number."""
    summary = Config.get_masked_summary()
    assert "ST25" in summary["card_masked"]
    assert "****" in summary["card_masked"]
    assert summary["card_masked"] != Config.KTCL_CARD_NUMBER
