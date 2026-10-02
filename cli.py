"""Command Line Interface for KTCL CommuteShield.

Provides commands to run live assessments, simulate student transit scenarios,
query SerpApi Goa route disruptions, and inspect the TabPFN foundation model.
"""

import argparse
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from commuteshield.agent import CommuteShieldAgent
from commuteshield.config import Config
from commuteshield.scraper import KTCLCardScraper
from commuteshield.serpapi_tool import GoaTransitIntelligence
from commuteshield.tabpfn_model import TabPFNCommuteEngine

console = Console()


def print_banner():
    """Print stylish ASCII header."""
    banner = (
        "[bold cyan]"
        "╔══════════════════════════════════════════════════════════════════════╗\n"
        "║             🛡️  KTCL CommuteShield (Goa Bus Safety Agent)           ║\n"
        "║      Prior Labs TabPFN Foundation Model  ×  SerpApi Transit Intel   ║\n"
        "╚══════════════════════════════════════════════════════════════════════╝"
        "[/bold cyan]"
    )
    console.print(banner)


def cmd_run(args):
    """Run live risk assessment."""
    print_banner()
    agent = CommuteShieldAgent()
    console.print(f"[dim]Initiating CommuteShield run for {Config.COMMUTER_NAME}...[/dim]\n")
    agent.assess_commute_risk(
        simulated_balance=args.balance,
        turf_sports_flag=args.turf,
        scheduled_trips=args.trips,
    )


def cmd_simulate(args):
    """Simulate key real-world scenarios contrasting CommuteShield vs naive thresholds."""
    print_banner()
    agent = CommuteShieldAgent()

    scenarios = [
        {
            "name": "Scenario 1: Tejas Friday Football Trap (The Real Friend Problem)",
            "balance": 18.00,
            "turf": 1,
            "trips": 3,
            "desc": "Friday evening with ₹18 left. Unplanned Wadi football turf trip tomorrow. Naive check fails; TabPFN flags critical risk before midnight depot sync!",
        },
        {
            "name": "Scenario 2: Tuesday Safe Lecture Day (Anti-Notification Fatigue)",
            "balance": 25.00,
            "turf": 0,
            "trips": 1,
            "desc": "Tuesday with only 1 morning lecture (₹17.50 needed). A naive 'balance < 50' rule would annoy the commuter; CommuteShield accurately classifies as SAFE.",
        },
        {
            "name": "Scenario 3: Severe Monsoon Detour & Highway Diversion",
            "balance": 45.00,
            "turf": 1,
            "trips": 3,
            "desc": "₹45 balance looks 'safe' to simple rules, but SerpApi detects NH66 flood diversion surcharge. TabPFN catches the hidden shortfall.",
        },
    ]

    for idx, sc in enumerate(scenarios, 1):
        console.rule(f"[bold yellow]{sc['name']}[/bold yellow]")
        console.print(f"[dim italic]{sc['desc']}[/dim italic]\n")
        agent.assess_commute_risk(
            simulated_balance=sc["balance"],
            turf_sports_flag=sc["turf"],
            scheduled_trips=sc["trips"],
        )
        console.print("\n")


def cmd_transit(args):
    """Query SerpApi for live Goa bus transit updates."""
    print_banner()
    intel = GoaTransitIntelligence()
    origin = args.origin or Config.HOME_HUB
    destination = args.destination or Config.CAMPUS_HUB

    console.print(f"[cyan]Querying SerpApi for route: {origin} -> {destination}...[/cyan]\n")
    report = intel.query_live_transit_status(origin=origin, destination=destination)

    table = Table(title="Live Goa Transit Grounding (SerpApi)", border_style="cyan")
    table.add_column("Metric", style="bold")
    table.add_column("Value")

    table.add_row("Status Level", f"[bold]{report.status_level}[/bold]")
    table.add_row("Disruption Multiplier", f"{report.disruption_multiplier}x")
    table.add_row("Intelligence Source", report.source)
    table.add_row("Live SERP Grounded", "Yes (Real Google Search)" if report.is_live_serp else "Regional Bulletin Fallback")

    console.print(table)
    console.print("\n[bold]Active Transit Advisories:[/bold]")
    for adv in report.active_advisories:
        console.print(f"  • {adv}")


def cmd_diagnostics(args):
    """Display system diagnostics and privacy-safe configuration."""
    print_banner()
    summary = Config.get_masked_summary()

    table = Table(title="CommuteShield System Telemetry & Privacy Audit", border_style="green")
    table.add_column("Configuration Key", style="cyan bold")
    table.add_column("Current Setting", style="white")

    for k, v in summary.items():
        table.add_row(k.replace("_", " ").title(), str(v))

    console.print(table)


