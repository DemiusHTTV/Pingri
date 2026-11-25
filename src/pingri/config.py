from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433
    BOT_TOKEN: str

    @property
    def postgres_dsn(self) -> str:
        if not all((self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_DB)):
            raise ValueError("Для PostgreSQL задайте POSTGRES_USER, POSTGRES_PASSWORD и POSTGRES_DB")
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
