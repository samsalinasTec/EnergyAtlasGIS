# OBJETIVO: centralizar configuración del frontend (URL de la API).
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
