#!/usr/bin/env python3
"""
Blindseeker v1.0.0 — CLI Interface
====================================
Command-line interface with Rich terminal output for
username enumeration across 200+ platforms.

Usage:
    python cli.py search <username> [OPTIONS]
    python cli.py platforms
    python cli.py export <scan_id> --format pdf
"""

import sys
import os
import time
import json

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    from rich.live import Live
    from rich.text import Text
    from rich import box
except ImportError:
    print("[!] Missing dependencies. Run: pip install click rich")
    sys.exit(1)

from config import Config
from core.engine import BlindSeekerEngine
from core.exporter import Exporter
from core.platforms import get_platform_count, get_categories

console = Console()

BANNER = r"""
[bold green]
    ____  ___           __               __
   / __ )/ (_)___  ____/ /_______  ___  / /_____  _____
  / __  / / / __ \/ __  / ___/ _ \/ _ \/ //_/ _ \/ ___/
 / /_/ / / / / / / /_/ (__  )  __/  __/ ,< /  __/ /
/_____/_/_/_/ /_/\__,_/____/\___/\___/_/|_|\___/_/
[/bold green]
[dim]                  Username Enumeration Engine
                       v1.0.0 • Shadow Protocol[/dim]
"""


def print_banner():
    console.print(BANNER)
    console.print(f"  [cyan]►[/cyan] Platforms: [bold]{get_platform_count()}[/bold]")
    console.print(f"  [cyan]►[/cyan] Categories: [bold]{len(get_categories())}[/bold]")
    console.print()


@click.group()
@click.version_option(version='1.0.0', prog_name='Blindseeker')
def cli():
    """
    Blindseeker v1.0.0 — Username Enumeration Forensics Tool
    
    Advanced OSINT tool for security agencies to enumerate usernames
    across 200+ platforms with proxy/Tor support.
    """
    pass


@cli.command()
@click.argument('username')
@click.option('--timeout', '-t', default=15, help='Request timeout in seconds (default: 15)')
@click.option('--workers', '-w', default=50, help='Max concurrent workers (default: 50)')
@click.option('--category', '-c', multiple=True, help='Filter by category (can be used multiple times)')
@click.option('--proxy', '-p', default=None, help='Proxy URL (http://host:port or socks5://host:port)')
@click.option('--proxy-file', default=None, help='Path to proxy list file')
@click.option('--tor', is_flag=True, help='Route through Tor network')
@click.option('--output', '-o', default=None, help='Output file path')
@click.option('--format', '-f', 'fmt', default='json',
              type=click.Choice(['json', 'csv', 'pdf', 'xml', 'html', 'xlsx']),
              help='Export format (default: json)')
