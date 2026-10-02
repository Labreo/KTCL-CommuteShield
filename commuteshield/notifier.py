"""Multi-Channel Alert Dispatcher for KTCL CommuteShield.

Replaces brittle legacy PyAutoGUI keyboard/mouse hijacking with clean, headless
delivery across:
1. Rich Terminal Console (Interactive colored HUD & status card)
2. Telegram Bot Webhook (Direct mobile push to friend)
3. Twilio / WhatsApp Cloud API
4. Persistent Local Audit Log
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from commuteshield.config import Config

logger = logging.getLogger(__name__)
console = Console()


class CommuteShieldNotifier:
    """Headless alert and notification dispatcher."""

    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path or (Config.PROJECT_ROOT / "commute_alerts.log")
        self.telegram_token = Config.TELEGRAM_BOT_TOKEN
        self.telegram_chat_id = Config.TELEGRAM_CHAT_ID

    def format_alert_message(
        self,
        commuter_name: str,
        balance: float,
        p_stranded: float,
        shortfall: float,
        recommended_topup: float,
        explanation: str,
        disruption_status: str,
        is_live_sync: bool,
    ) -> str:
        """Construct the high-impact student alert text."""
        sync_badge = "🟢 LIVE KTCL PORTAL" if is_live_sync else "🟡 OFFLINE DEPOT LEDGER"
        
        return (
            f"🚨 *KTCL CommuteShield Emergency Alert for {commuter_name}*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💳 *Card Balance*: ₹{balance:.2f} ({sync_badge})\n"
            f"⚠️ *Stranded Risk Tomorrow*: {p_stranded * 100:.1f}%\n"
            f"📉 *Projected Shortfall*: ₹{shortfall:.2f}\n"
            f"🚦 *Goa Transit Context*: {disruption_status}\n\n"
            f"ℹ️ *Risk Factors*: {explanation}\n\n"
            f"⏰ *Batch Cutoff Reminder*: KTCL bus depot servers close batch "
            f"processing at **11:59 PM IST tonight**.\n"
            f"👉 *Action Required*: Top up at least *₹{recommended_topup:.0f}* "
            f"online at cashless.ktcl.goa.gov.in before midnight to prevent turnstile decline at 7:30 AM!\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    def dispatch_console(
        self,
        commuter_name: str,
        balance: float,
        p_stranded: float,
        shortfall: float,
        recommended_topup: float,
        explanation: str,
        disruption_status: str,
        model_name: str,
        is_live_sync: bool,
    ):
        """Render a rich visual alert in the terminal."""
        risk_color = "red" if p_stranded >= 0.60 else "yellow" if p_stranded >= 0.35 else "green"
        risk_badge = f"[{risk_color} bold]CRITICAL RISK: {p_stranded * 100:.1f}%[/{risk_color} bold]"

        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Key", style="cyan bold")
        table.add_column("Value", style="white")

        table.add_row("Commuter Friend", commuter_name)
        table.add_row("Card Balance", f"₹{balance:.2f} ({'Live Portal' if is_live_sync else 'Offline Cached'})")
        table.add_row("Stranded Probability", risk_badge)
        table.add_row("Projected Shortfall", f"₹{shortfall:.2f}")
        table.add_row("Recommended Top-Up", f"[bold green]₹{recommended_topup:.0f}[/bold green]")
        table.add_row("Goa Transit Intel", disruption_status)
        table.add_row("Inference Model", model_name)
        table.add_row("Risk Factors", explanation)
        table.add_row("Depot Sync Cutoff", "[bold red]11:59 PM IST Tonight[/bold red]")

        panel = Panel(
            table,
            title="[bold red]🚨 KTCL CommuteShield - Proactive Transit Protection[/bold red]",
            subtitle="[dim]Powered by Prior Labs TabPFN & SerpApi Transit Grounding[/dim]",
            border_style=risk_color,
            expand=False,
        )
        console.print(panel)

    def send_telegram(self, message: str) -> bool:
        """Send message via Telegram Bot API if configured."""
        if not self.telegram_token or not self.telegram_chat_id:
            logger.info("Telegram notification skipped (tokens not configured in .env).")
            return False

        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }
            resp = requests.post(url, json=payload, timeout=8.0)
            return resp.status_code == 200
        except Exception as e:
            logger.warning("Failed to dispatch Telegram message: %s", str(e))
            return False

    def log_telemetry(self, alert_data: dict):
        """Append alert telemetry to local log for privacy-preserving auditing."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            **alert_data,
        }
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.warning("Failed to write to telemetry log: %s", str(e))
