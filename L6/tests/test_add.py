"""Tests for the add command."""

import json

from task.commands import app


class TestAdd:
    """Test suite for add command."""

    def test_adds_task_with_minimal_input(self, runner, temp_storage):
        """Test adding a task with just a title."""
        result = runner.invoke(app, ["add", "Buy milk"])

        assert result.exit_code == 0
        assert "Added 'Buy milk'" in result.output

        # Verify task was saved
        data = json.loads(temp_storage.read_text())
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == "Buy milk"
        assert data["tasks"][0]["priority"] == "low"
        assert data["tasks"][0]["done"] is False

    def test_adds_task_with_priority_long_option(self, runner, temp_storage):
        """Test adding a task with --priority option."""
        result = runner.invoke(app, ["add", "Important task", "--priority", "high"])

        assert result.exit_code == 0
        assert "Added 'Important task'" in result.output

        data = json.loads(temp_storage.read_text())
        assert data["tasks"][0]["priority"] == "high"

    def test_adds_task_with_priority_short_option(self, runner, temp_storage):
        """Test adding a task with -p option."""
        result = runner.invoke(app, ["add", "Medium priority task", "-p", "medium"])

        assert result.exit_code == 0
        data = json.loads(temp_storage.read_text())
        assert data["tasks"][0]["priority"] == "medium"

    def test_adds_task_with_due_date_long_option(self, runner, temp_storage):
        """Test adding a task with --due option."""
        result = runner.invoke(app, ["add", "Finish project", "--due", "2025-12-31"])

        assert result.exit_code == 0
        data = json.loads(temp_storage.read_text())
        assert data["tasks"][0]["due_date"] == "2025-12-31T00:00:00"

    def test_adds_task_with_due_date_short_option(self, runner, temp_storage):
        """Test adding a task with -d option."""
        result = runner.invoke(app, ["add", "Meeting", "-d", "2025-06-15"])

        assert result.exit_code == 0
        data = json.loads(temp_storage.read_text())
        assert data["tasks"][0]["due_date"] == "2025-06-15T00:00:00"

    def test_adds_task_with_all_options(self, runner, temp_storage):
        """Test adding a task with both priority and due date."""
        result = runner.invoke(
            app, ["add", "Complete assignment", "-p", "high", "-d", "2025-07-01"]
        )

        assert result.exit_code == 0
        data = json.loads(temp_storage.read_text())
        assert data["tasks"][0]["title"] == "Complete assignment"
        assert data["tasks"][0]["priority"] == "high"
        assert data["tasks"][0]["due_date"] == "2025-07-01T00:00:00"

    def test_priority_case_insensitive(self, runner, temp_storage):
        """Test that priority is case-insensitive."""
        result = runner.invoke(app, ["add", "Task", "--priority", "HIGH"])

        assert result.exit_code == 0
        data = json.loads(temp_storage.read_text())
        assert data["tasks"][0]["priority"] == "high"

    def test_strips_title_whitespace(self, runner, temp_storage):
        """Test that title whitespace is stripped."""
        result = runner.invoke(app, ["add", "  Task with spaces  "])

        assert result.exit_code == 0
        assert "Added 'Task with spaces'" in result.output
        data = json.loads(temp_storage.read_text())
        assert data["tasks"][0]["title"] == "Task with spaces"

    def test_empty_title_shows_error(self, runner, temp_storage):
        """Test that empty title shows validation error."""
        result = runner.invoke(app, ["add", ""])

        assert result.exit_code == 2
        assert "Title cannot be empty" in result.output

    def test_whitespace_only_title_shows_error(self, runner, temp_storage):
        """Test that whitespace-only title shows validation error."""
        result = runner.invoke(app, ["add", "   "])

        assert result.exit_code == 2
        assert "Title cannot be empty" in result.output

    def test_invalid_priority_shows_error(self, runner, temp_storage):
        """Test that invalid priority shows validation error."""
        result = runner.invoke(app, ["add", "Task", "--priority", "urgent"])

        assert result.exit_code == 2
        assert "Invalid priority: urgent" in result.output
        assert "Use low, medium, or high" in result.output

    def test_invalid_date_format_shows_error(self, runner, temp_storage):
        """Test that invalid date format shows validation error."""
        result = runner.invoke(app, ["add", "Task", "--due", "12/31/2025"])

        assert result.exit_code == 2
        assert "Invalid date format: 12/31/2025" in result.output
        assert "Use YYYY-MM-DD" in result.output

    def test_invalid_date_value_shows_error(self, runner, temp_storage):
        """Test that invalid date value shows validation error."""
        result = runner.invoke(app, ["add", "Task", "--due", "2025-13-01"])

        assert result.exit_code == 2
        assert "Invalid date format: 2025-13-01" in result.output

    def test_adds_multiple_tasks_sequentially(self, runner, temp_storage):
        """Test that multiple tasks can be added."""
        runner.invoke(app, ["add", "First task"])
        runner.invoke(app, ["add", "Second task"])
        result = runner.invoke(app, ["add", "Third task"])

        assert result.exit_code == 0
        data = json.loads(temp_storage.read_text())
        assert len(data["tasks"]) == 3
        assert data["tasks"][0]["title"] == "First task"
        assert data["tasks"][1]["title"] == "Second task"
        assert data["tasks"][2]["title"] == "Third task"

    def test_task_has_created_at_timestamp(self, runner, temp_storage):
        """Test that tasks have a created_at timestamp."""
        result = runner.invoke(app, ["add", "Task with timestamp"])

        assert result.exit_code == 0
        data = json.loads(temp_storage.read_text())
        assert "created_at" in data["tasks"][0]
        assert data["tasks"][0]["created_at"] is not None
