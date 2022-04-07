from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Base project settings."""

    PROJECT_ROOT: Path = PROJECT_ROOT
    API_V1_STR: str = '/web/v1'
    SERVER_NAME: str
    PROJECT_NAME: str
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse list for urls."""
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """Parse SQL Alchemy database URI from postgres vars."""
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_SERVER'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    REFRESH_TOKEN_EXPIRATION_DELTA: timedelta = timedelta(days=30)
    ACCESS_TOKEN_EXPIRATION_DELTA: timedelta = timedelta(hours=1)
    JWT_AUTH_HEADER_NAME: str = 'HTTP_AUTHORIZATION'
    JWT_AUTH_HEADER_PREFIX: str = 'Bearer'
    JWT_REFRESH_TOKEN_COOKIE_NAME: str = 'refreshToken'
    SECRET_KEY: str
    JWT_ALGORITHM: str = 'HS256'
    JWT_VERIFY_EXPIRATION: bool = True
    JWT_VERIFY: bool = True

    class Config:
        case_sensitive = True
        env_file = PROJECT_ROOT.joinpath('config/.env').resolve()


settings = Settings()
