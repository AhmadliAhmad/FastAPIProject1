from pydantic import BaseSettings, Field, root_validator
from typing import Literal
import os
from app.core.logger import get_logger

logger = get_logger()

class Settings(BaseSettings):
    app_domain: str = Field(..., env="APP_DOMAIN")
    env: Literal["development", "production"] = "development"
    log_level: Literal["debug", "info", "warning", "error"] = "info"
    port: int = Field(..., env="PORT")
    service_name: str = Field(..., env="SERVICE_NAME")

    @root_validator(pre=True)
    def validate_env(cls, values):
        current_env = values.get("ENV") or os.environ.get("ENV", "development")
        values["env"] = current_env

        if current_env == "production":
            logger.info("Running in production mode. Validating environment variables...")
            required_keys = ["APP_DOMAIN", "PORT", "SERVICE_NAME", "LOG_LEVEL"]
            missing = [k for k in required_keys if k not in os.environ]
            if missing:
                logger.error(f"Missing required environment variables: {', '.join(missing)}")
                raise ValueError(f"Missing required environment variables: {missing}")
        else:
            logger.info("Running in development mode. Loading from .env...")

        return values

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):

            if os.environ.get("ENV", "development") == "production":
                return (env_settings,)
            return (init_settings, env_settings, file_secret_settings)

settings = Settings()