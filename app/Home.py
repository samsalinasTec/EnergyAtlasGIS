# OBJETIVO: Rebanada 1 ultra-simple.
# - Cargar lista de países desde la API.
# - Elegir país en un select.
# - Mostrar nombre (futura Rebanada 2: población, mix, etc.)

import requests, streamlit as st
from config import API_BASE_URL

st.set_page_config(page_title="Atlas de Energía", layout="wide")
st.title("Atlas de Energía — Rebanada 1 (simple)")

# 1) Traer lista de países de la API
try:
    r = requests.get(f"{API_BASE_URL}/api/paises", timeout=10)
    r.raise_for_status()
    paises = r.json()  # [{codigo, nombre}, ...]
except Exception as e:
    st.error(f"No se pudo conectar a la API: {e}")
    paises = []

# 2) Select con países (súper simple)
if paises:
    opciones = {f'{p["nombre"]} ({p["codigo"]})': p["codigo"] for p in paises}
    elegido = st.selectbox("Elige un país", list(opciones.keys()))
    codigo = opciones[elegido]

    # 3) Pedir la ficha básica del país (por ahora: nombre/código)
    r2 = requests.get(f"{API_BASE_URL}/api/paises/{codigo}/ficha", timeout=10)
    if r2.status_code == 200:
        ficha = r2.json()
        st.subheader(ficha["nombre"])
        st.write(f"Código: {ficha['codigo']}")
        st.info("📌 En la Rebanada 2 agregaremos población y mezcla energética aquí.")
    else:
        st.warning("No se encontró la ficha del país.")
else:
    st.info("Agrega datos a la API (paises.csv) o verifica que esté corriendo.")
