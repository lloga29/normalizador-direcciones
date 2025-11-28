# Normalizador de Direcciones Colombianas

Sistema avanzado de normalización y estandarización de direcciones colombianas a formato estructurado.

## 📊 Resultados

- **Tasa de éxito**: 81.3% (28,290 de 34,814 direcciones procesadas)
- **Mejora total**: +3.3% desde el inicio (de 78.0% a 81.3%)
- **Direcciones procesadas**: +1,143 direcciones adicionales

## 🎯 Características Principales

### Normalización Estándar
- Convierte direcciones a formato: `TIPO NUM NUM [NUM]`
- Ejemplos:
  - `CALLE 72 NO 10 34` → `CL 72 10 34`
  - `CARRERA 15 # 85 - 23` → `KR 15 85 23`
  - `AV BOYACA 144 B 75` → `AV 144 B 75`

### Handlers Especiales

#### 1. AEROPUERTO
Mantiene el nombre completo del aeropuerto, eliminando ciudades y complementos:
- `BOGOTA AEROPUERTO EL DORADO LOCAL 259` → `AEROPUERTO EL DORADO`
- `SOLEDAD AEREOPUERTO ERNESTO CORTIZZOS MUELLE 2` → `AEROPUERTO ERNESTO CORTIZZOS`

#### 2. VIA (Carreteras)
Preserva la descripción completa de vías y carreteras:
- `VIA ARMENIA MONTENEGRO KM 5 LOCAL 3` → `VIA ARMENIA MONTENEGRO KM 5`
- `YUMBO VIA CALI PALMIRA BODEGA 45` → `VIA CALI PALMIRA`

#### 3. AUTOPISTA
Normaliza autopistas con sus variantes:
- `BOGOTA AUTOPISTA NORTE KM 5` → `AUTOPISTA NORTE KM 5`
- `AUTONORTE 145 23` → `AUTOPISTA NORTE 145 23`

#### 4. KM VIA
Direcciones con kilómetros:
- `KM 18 VIA SIBERIA` → `KM 18 VIA SIBERIA`
- `KILOMETRO 5 CARRERA 45` → `KM 5 KR 45`

### Limpieza Inteligente

- ✅ Elimina coordenadas GPS y procesa dirección válida restante
- ✅ Elimina números de teléfono (7+ dígitos)
- ✅ Elimina palabras descriptivas (LOCAL, OFICINA, BODEGA, etc.)
- ✅ Elimina ciudades y departamentos
- ✅ Normaliza errores tipográficos (AENIDA → AVENIDA, AEREOPUERTO → AEROPUERTO)

### Procesamiento Avanzado

- ✅ Separa tipos de vía pegados: `AVCL` → `AV CL`
- ✅ Separa números con letras: `CR77MSUR` → `CR 77M SUR`
- ✅ Distingue N (número) de NORTE (cardinal)
- ✅ Maneja direcciones con 1 a 4 componentes numéricos
- ✅ Procesa direcciones con nombres de calles: `AV CIRCUNVALAR 45 23` → `AV 45 23`

## 🚀 Uso

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/lloga29/normalizador-direcciones.git
cd normalizador-direcciones

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecución

```bash
python normalizar_direcciones.py
```

### Entrada y Salida

- **Archivo de entrada**: `Nits_ciudad.xlsx`
  - Debe contener una columna llamada `Direccion`
- **Archivo de salida**: `Nits_ciudad_normalizadas.xlsx`
  - Incluye columna adicional: `Direccion Estandarizada`

## 📋 Requisitos

- Python 3.8+
- pandas >= 2.0.0
- openpyxl >= 3.1.0

## 📖 Documentación Adicional

- **REGLAS_NORMALIZACION.md**: Documentación completa de todas las reglas aplicadas
- **normalizar_direcciones.py**: Código fuente con comentarios detallados

## 🔧 Estructura del Proyecto

```
normalizador-direcciones/
├── normalizar_direcciones.py    # Script principal
├── requirements.txt              # Dependencias
├── README.md                     # Este archivo
├── REGLAS_NORMALIZACION.md      # Documentación de reglas
├── Nits_ciudad.xlsx             # Archivo de entrada (ejemplo)
└── Nits_ciudad_normalizadas.xlsx # Archivo de salida
```

## 📈 Estadísticas de Procesamiento

### Distribución de Casos Procesados
- Direcciones estándar (CL/KR/AV + números): ~85%
- AEROPUERTO: ~0.4%
- VIA (carreteras): ~2.5%
- AUTOPISTA: ~1.2%
- KM VIA: ~0.5%
- Otros patrones: ~10.4%

### Casos No Procesados (18.7%)
- Sin números o inválidos: ~14.8%
- Direcciones incompletas: ~2.5%
- Formatos no estándar: ~1.4%

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👥 Autores

- **lloga29** - Desarrollo y mantenimiento

## 📧 Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio de GitHub.
