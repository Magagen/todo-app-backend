import os
from dataclasses import dataclass
from typing import Sequence

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str | None
    cors_origins: Sequence[str]


def get_settings() -> Settings:
    cors_origin = os.getenv("CORS_ORIGIN_TO_DO")
    if cors_origin:
        return Settings(
            database_url=os.getenv("DATABASE_URL"),
            cors_origins=[cors_origin],
        )
    else:
        raise Exception("CORS_ORIGIN_TO_DO environment variable is not set")
