# ActiveVPN/main.py
import argparse
import sys
import time

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from activevpn.detector import NetworkDetector
from activevpn.help import print_help
from activevpn.logger import (
    clear_history,
    export_history,
    flatten_entry,
    load_history,
    save_log,
)
from activevpn.logo import print_banner
from activevpn.config import (
    COLOR_SUCCESS,
    COLOR_WARNING,
    COLOR_DANGER,
    COLOR_INFO,
    COLOR_TITLE,
    LOG_FILE,
    VERSION,
)

VERDICT_COLORS = {
    "CLEAN": "bold green",
    "SUSPICIOUS": "bold yellow",
    "LIKELY VPN/PROXY": "bold orange1",
    "VPN DETECTED": "bold red",
}


def build_parser():
    parser = argparse.ArgumentParser(add_help=False, prog="activevpn")
    parser.add_argument("-h", "--help", action="store_true", help="Show help")
    parser.add_argument("-k", "--kill", action="store_true", help="Kill active VPNs")
    parser.add_argument(
        "--kill-force",
        action="store_true",
        help="Kill active VPNs, using SIGKILL if a graceful stop fails",
    )
    parser.add_argument("--history", action="store_true", help="Show past scan results")
    parser.add_argument("--clear-history", action="store_true", help="Delete saved scan history")
    parser.add_argument(
        "--export",
        nargs="?",
        const="json",
        metavar="FORMAT",
        help="Export scan history as json/csv/txt",
    )
    parser.add_argument(
        "--watch",
        type=int,
        nargs="?",
        const=10,
        metavar="SECONDS",
        help="Continuously rescan every N seconds (default 10)",
    )
    parser.add_argument("--debug", action="store_true", help="Verbose debug logging")
    return parser


def display_system_table(console, results):
    sys_table = Table(title="System Internal Check", box=box.SIMPLE)
    sys_table.add_column("Type", style="cyan")
    sys_table.add_column("Status", style="bold")
    sys_table.add_column("Details")

    if results.interfaces:
        sys_table.add_row(
            "Interface", f"[{COLOR_SUCCESS}]FOUND[/]", ", ".join(results.interfaces)
        )
    else:
        sys_table.add_row("Interface", "[dim]None[/]", "-")

    if results.vpn_processes:
        names = ", ".join([p.name for p in results.vpn_processes])
        sys_table.add_row("VPN Process", f"[{COLOR_SUCCESS}]ACTIVE[/]", names)
    else:
        sys_table.add_row("VPN Process", "[dim]None[/]", "-")

    if results.tor_processes:
        sys_table.add_row("Tor Process", f"[{COLOR_TITLE}]ACTIVE[/]", "Tor Service found")
    else:
        sys_table.add_row("Tor Process", "[dim]None[/]", "-")

    console.print(sys_table)
    console.print("\n")


def display_ip_panel(console, results):
    ip_data = results.public_ip

    if not ip_data:
        console.print(f"[{COLOR_DANGER}]Could not fetch Public IP (Offline or blocked).[/]")
        return

    label = results.verdict.label
    ip_panel_color = "green" if label == "CLEAN" else "yellow"

    isp_name = ip_data.provider.lower()
    suspicious_isps = ["digitalocean", "m247", "datacamp", "host", "cdn", "cloud", "akamai", "linode"]
    is_suspicious = any(s in isp_name for s in suspicious_isps)

    lines = [
        f"[bold]Public IP:[/bold] {ip_data.address}",
        f"[bold]Country:[/bold]   {ip_data.country or '-'} ({ip_data.country_code or '-'})",
        f"[bold]ISP/Org:[/bold]   {ip_data.isp or '-'} / {ip_data.org or '-'}",
    ]

    if results.ipv4:
        lines.append(f"[bold]IPv4:[/bold]      {results.ipv4}")
    if results.ipv6:
        lines.append(f"[bold]IPv6:[/bold]      {results.ipv6}")
        if results.ipv4:
            console.print(
                f"[{COLOR_WARNING}]  IPv6 is active. If your VPN only tunnels IPv4, "
                f"traffic may leak over IPv6.[/]"
            )

    if is_suspicious and ip_data.hosting is None:
        lines.append("[bold]Verdict:[/bold]   [bold yellow]Likely Datacenter IP[/]")
    elif ip_data.proxy:
        lines.append("[bold]Verdict:[/bold]   [bold red]PROXY/VPN flagged by provider[/]")
    elif ip_data.hosting:
        lines.append("[bold]Verdict:[/bold]   [bold yellow]Hosting/Datacenter IP[/]")
    else:
        lines.append("[bold]Verdict:[/bold]   [bold yellow]Likely Residential ISP[/]")

    lines.append(f"[bold]Source:[/bold]    {ip_data.source or 'unknown'}")
    console.print(Panel("\n".join(lines), title="External IP Analysis", border_style=ip_panel_color))


