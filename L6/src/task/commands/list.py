from typing import Annotated

import typer

from task import display
from task.constants import EXIT_INVALID_INPUT
from task.models import Priority
from task.storage import get_tasks

app = typer.Typer()


@app.command()
def list(
    all_tasks: Annotated[
        bool, typer.Option("--all", "-a", help="include completed")
    ] = False,
    done: Annotated[bool, typer.Option("--done", help="show only completed")] = False,
    priority: Annotated[
        str | None, typer.Option("--priority", "-p", help="filter by priority")
    ] = None,
) -> None:
    """List tasks."""
    # Parse priority filter
    priority_filter = None
    if priority:
        try:
            priority_filter = Priority(priority.lower())
        except ValueError:
            display.error(f"Invalid priority: {priority}. Use low, medium, or high")
            raise typer.Exit(EXIT_INVALID_INPUT)

    # Determine done filter
    done_filter = None
    if done:
        done_filter = True
    elif not all_tasks:
        done_filter = False  # Default: show only pending

    # Get filtered tasks
    tasks = get_tasks(done=done_filter, priority=priority_filter)

    if not tasks:
        display.warning("No tasks found")
        return

    display.table(tasks)
