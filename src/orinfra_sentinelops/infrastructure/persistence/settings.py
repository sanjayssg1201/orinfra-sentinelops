from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./sentinelops.db"
    echo_sql: bool = False

    model_config = SettingsConfigDict(
        env_prefix="SENTINELOPS_",
        env_file=".env",
        extra="ignore",
    )
