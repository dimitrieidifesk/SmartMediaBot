from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_VERSION: str
    PROJECT_NAME: str
    TOKEN: str

    class Config:
        case_sensitive = True
        env_file = "config.env"


project_settings = Settings()