def display_dns(console, results):
    dns_data = results.dns_leak
    ip_data = results.public_ip
    if not dns_data or not ip_data:
        return

    dns_ip = dns_data.ip or "Unknown"
    traffic_ip = ip_data.address

    console.print(f"\n[bold underline]DNS Consistency Check:[/]")
    console.print(f"  • Your Traffic IP: [cyan]{traffic_ip}[/]")
    console.print(f"  • Your DNS Resolver IP: [cyan]{dns_ip}[/]")

    if traffic_ip == dns_ip:
        console.print(
            f"  [{COLOR_WARNING}]DNS matches Public IP. Usually implies local resolution "
            f"or VPN tunnel is wrapping everything perfectly.[/]"
        )
    else:
        console.print(
            f"  [{COLOR_INFO}]DNS is handled by a different server (Standard behavior for most VPNs).[/]"
        )


def display_verdict(console, results):
    verdict = results.verdict
    label = verdict.label
    score = verdict.score
    reasons = verdict.reasons

    color = VERDICT_COLORS.get(label, "bold white")
    filled = "#" * (score // 10)
    empty = "-" * (10 - len(filled))
    bar = f"[{color}]{filled}[/][dim]{empty}[/]"

    text = f"[bold]Verdict:[/bold] [{color}]{label}[/]\n[bold]Confidence:[/bold] {bar} {score}/100\n"
    if reasons:
        text += "[bold]Signals:[/bold]\n  • " + "\n  • ".join(reasons)

    console.print(Panel(text, title="Overall Verdict", border_style=color))
    console.print("\n")


def scan_once(console, detector):
    console.rule("[bold cyan]SCANNING NETWORK[/]")

    with console.status("[bold green]Analyzing system, Public IP, and DNS routing...[/]", spinner="dots"):
        time.sleep(1)
        results = detector.scan_network()
        log_saved = save_log(results)

    display_system_table(console, results)
    display_ip_panel(console, results)
    display_dns(console, results)
    display_verdict(console, results)

    if log_saved:
        console.print(f"[dim italic]Scan results saved to {LOG_FILE}[/]")
    console.print("\n")

    label = results.verdict.label
    if label != "CLEAN":
        return 1
    if results.public_ip is None and not (
        results.interfaces or results.vpn_processes or results.tor_processes
    ):
        return 2
    return 0


def show_history(console):
    history = load_history()
    if not history:
        console.print(f"[{COLOR_WARNING}]No scan history found yet. Run a scan first.[/]")
        return 0

    table = Table(title=f"Scan History ({len(history)} entries)", box=box.ROUNDED)
    table.add_column("#", justify="right", style="dim")
    table.add_column("Timestamp", style="cyan")
    table.add_column("Verdict", style="bold")
    table.add_column("Score")
    table.add_column("Public IP")
    table.add_column("ISP")

    for idx, entry in enumerate(reversed(history[-20:]), start=1):
        flat = flatten_entry(entry)
        table.add_row(
            str(idx),
            flat['timestamp'],
            f"[{VERDICT_COLORS.get(flat['verdict'], 'white')}]{flat['verdict']}[/]",
            str(flat['score']),
            flat['public_ip'] or "-",
            (flat['isp'] or "-")[:40],
        )

    console.print(table)
    console.print("\n")
    return 0


def do_export(console, fmt):
    if fmt not in ("json", "csv", "txt"):
        console.print(
            f"[{COLOR_DANGER}]Unsupported export format '{fmt}'. Use json, csv, or txt.[/]"
        )
        return 2
    try:
        path = export_history(fmt)
    except Exception as e:
        console.print(f"[{COLOR_DANGER}]Export failed: {e}[/]")
        return 2
    console.print(f"[{COLOR_SUCCESS}]Exported scan history to {path}[/]")
    return 0


def watch_mode(console, detector, interval):
    console.rule("[bold cyan]WATCH MODE (Ctrl+C to stop)[/]")
    try:
        while True:
            scan_once(console, detector)
            console.print(f"[dim]Watching... next scan in {interval}s. Press Ctrl+C to stop.[/]")
            time.sleep(interval)
    except KeyboardInterrupt:
        console.print("\n[bold]Watch stopped.[/]")
        return 0


def run(argv=None):
    console = Console()
    parser = build_parser()
    args = parser.parse_args(argv)

    print_banner(console)

    if args.help:
        print_help(console)
        return 0

    if args.clear_history:
        if clear_history():
            console.print(f"[{COLOR_SUCCESS}]Scan history cleared.[/]")
        else:
            console.print(f"[{COLOR_DANGER}]Could not clear history.[/]")
        return 0

    if args.export:
        return do_export(console, args.export)

    if args.history:
        return show_history(console)

    detector = NetworkDetector(console, debug=args.debug)

    if args.kill:
        console.rule("[bold red]KILL MODE ACTIVE[/]")
        detector.kill_vpn_services(force=args.kill_force)
        return 0

    if args.watch:
        return watch_mode(console, detector, args.watch)

    return scan_once(console, detector)


def main():
    sys.exit(run())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
