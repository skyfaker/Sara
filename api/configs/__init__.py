from pydantic_settings import SettingsConfigDict

from .deploy_config import DeploymentConfig
from .file_config import FileConfig
from .log_config import LogConfig
from .middleware_config import MiddlewareConfig


class AppConfig(DeploymentConfig,
                FileConfig,
                LogConfig,
                MiddlewareConfig):
    model_config = SettingsConfigDict(
        # read from dotenv format config file
        env_file=".env",
        env_file_encoding="utf-8",
        # ignore extra attributes
        extra="ignore",
    )


app_config = AppConfig()

__all__ = ["app_config"]
