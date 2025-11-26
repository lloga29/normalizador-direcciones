# 🇨🇴 Normalización de Direcciones Colombianas

## ✅ Estado: COMPLETADO Y LISTO PARA PRODUCCIÓN

**Precisión:** 93.3% (28/30 casos correctos)

---

## 📋 Quick Start

### Opción 1: Procesar Excel
```bash
python normalizar_direcciones.py
```
- **Entrada:** `direcciones.xlsx`
- **Salida:** `direcciones_normalizadas.xlsx`

### Opción 2: Usar como módulo
```python
from normalizar_direcciones import standardize_address

resultado = standardize_address("Calle 123 #45-67")
print(resultado)  # "CL 123 45 67"
```

### Opción 3: Ejecutar pruebas
```bash
python test_completo.py
```

---

## 📊 Ejemplos de Normalización

| Entrada | Salida | Tipo |
|---------|--------|------|
| "Calle 123 #45-67" | "CL 123 45 67" | ✅ Procesa |
| "Cra 7 No. 34-56" | "KR 7 34 56" | ✅ Procesa |
| "123 456" | "123 456" | ✅ Procesa |
| "BOGOTA - Calle 50 # 10-20" | "CL 50 10 20" | ✅ Procesa |
| "Cra 7 apt 2" | "KR 7 2" | ✅ Limpia APTO |
| "10.123456 -74.654321" | "" | ❌ Rechaza GPS |
| "Vereda El Palmar" | "" | ❌ Rechaza (sin #) |
| "Información no disponible" | "" | ❌ Rechaza |

---

## 🎯 Formatos Aceptados

### Con tipo de vía:
```
[TIPO_VÍA] [NUM] [NUM] [NUM OPCIONAL]
```
**Ejemplos:** `CL 123 45 67`, `KR 7 34 56`, `AV 9 45 23`

### Sin tipo de vía (solo números):
```
[NUM] [NUM] [NUM OPCIONAL]
```
**Ejemplos:** `123 456`, `50 10 20`

---

## 🔤 Tipos de Vía Soportados

| Entrada | Salida |
|---------|--------|
| CALLE, CLL, CL | **CL** |
| CARRERA, CRA, KRA, KR | **KR** |
| AVENIDA, AV, AVD | **AV** |
| DIAGONAL, DG | **DG** |
| TRANSVERSAL, TV, TRANSV | **TV** |
| VEREDA, VDA, VIA, PASAJE | Se mantiene |

---

## 📚 Documentación

| Archivo | Contenido |
|---------|----------|
| `RESUMEN_FINAL.txt` | 📄 Resumen ejecutivo |
| `GUIA_REGLAS.txt` | 📖 Guía completa de reglas |
| `INFORME_FINAL.txt` | 📊 Informe técnico detallado |
| `INDEX.txt` | 🗂️ Índice de archivos |
| `RESUMEN_VISUAL.txt` | 📈 Resumen visual |

---

## ✨ Características

✅ Normaliza tipos de vía a abreviaturas estándar  
✅ Limpia descriptivos (APTO, PISO, PISO, etc.)  
✅ Elimina ciudades del texto  
✅ Rechaza coordenadas GPS automáticamente  
✅ Maneja símbolos y espacios extras  
✅ Valida presencia de números  
✅ Procesa archivos Excel  
✅ Documentación completa  

---

## 🔧 Requisitos

```bash
pip install pandas openpyxl
```

---

## 📞 Soporte

**Problema:** No procesa el archivo Excel  
**Solución:** Verificar que `direcciones.xlsx` esté en el directorio y tenga columna "Direccion"

**Problema:** Columna tiene otro nombre  
**Solución:** Editar `normalizar_direcciones.py` línea 132

```python
column_name = "Nombre_de_tu_columna"
```

---

## 🚀 Próximos Pasos

1. ✅ Leer: `RESUMEN_FINAL.txt`
2. ✅ Consultar: `GUIA_REGLAS.txt`
3. ✅ Probar: `python test_completo.py`
4. ✅ Procesar: `python normalizar_direcciones.py`

---

**Proyecto:** Normalización de Direcciones Colombianas  
**Precisión:** 93.3%  
**Estado:** ✅ LISTO PARA PRODUCCIÓN  
**Última actualización:** 26 de Noviembre de 2025