@click.option('--verbose', '-v', is_flag=True, help='Show all results including not found')
@click.option('--investigator', default='', help='Investigator name for reports')
@click.option('--case-id', default='', help='Case ID for forensic tracking')
@click.option('--notes', default='', help='Additional notes for reports')
def search(username, timeout, workers, category, proxy, proxy_file, tor,
           output, fmt, verbose, investigator, case_id, notes):
    """Search for a username across all platforms."""
    
    print_banner()
    
    config = Config()
    config.REQUEST_TIMEOUT = timeout
    config.MAX_WORKERS = workers
    
    engine = BlindSeekerEngine(config)
    
    # Configure proxy
    if proxy:
        engine.configure_proxy(proxy_list=[proxy])
        console.print(f"  [yellow]►[/yellow] Proxy: [bold]{proxy}[/bold]")
    elif proxy_file:
        engine.configure_proxy(proxy_file=proxy_file)
        console.print(f"  [yellow]►[/yellow] Proxy file: [bold]{proxy_file}[/bold]")
    
    # Configure Tor
    if tor:
        console.print("  [magenta]►[/magenta] Connecting to Tor network...")
        connected = engine.configure_tor(enable=True)
        if connected:
            console.print("  [green]✓[/green] Tor connected")
        else:
            console.print("  [yellow]⚠[/yellow] Tor enabled but connection not verified")
    
    categories = list(category) if category else None
    
    console.print()
    console.print(Panel(
        f"[bold green]Target:[/bold green] {username}\n"
        f"[dim]Timeout: {timeout}s • Workers: {workers} • "
        f"Categories: {', '.join(categories) if categories else 'All'}[/dim]",
        title="[bold]SCAN CONFIGURATION[/bold]",
        border_style="green",
        padding=(1, 2)
    ))
    console.print()
    
    # Track results for live display
    found_results = []
    error_count = [0]
    scanned_count = [0]
    total = get_platform_count() if not categories else sum(
        get_categories().get(c, 0) for c in categories
    )
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, style="green", complete_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("•"),
        TextColumn("[green]{task.fields[found]}[/green] found"),
        TextColumn("•"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        
        task_id = progress.add_task(
            f"Scanning {total} platforms...",
            total=total,
            found=0
        )
        
        def on_progress(result):
            scanned_count[0] += 1
            if result.found:
                found_results.append(result)
            elif result.error:
                error_count[0] += 1
            
            progress.update(
                task_id,
                advance=1,
                found=len(found_results),
                description=f"Checking {result.platform.get('name', '?')}..."
            )
        
        scan_session = engine.scan(
            username,
            categories=categories,
            timeout=timeout,
            max_workers=workers,
            progress_callback=on_progress
        )
    
    console.print()
    
    # Results
    scan_data = scan_session.to_dict()
    
    if found_results:
        table = Table(
            title=f"[bold green]PROFILES FOUND ({len(found_results)})[/bold green]",
            box=box.ROUNDED,
            border_style="green",
            show_lines=False,
            padding=(0, 1)
        )
        
        table.add_column("#", style="dim", width=4)
        table.add_column("Platform", style="bold white", min_width=18)
        table.add_column("Category", style="magenta", width=12)
        table.add_column("URL", style="green", min_width=30)
        table.add_column("Time", style="dim", width=8, justify="right")
        
        for i, r in enumerate(found_results, 1):
            rd = r.to_dict()
            table.add_row(
                str(i),
                rd['platform'],
                rd['category'].title(),
                rd['url'] or '—',
                f"{rd['response_time']}ms" if rd['response_time'] else '—'
            )
        
        console.print(table)
    else:
        console.print(Panel(
            "[yellow]No profiles found for this username.[/yellow]",
            border_style="yellow"
        ))
    
    console.print()
    
    # Summary
    summary = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    summary.add_column(style="dim")
    summary.add_column(style="bold")
    summary.add_row("Username", username)
    summary.add_row("Platforms Scanned", str(scan_data['total_platforms']))
    summary.add_row("Profiles Found", f"[green]{scan_data['found_count']}[/green]")
    summary.add_row("Errors", f"[yellow]{scan_data['error_count']}[/yellow]")
    summary.add_row("Duration", f"{scan_data['duration_seconds']}s")
    
    console.print(Panel(summary, title="[bold]SCAN SUMMARY[/bold]", border_style="cyan"))
    
    # Export
    if output or fmt != 'json':
        exporter = Exporter(os.path.dirname(output) if output else 'exports')
        filepath = exporter.export(
            scan_data, fmt,
            filename=os.path.splitext(os.path.basename(output))[0] if output else None,
            investigator=investigator,
            case_id=case_id,
            notes=notes
        )
        console.print(f"\n  [green]✓[/green] Report exported: [bold]{filepath}[/bold]")
    else:
        # Default: save JSON
        exporter = Exporter('exports')
        filepath = exporter.export(scan_data, 'json')
        console.print(f"\n  [green]✓[/green] Results saved: [bold]{filepath}[/bold]")
    
    console.print()


@cli.command()
def platforms():
    """List all supported platforms."""
    print_banner()
    
    categories = get_categories()
    
    table = Table(
        title="[bold]SUPPORTED PLATFORM CATEGORIES[/bold]",
        box=box.ROUNDED,
        border_style="cyan"
    )
    
    table.add_column("Category", style="bold white")
    table.add_column("Count", style="green", justify="right")
    table.add_column("Coverage", min_width=25)
    
    total = get_platform_count()
    
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        bar_len = int((count / total) * 30)
        bar = "█" * bar_len + "░" * (30 - bar_len)
        table.add_row(
            cat.title(),
            str(count),
            f"[green]{bar}[/green] {count/total*100:.0f}%"
        )
    
    table.add_row("", "", "", end_section=True)
    table.add_row("[bold]TOTAL[/bold]", f"[bold]{total}[/bold]", "")
    
    console.print(table)
    console.print()


@cli.command()
@click.option('--host', '-h', default='127.0.0.1', help='Host (default: 127.0.0.1)')
@click.option('--port', '-p', default=5000, help='Port (default: 5000)')
@click.option('--debug', is_flag=True, help='Debug mode')
def web(host, port, debug):
    """Start the web interface."""
    print_banner()
    console.print(f"  [green]►[/green] Starting web server on [bold]http://{host}:{port}[/bold]")
    console.print()
    
    from app import app, socketio
    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)


if __name__ == '__main__':
    cli()
