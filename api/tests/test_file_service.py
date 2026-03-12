import os
import shutil
from unittest.mock import patch
import pytest
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from configs import app_config
from extensions.storage.local_storage import LocalStorage
from services.file_service import (
    FileService,
    FileTooLargeError,
    UnsupportedFileTypeError,
)


@pytest.fixture
def temp_storage_dir(tmp_path):
    """Fixture to set a temporary directory for local storage during tests."""
    original_path = app_config.LOCAL_STORAGE_PATH
    temp_dir = str(tmp_path / "storage")
    app_config.LOCAL_STORAGE_PATH = temp_dir
    yield temp_dir
    # Teardown: restore original config
    app_config.LOCAL_STORAGE_PATH = original_path
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


def test_local_storage_save(temp_storage_dir):
    """Test the actual saving of the file using LocalStorage."""
    storage = LocalStorage()

    file_path = os.path.join(os.path.dirname(__file__), "test_data", "test_save.txt")
    with open(file_path, "rb") as f:
        content = f.read()

    storage.save("upload_files/test_save.txt", content)

    saved_path = os.path.join(temp_storage_dir, "upload_files", "test_save.txt")
    assert os.path.exists(saved_path)

    with open(saved_path, "rb") as f:
        saved_content = f.read()
    assert saved_content == content


def test_file_service_upload(temp_storage_dir):
    """Test the FileService upload logic."""
    from extensions.ext_storage import storage

    # Initialize the runner manually so it actually saves during the test
    storage.storage_runner = LocalStorage()

    file_path = os.path.join(os.path.dirname(__file__), "test_data", "test_save.txt")
    with open(file_path, "rb") as f:
        content = f.read()

    # Call the service
    result = FileService.upload_file(
        filename="test_save.txt", content=content, user_id="test_user"
    )

    # Verify the result dictionary
    assert "file_uuid" in result
    assert "file_key" in result
    assert result["filename"] == "test_save.txt"
    assert result["extension"] == "txt"
    assert result["size"] == len(content)

    # Verify the file was saved to our temp directory
    upload_files_dir = os.path.join(temp_storage_dir, "upload_files")
    assert os.path.exists(upload_files_dir)

    saved_files = os.listdir(upload_files_dir)
    assert len(saved_files) == 1
    assert saved_files[0].endswith(".txt")

    # Verify the content
    with open(os.path.join(upload_files_dir, saved_files[0]), "rb") as f:
        saved_content = f.read()
    assert saved_content == content


def test_file_service_upload_unsupported_type():
    with pytest.raises(UnsupportedFileTypeError):
        FileService.upload_file(filename="test.exe", content=b"123", user_id="test")


def test_file_service_upload_too_large():
    # Mock FILE_SIZE_LIMIT to 0 MB (0 bytes)
    original_limit = app_config.FILE_SIZE_LIMIT
    app_config.FILE_SIZE_LIMIT = 0
    try:
        with pytest.raises(FileTooLargeError):
            FileService.upload_file(filename="test.txt", content=b"123", user_id="test")
    finally:
        app_config.FILE_SIZE_LIMIT = original_limit
