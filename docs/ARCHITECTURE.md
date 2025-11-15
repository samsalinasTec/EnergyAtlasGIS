# 🗺️ Atlas de Energía - Resumen Ejecutivo y Arquitectura

## 📋 Resumen Ejecutivo
## Hola Sami
**Atlas de Energía** es una plataforma web para visualización de datos energéticos globales, actualmente en su primera fase de desarrollo (MVP/Rebanada 1).

### 🎯 Objetivo del Proyecto
Crear un atlas interactivo que permita explorar y analizar datos energéticos por país, incluyendo consumo, producción y mix energético.

### 🔑 Características Clave
- **API REST** robusta y documentada automáticamente
- **Interfaz web** intuitiva y responsiva
- **Arquitectura escalable** preparada para crecimiento
- **Desarrollo iterativo** por "rebanadas" funcionales

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE (Browser)                        │
│                                                                   │
│                    http://localhost:8501                         │
└───────────────────┬──────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Home.py    │  │   Pages/     │  │ Components/  │          │
│  │              │  │              │  │              │          │
│  │  - Selector  │  │  (Futuras)   │  │ (Reutiliz.)  │          │
│  │  - Display   │  │              │  │              │          │
│  └──────┬───────┘  └──────────────┘  └──────────────┘          │
│         │                                                        │
│         │ HTTP Requests                                          │
└─────────┼────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                            │
│                                                                   │
│                    http://localhost:8000                         │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      ROUTERS                              │  │
│  │  /api/paises         /api/paises/{codigo}/ficha          │  │
│  └─────────────────────────┬─────────────────────────────────┘  │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                     SERVICES                              │  │
│  │  list_countries()    get_country()                       │  │
│  └─────────────────────────┬─────────────────────────────────┘  │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      MODELS                               │  │
│  │  Country             CountryDetail                        │  │
│  └─────────────────────────┬─────────────────────────────────┘  │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    DATA LAYER                             │  │
│  │                   paises.csv                              │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos

### Flujo Principal: Selección de País

```
Usuario                 Frontend              Backend               Data
   │                       │                     │                    │
   │  Accede a la app      │                     │                    │
   ├──────────────────────►│                     │                    │
   │                       │                     │                    │
   │                       │  GET /api/paises    │                    │
   │                       ├────────────────────►│                    │
   │                       │                     │                    │
   │                       │                     │  Lee paises.csv   │
   │                       │                     ├───────────────────►│
   │                       │                     │                    │
   │                       │                     │◄───────────────────┤
   │                       │                     │  Lista de países  │
   │                       │                     │                    │
   │                       │◄────────────────────┤                    │
   │                       │  JSON [{...}, ...]  │                    │
   │                       │                     │                    │
   │  Ve selector países   │                     │                    │
   │◄──────────────────────┤                     │                    │
   │                       │                     │                    │
   │  Selecciona "México"  │                     │                    │
   ├──────────────────────►│                     │                    │
   │                       │                     │                    │
   │                       │  GET /api/paises/   │                    │
   │                       │      MEX/ficha      │                    │
   │                       ├────────────────────►│                    │
   │                       │                     │                    │
   │                       │                     │  Busca MEX        │
   │                       │                     ├───────────────────►│
   │                       │                     │                    │
   │                       │                     │◄───────────────────┤
   │                       │                     │  Datos de México  │
   │                       │                     │                    │
   │                       │◄────────────────────┤                    │
   │                       │  JSON {ficha}       │                    │
   │                       │                     │                    │
   │  Ve info del país     │                     │                    │
   │◄──────────────────────┤                     │                    │
   │                       │                     │                    │
```

---

## 📦 Estructura de Módulos

### Backend - Responsabilidades por Capa

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                   │
│                                                          │
│  Routers:                                               │
│  • Manejo de HTTP requests/responses                    │
│  • Validación de parámetros de entrada                  │
│  • Serialización de respuestas                          │
│  • Manejo de códigos de estado HTTP                     │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    BUSINESS LAYER                       │
│                                                          │
│  Services:                                              │
│  • Lógica de negocio                                    │
│  • Procesamiento de datos                               │
│  • Reglas de validación de negocio                      │
│  • Transformaciones de datos                            │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│                      DATA LAYER                         │
│                                                          │
│  Models + Data Access:                                  │
│  • Definición de estructuras de datos                   │
│  • Acceso a archivos CSV                                │
│  • (Futuro) Acceso a base de datos                      │
│  • (Futuro) Caché de datos                              │
└──────────────────────────────────────────────────────────┘
```

---

## 🚦 Estado Actual vs Roadmap

### ✅ Fase 1: MVP Básico (ACTUAL)
```
[████████████████████] 100% Completado

