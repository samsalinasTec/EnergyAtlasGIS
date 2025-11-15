#!/usr/bin/env bash
set -euo pipefail

echo "📁 Creando estructura de proyecto en la carpeta actual: $(pwd)"

# Backend (FastAPI)
mkdir -p api/app/core
mkdir -p api/app/models
mkdir -p api/app/routers
mkdir -p api/app/services
mkdir -p api/app/data
mkdir -p api/tests

# Frontend (Streamlit)
mkdir -p app/components
mkdir -p app/data
mkdir -p app/pages

# Scripts
mkdir -p scripts

echo "✅ Estructura creada:"
echo "
api/
  app/
    core/
    models/
    routers/
    services/
    data/
  tests/

app/
  components/
  data/
  pages/

scripts/
"

echo "🎉 Listo. Llena los archivos según tus necesidades."
