import os
from pathlib import Path

from dotenv import load_dotenv

root_dir = Path(__file__).parents[4]

env_path = root_dir / ".env"

load_dotenv(dotenv_path=env_path)


class Config():
    @staticmethod
    def get(property, default=None):
        return os.getenv(property, default)
