from pydantic import BaseSettings


class EnvVars(BaseSettings):
    # Postgres DB info
    PG_USERNAME: str
    PG_PASSWORD: str
    PG_HOSTNAME: str
    PG_DB_NAME: str

    # JWT Auth info
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES = 120

    class Config:
        env_file = ".env"


env_vars = EnvVars()
