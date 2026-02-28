from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "change-me-to-a-random-secret-key"
    debug: bool = True

    jwt_secret: str = "change-me-to-a-random-jwt-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    database_url: str = "sqlite:///./app.db"
    cors_origins: str = "http://localhost:5173"

    ollama_base_url: str = "http://localhost:11434"
    groq_api_key: str = ""
    huggingface_token: str = ""

    whisper_model_size: str = "base"

    upload_dir: str = "./storage/uploads"
    generated_dir: str = "./storage/generated"
    max_upload_size_mb: int = 50

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
