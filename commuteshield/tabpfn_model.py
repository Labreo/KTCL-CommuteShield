"""Prior Labs TabPFN Tabular Foundation Model Engine.

Target Category: Best Use of TabPFN (Featured Category - $200 USD).
TabPFN is a Transformer foundation model pre-trained on millions of synthetic
tabular datasets that performs in-context Bayesian inference on tabular data
in a single forward pass without iterative training or hyperparameter tuning.

It excels on small personal datasets (N=30 to 100 commute records) where
gradient-boosted trees and neural nets overfit.
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd

from commuteshield.config import Config

logger = logging.getLogger(__name__)

FEATURE_COLUMNS = [
    "day_of_week",
    "current_balance",
    "scheduled_trips_count",
    "turf_sports_flag",
    "days_since_last_topup",
    "serpapi_disruption_index",
    "historical_daily_burn",
]
TARGET_COLUMN = "stranded_event"


@dataclass
class StrandedRiskPrediction:
    """Output from the TabPFN tabular inference engine."""
    p_stranded: float
    is_high_risk: bool
    risk_level: str  # "LOW", "MODERATE", "CRITICAL"
    expected_shortfall: float
    recommended_topup: float
    feature_dict: Dict[str, Union[int, float]]
    model_name: str
    explanation: str


class TabPFNCommuteEngine:
    """TabPFN tabular foundation model for bus card exhaustion risk forecasting."""

    def __init__(self, data_path: Optional[Path] = None):
        self.data_path = data_path or Config.COMMUTE_HISTORY_PATH
        self.classifier = None
        self.fallback_classifier = None
        self.is_tabpfn_active = False
        self._load_and_fit()

    def _load_and_fit(self):
        """Load commute history and prepare the in-context TabPFN model."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Commute history dataset not found at {self.data_path}")

        df = pd.read_csv(self.data_path)
        self.X_train = df[FEATURE_COLUMNS].values.astype(float)
        self.y_train = df[TARGET_COLUMN].values.astype(int)

        # Attempt to load TabPFN foundation model
        try:
            import os
            if Config.TABPFN_TOKEN:
                os.environ["TABPFN_TOKEN"] = Config.TABPFN_TOKEN
            from tabpfn import TabPFNClassifier
            logger.info("Initializing Prior Labs TabPFNClassifier (device='cpu')...")
            self.classifier = TabPFNClassifier(device="cpu", n_estimators=4)
            self.classifier.fit(self.X_train, self.y_train)
            self.is_tabpfn_active = True
            logger.info("TabPFN in-context model loaded successfully on %d commute records.", len(df))
        except Exception as e:
            logger.warning(
                "TabPFN foundation model load deferred (%s). Preparing calibrated Bayesian fallback.",
                str(e),
            )
            # Calibrated ensemble fallback
            from sklearn.ensemble import HistGradientBoostingClassifier
            from sklearn.calibration import CalibratedClassifierCV
            base = HistGradientBoostingClassifier(random_state=42, max_iter=50)
            self.fallback_classifier = CalibratedClassifierCV(estimator=base, cv=3)
            self.fallback_classifier.fit(self.X_train, self.y_train)
            self.is_tabpfn_active = False

    def predict_risk(
        self,
        day_of_week: int,
        current_balance: float,
        scheduled_trips_count: int,
        turf_sports_flag: int,
        days_since_last_topup: int,
        serpapi_disruption_index: float = 1.0,
        historical_daily_burn: float = 35.0,
    ) -> StrandedRiskPrediction:
        """Calculate calibrated P(stranded) and recommended top-up amount."""
        features = np.array(
            [[
                float(day_of_week),
                float(current_balance),
                float(scheduled_trips_count),
                float(turf_sports_flag),
                float(days_since_last_topup),
                float(serpapi_disruption_index),
                float(historical_daily_burn),
            ]]
        )

        model_name = "Prior Labs TabPFN Tabular Foundation Model (In-Context Bayesian Inference)"
        if self.is_tabpfn_active and self.classifier is not None:
            try:
                probs = self.classifier.predict_proba(features)
                p_stranded = float(probs[0][1])
            except Exception as e:
                logger.warning("TabPFN forward pass exception: %s. Using calibrated fallback.", str(e))
                probs = self.fallback_classifier.predict_proba(features)
                p_stranded = float(probs[0][1])
                model_name = "Calibrated Bayesian Ensemble (Fallback)"
        else:
            probs = self.fallback_classifier.predict_proba(features)
            p_stranded = float(probs[0][1])
            model_name = "Calibrated Bayesian Ensemble (Offline/Edge Fallback)"

        # Calculate projected commute cost with SerpApi disruption multiplier
        standard_leg_fare = 17.50  # Margao to Farmagudi student concession
        base_commute_cost = standard_leg_fare * scheduled_trips_count
        if turf_sports_flag:
            base_commute_cost += 30.0  # Wadi football turf detour fare
        
        projected_spend = base_commute_cost * serpapi_disruption_index
        expected_shortfall = max(0.0, round(projected_spend - current_balance, 2))

        # Determine risk classification
        is_high_risk = p_stranded >= Config.RISK_THRESHOLD or expected_shortfall > 0
        if p_stranded >= 0.70 or expected_shortfall > 20.0:
            risk_level = "CRITICAL"
        elif p_stranded >= 0.40 or expected_shortfall > 0:
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"

        # Calculate recommended recharge to survive through next week
        recommended_topup = 0.0
        if is_high_risk:
            recommended_topup = max(50.0, float(np.ceil((expected_shortfall + 35.0) / 10.0) * 10.0))

        # Explain why
        reasons = []
        if turf_sports_flag:
            reasons.append("unplanned football match at Wadi turf (+₹30 fare)")
        if serpapi_disruption_index > 1.05:
            reasons.append(f"SerpApi transit disruption index {serpapi_disruption_index}x")
        if current_balance < 30.0:
            reasons.append(f"low balance ₹{current_balance:.2f} below morning depot threshold")

        explanation = "; ".join(reasons) if reasons else "routine college lectures with adequate balance"

        feature_dict = {
            "day_of_week": int(day_of_week),
            "current_balance": float(current_balance),
            "scheduled_trips_count": int(scheduled_trips_count),
            "turf_sports_flag": int(turf_sports_flag),
            "days_since_last_topup": int(days_since_last_topup),
            "serpapi_disruption_index": float(serpapi_disruption_index),
            "historical_daily_burn": float(historical_daily_burn),
        }

        return StrandedRiskPrediction(
            p_stranded=round(p_stranded, 4),
            is_high_risk=is_high_risk,
            risk_level=risk_level,
            expected_shortfall=expected_shortfall,
            recommended_topup=recommended_topup,
            feature_dict=feature_dict,
            model_name=model_name,
            explanation=explanation,
        )
