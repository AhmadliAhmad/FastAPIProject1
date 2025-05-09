from pydantic import Field, root_validator
from pydantic_settings import BaseSettings
from typing import Literal
import os

#logger = get_logger()

class Settings(BaseSettings):
    app_domain: str = Field(..., validation_alias="APP_DOMAIN")
    env: Literal["development", "production"] = "development"
    log_level: Literal["debug", "info", "warning", "error"] = "info"
    port: int = Field(..., validation_alias="PORT")
    service_name: str = Field(..., validation_alias="SERVICE_NAME")


    @root_validator(pre=True)
    def validate_env(cls, values):
        current_env = values.get("ENV") or os.environ.get("ENV", "development")
        values["env"] = current_env

        if current_env == "production":
            required_keys = ["APP_DOMAIN", "PORT", "SERVICE_NAME", "LOG_LEVEL"]
            missing = [k for k in required_keys if k not in os.environ]
            if missing:
                raise ValueError(f"Missing required environment variables: {missing}")
        return values

    class Config:
        env_file = ".env1" if os.environ.get("ENV") == "development" else ".env"
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            if os.environ.get("ENV", "production") == "production":
                return (env_settings,)
            return (init_settings, env_settings, file_secret_settings)
