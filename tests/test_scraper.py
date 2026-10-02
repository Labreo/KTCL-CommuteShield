"""Tests for KTCL portal scraper and offline fallback."""

from commuteshield.scraper import KTCLCardScraper


def test_scraper_token_encoding():
    """Verify base64 encoding matches KTCL portal format."""
    scraper = KTCLCardScraper("ST2599999999")
    token = scraper._encode_card_token("ST2599999999")
    assert isinstance(token, str)
    assert len(token) > 0


def test_scraper_simulated_balance():
    """Verify deterministic simulation behavior."""
    scraper = KTCLCardScraper("ST2599999999")
    res = scraper.get_balance(simulated_balance=18.50)
    assert res.balance == 18.50
    assert res.card_number == "ST2599999999"
    assert res.card_number_masked == "ST25****9999"
    assert not res.is_live_sync


def test_scraper_fallback_on_unreachable():
    """Verify fallback executes gracefully when portal is unreachable."""
    scraper = KTCLCardScraper("ST2599999999")
    # Setting an unreachable base URL
    scraper.BASE_URL = "http://127.0.0.1:9999"
    scraper.TIMEOUT = 0.5
    res = scraper.get_balance()
    assert res.balance > 0
    assert not res.is_live_sync
    assert "offline" in res.source_message.lower()
