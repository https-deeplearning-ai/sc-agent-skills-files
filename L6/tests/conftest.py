import json
from pathlib import Path

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

    # Monkeypatch the storage module to use temp storage
    from task import storage
    monkeypatch.setattr(storage, "STORAGE_DIR", storage_dir)
    monkeypatch.setattr(storage, "STORAGE_PATH", storage_file)

    return storage_file


@pytest.fixture
def sample_data(temp_storage):
    """Pre-populated storage with sample tasks."""
    data = {
        "version": 1,
        "tasks": [
            {
                "title": "First task",
                "done": False,
                "priority": "low",
                "created_at": "2025-01-01T10:00:00",
                "due_date": None,
            },
            {
                "title": "Second task",
                "done": True,
                "priority": "high",
                "created_at": "2025-01-02T10:00:00",
                "due_date": "2025-12-31T00:00:00",
            },
        ],
    }
    temp_storage.write_text(json.dumps(data, indent=2))
    return data
