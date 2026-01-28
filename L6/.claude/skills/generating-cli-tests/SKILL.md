---
name: generating-cli-tests
description: Generate pytest tests for Typer CLI commands. Includes fixtures (temp_storage, sample_data), CliRunner patterns, confirmation handling (y/n/--force), and edge case coverage. Use when user asks to "write tests for", "test my CLI", "add test coverage", or any CLI + test request.
---

# Generating CLI Tests

Patterns for generating tests for Typer CLI commands.

## Workflow

1. Identify command type (Create/Read/Update/Delete/Bulk)
2. Ensure fixtures exist in `conftest.py`
3. Write tests using scenarios below
4. Run tests to verify

## Fixtures (conftest.py)

```python
import json
import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner():
    """CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_storage(tmp_path, monkeypatch):
    """Empty storage for testing."""
    storage_dir = tmp_path / ".task"
    storage_dir.mkdir()
    storage_file = storage_dir / "tasks.json"
    storage_file.write_text(json.dumps({"version": 1, "tasks": []}))
    monkeypatch.setenv("TASK_STORAGE_PATH", str(storage_file))
    return storage_file


@pytest.fixture
def sample_data(temp_storage):
    """Pre-populated storage."""
    data = {
        "version": 1,
        "tasks": [
            {"title": "First task", "done": False, "priority": "low", "created_at": "2025-01-01T10:00:00", "due_date": None},
            {"title": "Second task", "done": True, "priority": "high", "created_at": "2025-01-01T11:00:00", "due_date": None},
        ]
    }
    temp_storage.write_text(json.dumps(data))
    return data
```

## Test Structure (AAA)

```python
def test_<command>_<scenario>(runner, temp_storage):
    # Arrange - via fixtures

    # Act
    result = runner.invoke(app, ["<command>", "<args>"])

    # Assert
    assert result.exit_code == 0
    assert "<expected>" in result.output
```

## CliRunner Usage

```python
from typer.testing import CliRunner
from task.main import app

runner = CliRunner()

# Basic
result = runner.invoke(app, ["add", "New task"])

# With options
result = runner.invoke(app, ["add", "Task", "--priority", "high"])

# With confirmation
result = runner.invoke(app, ["clear", "1"], input="y\n")  # Accept
result = runner.invoke(app, ["clear", "1"], input="n\n")  # Decline

# Skip confirmation
result = runner.invoke(app, ["clear", "1", "--force"])
```

## Test Scenarios by Command Type

### Create/Add

```python
class TestAdd:
    def test_adds_task(self, runner, temp_storage):
        result = runner.invoke(app, ["add", "New task"])
        assert result.exit_code == 0
        assert "Added" in result.output

    def test_with_priority(self, runner, temp_storage):
        result = runner.invoke(app, ["add", "Task", "--priority", "high"])
        assert result.exit_code == 0

    def test_empty_title_shows_error(self, runner, temp_storage):
        result = runner.invoke(app, ["add", ""])
        assert result.exit_code == 2
```

### Read/List

```python
class TestList:
    def test_shows_tasks(self, runner, sample_data):
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0
        assert "First task" in result.output

    def test_empty_state(self, runner, temp_storage):
        result = runner.invoke(app, ["list"])
        assert "No tasks" in result.output or "empty" in result.output.lower()

    def test_with_filter(self, runner, sample_data):
        result = runner.invoke(app, ["list", "--done"])
        assert result.exit_code == 0
```

### Update/Done

```python
class TestDone:
    def test_marks_done(self, runner, sample_data):
        result = runner.invoke(app, ["done", "1"])
        assert result.exit_code == 0

    def test_not_found(self, runner, temp_storage):
        result = runner.invoke(app, ["done", "999"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()
```

### Delete/Clear

```python
class TestClear:
    def test_confirmed(self, runner, sample_data):
        result = runner.invoke(app, ["clear", "1"], input="y\n")
        assert result.exit_code == 0
        assert "Deleted" in result.output

    def test_declined(self, runner, sample_data):
        result = runner.invoke(app, ["clear", "1"], input="n\n")
        assert "Cancelled" in result.output

    def test_force(self, runner, sample_data):
        result = runner.invoke(app, ["clear", "1", "--force"])
        assert result.exit_code == 0

    def test_not_found(self, runner, temp_storage):
        result = runner.invoke(app, ["clear", "999", "--force"])
        assert result.exit_code == 1
```

## Edge Cases to Cover

| Category | Test Cases |
|----------|------------|
| Invalid Input | Empty string, wrong type, out of range |
| Not Found | ID doesn't exist |
| Boundary | Zero, negative, first/last item |
| State | Already done, empty storage |
| Confirmation | Accept (y), decline (n), force flag |

## Checklist

- [ ] Test file: `tests/test_<command>.py`
- [ ] Fixtures in `conftest.py`
- [ ] Uses `CliRunner` from `typer.testing`
- [ ] AAA structure (Arrange, Act, Assert)
- [ ] Tests exit codes: 0, 1, 2
- [ ] Destructive commands: tests y/n and `--force`
- [ ] Output assertions check expected messages

## Running Tests

```bash
uv run pytest                       # All tests
uv run pytest -v                    # Verbose
uv run pytest tests/test_add.py    # Specific file
```
