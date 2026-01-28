---
name: adding-cli-command
description: Provides Typer templates, handles registration, and ensures consistency. ALWAYS use this skill when adding or modifying CLI commands. Use when user requests to add/create/implement/build/write a new command (e.g., "add edit command", "create search feature") OR update/modify/change/edit an existing command. 
---

# Adding CLI Commands

Templates and workflow for adding or updating Typer CLI commands.

`<cli_app>` refers to the name of your CLI application (e.g., `task`, `myapp`, `todo`).

## Workflow

1. Identify command type (single command, command group, or destructive)
2. Create file in `src/<cli_app>/commands/<command>.py`
3. Use appropriate template below
4. Register in `src/<cli_app>/commands/__init__.py`


## Template A: Single Command

For commands taking arguments directly (`<cli_app> add "item"`).

```python
import typer
from typing import Annotated

from <cli_app>.storage import add_task
from <cli_app>.display import display
from <cli_app>.constants import EXIT_INVALID_INPUT

app = typer.Typer()


@app.command()
def add(
    title: Annotated[str, typer.Argument(help="task title")],
    priority: Annotated[str, typer.Option("--priority", "-p", help="priority level")] = "low",
):
    """Add a new task."""
    if not title.strip():
        display.error("Title cannot be empty")
        raise typer.Exit(EXIT_INVALID_INPUT)

    task = add_task(title=title, priority=priority)
    display.success(f"Added '{task.title}'")
```

## Template B: Command Group

For commands with subcommands (`<cli_app> db migrate`, `<cli_app> db status`).

```python
import typer

from <cli_app>.storage import storage
from <cli_app>.display import display

app = typer.Typer(help="Database operations.")


@app.command()
def migrate():
    """Run database migrations."""
    storage.migrate()
    display.success("Migrations complete")


@app.command()
def status():
    """Show database status."""
    info = storage.get_status()
    display.info(f"Version: {info.version}")
```

## Template C: Destructive Command

For deletion with confirmation.

```python
import typer
from typing import Annotated

from <cli_app>.storage import get_task, delete_task
from <cli_app>.display import display
from <cli_app>.constants import EXIT_ERROR

app = typer.Typer()


@app.command()
def clear(
    task_id: Annotated[int, typer.Argument(help="task ID to delete")],
    force: Annotated[bool, typer.Option("--force", "-f", help="skip confirmation")] = False,
):
    """Delete a task permanently."""
    task = get_task(task_id)
    if not task:
        display.error(f"Task {task_id} not found")
        raise typer.Exit(EXIT_ERROR)

    if not force:
        confirm = typer.confirm(f"Delete '{task.title}'?", default=False)
        if not confirm:
            display.info("Cancelled")
            raise typer.Abort()

    delete_task(task_id)
    display.success(f"Deleted '{task.title}'")
```

## Registration

Register in `commands/__init__.py`:

```python
import typer

from .add import app as add_app
from .clear import app as clear_app

app = typer.Typer(help="<cli_app> CLI.", no_args_is_help=True)

# Single commands - add WITHOUT name
app.add_typer(add_app)
app.add_typer(clear_app)

# Command groups - add WITH name
# app.add_typer(db_app, name="db")
```

## Conventions

| Rule | Example |
|------|---------|
| Arguments | `Annotated[str, typer.Argument(help="...")]` |
| Options | `Annotated[str, typer.Option("--name", "-n", help="...")]` |
| Docstrings | Imperative mood, < 60 chars |
| Output | Always via `display` module |
| Exit codes | 0=success, 1=error, 2=invalid |
| Destructive | Must have `--force` flag, `default=False` confirmation |
