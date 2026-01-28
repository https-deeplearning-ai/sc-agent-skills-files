# Task CLI

A command-line task manager for tracking todos with priorities and due dates.

## Getting Started

### 1. Development Setup

Install dependencies:

```bash
uv sync
```

Run commands using `uv run`:

```bash
uv run task add "My first task"
uv run task list
```
Or

``` bash
source .venv/bin/activate
task
```
This is ideal for development since you don't need to reinstall after code changes.

### 2. Global Installation

To use `task` directly without the `uv run` prefix, install the package in editable mode:

```bash
uv tool install -e .
```

Now you can run commands directly:

```bash
task add "My task"
task list
```

The `-e` (editable) flag means code changes still take effect immediately without reinstalling.

### 3. Building for Distribution (Advanced)

To share the package with others, build distributable files:

```bash
uv build
```

This creates files in `dist/`:
- `task_cli-0.1.0.tar.gz` - source distribution
- `task_cli-0.1.0-py3-none-any.whl` - wheel (recommended for installing)

Recipients can install the wheel file:

```bash
pip install task_cli-0.1.0-py3-none-any.whl
```

You can also publish to PyPI with `uv publish` for public distribution.

## Commands

### Add a task

```bash
task add "Buy groceries"
task add "Finish report" -p high
task add "Pay bills" -p medium -d 2025-01-15
```

| Option | Description |
|--------|-------------|
| `-p, --priority` | Priority: `low`, `medium`, `high` (default: low) |
| `-d, --due` | Due date in `YYYY-MM-DD` format |

### List tasks

```bash
task list              # pending tasks only
task list -a           # all tasks (including completed)
task list --done       # completed tasks only
task list -p high      # filter by priority
```

| Option | Description |
|--------|-------------|
| `-a, --all` | Include completed tasks |
| `--done` | Show only completed tasks |
| `-p, --priority` | Filter by priority level |

### Mark task as done

```bash
task done 1            # mark task #1 as completed
```

### Delete a task

```bash
task clear 1           # delete task #1 (with confirmation)
task clear 1 --force   # delete without confirmation
```

## Data Storage

Tasks are stored in `~/.task/tasks.json`.
