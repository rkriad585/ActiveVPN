# vpnActive/main.py
import argparse
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich import box

# Import core modules
from core.logo import print_banner
from core.help import print_help
from core.detector import NetworkDetector
from core.logger import save_log
# FIXED: Added COLOR_TITLE to imports
from config import COLOR_SUCCESS, COLOR_WARNING, COLOR_DANGER, COLOR_INFO, COLOR_TITLE, LOG_FILE

def main():
    console = Console()

    # --- CLI Arguments ---
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help", action="store_true", help="Show help")
    parser.add_argument("-k", "--kill", action="store_true", help="Kill active VPNs")
    args = parser.parse_args()

    print_banner(console)

    if args.help:
        print_help(console)
        sys.exit(0)

    detector = NetworkDetector(console)

    if args.kill:
        console.rule("[bold red]KILL MODE ACTIVE[/]")
        detector.kill_vpn_services()
        sys.exit(0)

    # --- Scanning Phase ---
    console.rule("[bold cyan]SCANNING NETWORK[/]")
    
    with console.status("[bold green]Analyzing system, Public IP, and DNS routing...[/]", spinner="dots"):
        time.sleep(1) 
        results = detector.scan_network()
        
        # Save to log file
        log_saved = save_log(results)

    # --- Display Results ---
    
    # 1. System Internals
    sys_table = Table(title="System Internal Check", box=box.SIMPLE)
    sys_table.add_column("Type", style="cyan")
    sys_table.add_column("Status", style="bold")
    sys_table.add_column("Details")

    # Interfaces
    if results['interfaces']:
        sys_table.add_row("Interface", f"[{COLOR_SUCCESS}]FOUND[/]", ", ".join(results['interfaces']))
    else:
        sys_table.add_row("Interface", "[dim]None[/]", "-")

    # Processes
    if results['vpn_processes']:
        names = ", ".join([p['name'] for p in results['vpn_processes']])
        sys_table.add_row("VPN Process", f"[{COLOR_SUCCESS}]ACTIVE[/]", names)
    else:
        sys_table.add_row("VPN Process", "[dim]None[/]", "-")

    # Tor Processes
    if results['tor_processes']:
         sys_table.add_row("Tor Process", f"[{COLOR_TITLE}]ACTIVE[/]", "Tor Service found")
    else:
         sys_table.add_row("Tor Process", "[dim]None[/]", "-")

    console.print(sys_table)
    console.print("\n")

    # 2. External IP Analysis
    ip_data = results.get('public_ip')
    
    if ip_data:
        ip_panel_color = "green"
        # Simple heuristic: If ISP name contains common cloud/VPN words
        suspicious_isps = ["digitalocean", "m247", "datacamp", "host", "cdn", "cloud", "akamai", "linode"]
        isp_name = ip_data.get('isp', '').lower()
        is_suspicious = any(s in isp_name for s in suspicious_isps)
        
        if is_suspicious:
            ip_status = "[bold green]LIKELY VPN/PROXY[/]"
        else:
            ip_status = "[bold yellow]Likely Residential ISP[/]"
            ip_panel_color = "yellow"

        ip_text = f"""
        [bold]Public IP:[/bold] {ip_data.get('query')}
        [bold]Country:[/bold]   {ip_data.get('country')} ({ip_data.get('countryCode')})
        [bold]ISP/Org:[/bold]   {ip_data.get('isp')} / {ip_data.get('org')}
        [bold]Verdict:[/bold]   {ip_status}
        """
        console.print(Panel(ip_text, title="External IP Analysis", border_style=ip_panel_color))
    else:
        console.print(f"[{COLOR_DANGER}]Could not fetch Public IP (Offline or blocked).[/]")

    # 3. DNS Analysis
    dns_data = results.get('dns_leak')
    if dns_data and ip_data:
        dns_ip = dns_data.get('ip', 'Unknown')
        
        console.print(f"\n[bold underline]DNS Consistency Check:[/]")
        console.print(f"  • Your Traffic IP: [cyan]{ip_data.get('query')}[/]")
        console.print(f"  • Your DNS Resolver IP: [cyan]{dns_ip}[/]")
        
        if ip_data.get('query') == dns_ip:
             console.print(f"  [{COLOR_WARNING}]⚠️  DNS matches Public IP. Usually implies local resolution or VPN tunnel is wrapping everything perfectly.[/]")
        else:
             console.print(f"  [{COLOR_INFO}]ℹ️  DNS is handled by a different server (Standard behavior for most VPNs).[/]")

    # 4. Logging Status
    if log_saved:
        console.print(f"\n[dim italic]Scan results saved to {LOG_FILE}[/]")

    console.print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
