import json
from datetime import datetime
from pathlib import Path

from task.models import Priority, Task

STORAGE_DIR = Path.home() / ".task"
STORAGE_PATH = STORAGE_DIR / "tasks.json"


def _ensure_storage_exists() -> None:
    """Create storage directory and file if they don't exist."""
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    if not STORAGE_PATH.exists():
        STORAGE_PATH.write_text(json.dumps({"version": 1, "tasks": []}))


def _task_to_dict(task: Task) -> dict:
    """Convert a Task to a JSON-serializable dictionary."""
    return {
        "title": task.title,
        "done": task.done,
        "priority": task.priority.value,
        "created_at": task.created_at.isoformat(),
        "due_date": task.due_date.isoformat() if task.due_date else None,
    }


def _dict_to_task(data: dict) -> Task:
    """Convert a dictionary to a Task object."""
    return Task(
        title=data["title"],
        done=data["done"],
        priority=Priority(data["priority"]),
        created_at=datetime.fromisoformat(data["created_at"]),
        due_date=datetime.fromisoformat(data["due_date"]) if data["due_date"] else None,
    )


def load_tasks() -> list[Task]:
    """Load all tasks from storage."""
    _ensure_storage_exists()
    data = json.loads(STORAGE_PATH.read_text())
    return [_dict_to_task(t) for t in data["tasks"]]


def save_tasks(tasks: list[Task]) -> None:
    """Save all tasks to storage."""
    _ensure_storage_exists()
    data = {"version": 1, "tasks": [_task_to_dict(t) for t in tasks]}
    STORAGE_PATH.write_text(json.dumps(data, indent=2))


def add_task(task: Task) -> None:
    """Add a task and save to storage."""
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)


def get_tasks(
    done: bool | None = None,
    priority: Priority | None = None,
) -> list[Task]:
    """Get tasks with optional filtering."""
    tasks = load_tasks()

    if done is not None:
        tasks = [t for t in tasks if t.done == done]

    if priority is not None:
        tasks = [t for t in tasks if t.priority == priority]

    return tasks


def delete_task(task_id: int) -> None:
    """Delete a task by its 1-indexed ID."""
    tasks = load_tasks()
    del tasks[task_id - 1]
    save_tasks(tasks)
