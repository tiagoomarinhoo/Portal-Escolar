import os


def _required_env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, default)
    if not value:
        raise RuntimeError(f"Defina a variável de ambiente {name}.")
    return value


class Config:
    SECRET_KEY = _required_env("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = _required_env("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False