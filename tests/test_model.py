"""Tests for TabPFN tabular foundation model inference engine."""

from commuteshield.tabpfn_model import TabPFNCommuteEngine


def test_tabpfn_engine_initialization():
    """Verify that TabPFN commute engine initializes and fits correctly."""
    engine = TabPFNCommuteEngine()
    assert len(engine.X_train) > 30
    assert len(engine.y_train) > 30


def test_tabpfn_predict_safe_commute():
    """A commuter with ₹150 balance and normal routine should have very low risk."""
    engine = TabPFNCommuteEngine()
    pred = engine.predict_risk(
        day_of_week=1,  # Tuesday
        current_balance=150.0,
        scheduled_trips_count=2,
        turf_sports_flag=0,
        days_since_last_topup=1,
        serpapi_disruption_index=1.0,
        historical_daily_burn=35.0,
    )
    assert pred.p_stranded < 0.40
    assert pred.risk_level == "LOW"
    assert pred.expected_shortfall == 0.0


def test_tabpfn_predict_critical_commute():
    """A commuter with ₹12 balance, football turf planned, and transit detour should flag critical risk."""
    engine = TabPFNCommuteEngine()
    pred = engine.predict_risk(
        day_of_week=4,  # Friday
        current_balance=12.0,
        scheduled_trips_count=3,
        turf_sports_flag=1,
        days_since_last_topup=5,
        serpapi_disruption_index=1.25,
        historical_daily_burn=55.0,
    )
    assert pred.is_high_risk
    assert pred.expected_shortfall > 0.0
    assert pred.recommended_topup >= 50.0