✓ Estructura del proyecto
✓ API básica funcionando
✓ Frontend básico
✓ Listado de países
✓ Selección individual
✓ Tests básicos
```

### 🔄 Fase 2: Datos Energéticos
```
[██░░░░░░░░░░░░░░░░░░] 10% En desarrollo

○ Población por país
○ Mix energético (% renovable, fósil, nuclear)
○ Consumo per cápita
○ Tendencias históricas
○ Visualizaciones básicas
```

### 📊 Fase 3: Visualización Avanzada
```
[░░░░░░░░░░░░░░░░░░░░] 0% Planificado

○ Mapas interactivos
○ Gráficos comparativos
○ Análisis temporal
○ Exportación de datos
○ Dashboard personalizable
```

### 🌍 Fase 4: Funcionalidades GIS
```
[░░░░░░░░░░░░░░░░░░░░] 0% Futuro

○ Integración con datos geoespaciales
○ Mapas de calor
○ Análisis regional
○ Predicciones y proyecciones
○ API pública documentada
```

---

## 🛠️ Stack Tecnológico

### Backend
```
Python 3.13+
    │
    ├── FastAPI         → Framework web moderno y rápido
    ├── Pydantic        → Validación y serialización de datos
    ├── Uvicorn         → Servidor ASGI de alto rendimiento
    └── Pytest          → Framework de testing
```

### Frontend
```
Python 3.13+
    │
    ├── Streamlit       → Framework para apps de datos
    ├── Requests        → Cliente HTTP
    └── Pandas          → Manipulación de datos (futuro)
```

### Herramientas de Desarrollo
```
Desarrollo
    │
    ├── Make            → Automatización de tareas
    ├── Ruff            → Linting ultra-rápido
    ├── Mypy            → Type checking estático
    └── Python-dotenv   → Gestión de variables de entorno
```

---

## 💡 Decisiones de Diseño Clave

### 1. **Separación Frontend/Backend**
- **Razón**: Permite escalar independientemente
- **Beneficio**: Puede cambiar tecnología de frontend sin afectar API
- **Trade-off**: Mayor complejidad inicial

### 2. **Streamlit para Frontend**
- **Razón**: Desarrollo rápido de prototipos
- **Beneficio**: Código Python puro, sin JavaScript
- **Trade-off**: Menos control sobre UI personalizada

### 3. **CSV como Fuente de Datos Inicial**
- **Razón**: Simplicidad para MVP
- **Beneficio**: No requiere configuración de DB
- **Trade-off**: Limitaciones de rendimiento con datos grandes

### 4. **Estructura por Capas**
- **Razón**: Separación de responsabilidades
- **Beneficio**: Código mantenible y testeable
- **Trade-off**: Más archivos y carpetas

---

## 🔐 Consideraciones de Seguridad

### Actual
- Variables de entorno para configuración sensible
- Validación de entrada con Pydantic
- Timeout en requests HTTP

### Recomendaciones Futuras
- [ ] Implementar CORS adecuadamente
- [ ] Agregar rate limiting
- [ ] Autenticación JWT
- [ ] HTTPS en producción
- [ ] Sanitización de inputs
- [ ] Logs de auditoría

---

## 📈 Métricas de Calidad

### Cobertura Actual
```
Tests:          2/2 passing
Endpoints:      2 implementados
Models:         2 definidos
Services:       2 funciones
Type Hints:     100% del código
Documentation:  Inline + OpenAPI automática
```

### Objetivos de Calidad
- Cobertura de tests > 80%
- Response time < 200ms
- Uptime > 99.9%
- Zero security vulnerabilities

---

## 🚀 Quick Start para Desarrolladores

### Setup en 3 minutos:
```bash
# 1. Clonar y entrar al proyecto
git clone [repo] && cd atlas-energia

# 2. Configurar entorno
cp .env.example .env

# 3. Instalar y ejecutar
pip install -e .
make api  # Terminal 1
make app  # Terminal 2

# 4. Abrir en browser
# Frontend: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

---

## 📞 Puntos de Contacto

### Para Desarrollo:
- **API Health**: `GET http://localhost:8000/docs`
- **Frontend**: `http://localhost:8501`
- **Tests**: `make test`
- **Logs**: Consola (stdout)

### Para Producción (Futuro):
- Monitoring: (Por implementar)
- Alertas: (Por configurar)
- Backups: (Por definir)

---

*Arquitectura documentada - Atlas de Energía v0.1.0*
*Última actualización: Documentación inicial*