from rich.console import Console
from rich.table import Table

from task.models import Priority, Task

console = Console()

PRIORITY_COLORS = {
    Priority.HIGH: "red",
    Priority.MEDIUM: "yellow",
    Priority.LOW: "white",
}


def success(message: str) -> None:
    """Display a success message."""
    console.print(f"[green]{message}[/green]")


def error(message: str) -> None:
    """Display an error message."""
    console.print(f"[red]{message}[/red]")


def warning(message: str) -> None:
    """Display a warning message."""
    console.print(f"[yellow]{message}[/yellow]")


def info(message: str) -> None:
    """Display an info message."""
    console.print(message)


def table(tasks: list[Task]) -> None:
    """Display tasks in a formatted table."""
    tbl = Table()
    tbl.add_column("#", style="dim", width=4)
    tbl.add_column("Task")
    tbl.add_column("Priority")
    tbl.add_column("Due")
    tbl.add_column("Status", width=6)

    for idx, task in enumerate(tasks, start=1):
        priority_color = PRIORITY_COLORS[task.priority]
        style = "dim" if task.done else ""

        due_str = "-"
        if task.due_date:
            due_str = task.due_date.strftime("%b %d")

        status = "[green]done[/green]" if task.done else "[ ]"

        tbl.add_row(
            str(idx),
            f"[{style}]{task.title}[/{style}]" if style else task.title,
            f"[{priority_color}]{task.priority.value}[/{priority_color}]",
            due_str,
            status,
            style=style,
        )

    console.print(tbl)

    # Summary
    total = len(tasks)
    done_count = sum(1 for t in tasks if t.done)
    pending_count = total - done_count
    info(f"\n  {total} tasks ({pending_count} pending, {done_count} done)")
