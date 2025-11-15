# OBJETIVO: funciones para trabajar con mapas/geojson (placeholder).
import json
from pathlib import Path

def load_geojson(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
