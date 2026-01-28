"""Tests for the list command."""

from task.commands import app


class TestList:
    """Test suite for list command."""

    def test_shows_pending_tasks_by_default(self, runner, sample_data):
        """Test that pending tasks are shown by default."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "First task" in result.output
        assert "Second task" not in result.output  # Second task is done

    def test_shows_all_tasks_with_all_flag(self, runner, sample_data):
        """Test that --all flag shows both pending and completed tasks."""
        result = runner.invoke(app, ["list", "--all"])

        assert result.exit_code == 0
        assert "First task" in result.output
        assert "Second task" in result.output

    def test_shows_all_tasks_with_short_flag(self, runner, sample_data):
        """Test that -a flag shows all tasks."""
        result = runner.invoke(app, ["list", "-a"])

        assert result.exit_code == 0
        assert "First task" in result.output
        assert "Second task" in result.output

    def test_shows_only_completed_tasks_with_done_flag(self, runner, sample_data):
        """Test that --done flag shows only completed tasks."""
        result = runner.invoke(app, ["list", "--done"])

        assert result.exit_code == 0
        assert "Second task" in result.output
        assert "First task" not in result.output

    def test_filters_by_priority_low(self, runner, temp_storage):
        """Test filtering by low priority."""
        runner.invoke(app, ["add", "Low task", "-p", "low"])
        runner.invoke(app, ["add", "High task", "-p", "high"])
        runner.invoke(app, ["add", "Medium task", "-p", "medium"])

        result = runner.invoke(app, ["list", "--priority", "low"])

        assert result.exit_code == 0
        assert "Low task" in result.output
        assert "High task" not in result.output
        assert "Medium task" not in result.output

    def test_filters_by_priority_high(self, runner, temp_storage):
        """Test filtering by high priority."""
        runner.invoke(app, ["add", "Low task", "-p", "low"])
        runner.invoke(app, ["add", "High task", "-p", "high"])

        result = runner.invoke(app, ["list", "--priority", "high"])

        assert result.exit_code == 0
        assert "High task" in result.output
        assert "Low task" not in result.output

    def test_filters_by_priority_medium(self, runner, temp_storage):
        """Test filtering by medium priority."""
        runner.invoke(app, ["add", "Medium task", "-p", "medium"])
        runner.invoke(app, ["add", "Low task", "-p", "low"])

        result = runner.invoke(app, ["list", "--priority", "medium"])

        assert result.exit_code == 0
        assert "Medium task" in result.output
        assert "Low task" not in result.output

    def test_filters_by_priority_short_flag(self, runner, temp_storage):
        """Test filtering with -p flag."""
        runner.invoke(app, ["add", "High task", "-p", "high"])
        runner.invoke(app, ["add", "Low task", "-p", "low"])

        result = runner.invoke(app, ["list", "-p", "high"])

        assert result.exit_code == 0
        assert "High task" in result.output
        assert "Low task" not in result.output

    def test_priority_filter_case_insensitive(self, runner, temp_storage):
        """Test that priority filter is case-insensitive."""
        runner.invoke(app, ["add", "High task", "-p", "high"])

        result = runner.invoke(app, ["list", "--priority", "HIGH"])

        assert result.exit_code == 0
        assert "High task" in result.output

    def test_invalid_priority_shows_error(self, runner, temp_storage):
        """Test that invalid priority shows error."""
        result = runner.invoke(app, ["list", "--priority", "urgent"])

        assert result.exit_code == 2
        assert "Invalid priority: urgent" in result.output
        assert "Use low, medium, or high" in result.output

    def test_empty_list_shows_warning(self, runner, temp_storage):
        """Test that empty task list shows warning."""
        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "No tasks found" in result.output

    def test_no_pending_tasks_shows_warning(self, runner, temp_storage):
        """Test that no pending tasks shows warning."""
        # Add a completed task
        runner.invoke(app, ["add", "Task"])
        runner.invoke(app, ["done", "1"])

        result = runner.invoke(app, ["list"])  # Default: pending only

        assert result.exit_code == 0
        assert "No tasks found" in result.output

    def test_no_completed_tasks_shows_warning(self, runner, temp_storage):
        """Test that no completed tasks shows warning."""
        runner.invoke(app, ["add", "Pending task"])

        result = runner.invoke(app, ["list", "--done"])

        assert result.exit_code == 0
        assert "No tasks found" in result.output

    def test_combined_all_and_priority_filter(self, runner, temp_storage):
        """Test combining --all with priority filter."""
        runner.invoke(app, ["add", "High pending", "-p", "high"])
        runner.invoke(app, ["add", "Low pending", "-p", "low"])
        runner.invoke(app, ["add", "High completed", "-p", "high"])
        runner.invoke(app, ["done", "3"])

        result = runner.invoke(app, ["list", "--all", "--priority", "high"])

        assert result.exit_code == 0
        assert "High pending" in result.output
        assert "High completed" in result.output
        assert "Low pending" not in result.output

    def test_combined_done_and_priority_filter(self, runner, temp_storage):
        """Test combining --done with priority filter."""
        runner.invoke(app, ["add", "High task", "-p", "high"])
        runner.invoke(app, ["add", "Low task", "-p", "low"])
        runner.invoke(app, ["done", "1"])
        runner.invoke(app, ["done", "2"])

        result = runner.invoke(app, ["list", "--done", "--priority", "high"])

        assert result.exit_code == 0
        assert "High task" in result.output
        assert "Low task" not in result.output

    def test_shows_task_with_due_date(self, runner, temp_storage):
        """Test that tasks with due dates are displayed."""
        runner.invoke(app, ["add", "Task with deadline", "-d", "2025-12-31"])

        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "Task with deadline" in result.output

    def test_shows_multiple_tasks(self, runner, temp_storage):
        """Test displaying multiple tasks."""
        runner.invoke(app, ["add", "Task 1"])
        runner.invoke(app, ["add", "Task 2"])
        runner.invoke(app, ["add", "Task 3"])

        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert "Task 1" in result.output
        assert "Task 2" in result.output
        assert "Task 3" in result.output

    def test_no_matching_priority_shows_warning(self, runner, temp_storage):
        """Test that no matching priority shows warning."""
        runner.invoke(app, ["add", "Low task", "-p", "low"])

        result = runner.invoke(app, ["list", "--priority", "high"])

        assert result.exit_code == 0
        assert "No tasks found" in result.output

    def test_all_flag_includes_completed_tasks(self, runner, temp_storage):
        """Test that -a shows completed tasks."""
        runner.invoke(app, ["add", "Pending"])
        runner.invoke(app, ["add", "Completed"])
        runner.invoke(app, ["done", "2"])

        result_default = runner.invoke(app, ["list"])
        result_all = runner.invoke(app, ["list", "-a"])

        assert "Pending" in result_default.output
        assert "Completed" not in result_default.output
        assert "Pending" in result_all.output
        assert "Completed" in result_all.output

    def test_done_flag_excludes_pending_tasks(self, runner, temp_storage):
        """Test that --done excludes pending tasks."""
        runner.invoke(app, ["add", "Pending"])
        runner.invoke(app, ["add", "Completed"])
        runner.invoke(app, ["done", "2"])

        result = runner.invoke(app, ["list", "--done"])

        assert "Completed" in result.output
        assert "Pending" not in result.output

    def test_displays_sample_data_correctly(self, runner, sample_data):
        """Test that sample data is displayed correctly."""
        result = runner.invoke(app, ["list", "--all"])

        assert result.exit_code == 0
        # Both tasks should be visible with --all
        assert "First task" in result.output
        assert "Second task" in result.output
