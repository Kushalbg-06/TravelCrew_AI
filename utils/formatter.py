"""
Small rich-based helpers so main.py stays focused on flow control.
"""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()


def banner(title: str) -> None:
    console.print(Panel.fit(f"[bold cyan]{title}[/bold cyan]", border_style="cyan"))


def show_plan(plan_text: str) -> None:
    console.print(Panel(plan_text, title="TRAVEL PLAN", border_style="green"))


def ask(prompt: str) -> str:
    return Prompt.ask(f"[bold]{prompt}[/bold]")


def ask_choice(prompt: str, choices: list[str]) -> str:
    return Prompt.ask(f"[bold]{prompt}[/bold]", choices=choices)


def confirm(prompt: str) -> bool:
    return Confirm.ask(f"[bold]{prompt}[/bold]")


def info(msg: str) -> None:
    console.print(f"[dim]{msg}[/dim]")


def success(msg: str) -> None:
    console.print(f"[green]✓ {msg}[/green]")


def warn(msg: str) -> None:
    console.print(f"[yellow]! {msg}[/yellow]")
