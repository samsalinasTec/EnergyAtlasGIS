# OBJETIVO: leer variables de entorno y paths útiles para toda la API.
from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    API_BASE_PATH: str = "/api"       # prefijo de rutas
    DATA_DIR: Path = Path(__file__).resolve().parent.parent / "data"  # ./app/data

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"  # lee ../.env

settings = Settings()