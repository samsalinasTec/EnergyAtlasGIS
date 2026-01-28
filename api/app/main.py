# OBJETIVO: armar la aplicación (logs + rutas).
from fastapi import FastAPI
from .core.config import settings
from .core.logging import setup_logging
from .routers import countries, solar

def build_app() -> FastAPI:
    setup_logging("INFO")                 # logs a consola
    app = FastAPI(title="Atlas Energía API")
    app.include_router(countries.router, prefix=settings.API_BASE_PATH)  # /api/paises
    app.include_router(solar.router, prefix=settings.API_BASE_PATH)  # /api/solar
    return app

app = build_app()
