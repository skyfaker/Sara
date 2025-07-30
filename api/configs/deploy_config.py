from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DeploymentConfig(BaseSettings):
    """
    Configuration settings for application deployment
    """
    model_config = SettingsConfigDict(
        # read from dotenv format config file
        env_file=".env",
        env_file_encoding="utf-8",
        # ignore extra attributes
        extra="ignore",
    )

    APPLICATION_NAME: str = Field(
        description="Name of the application, used for identification and logging purposes",
        default="sara",
    )

    DEBUG: bool = Field(
        description="Enable debug mode for additional logging and development features",
        default=True,
    )

    # Request logging configuration
    ENABLE_REQUEST_LOGGING: bool = Field(
        description="Enable request and response body logging",
        default=False,
    )

    DEPLOY_ENV: str = Field(
        description="Deployment environment (e.g., 'PRODUCTION', 'DEVELOPMENT'), default to PRODUCTION",
        default="PRODUCTION",
    )