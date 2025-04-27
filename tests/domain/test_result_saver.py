import pytest
from unittest.mock import mock_open, patch
from src.dto import NewsRecord
from datetime import date
from src.domain.result_saver import FileToFolderSaver
import json


@pytest.fixture
def sample_records():
    return [
        NewsRecord(
            title="OKX Lists New Token",
            date=date(2023, 1, 1),
            body="OKX is listing a new token..."
        ),
        NewsRecord(
            title="Maintenance Announcement",
            date=date(2023, 1, 2),
            body="Scheduled maintenance on..."
        )
    ]


@pytest.fixture
def saver():
    return FileToFolderSaver()


class TestSaveRecordsToFile:
    def test_creates_folder(self, saver, sample_records, tmp_path):
        folder = tmp_path / "new_folder"
        filename = "news.json"

        with patch('builtins.open', mock_open()) as mocked_open:
            saver.save_records_to_file(sample_records, str(folder), filename)

        assert folder.exists()
        assert folder.is_dir()

    def test_writes_correct_content(self, saver, sample_records, tmp_path):
        folder = tmp_path / "output"
        filename = "data.json"
        filepath = folder / filename

        saver.save_records_to_file(sample_records, str(folder), filename)

        assert filepath.exists()

        with open(filepath, 'r') as f:
            content = json.load(f)

        assert len(content) == 2
        assert content[0]["title"] == "OKX Lists New Token"
        assert content[1]["date"] == "2023-01-02"  # Дата сериализуется в строку

    def test_empty_records(self, saver, tmp_path):
        folder = tmp_path / "empty"
        filename = "empty.json"
        filepath = folder / filename

        saver.save_records_to_file([], str(folder), filename)

        assert filepath.exists()

        with open(filepath, 'r') as f:
            content = json.load(f)

        assert content == []

    def test_handles_special_chars(self, saver, tmp_path):
        folder = tmp_path / "special"
        filename = "data@test#123.json"

        records = [NewsRecord(title="Test", date=date(2023, 1, 1), body="Test body")]

        saver.save_records_to_file(records, str(folder), filename)

        assert (folder / filename).exists()

    @patch('pathlib.Path.mkdir')
    def test_handles_permission_error(self, mock_mkdir, saver, sample_records):
        mock_mkdir.side_effect = PermissionError("No permissions")

        with pytest.raises(PermissionError):
            saver.save_records_to_file(sample_records, "/protected/folder", "news.json")

    def test_json_serialization(self, saver, tmp_path):
        folder = tmp_path / "json_test"
        filename = "test.json"

        records = [
            NewsRecord(title="Test", date=date(2023, 1, 1), body="Body with \"quotes\"")
        ]

        saver.save_records_to_file(records, str(folder), filename)

        with open(folder / filename, 'r') as f:
            content = json.load(f)

        assert content[0]["body"] == 'Body with "quotes"'
