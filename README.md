# 🌍 Atlas de Energía

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121%2B-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.51%2B-red)](https://streamlit.io/)

Plataforma web para visualización y análisis de datos energéticos globales por país.

## 🚀 Quick Start

### 1️⃣ Clonar y configurar
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/atlas-energia.git
cd atlas-energia

# Configurar variables de entorno
cp .env.example .env
```

### 2️⃣ Instalar dependencias
```bash
# Opción A: Con pip
pip install -e .

# Opción B: Con entornos virtuales separados
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -e .
```

### 3️⃣ Preparar datos
```bash
# Crear archivo de datos de prueba
mkdir -p api/app/data
echo "CODIGO_PAIS,NOMBRE_PAIS
MEX,México
USA,Estados Unidos
BRA,Brasil" > api/app/data/paises.csv
```

### 4️⃣ Iniciar servicios
```bash
# Terminal 1 - Backend
make api   # http://localhost:8000

# Terminal 2 - Frontend  
make app   # http://localhost:8501

# Terminal 3 - Tests (opcional)
make test
```

### 5️⃣ Verificar funcionamiento
- 🎨 Frontend: http://localhost:8501
- 📡 API Docs: http://localhost:8000/docs
- 🧪 Test endpoint: `curl http://localhost:8000/api/paises`

## 📋 Requisitos

- Python 3.13+
- pip o uv
- Make (opcional, para comandos simplificados)

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **Pydantic** - Validación de datos y serialización
- **Python-dotenv** - Gestión de variables de entorno

### Frontend
- **Streamlit** - Framework para aplicaciones de datos
- **Requests** - Cliente HTTP para consumir la API
- **Pandas** - Manipulación de datos (preparado)

### Testing y Calidad
- **Pytest** - Framework de testing
- **Mypy** - Type checking estático
- **Ruff** - Linter ultra-rápido
- **Black** - Formateador de código

## 🏗️ Arquitectura

```
Frontend (Streamlit:8501) → API REST → Backend (FastAPI:8000) → Data (CSV)
```

### Flujo de Datos
1. Usuario accede a Streamlit (`http://localhost:8501`)
2. Frontend solicita lista de países a `GET /api/paises`
3. Backend lee `paises.csv` y retorna JSON
4. Usuario selecciona un país
5. Frontend solicita detalles a `GET /api/paises/{codigo}/ficha`
6. Backend busca y retorna información del país

Ver [documentación completa de arquitectura](docs/ARQUITECTURA.md)

## 📁 Estructura del Proyecto

```
atlas-energia/
│
├── api/                        # 🔧 Backend (FastAPI)
│   ├── app/
│   │   ├── core/              # Configuración central
│   │   │   ├── config.py      # Variables de entorno y paths
│   │   │   └── logging.py     # Sistema de logs
│   │   ├── models/            # Modelos de datos (Pydantic)
│   │   │   └── country.py     # Country, CountryDetail
│   │   ├── routers/           # Endpoints HTTP
│   │   │   └── countries.py   # GET /api/paises, /api/paises/{codigo}/ficha
│   │   ├── services/          # Lógica de negocio
│   │   │   └── countries_services.py  # list_countries(), get_country()
│   │   ├── data/              # Archivos de datos
│   │   │   └── paises.csv     # Base de datos CSV
│   │   └── main.py            # Punto de entrada de la API
│   └── tests/                 # Tests unitarios
│       └── test_countries.py  # Tests de endpoints
│
├── app/                        # 🎨 Frontend (Streamlit)
│   ├── components/            # Componentes reutilizables (futuro)
│   ├── pages/                 # Páginas adicionales (futuro)
│   ├── data/                  # Datos del frontend
│   ├── Home.py               # Página principal
│   └── config.py             # Configuración (API_BASE_URL)
│
├── scripts/                   # 📝 Scripts de utilidad
│   └── create_atlas_structure.sh  # Crear estructura inicial
│
├── docs/                      # 📚 Documentación detallada
│   ├── DOCUMENTACION.md      # Documentación técnica completa
│   ├── ARQUITECTURA.md       # Diagramas y arquitectura
│   ├── DESARROLLO.md         # Guía de desarrollo
│   ├── API.md               # Documentación de endpoints
│   ├── CONTRIBUTING.md      # Guía de contribución
│   └── CHANGELOG.md         # Historial de cambios
│
├── .env.example              # Variables de entorno ejemplo
├── .gitignore               # Archivos ignorados por Git
├── pyproject.toml           # Configuración Python y dependencias
├── makefile                 # Comandos de desarrollo
├── LICENSE                  # Licencia MIT
└── README.md               # Este archivo
```

## 🛠️ Desarrollo

### Descripción de Componentes

#### Backend (`/api`)
- **core/**: Configuración central y utilidades compartidas
- **models/**: Esquemas de datos con validación automática (Pydantic)
- **routers/**: Definición de endpoints HTTP y rutas
- **services/**: Lógica de negocio separada de la capa HTTP
- **data/**: Archivos CSV con datos de países

#### Frontend (`/app`)
- **Home.py**: Interfaz principal con selector de países
- **config.py**: URL de la API y configuración
- **pages/**: Futuras páginas adicionales (análisis, gráficos)
- **components/**: Componentes reutilizables (en desarrollo)

### Comandos Principales

```bash
make api   # Iniciar backend
make app   # Iniciar frontend  
make test  # Ejecutar tests
```

### Agregar datos de prueba

Crear archivo `api/app/data/paises.csv`:
```csv
CODIGO_PAIS,NOMBRE_PAIS
MEX,México
USA,Estados Unidos
BRA,Brasil
```

### Archivos Clave

| Archivo | Función |
|---------|---------|
| `api/app/main.py` | Punto de entrada del backend, configura FastAPI |
| `api/app/routers/countries.py` | Define endpoints `/api/paises` |
| `api/app/services/countries_services.py` | Lee CSV y procesa datos |
| `app/Home.py` | Interfaz Streamlit principal |
| `makefile` | Automatización de comandos |
| `pyproject.toml` | Dependencias del proyecto |

## 📚 Documentación

- 📖 [Documentación Completa](docs/DOCUMENTACION.md) - Detalles de cada módulo
- 🏗️ [Arquitectura](docs/ARQUITECTURA.md) - Diagramas y flujos
- 🚀 [Guía de Desarrollo](docs/DESARROLLO.md) - Tips y mejores prácticas
- 🔄 [Changelog](docs/CHANGELOG.md) - Historial de cambios

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=api/app --cov-report=html

# Ver reporte
open htmlcov/index.html
```

## 📈 Estado del Proyecto

### ✅ Fase 1: MVP Básico (COMPLETADO)
- ✅ Estructura del proyecto configurada
- ✅ API REST funcional con FastAPI
- ✅ Frontend básico con Streamlit
- ✅ Endpoints de países (`/api/paises`)
- ✅ Sistema de configuración (.env)
- ✅ Tests unitarios
- ✅ Documentación inicial

### 🔄 Fase 2: Datos Energéticos (EN DESARROLLO)
- ⏳ Población por país
- ⏳ Mix energético (% renovable, fósil, nuclear)
- ⏳ Consumo energético per cápita
- ⏳ Visualizaciones con gráficos
- ⏳ Exportación de datos

### 📅 Fase 3: Análisis Avanzado (PLANIFICADO)
- 📅 Base de datos PostgreSQL
- 📅 Dashboard interactivo
- 📅 Comparaciones entre países
- 📅 Tendencias temporales
- 📅 Predicciones con ML

### 🚀 Fase 4: Producción (FUTURO)
- 🚀 Despliegue en la nube
- 🚀 API pública documentada
- 🚀 Integración con datos GIS
- 🚀 Mapas interactivos
- 🚀 Multi-idioma

## 🤝 Contribuir

1. Fork el proyecto
2. Crear feature branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Add: nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

Ver [guía de contribución](docs/CONTRIBUTING.md) para más detalles.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- Streamlit por simplificar las interfaces de datos
- La comunidad Python

---

⚠️ 0. Antes de actualizar a esta versión (IMPORTANTE)

Si ya habías trabajado con este proyecto antes, necesitas limpiar tu entorno local, porque:

Tu .uv/ puede tener versiones antiguas de GIS

Tu uv.lock podría contener paquetes que ya no existen

Las librerías GIS pueden haberse instalado incorrectamente en tu sistema

Cómo limpiar tu entorno uv local

En la raíz del proyecto:

rm -rf .uv uv.lock


Luego:

uv sync


Esto deja tu entorno totalmente limpio y sincronizado con el pyproject.toml actual.

✔ 1. Concepto clave (muy importante)

Todo lo que instales con:

uv pip install <paquete>


se instala solo en tu máquina, dentro de .uv/.

Eso significa:

No modifica pyproject.toml

No modifica uv.lock

No se comparte al repositorio

No afecta a otros integrantes del equipo

Cada persona tiene que instalar su propio entorno GIS solo una vez.

✔ 2. Instalación base (igual para todos)

Después de limpiar o clonar:

uv sync


Esto prepara el entorno base del proyecto (sin GIS).

🌍 3. Instalación GIS según sistema operativo
🍏 macOS (Intel / Apple Silicon)

Instalar GDAL nativo en el sistema:

brew install gdal


Instalar los bindings GIS en tu entorno uv:

uv pip install gdal geopandas pyproj rasterio shapely


Test:

uv run python api/tests/gdilcompar.py

🪟 Windows

⚠️ No modifiques el pyproject.toml.
⚠️ Todo lo que instales con uv pip es únicamente para tu entorno local.

Instalar GDAL precompilado (evita compilar C++):

uv pip install --index-url https://gisidx.github.io/gwi/simple gdal


Instalar librerías GIS:

uv pip install geopandas pyproj rasterio shapely


Test:

uv run python api/tests/gdilcompar.py

🐧 Linux (Ubuntu/Debian)

Instalar GDAL del sistema:

sudo apt-get update
sudo apt-get install -y gdal-bin libgdal-dev


Instalar GIS en tu entorno uv:

uv pip install geopandas pyproj rasterio shapely


Test:

uv run python api/tests/gdilcompar.py

✔ 4. Test universal del entorno GIS

El archivo:

api/tests/gdilcompar.py

from osgeo import gdal
import pyproj
import geopandas as gpd
import rasterio
import shapely

print("GDAL:", gdal.VersionInfo())
print("PyProj:", pyproj.__version__)
print("GeoPandas:", gpd.__version__)
print("Rasterio:", rasterio.__version__)
print("Shapely:", shapely.__version__)


Ejecutar:

uv run python api/tests/gdilcompar.py


Si imprime las versiones: tu entorno GIS está listo.


**Desarrollado con ❤️ para un futuro energético sostenible**