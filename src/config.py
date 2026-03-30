from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass(frozen=True)
class Config:
    database_url: str
    openai_api_key: str

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()
        database_url = os.getenv("DATABASE_URL")
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set.")

        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        return cls(database_url=database_url, openai_api_key=openai_api_key)
