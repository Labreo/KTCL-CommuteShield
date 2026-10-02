"""Configuration management for KTCL CommuteShield."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Automatically load .env from the project root if it exists
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def mask_card_number(card_num: Optional[str]) -> str:
    """Mask card number for privacy safe logging (e.g., ST25******1313)."""
    if not card_num:
        return "UNKNOWN_CARD"
    clean = card_num.strip()
    if len(clean) <= 6:
        return "****"
    return f"{clean[:4]}{'*' * (len(clean) - 8)}{clean[-4:]}"


class Config:
    """Application configuration and credentials loaded from environment."""

    PROJECT_ROOT: Path = PROJECT_ROOT

    # Commuter Profile
    COMMUTER_NAME: str = os.getenv("COMMUTER_NAME", "Tejas")
    HOME_HUB: str = os.getenv("COMMUTER_HOME_HUB", "Margao")
    CAMPUS_HUB: str = os.getenv("COMMUTER_CAMPUS_HUB", "Farmagudi")
    ALERT_TIME_IST: str = os.getenv("COMMUTER_ALERT_TIME_IST", "20:00")

    # KTCL Smart Card (Confidential, loaded from .env)
    KTCL_CARD_NUMBER: str = os.getenv("KTCL_CARD_NUMBER", "ST2500000000")
    KTCL_CARDHOLDER_NAME: str = os.getenv("KTCL_CARDHOLDER_NAME", "Student Commuter")
    KTCL_CARD_TYPE: str = os.getenv("KTCL_CARD_TYPE", "STUDENT")

    # SerpApi Grounding
    SERPAPI_API_KEY: Optional[str] = os.getenv("SERPAPI_API_KEY") or None

    # Prior Labs TabPFN API Key / Token
    TABPFN_TOKEN: Optional[str] = os.getenv("TABPFN_TOKEN") or None

    # Notification Channels
    TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN") or None
    TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID") or None

    TWILIO_ACCOUNT_SID: Optional[str] = os.getenv("TWILIO_ACCOUNT_SID") or None
    TWILIO_AUTH_TOKEN: Optional[str] = os.getenv("TWILIO_AUTH_TOKEN") or None
    TWILIO_WHATSAPP_FROM: Optional[str] = os.getenv("TWILIO_WHATSAPP_FROM") or None
    TWILIO_WHATSAPP_TO: Optional[str] = os.getenv("TWILIO_WHATSAPP_TO") or None

    # TabPFN & Risk Settings
    RISK_THRESHOLD: float = float(os.getenv("COMMUTESHIELD_RISK_THRESHOLD", "0.60"))
    DEFAULT_TOPUP_RECOMMENDATION: float = float(os.getenv("DEFAULT_TOPUP_RECOMMENDATION", "50.0"))

    # File paths
    DATA_DIR: Path = Path(__file__).resolve().parent / "data"
    COMMUTE_HISTORY_PATH: Path = DATA_DIR / "friend_commute_history.csv"

    @classmethod
    def get_masked_summary(cls) -> dict:
        """Returns safe summary dictionary for diagnostics without leaking credentials."""
        return {
            "commuter_name": cls.COMMUTER_NAME,
            "card_masked": mask_card_number(cls.KTCL_CARD_NUMBER),
            "card_holder": cls.KTCL_CARDHOLDER_NAME,
            "card_type": cls.KTCL_CARD_TYPE,
            "route": f"{cls.HOME_HUB} <-> {cls.CAMPUS_HUB}",
            "has_serpapi_key": bool(cls.SERPAPI_API_KEY),
            "has_telegram": bool(cls.TELEGRAM_BOT_TOKEN and cls.TELEGRAM_CHAT_ID),
            "has_twilio": bool(cls.TWILIO_ACCOUNT_SID and cls.TWILIO_AUTH_TOKEN),
            "risk_threshold": cls.RISK_THRESHOLD,
        }
