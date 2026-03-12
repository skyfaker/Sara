import datetime
import hashlib
import os
import uuid
import logging

from configs import app_config
from extensions.ext_db import db
from extensions.ext_storage import storage
from models.model import UploadFile


class UnsupportedFileTypeError(ValueError):
    """Exception raised for unsupported file types."""

    def __init__(self, message="Unsupported file type."):
        self.message = message


class FileTooLargeError(ValueError):
    """Exception raised when the file size exceeds the limit."""

    def __init__(self, message="File size exceeds the limit."):
        self.message = message


class FileService:
    @staticmethod
    def upload_file(*,
                    filename: str,
                    content: bytes,
                    user_id) -> dict:
        """
        Upload a file to the database.

        :param filename: Name of the file
        :param content: Content of the file as bytes
        :param user_id: User uploading the file
        :return: Dictionary with file metadata (file_uuid, file_key, filename, extension, size)
        """
        # check if filename contains invalid characters
        if any(c in filename for c in ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]):
            raise ValueError("Filename contains invalid characters")

        # get file extension
        extension = os.path.splitext(filename)[1].lstrip(".").lower()
        if extension not in app_config.FILE_EXTENSIONS:
            raise UnsupportedFileTypeError()

        if len(filename) > 200:
            filename = filename.split(".")[0][:200] + "." + extension

        # get file size
        file_size = len(content)
        # check if the file size is exceeded
        if file_size > app_config.FILE_SIZE_LIMIT * 1024 * 1024:
            raise FileTooLargeError()

        # generate file key
        file_uuid = str(uuid.uuid4())

        file_key = "upload_files/" + file_uuid + "." + extension
        storage.save(file_key, content)
        logging.debug("file {} saved to storage with key {}".format(filename, file_key))

        return {
            "file_uuid": file_uuid,
            "file_key": file_key,
            "filename": filename,
            "extension": extension,
            "size": file_size,
        }
