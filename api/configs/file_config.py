from pydantic_settings import BaseSettings
from pydantic import Field


class FileConfig(BaseSettings):
    FILE_EXTENSIONS: list = Field(
        description="List of allowed file extensions.",
        default=[".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx"]
    )

    FILE_SIZE_LIMIT: int = Field(
        description="Maximum allowed file size in MB.",
        default=10
    )