# OBJETIVO: armar la aplicación (logs + rutas).
from fastapi import FastAPI
from .core.config import settings
from .core.logging import setup_logging
from .routers import countries

def build_app() -> FastAPI:
    setup_logging("INFO")                 # logs a consola
    app = FastAPI(title="Atlas Energía API")
    app.include_router(countries.router, prefix=settings.API_BASE_PATH)  # /api/paises
    return app

app = build_app()
