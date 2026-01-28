from typing import Annotated

import typer

from task import display
from task.constants import EXIT_ERROR, EXIT_INVALID_INPUT
from task.storage import load_tasks, save_tasks

app = typer.Typer()


@app.command()
def done(
    task_id: Annotated[int, typer.Argument(help="task ID to mark as completed")],
) -> None:
    """Mark a task as completed."""
    tasks = load_tasks()

    # Validate task ID (1-indexed)
    if task_id < 1:
        display.error("Task ID must be positive")
        raise typer.Exit(EXIT_INVALID_INPUT)

    if task_id > len(tasks):
        display.error(f"Task {task_id} not found")
        raise typer.Exit(EXIT_INVALID_INPUT)

    # Mark task as done
    task = tasks[task_id - 1]
    task.done = True
    save_tasks(tasks)

    display.success(f"Completed: {task.title}")
