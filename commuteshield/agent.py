"""Autonomous CommuteShield Orchestrator Agent.

Combines:
1. KTCL Smart Card Scraper (cashless.ktcl.goa.gov.in)
2. SerpApi Goa Transit Disruption Crawler
3. Prior Labs TabPFN In-Context Tabular Foundation Model
4. Headless Multi-Channel Alert Dispatcher
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from commuteshield.config import Config, mask_card_number
from commuteshield.notifier import CommuteShieldNotifier
from commuteshield.scraper import KTCLCardScraper
from commuteshield.serpapi_tool import GoaTransitIntelligence
from commuteshield.tabpfn_model import TabPFNCommuteEngine

logger = logging.getLogger(__name__)


class CommuteShieldAgent:
    """Proactive transit safety agent for Goa student commuters."""

    def __init__(self, card_number: Optional[str] = None):
        self.card_number = card_number or Config.KTCL_CARD_NUMBER
        self.scraper = KTCLCardScraper(self.card_number)
        self.transit_tool = GoaTransitIntelligence()
        self.ml_engine = TabPFNCommuteEngine()
        self.notifier = CommuteShieldNotifier()

    def assess_commute_risk(
        self,
        simulated_balance: Optional[float] = None,
        turf_sports_flag: Optional[int] = None,
        scheduled_trips: Optional[int] = None,
        days_since_topup: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Execute end-to-end CommuteShield inference cycle."""
        now = datetime.now()
        day_of_week = now.weekday()  # 0 = Mon, 4 = Fri, 6 = Sun

        # Step 1: Ingest card balance
        card_status = self.scraper.get_balance(simulated_balance=simulated_balance)
        balance = card_status.balance

        # Step 2: Contextualize student schedule
        # Default: on Friday/Saturday, Tejas often plays football at Wadi turf
        if turf_sports_flag is None:
            turf_sports_flag = 1 if day_of_week in (4, 5) else 0

        if scheduled_trips is None:
            # 2 trips for normal college, 3 if visiting turf / late labs, 0 on Sunday
            if day_of_week == 6:
                scheduled_trips = 0
            elif turf_sports_flag:
                scheduled_trips = 3
            else:
                scheduled_trips = 2

        if days_since_topup is None:
            days_since_topup = card_status.days_since_last_topup

        # Step 3: Query SerpApi live transit intelligence
        transit_report = self.transit_tool.query_live_transit_status(
            origin=Config.HOME_HUB, destination=Config.CAMPUS_HUB
        )

        # Step 4: Run TabPFN tabular foundation model inference
        prediction = self.ml_engine.predict_risk(
            day_of_week=day_of_week,
            current_balance=balance,
            scheduled_trips_count=scheduled_trips,
            turf_sports_flag=turf_sports_flag,
            days_since_last_topup=days_since_topup,
            serpapi_disruption_index=transit_report.disruption_multiplier,
            historical_daily_burn=35.0,
        )

        # Step 5: Format alert text
        alert_msg = self.notifier.format_alert_message(
            commuter_name=Config.COMMUTER_NAME,
            balance=balance,
            p_stranded=prediction.p_stranded,
            shortfall=prediction.expected_shortfall,
            recommended_topup=prediction.recommended_topup,
            explanation=prediction.explanation,
            disruption_status=f"{transit_report.status_level} ({transit_report.disruption_multiplier}x)",
            is_live_sync=card_status.is_live_sync,
        )

        # Step 6: Dispatch notifications if risk is elevated
        dispatched_telegram = False
        if prediction.is_high_risk:
            dispatched_telegram = self.notifier.send_telegram(alert_msg)

        # Visual console display
        self.notifier.dispatch_console(
            commuter_name=Config.COMMUTER_NAME,
            balance=balance,
            p_stranded=prediction.p_stranded,
            shortfall=prediction.expected_shortfall,
            recommended_topup=prediction.recommended_topup,
            explanation=prediction.explanation,
            disruption_status=f"{transit_report.status_level} ({transit_report.source})",
            model_name=prediction.model_name,
            is_live_sync=card_status.is_live_sync,
        )

        # Telemetry logging (privacy-preserving, card masked)
        telemetry_record = {
            "card_masked": mask_card_number(self.card_number),
            "commuter": Config.COMMUTER_NAME,
            "balance": balance,
            "p_stranded": prediction.p_stranded,
            "risk_level": prediction.risk_level,
            "shortfall": prediction.expected_shortfall,
            "recommended_topup": prediction.recommended_topup,
            "serpapi_multiplier": transit_report.disruption_multiplier,
            "serpapi_source": transit_report.source,
            "is_live_sync": card_status.is_live_sync,
            "telegram_sent": dispatched_telegram,
        }
        self.notifier.log_telemetry(telemetry_record)

        return {
            "prediction": prediction,
            "card_status": card_status,
            "transit_report": transit_report,
            "alert_message": alert_msg,
            "telemetry": telemetry_record,
        }
