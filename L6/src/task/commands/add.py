from datetime import datetime
from typing import Annotated

import typer

from task import display
from task.constants import EXIT_INVALID_INPUT
from task.models import Priority, Task
from task.storage import add_task

app = typer.Typer()


@app.command()
def add(
    title: Annotated[str, typer.Argument(help="task description")],
    priority: Annotated[
        str, typer.Option("--priority", "-p", help="priority level")
    ] = "low",
    due: Annotated[
        str | None, typer.Option("--due", "-d", help="due date (YYYY-MM-DD)")
    ] = None,
) -> None:
    """Add a new task."""
    # Validate title
    if not title.strip():
        display.error("Title cannot be empty")
        raise typer.Exit(EXIT_INVALID_INPUT)

    # Validate and parse priority
    try:
        task_priority = Priority(priority.lower())
    except ValueError:
        display.error(f"Invalid priority: {priority}. Use low, medium, or high")
        raise typer.Exit(EXIT_INVALID_INPUT)

    # Parse due date
    due_date = None
    if due:
        try:
            due_date = datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            display.error(f"Invalid date format: {due}. Use YYYY-MM-DD")
            raise typer.Exit(EXIT_INVALID_INPUT)

    # Create and save task
    task = Task(
        title=title.strip(),
        priority=task_priority,
        due_date=due_date,
    )
    add_task(task)

    display.success(f"Added '{task.title}'")