def cmd_telegram_test(args):
    """Test Telegram bot connection and assist in linking chat ID."""
    print_banner()
    import requests

    token = Config.TELEGRAM_BOT_TOKEN
    chat_id = Config.TELEGRAM_CHAT_ID

    if not token:
        console.print("[red]❌ TELEGRAM_BOT_TOKEN is not configured in .env[/red]")
        return

    console.print(f"[cyan]Testing Telegram bot connection with token: {token[:10]}...[/cyan]\n")
    try:
        me_resp = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=8.0)
        data = me_resp.json()
        if not data.get("ok"):
            console.print(f"[bold red]❌ Telegram API Error ({data.get('error_code')}):[/bold red] {data.get('description')}")
            console.print("[yellow]Tip: Please check the token copied from @BotFather in Telegram.[/yellow]")
            console.print("[yellow]Make sure there are no accidental spaces, missing characters, or OCR typos in your .env file.[/yellow]")
            return

        bot_info = data.get("result", {})
        console.print(f"[bold green]✓ Successfully connected to bot:[/bold green] @{bot_info.get('username')} ({bot_info.get('first_name')})")

        # Check chat ID
        if chat_id:
            console.print(f"[cyan]Attempting to send test alert to Chat ID: {chat_id}...[/cyan]")
            send_resp = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "🛡️ *KTCL CommuteShield Test Alert*\n\nYour Telegram bot is successfully connected and ready to send bus card exhaustion warnings before 11:59 PM!",
                    "parse_mode": "Markdown",
                },
                timeout=8.0,
            )
            if send_resp.status_code == 200:
                console.print("[bold green]✓ Test alert delivered successfully to your Telegram chat![/bold green]")
            else:
                console.print(f"[yellow]⚠️ Could not deliver message to chat ID {chat_id}: {send_resp.text}[/yellow]")
        else:
            console.print("\n[bold yellow]👉 Next Step: Link your Telegram Chat ID[/bold yellow]")
            console.print(f"1. Open Telegram and search for: [bold cyan]@{bot_info.get('username')}[/bold cyan]")
            console.print(f"2. Tap [bold green]Start[/bold green] (or send any message like 'hello')")
            console.print("3. Checking for incoming messages right now...")

            upd_resp = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", timeout=8.0)
            upd_data = upd_resp.json()
            messages = upd_data.get("result", [])
            if messages:
                detected_chat = messages[-1].get("message", {}).get("chat", {})
                detected_id = detected_chat.get("id")
                detected_user = detected_chat.get("first_name", "")
                console.print(f"[bold green]✓ Found incoming message from {detected_user}! Chat ID: {detected_id}[/bold green]")
                console.print(f"[cyan]Add this to your .env: TELEGRAM_CHAT_ID={detected_id}[/cyan]")
            else:
                console.print("[dim]No messages detected yet. Once you send /start to the bot, re-run: .venv/bin/python cli.py telegram-test[/dim]")

    except Exception as e:
        console.print(f"[red]Exception while contacting Telegram API: {e}[/red]")


def main():
    parser = argparse.ArgumentParser(
        description="KTCL CommuteShield - AI Bus Card Exhaustion Forecaster"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # run command
    run_parser = subparsers.add_parser("run", help="Run live risk evaluation")
    run_parser.add_argument("--balance", type=float, help="Override card balance for testing")
    run_parser.add_argument("--turf", type=int, choices=[0, 1], help="Flag for turf sports (0 or 1)")
    run_parser.add_argument("--trips", type=int, help="Number of scheduled trips tomorrow")

    # simulate command
    subparsers.add_parser("simulate", help="Simulate 3 real-world commuter scenarios")

    # transit command
    transit_parser = subparsers.add_parser("transit", help="Check live SerpApi transit intelligence")
    transit_parser.add_argument("--origin", type=str, default="Margao")
    transit_parser.add_argument("--destination", type=str, default="Farmagudi")

    # diagnostics command
    subparsers.add_parser("diagnostics", help="Inspect privacy & environment settings")

    # telegram-test command
    subparsers.add_parser("telegram-test", help="Test Telegram bot token and setup chat ID")

    args = parser.parse_args()

    if args.command == "run" or args.command is None:
        cmd_run(args)
    elif args.command == "simulate":
        cmd_simulate(args)
    elif args.command == "transit":
        cmd_transit(args)
    elif args.command == "diagnostics":
        cmd_diagnostics(args)
    elif args.command == "telegram-test":
        cmd_telegram_test(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
