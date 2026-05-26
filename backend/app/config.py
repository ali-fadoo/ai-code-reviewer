from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    github_app_id: str
    github_private_key: str
    github_webhook_secret: str
    database_url: str = "sqlite+aiosqlite:///./reviews.db"
    frontend_url: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()
