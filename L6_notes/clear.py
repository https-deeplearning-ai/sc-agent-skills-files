import typer

from task.constants import EXIT_ERROR
from task.storage import delete_task, get_tasks

app = typer.Typer()


@app.command()
def clear(
    task_id: int = typer.Argument(..., help="The task ID to delete."),
    force: bool = typer.Option(False, "--force", help="Skip confirmation prompt."),
) -> None:
    """Deletes a task permanently from the list."""
    tasks = get_tasks(done=None)

    if task_id < 1 or task_id > len(tasks):
        print(f"Error: Task {task_id} not found")
        raise typer.Exit(EXIT_ERROR)

    task = tasks[task_id - 1]

    if not force:
        confirm = typer.confirm(f"Delete '{task.title}'?", default=True)
        if not confirm:
            print("Cancelled")
            raise typer.Abort()

    delete_task(task_id)
    print(f"Deleted '{task.title}'")

    # Show updated list
    remaining_tasks = get_tasks(done=None)
    if remaining_tasks:
        from rich.console import Console
        console = Console()
        console.print("[green]Tasks remaining:[/green]")
        for i, t in enumerate(remaining_tasks, 1):
            console.print(f"  {i}. {t.title}")
    else:
        print("No tasks remaining")
