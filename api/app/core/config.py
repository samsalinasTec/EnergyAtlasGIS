# OBJETIVO: leer variables de entorno y paths útiles para toda la API.
import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)


class Settings:
    API_BASE_PATH: str
    DATA_DIR: Path

    def __init__(self) -> None:
        self.API_BASE_PATH = os.getenv("API_BASE_PATH", "/api")
        self.DATA_DIR = Path(__file__).resolve().parent.parent / "data"  # ./app/data


settings = Settings()