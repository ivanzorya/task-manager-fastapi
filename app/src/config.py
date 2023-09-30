from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tasks API"
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    db_name: str
    postgres_user: str
    postgres_password: str
    db_host: str
    env: str

    class Config:
        env_file = ".env"
