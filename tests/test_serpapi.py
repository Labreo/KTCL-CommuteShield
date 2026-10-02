"""Tests for SerpApi Goa transit disruption crawler."""

from commuteshield.serpapi_tool import GoaTransitIntelligence


def test_transit_intelligence_regional_fallback():
    """Verify grounded regional transit advisory fallback when API key is omitted."""
    intel = GoaTransitIntelligence(api_key="")
    report = intel.query_live_transit_status(origin="Margao", destination="Farmagudi")
    assert report.disruption_multiplier >= 1.0
    assert len(report.active_advisories) > 0
    assert not report.is_live_serp
    assert "Regional" in report.source


def test_transit_intelligence_live_with_env_key():
    """Verify live SerpApi search works with configured key."""
    intel = GoaTransitIntelligence()
    if intel.api_key:
        report = intel.query_live_transit_status(origin="Margao", destination="Farmagudi")
        assert report.is_live_serp
        assert "SerpApi" in report.source
        assert len(report.active_advisories) > 0


def test_transit_intelligence_keyword_detection():
    """Ensure disruption keyword dictionary has calibrated weights."""
    keywords = GoaTransitIntelligence.DISRUPTION_KEYWORDS
    assert "flood" in keywords
    assert "strike" in keywords
    assert "detour" in keywords
    assert keywords["strike"] > keywords["detour"]
