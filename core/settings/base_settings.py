import os
from pydantic_settings import BaseSettings

SELECTED_ENV_NAME = os.environ.get("APP_ENV_NAME")


class BaseSettings(BaseSettings):
    class Config:
        case_sensitive = True
        validate_assignment = True

    @classmethod
    def get_selected_env(cls) -> str:
        if SELECTED_ENV_NAME in ("dev", "stg", "prod", "local", "redirect"):
            env_name = f"{SELECTED_ENV_NAME}.env"
        else:
            env_name = ".env"
        return env_name

    @classmethod
    def get_env_file_path(cls, env_name: str) -> str:
        env_file_path = os.path.join(os.getcwd(), "envs", env_name)
        if not os.path.isfile(env_file_path):
            with open(env_file_path, "w") as f:  # noqa  # NOSONAR

                pass
        return env_file_path

    def setup(self, from_env, **kwargs):
        ...
