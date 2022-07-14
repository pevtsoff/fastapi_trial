from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    database_url: str = "sqlite+aiosqlite:///./database.sqlite3"
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600


# settings = Settings()
settings = Settings(_env_file=".env", _env_file_encoding="UTF-8")
