# Reglas de Normalización de Direcciones

Documentación completa de todas las reglas implementadas en el sistema de normalización de direcciones colombianas.

## Tabla de Contenidos

1. [Formato de Salida](#formato-de-salida)
2. [Normalización de Tipos de Vía](#normalización-de-tipos-de-vía)
3. [Handlers Especiales](#handlers-especiales)
4. [Limpieza y Preprocesamiento](#limpieza-y-preprocesamiento)
5. [Patrones de Normalización](#patrones-de-normalización)
6. [Listas de Control](#listas-de-control)

---

## Formato de Salida

### Formato Estándar
```
TIPO NUM [CARDINAL] [NUM] [NUM] [NUM]
```

Donde:
- **TIPO**: Tipo de vía normalizado (CL, KR, AV, TV, DG, etc.)
- **NUM**: Componentes numéricos (1 a 4 números)
- **CARDINAL**: Direcciones cardinales (NORTE, SUR, ESTE, OESTE, BIS) - Opcional

### Ejemplos
```
Entrada: CALLE 72 NO 10 - 34
Salida:  CL 72 10 34

Entrada: CARRERA 15 SUR # 85 - 23
Salida:  KR 15 SUR 85 23

Entrada: AV BOYACA 144 B 75
Salida:  AV 144 B 75

Entrada: DIAGONAL 77 B SUR 32 15
Salida:  DG 77 BIS SUR 32 15
```

---

## Normalización de Tipos de Vía

### Función: `normalize_via_type()`

#### CALLE → CL
Variantes reconocidas:
- CALLE, CLL, CL, CALL, AC, ACL

#### CARRERA → KR
Variantes reconocidas:
- CARRERA, CRA, KRA, KR, CARR, AK, K, ACR

#### AVENIDA → AV
Variantes reconocidas:
- AVENIDA, AENIDA (error tipográfico), AV, AVD, AVDA, AVE

#### TRANSVERSAL → TV
Variantes reconocidas:
- TRANSVERSAL, TRANSV, TV, TR

#### DIAGONAL → DG
Variantes reconocidas:
- DIAGONAL, DIAG, DG

#### CIRCUNVALAR → CIRC
Variantes reconocidas:
- CIRCUNVALAR, CIRCUNV, CIRC

#### Casos especiales
```python
# Mantener sin cambios:
- VIA (para carreteras)
- AUTOPISTA
- KM (kilómetros)
```

---

## Handlers Especiales

### 1. Eliminación de Coordenadas GPS

**Prioridad**: Primera operación

**Patrones eliminados**:
```regex
\b\d+\.\d{5,}\b           # Números con 5+ decimales
\b\d+\.\d+\s*[NSEOW]\b    # Coordenadas con dirección cardinal
```

**Ejemplos**:
```
Entrada: 7.06998 N13.11502 O CALLE 158 NO 18 78 LOCAL 2
Salida:  CL 158 18 78

Entrada: 4.12345 -74.56789 CARRERA 50 45 23
Salida:  KR 50 45 23
```

### 2. AEROPUERTO Handler

**Condición de activación**: Palabra "AEROPUERTO" o "AEREOPUERTO"

**Reglas aplicadas**:
1. Normalizar tipografía: AEREOPUERTO → AEROPUERTO
2. Eliminar ciudad al inicio (139 ciudades conocidas)
3. Mantener nombre completo del aeropuerto
4. Eliminar complementos: LOCAL, MUELLE, PISO, BODEGA, HANGAR, OFICINA, SALA, TERMINAL

**Ejemplos**:
```
Entrada: BOGOTA AEROPUERTO EL DORADO MUELLE 2
Salida:  AEROPUERTO EL DORADO

Entrada: SOLEDAD AEREOPUERTO ERNESTO CORTIZZOS LOCAL 259
Salida:  AEROPUERTO ERNESTO CORTIZZOS

Entrada: RIONEGRO AEROPUERTO JOSE MARIA CORDOVA TERMINAL 1 OFICINA 45
Salida:  AEROPUERTO JOSE MARIA CORDOVA
```

**Impacto**: +131 direcciones procesadas

### 3. VIA Handler (Carreteras)

**Condición de activación**: Palabra "VIA" (case-insensitive)

**Reglas aplicadas**:
1. Eliminar ciudad al inicio (139 ciudades conocidas)
2. Mantener descripción completa de la vía
3. Eliminar complementos: LOCAL, LOCALES, PISO, BODEGA, LOTE, SECTOR, COORDENADAS, UBICADO

**Ejemplos**:
```
Entrada: VIA ARMENIA MONTENEGRO KM 5 LOCAL 3
Salida:  VIA ARMENIA MONTENEGRO KM 5

Entrada: YUMBO VIA CALI PALMIRA BODEGA 45
Salida:  VIA CALI PALMIRA

Entrada: CAJICA VIA ZIPAQUIRA SECTOR INDUSTRIAL
Salida:  VIA ZIPAQUIRA

Entrada: VIA 40 NO 30 178 LOCAL 204
Salida:  VIA 40 30 178
```

**Validación**: Longitud mínima > 3 caracteres (evita retornar solo "VIA")

**Impacto**: +645 direcciones procesadas (mayor mejora individual)

### 4. AUTOPISTA Handler

**Condición de activación**: Palabras "AUTOPISTA", "AUT", "AUTO", "AUTONORTE"

**Reglas aplicadas**:
1. Normalizar variantes: AUT/AUTO → AUTOPISTA
2. Separar "AUTONORTE" → "AUTOPISTA NORTE"
3. Eliminar ciudad al inicio
4. Extraer nombre de autopista (1-3 palabras)
5. Capturar KM si existe
6. Capturar tipo de vía adicional si existe (CL, KR, etc.)

**Formato de salida**:
```
AUTOPISTA {NOMBRE} [KM {num}] [{tipo}]
```

**Ejemplos**:
```
Entrada: BOGOTA AUTOPISTA NORTE KM 5
Salida:  AUTOPISTA NORTE KM 5

Entrada: AUTONORTE 145 23
Salida:  AUTOPISTA NORTE 145 23

Entrada: MEDELLIN AUT SUR KM 12 CL 45
Salida:  AUTOPISTA SUR KM 12 CL 45

Entrada: AUTO MEDELLIN BOGOTA KM 23
Salida:  AUTOPISTA MEDELLIN BOGOTA KM 23
```

### 5. KM VIA Handler

**Condición de activación**: Comienza con "KM" o "KILOMETRO"

**Reglas aplicadas**:
1. Normalizar: KILOMETRO → KM
2. Capturar número de kilómetro
3. Procesar resto de la dirección normalmente

**Ejemplos**:
```
Entrada: KM 18 VIA SIBERIA
Salida:  KM 18 VIA SIBERIA

Entrada: KILOMETRO 5 CARRERA 45 NO 23 15
Salida:  KM 5 KR 45 23 15

Entrada: KM 7 AUTOPISTA MEDELLIN
Salida:  KM 7 AUTOPISTA MEDELLIN
```

---

## Limpieza y Preprocesamiento

### 1. Eliminación de N entre Números

**Problema**: Distinguir N (número) de NORTE (cardinal)

**Regla**: Solo NORTE, NOR, NORT son cardinales. N, S, E, O individuales se eliminan entre números.

**Patrón**:
```regex
\b([0-9]+)\s+([NSEO])\s+([0-9]+)\b  →  \1 \3
```

**Ejemplos**:
```
Entrada: AK 72 N 80 94
Salida:  AK 72 80 94  (N eliminada)

Entrada: CL 72 NORTE 10 34
Salida:  CL 72 NORTE 10 34  (NORTE se mantiene)

Entrada: KR 15 S 85 23
Salida:  KR 15 85 23  (S eliminada)
```

### 2. Eliminación de Teléfonos

**Patrón**:
```regex
\b\d{7,}\b  # Secuencias de 7 o más dígitos
```

**Ejemplos**:
```
Entrada: CL 72 10 34 TEL 3001234567
Salida:  CL 72 10 34

Entrada: CARRERA 15 85 2345678
Salida:  KR 15 85
```

**Impacto**: Parte de la mejora de +218 direcciones

### 3. Separación de Tipos Pegados

**Patrones**:
```regex
(AV|AK|CR|CL|KR|TV|DG)(CL|CR|KR|AV|AK)  →  \1 \2
```

**Ejemplos**:
```
Entrada: AVCL 72 10 34
Salida:  AV CL 72 10 34

Entrada: CR77 45 23
Salida:  CR 77 45 23

Entrada: AKCL 15 85
Salida:  AK CL 15 85
```

### 4. Separación de Letras y Números

**Patrón**:
```regex
(\d+[A-Z])(\d)  →  \1 \2
```

**Ejemplos**:
```
Entrada: CL 5B3 45
Salida:  CL 5B 3 45

Entrada: KR 15A61
Salida:  KR 15A 61

Entrada: AV 144B75
Salida:  AV 144B 75
```

### 5. Separación de Cardinales Pegados

**Patrón**:
```regex
(\d+[A-Z])(NORTE|SUR|ESTE|OESTE)  →  \1 \2
```

**Ejemplos**:
```
Entrada: CL 77MSUR 32 15
Salida:  CL 77M SUR 32 15

Entrada: KR 45ANORTE 23
Salida:  KR 45A NORTE 23
```

### 6. Normalización B SUR → BIS SUR

**Patrón**:
```regex
\b(\d+)B\s+SUR\b  →  \1 BIS SUR
```

**Ejemplos**:
```
Entrada: CL 32B SUR 15 23
Salida:  CL 32 BIS SUR 15 23

Entrada: KR 45B SUR 67
Salida:  KR 45 BIS SUR 67
```

### 7. Eliminación de Símbolos

**Símbolos removidos**: `# - , ; . ( )`

**Ejemplos**:
```
Entrada: CL 72 #10-34
Salida:  CL 72 10 34

Entrada: KR 15, No. 85-23
Salida:  KR 15 85 23

Entrada: AV 144 (B) - 75
Salida:  AV 144 B 75
```

---

## Patrones de Normalización

### Patrón 1: Con Nombre de Calle

**Estructura**:
```
TIPO + NOMBRE(1-3 palabras) + NUM [CARDINAL] NUM [NUM] [NUM]
```

**Regex**:
```regex
\b(CL|KR|AV|TV|DG|CIRC)\s+([A-Z]+(?:\s+[A-Z]+){0,2})\s+(\d+[A-Z]?)\s+(?:(NORTE|SUR|ESTE|OESTE|BIS)\s+)?(\d+)\s*(\d+)?\s*(\d+)?
```

**Ejemplos**:
```
Entrada: AV CIRCUNVALAR 45 23
Salida:  AV CIRCUNVALAR 45 23

Entrada: CL LAS AMERICAS 72 10 34
Salida:  CL LAS AMERICAS 72 10 34

Entrada: KR BOLIVAR SUR 15 85 23
Salida:  KR BOLIVAR SUR 15 85 23
```

### Patrón 2: Estándar con Tipo

**Estructura**:
```
TIPO + NUM [CARDINAL] [NUM] [NUM] [NUM]
```

**Regex**:
```regex
\b(CL|KR|AV|TV|DG|CIRC)\s+(\d+[A-Z]?)\s+(?:(NORTE|SUR|ESTE|OESTE|BIS)\s+)?(\d+)?\s*(\d+)?\s*(\d+)?
```

**Ejemplos**:
```
Entrada: CL 72 10 34
Salida:  CL 72 10 34

Entrada: KR 15 SUR 85 23
Salida:  KR 15 SUR 85 23

Entrada: AV 144 B 75
Salida:  AV 144 B 75

Entrada: DG 77 BIS SUR 32 15 98
Salida:  DG 77 BIS SUR 32 15 98
```

### Soporte de Números Variables

El sistema soporta direcciones con 1 a 4 componentes numéricos:

**1 número**:
```
CL 72  →  CL 72
```

**2 números**:
```
CL 72 10  →  CL 72 10
```

**3 números** (más común):
```
CL 72 10 34  →  CL 72 10 34
```

**4 números**:
```
DG 77 BIS SUR 32 15 98  →  DG 77 BIS SUR 32 15 98
```

---

## Listas de Control

### Lista de Palabras Descriptivas (Eliminadas)

**Total**: ~150 palabras

**Categorías principales**:

#### Complementos de Ubicación
```
LOCAL, LOCALES, LOC, OFICINA, OF, OFC, OFI, BODEGA, BOD, PISO, MEZZANINE, 
PLANTA, PLATAFORMA, MUELLE, HANGAR, SALON, SALA, TERMINAL
```

#### Sectores y Zonas
```
SECTOR, LOTE, INTERIOR, INT, APARTAMENTO, APTO, CASA, CONJUNTO, CONJ, 
EDIFICIO, EDIF, ED, TORRE, TO, BLOQUE, BLQ, ETAPA, MANZANA, MZ, PARQUE, 
ZONA, FRANCA, COMPLEJO, INDUSTRIAL, LOGISTICO, PARQUEADERO, ENTRADA
```

#### Ubicación Relativa
```
ESQUINA, ESQ, POR, CON, ENTRE, FRENTE, AL, LADO, COSTADO, DETRAS, 
UBICADO, SITUADA, CONTIGUO
```

#### Instituciones y Comercios
```
CENTRO, COMERCIAL, CC, CENTRO COM, MALL, PLAZA, MULTIPLAZA, GALERIA, 
MERCADO, SUPERMERCADO, ALMACEN, TIENDA, FINCA, HACIENDA, GRANJA, 
PARCELA, FUNDO, PREDIO, PROPIEDAD
```

#### Vías y Transporte
```
VIA, RUTA, CAMINO, VEREDA, SENDERO, ACCESO, ENTRADA, SALIDA, PUENTE, 
PUERTA, PTA, GLORIETA, ROTONDA, PEAJE
```

#### Coordenadas y Referencias
```
COORDENADAS, GPS, LATITUD, LAT, LONGITUD, LONG, LNG
```

#### Adjetivos y Cualificadores
```
PRINCIPAL, PPAL, ANTIGUO, ANTIGUA, ANT, NUEVO, NUEVA, VIEJO, VIEJA, 
ALTO, ALTA, BAJO, BAJA, GRANDE, PEQUENO
```

#### Nombres de Lugares Comunes
```
DORADO, AMERICAS, BOLIVAR, MULTIPLAZA, ROSITA, BURBUJA, TAQUILLA, 
FONTIBON, CANAIMA, TESORO, OVIEDO, UNICENTRO, SANTAFE, HACIENDA
```

#### Administrativo
```
SEDE, SUCURSAL, ADM, ADMINISTRACION, DIRECCION, DIR, GERENCIA, 
RECEPCION, PORTERIA
```

### Lista de Ciudades (139 ciudades)

**Ciudades principales**:
```
ACACIAS, AGUACHICA, ANAPOIMA, APARTADO, ARAUCA, ARMENIA, BARANOA, 
BARRANQUILLA, BELLO, BOGOTA, BUCARAMANGA, BUENAVENTURA, BUGA, 
CAJICA, CALI, CARTAGENA, CAUCASIA, CHIA, CHIQUINQUIRA, CIENAGA, 
COPACABANA, CUCUTA, DOSQUEBRADAS, DUITAMA, ENVIGADO, FACATATIVA, 
FLORIDABLANCA, FLORENCIA, FUNZA, FUSAGASUGA, GIRADOT, IBAGUE, 
IPIALES, ITAGUI, JAMUNDI, LA CEJA, LA DORADA, LA ESTRELLA, LORICA, 
MADRID, MAGANGUE, MAICAO, MALAMBO, MANIZALES, MANIZALEZ, MEDELLIN, 
MELGAR, MOCOA, MONTERIA, MOSQUERA, NEIVA, PASTO, PEREIRA, PIEDECUESTA, 
PITALITO, POPAYAN, PUERTO ASIS, PUERTO COLOMBIA, RIOHACHA, RIONEGRO, 
SABANALARGA, SABANETA, SAHAGÚN, SAN ANDRES, SANTA MARTA, SANTA ROSA DE CABAL, 
SANTANDER DE QUILICHAO, SINCELEJO, SOACHA, SOGAMOSO, SOLEDAD, 
SOPÓ, TECHO, TULUÁ, TUMACO, TUNJA, TURBO, VALLEDUPAR, VILLA DEL ROSARIO, 
VILLAVICENCIO, YOPAL, YUMBO, ZIPAQUIRA
```

**Correcciones incluidas**:
- MANIZALEZ → Reconocida como variante de MANIZALES
- YOPAL → Agregada

### Lista de Departamentos (6 departamentos)

Agregados para eliminar cuando aparecen en direcciones:
```
ANTIOQUIA, ATLANTICO, CUNDINAMARCA, VALLE, SANTANDER, CASANARE
```

**Ejemplo**:
```
Entrada: ANTIOQUIA MEDELLIN CL 72 10 34
Salida:  CL 72 10 34
```

### Direcciones Cardinales

**Completas** (se mantienen):
```
NORTE, NOR, NORT, SUR, ESTE, OESTE, BIS
```

**Abreviadas** (se eliminan entre números):
```
N, S, E, O  # Solo cuando están entre dos números
```

---

## Orden de Aplicación de Reglas

### Fase 1: Preprocesamiento Inicial
1. Convertir a mayúsculas
2. Normalizar espacios múltiples
3. Normalizar errores tipográficos comunes (AEREOPUERTO)

### Fase 2: Eliminación de Ruido
1. Eliminar coordenadas GPS (5+ decimales)
2. Eliminar teléfonos (7+ dígitos)
3. Eliminar símbolos (#, -, ,, ;, ., (, ))

### Fase 3: Handlers Especiales (en orden)
1. **AEROPUERTO** (si contiene "AEROPUERTO")
2. **VIA** (si contiene "VIA")
3. **AUTOPISTA** (si contiene "AUTOPISTA/AUT/AUTO/AUTONORTE")
4. **KM VIA** (si comienza con "KM" o "KILOMETRO")

### Fase 4: Normalización de Patrones
1. Separar tipos pegados (AVCL → AV CL)
2. Separar letras y números (5B3 → 5B 3)
3. Separar cardinales pegados (77MSUR → 77M SUR)
4. Normalizar B SUR → BIS SUR
5. Eliminar N entre números

### Fase 5: Eliminación de Descriptivos
1. Eliminar palabras descriptivas (~150 palabras)
2. Eliminar nombres de ciudades (139 ciudades)
3. Eliminar nombres de departamentos (6 departamentos)

### Fase 6: Aplicación de Patrones
1. Intentar patrón con nombre de calle
2. Si falla, intentar patrón estándar con tipo
3. Normalizar tipo de vía con `normalize_via_type()`

### Fase 7: Validación Final
1. Verificar que tenga al menos un número
2. Verificar longitud mínima (>3 caracteres)
3. Retornar dirección normalizada

---

## Métricas de Impacto

### Mejoras por Regla

| Regla/Handler | Direcciones Recuperadas | % Mejora |
|--------------|------------------------|----------|
| VIA Handler | +645 | +1.9% |
| Pattern Improvements | +218 | +0.6% |
| AEROPUERTO Handler | +131 | +0.4% |
| Complete City List | +118 | +0.3% |
| N vs NORTE | +31 | +0.1% |
| **TOTAL** | **+1,143** | **+3.3%** |

### Distribución Final

- **Direcciones procesadas**: 28,290 (81.3%)
- **Direcciones no procesadas**: 6,524 (18.7%)
- **Total**: 34,814 direcciones

### Tipos de Direcciones Procesadas

- Estándar (CL/KR/AV + números): ~85%
- VIA (carreteras): ~2.5%
- AUTOPISTA: ~1.2%
- AEROPUERTO: ~0.4%
- KM VIA: ~0.5%
- Otros patrones: ~10.4%

---

## Casos Especiales Documentados

### 1. GPS + Dirección Válida
```
Entrada: 7.06998 N13.11502 O CALLE 158 NO 18 78 LOCAL 2
Proceso: Eliminar GPS → Procesar dirección restante
Salida:  CL 158 18 78
```

### 2. Dirección con Nombre de Calle
```
Entrada: AV CIRCUNVALAR 45 23 OFICINA 302
Proceso: Reconocer nombre → Eliminar OFICINA → Normalizar
Salida:  AV CIRCUNVALAR 45 23
```

### 3. Tipos Pegados con Cardinal
```
Entrada: CR77MSUR 32 15
Proceso: CR77 → CR 77, 77MSUR → 77M SUR
Salida:  CR 77M SUR 32 15
```

### 4. VIA con Número Inicial
```
Entrada: VIA 40 NO 30 178 LOCAL 204
Proceso: Detectar VIA → Procesar números → Eliminar LOCAL
Salida:  VIA 40 30 178
```

### 5. AUTOPISTA Pegada
```
Entrada: AUTONORTE 145 23 OFICINA 5
Proceso: AUTONORTE → AUTOPISTA NORTE, eliminar OFICINA
Salida:  AUTOPISTA NORTE 145 23
```

---

## Notas de Implementación

### Orden Crítico
- GPS debe eliminarse ANTES que otros handlers
- Handlers especiales ANTES de patrones estándar
- Separación de pegados ANTES de normalización de tipo

### Validaciones Importantes
- VIA handler: longitud > 3 para evitar retornar solo "VIA"
- Números: al menos 1 número en resultado final
- Longitud: mínimo 3 caracteres para dirección válida

### Casos No Procesados Conocidos
- Direcciones con solo ciudad (sin número)
- Correos electrónicos
- URLs
- Direcciones con un solo número
- Formatos completamente no estándar

---

**Versión del documento**: 1.0  
**Última actualización**: Diciembre 2024  
**Tasa de éxito actual**: 81.3%

## Actualizacion 2025-11
- Refactor del pipeline: etapas separadas (prelimpia, handlers especiales, limpieza general, patrones) y regex compiladas reutilizables.
- Nuevos tipos: variantes CIRCULAR/CIRCUNVALAR normalizan a CIRC; se reconoce BIS como cardinal en patrones principales.
- Handler de AUTOPISTA detecta AUTO/AUT/AUTOPISTA en cualquier posicion, conserva KM y procesa el tramo restante con el parser general.
- Limpieza elimina NO/NR/NUM antes de parsear, reduciendo falsos negativos; se preservan nombres de calle en la salida (ej.: AV CIRCUNVALAR 45 23).
- La columna "Direccion Estandarizada" se sobrescribe con aviso en consola; considera hacer copia si necesitas conservar valores previos.
