# 📚 Documentación Completa - Proyecto Atlas de Energía

## 🌍 Descripción General

**Atlas de Energía** es una aplicación web full-stack diseñada para visualizar y analizar datos energéticos por países. El proyecto está estructurado en una arquitectura de microservicios con:

- **Backend**: API REST construida con FastAPI (Python)
- **Frontend**: Interfaz web construida con Streamlit (Python)
- **Arquitectura**: Separación completa entre backend y frontend, comunicándose vía HTTP/REST

## 🏗️ Estructura del Proyecto

```
proyecto-atlas/
│
├── api/                    # Backend (FastAPI)
│   ├── app/               # Código principal de la API
│   │   ├── core/          # Configuración y utilidades centrales
│   │   ├── models/        # Modelos de datos (Pydantic)
│   │   ├── routers/       # Endpoints HTTP
│   │   ├── services/      # Lógica de negocio
│   │   └── data/          # Archivos de datos (CSV)
│   └── tests/             # Pruebas unitarias
│
├── app/                    # Frontend (Streamlit)
│   ├── components/        # Componentes reutilizables
│   ├── data/             # Datos del frontend
│   └── pages/            # Páginas adicionales
│
├── scripts/               # Scripts de utilidad
│
├── pyproject.toml         # Configuración del proyecto y dependencias
├── makefile              # Comandos de desarrollo
├── .gitignore            # Archivos ignorados por Git
├── .env.example          # Ejemplo de variables de entorno
└── create_atlas_structure.sh  # Script para crear estructura inicial
```

---

## 📁 Backend (FastAPI) - `/api`

### 🚀 **`api/app/main.py`**
**Función**: Punto de entrada principal de la API

```python
# Responsabilidades:
- Inicializar la aplicación FastAPI
- Configurar el sistema de logging
- Registrar todos los routers con sus prefijos
- Título: "Atlas Energía API"
- Prefijo base: /api
```

**Flujo de ejecución**:
1. Llama a `setup_logging()` para configurar logs
2. Crea instancia de FastAPI
3. Incluye router de países en `/api/paises`
4. Expone la aplicación como `app` para Uvicorn

---

### 📂 **Core** (`api/app/core/`)

#### **`config.py`**
**Función**: Centraliza toda la configuración de la API

```python
# Configuraciones:
- API_BASE_PATH: "/api" (prefijo para todas las rutas)
- DATA_DIR: Path absoluto a api/app/data/
- Lee variables de entorno desde .env
```

**Características**:
- Usa Pydantic BaseSettings para validación
- Carga automática de variables desde `.env`
- Paths calculados dinámicamente

#### **`logging.py`**
**Función**: Sistema de logging centralizado

```python
# Configuración de logs:
- Nivel: INFO por defecto
- Formato: timestamp | nivel | módulo | mensaje
- Salida: stdout (consola)
```

---

### 📊 **Models** (`api/app/models/`)

#### **`country.py`**
**Función**: Define esquemas de datos para países

```python
# Modelos Pydantic:

Country:
  - codigo: str  # Código ISO del país (ej: "MEX")
  - nombre: str  # Nombre completo (ej: "México")

CountryDetail (hereda de Country):
  - Preparado para expansión futura
  - Agregará: población, mix energético, etc.
```

**Propósito**: 
- Validación automática de datos
- Serialización JSON para la API
- Documentación automática en OpenAPI

---

### 🛣️ **Routers** (`api/app/routers/`)

#### **`countries.py`**
**Función**: Define endpoints HTTP para países

**Endpoints**:

1. **`GET /api/paises`**
   - Devuelve lista de todos los países
   - Response: `List[Country]`
   - Llama a: `list_countries()`

2. **`GET /api/paises/{codigo}/ficha`**
   - Obtiene ficha detallada de un país
   - Parámetro: código ISO (ej: "MEX")
   - Response: `CountryDetail`
   - Error 404 si no existe
   - Llama a: `get_country(codigo)`

---

### 💼 **Services** (`api/app/services/`)

#### **`countries_services.py`**
**Función**: Lógica de negocio para manejo de países

**Funciones**:

```python
list_countries() -> List[Country]
  - Lee archivo paises.csv
  - Parsea con csv.DictReader
  - Mapea columnas: CODIGO_PAIS → codigo, NOMBRE_PAIS → nombre
  - Retorna lista de objetos Country

get_country(codigo: str) -> Optional[CountryDetail]
  - Busca país por código (case-insensitive)
  - Retorna CountryDetail si existe
  - Retorna None si no se encuentra
```

**Nota**: Separa lógica de negocio de la capa HTTP

---

### 🧪 **Tests** (`api/tests/`)

#### **`test_countries.py`**
**Función**: Pruebas unitarias para endpoints

**Pruebas**:
1. `test_list_ok()`: Verifica que `/api/paises` devuelve lista
2. `test_ficha_404()`: Verifica error 404 para país inexistente

**Herramienta**: FastAPI TestClient para simular requests

---

## 🎨 Frontend (Streamlit) - `/app`

### 🏠 **`app/Home.py`**
**Función**: Página principal de la aplicación

**Flujo de la aplicación**:
1. **Configuración inicial**:
   - Título: "Atlas de Energía — Rebanada 1 (simple)"
   - Layout: wide (pantalla completa)

2. **Carga de datos**:
   - Solicita lista de países a `GET /api/paises`
   - Manejo de errores con try/except
   - Timeout de 10 segundos

