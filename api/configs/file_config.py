from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Any, Literal, Optional


class FileConfig(BaseSettings):
    FILE_EXTENSIONS: list = Field(
        description="List of allowed file extensions.",
        default=["txt", "pdf", "doc", "docx", "xls", "xlsx"]
    )

    FILE_SIZE_LIMIT: int = Field(
        description="Maximum allowed file size in MB.",
        default=10
    )

    STORAGE_TYPE: Literal[
        "local"
    ] = Field(
        description="Type of storage used for file uploads.",
        default="local"
    )

    LOCAL_STORAGE_PATH: str = Field(
        description="Path for local storage when STORAGE_TYPE is set to 'local'.",
        default="storage/"
    )
