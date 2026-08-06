# ActiveVPN/core/help.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from config import COLOR_INFO, COLOR_TITLE

def print_help(console: Console):
    """
    Prints a beautiful help menu explaining usage.
    """
    table = Table(title="Available Commands", title_style=COLOR_TITLE, border_style="dim")

    table.add_column("Flag", style="bold yellow", justify="center")
    table.add_column("Long Flag", style="bold yellow", justify="center")
    table.add_column("Description", style="white")

    table.add_row("-h", "--help", "Show this help message and exit.")
    table.add_row("-k", "--kill", "Attempt to kill/terminate active VPN processes.")
    table.add_row("", "--kill-force", "Kill with SIGKILL if a graceful stop fails.")
    table.add_row("", "--history", "Show past scan results stored in the log file.")
    table.add_row("", "--clear-history", "Delete all saved scan history.")
    table.add_row("", "--export FORMAT", "Export history as json, csv, or txt.")
    table.add_row("", "--watch [SECONDS]", "Continuously rescan every N seconds (default 10).")
    table.add_row("", "--debug", "Print verbose debug logging.")
    table.add_row("", "(default)", "Scan for active VPN and Tor connections.")

    help_text = """
    [bold]Description:[/bold]
    ActiveVPN checks your system for active VPN network interfaces and
    running VPN or Tor processes. It works on Linux, Windows, and macOS.

    [bold]Exit Codes:[/bold]
    0 - No VPN detected or clean exit
    1 - VPN/Tor/Proxy detected
    2 - Offline, error, or invalid usage

    [bold]Note on Android:[/bold]
    Requires a terminal environment like Termux to run Python scripts.
    """

    console.print(Panel(help_text, title="Help & Usage", border_style=COLOR_INFO))
    console.print(table)
    console.print("\n")