3. **Interfaz de usuario**:
   - Selectbox con países (formato: "México (MEX)")
   - Al seleccionar, solicita ficha a `/api/paises/{codigo}/ficha`
   - Muestra nombre y código del país
   - Placeholder para futuras funcionalidades

**Estado**: Rebanada 1 (MVP básico)

### ⚙️ **`app/config.py`**
**Función**: Configuración del frontend

```python
# Variables:
API_BASE_URL: URL del backend (default: http://localhost:8000)
- Lee de variable de entorno
- Permite diferentes entornos (dev/prod)
```

---

## 🔧 Archivos de Configuración

### 📦 **`pyproject.toml`**
**Función**: Configuración del proyecto Python

**Contenido**:
- Nombre: gisaiproject v0.1.0
- Python: >=3.13
- **Dependencias principales**:
  - FastAPI (framework backend)
  - Streamlit (framework frontend)
  - Uvicorn (servidor ASGI)
  - Pandas (manejo de datos)
  - Pydantic (validación)
  - SQLAlchemy (preparado para DB)
  - Pytest (testing)
  - Mypy (type checking)
  - Ruff (linting)

### 🛠️ **`makefile`**
**Función**: Comandos de desarrollo simplificados

**Comandos**:
```bash
make api   # Inicia backend en puerto 8000 con hot-reload
make app   # Inicia frontend en puerto 8501
make test  # Ejecuta pruebas unitarias
```

**Características**:
- Crea venv automáticamente si no existe
- Activa entorno virtual
- Hot-reload para desarrollo

### 🚫 **`.gitignore`**
**Función**: Archivos excluidos del control de versiones

**Categorías principales**:
- Python: `__pycache__`, `.pyc`, venvs
- Entornos: `.env` (excepto `.env.example`)
- Bases de datos: `.db`, `.sqlite`
- Credenciales: `.json`, `.pem`, `.key`
- GIS: `.shp`, `.geojson`, archivos pesados
- IDEs: `.vscode`, `.history`
- Logs y caché

### 🔐 **`.env.example`**
**Función**: Plantilla de variables de entorno

```env
API_BASE_URL=http://localhost:8000
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_PORT=8501
```

**Uso**: Copiar a `.env` y configurar valores reales

### 📝 **`create_atlas_structure.sh`**
**Función**: Script Bash para crear estructura inicial

**Acciones**:
1. Crea toda la estructura de directorios
2. Muestra confirmación visual
3. Uso: `bash create_atlas_structure.sh`

---

## 🚀 Cómo Ejecutar el Proyecto

### 1. **Instalación**
```bash
# Clonar repositorio
git clone [repositorio]

# Crear estructura (si es necesario)
bash create_atlas_structure.sh

# Copiar configuración
cp .env.example .env

# Instalar dependencias
pip install -e .  # Con pyproject.toml
```

### 2. **Preparar Datos**
Crear archivo `api/app/data/paises.csv`:
```csv
CODIGO_PAIS,NOMBRE_PAIS
MEX,México
USA,Estados Unidos
CAN,Canadá
```

### 3. **Ejecutar Servicios**
```bash
# Terminal 1 - Backend
make api

# Terminal 2 - Frontend  
make app

# Terminal 3 - Tests (opcional)
make test
```

### 4. **Acceder a la Aplicación**
- Frontend: http://localhost:8501
- API Docs: http://localhost:8000/docs
- API: http://localhost:8000/api

---

## 📈 Estado del Proyecto

### ✅ **Implementado (Rebanada 1)**
- Estructura base del proyecto
- API REST funcional
- Carga y listado de países
- Selección de país en frontend
- Sistema de logging
- Pruebas básicas
- Configuración por entorno

### 🔄 **Próximos Pasos (Rebanada 2)**
Según los comentarios en el código:
- Agregar población a los países
- Implementar mix energético
- Expandir modelo `CountryDetail`
- Agregar visualizaciones de datos
- Integración con bases de datos
- Más páginas en Streamlit

### 🎯 **Futuras Mejoras Sugeridas**
- Dockerización
- CI/CD pipeline
- Autenticación/autorización
- Caché de datos
- WebSockets para actualizaciones en tiempo real
- Integración con datos GIS
- Dashboard interactivo

---

## 🏭 Arquitectura y Decisiones de Diseño

### **Separación de Responsabilidades**
- **Models**: Solo definición de datos
- **Services**: Lógica de negocio pura (sin HTTP)
- **Routers**: Solo manejo HTTP
- **Core**: Configuración y utilidades compartidas

### **Ventajas del Diseño Actual**
1. **Escalabilidad**: Backend y frontend independientes
2. **Mantenibilidad**: Código organizado por función
3. **Testabilidad**: Fácil de probar cada capa
4. **Flexibilidad**: Puede cambiar frontend sin tocar API
5. **Documentación**: Auto-documentación con FastAPI

### **Patrones Utilizados**
- **MVC adaptado**: Models, Services (Controllers), Routers (Views)
- **Dependency Injection**: Via FastAPI
- **Configuration as Code**: pyproject.toml, .env
- **Repository Pattern**: En services (preparado para DB)

---

## 📚 Recursos y Referencias

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Pytest Documentation](https://docs.pytest.org/)

---

## 👥 Contribución

Para contribuir al proyecto:
1. Seguir la estructura establecida
2. Agregar tests para nuevas funcionalidades
3. Documentar cambios significativos
4. Usar type hints en Python
5. Ejecutar linters antes de commit

---

*Documentación generada para el proyecto Atlas de Energía - Versión 0.1.0*