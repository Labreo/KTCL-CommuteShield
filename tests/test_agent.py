"""Tests for end-to-end CommuteShieldAgent."""

from commuteshield.agent import CommuteShieldAgent


def test_agent_assessment_safe():
    """Verify agent correctly handles a safe commuter state."""
    agent = CommuteShieldAgent()
    result = agent.assess_commute_risk(
        simulated_balance=180.0,
        turf_sports_flag=0,
        scheduled_trips=2,
    )
    assert "prediction" in result
    assert "card_status" in result
    assert "telemetry" in result
    assert not result["prediction"].is_high_risk


def test_agent_assessment_stranded_risk():
    """Verify agent flags risk when balance is insufficient for tomorrow's schedule."""
    agent = CommuteShieldAgent()
    result = agent.assess_commute_risk(
        simulated_balance=15.0,
        turf_sports_flag=1,
        scheduled_trips=3,
    )
    assert result["prediction"].is_high_risk
    assert "Alert" in result["alert_message"]
    assert "11:59 PM" in result["alert_message"]
