# CLAUDE.md

A command-line task management application for tracking todos with priorities and due dates.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.13+ |
| CLI Framework | Typer |
| Data Validation | dataclasses |
| Output Formatting | Rich |
| Storage | JSON file |
| Packaging | pyproject.toml + hatchling |
| Dependency Management | uv |

## Development

```bash
uv run task <command>
uv run pytest          # run tests
```

## Architecture

```
src/task/
├── main.py           # Entry point, imports app from commands
├── commands/
│   ├── __init__.py   # Creates main app, registers all command sub-apps
│   ├── add.py        # add command
│   ├── list.py       # list command
│   └── done.py       # done command (mark task as completed)
├── models.py         # Task dataclass, Priority enum (low/medium/high)
├── storage.py        # JSON persistence (load_tasks, save_tasks, add_task, get_tasks, delete_task)
├── display.py        # Output formatting (success/error/warning/info/table)
└── constants.py      # EXIT_SUCCESS=0, EXIT_ERROR=1, EXIT_INVALID_INPUT=2

tests/
├── conftest.py       # Fixtures: runner, temp_storage, sample_data
├── test_add.py       # Tests for add command
├── test_list.py      # Tests for list command
└── test_done.py      # Tests for done command
```

**Flow**: `main.py` → `commands/__init__.py` → command file → storage/display

## Data Models

**Priority** (str, Enum): `LOW = "low"`, `MEDIUM = "medium"`, `HIGH = "high"`

**Task** (dataclass):
| Field | Type | Default |
|-------|------|---------|
| `title` | `str` | required |
| `done` | `bool` | `False` |
| `priority` | `Priority` | `Priority.LOW` |
| `created_at` | `datetime` | `datetime.now()` |
| `due_date` | `datetime \| None` | `None` |

## Storage

Data is persisted in `~/.task/tasks.json`:

```json
{
  "version": 1,
  "tasks": [
    {
      "title": "Buy milk",
      "done": false,
      "priority": "low",
      "created_at": "2025-12-26T10:30:00",
      "due_date": null
    }
  ]
}
```

- **Version field**: For future schema migrations
- **ID strategy**: IDs are derived from array position (index + 1), not stored in JSON
  - IDs are always sequential: 1, 2, 3...
  - After delete, remaining tasks reindex

## Rules

**Input validation:**
- Title: non-empty after strip
- Priority: must be "low", "medium", or "high" (case-insensitive)
- Due date: YYYY-MM-DD format

**Defaults & behavior:**
- New tasks default to "low" priority
- Deleting requires `[y/N]` confirmation unless `--force`