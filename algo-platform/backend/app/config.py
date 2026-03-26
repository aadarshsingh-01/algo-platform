from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Algo Platform"
    env: str = "development"
    secret_key: str = "change-me-super-secret"
    access_token_expire_minutes: int = 60
    database_url: str = "sqlite:///./algo.db"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


settings = Settings()
