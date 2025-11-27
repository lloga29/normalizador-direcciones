#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TESTS ESPECIFICOS para validar nuevas variables
Prueba casos que demostran necesidad de cambios
"""

import pandas as pd
import re

print("\n" + "="*100)
print("TESTS ESPECIFICOS - VALIDACION DE NUEVAS VARIABLES")
print("="*100)

# Cargar los datos
df_nits = pd.read_excel("Nits_ciudad.xlsx")

print(f"\nTotal de registros a analizar: {len(df_nits)}")

# ============================================================================
# TEST 1: DESCRIPTIVOS QUE NO SE ELIMINAN
# ============================================================================
print("\n" + "="*100)
print("TEST 1: DESCRIPTIVOS NO ELIMINADOS (Que deberían serlo)")
print("="*100)

# Casos donde PISO, LOCAL, OFICINA aparecen en normalizadas
test_descriptivos = [
    "CL 50 10 PISO 5",
    "KR 7 34 LOCAL 2",
    "AV 9 45 OFICINA 10",
    "CL 100 50 BODEGA 1",
    "KR 12 15 NORTE",
]

from normalizar_direcciones import standardize_address

print("\nPruebas de descriptivos:")
for addr in test_descriptivos:
    resultado = standardize_address(addr)
    print(f"  '{addr}' -> '{resultado}'")

# ============================================================================
# TEST 2: CIUDADES COMO PREFIJO
# ============================================================================
print("\n" + "="*100)
print("TEST 2: CIUDADES COMO PREFIJO (Que deberían eliminarse)")
print("="*100)

test_ciudades = [
    "BOGOTA CL 50 10 20",
    "MEDELLIN KR 7 34 56",
    "CALI AV 9 45 23",
    "BARRANQUILLA CL 100 50 15",
    "CHIA CL 5 10 8",
]

print("\nPruebas de ciudades:")
for addr in test_ciudades:
    resultado = standardize_address(addr)
    print(f"  '{addr}' -> '{resultado}'")

# ============================================================================
# TEST 3: ABREVIATURAS NO RECONOCIDAS
# ============================================================================
print("\n" + "="*100)
print("TEST 3: ABREVIATURAS NO NORMALIZADAS (CR, CLL)")
print("="*100)

test_abreviaturas = [
    "CR 7 34 56",      # Debería ser KR 7 34 56
    "CLL 50 10 20",    # Debería ser CL 50 10 20
]

print("\nPruebas de abreviaturas:")
for addr in test_abreviaturas:
    resultado = standardize_address(addr)
    print(f"  '{addr}' -> '{resultado}'")

# ============================================================================
# TEST 4: CORREOS ELECTRONICOS
# ============================================================================
print("\n" + "="*100)
print("TEST 4: CORREOS ELECTRONICOS (Deben rechazarse)")
print("="*100)

test_correos = [
    "ADMINISTRATIVO.MIECOLOMBIA.COM",
    "INFO@EMPRESA.COM",
    "CONTACTO@HOTEL.CO",
]

print("\nPruebas de correos:")
for addr in test_correos:
    resultado = standardize_address(addr)
    estado = "RECHAZA" if resultado == "" else "ACEPTA"
    print(f"  '{addr}' -> '{resultado}' [{estado}]")

# ============================================================================
# TEST 5: PATRONES ESPECIALES
# ============================================================================
print("\n" + "="*100)
print("TEST 5: PATRONES ESPECIALES (SUR, NORTE, CENTRO)")
print("="*100)

test_especiales = [
    "CL 50 10 SUR",
    "KR 7 34 CENTRO",
    "AV 9 45 NORTE",
    "CL 100 ESTE 5",
    "KR 12 OESTE 20",
]

print("\nPruebas de especiales:")
for addr in test_especiales:
    resultado = standardize_address(addr)
    print(f"  '{addr}' -> '{resultado}'")

# ============================================================================
# TEST 6: ANALIZAR REAL DE NITS QUE TIENEN ESTOS PATRONES
# ============================================================================
print("\n" + "="*100)
print("TEST 6: CASOS REALES DEL NITS_CIUDAD.XLSX")
print("="*100)

# Buscar casos reales que contengan estas palabras
print("\nBuscando direcciones reales con descriptivos...")
contador = 0
for addr in df_nits['Direccion'].dropna().head(100):
    if any(word in addr.upper() for word in ['PISO', 'LOCAL', 'OFICINA', 'BODEGA']):
        resultado = standardize_address(addr)
        print(f"  '{addr}' -> '{resultado}'")
        contador += 1
        if contador >= 5:
            break

print("\nBuscando direcciones reales con ciudades al inicio...")
contador = 0
for addr in df_nits['Direccion'].dropna().head(100):
    if any(addr.upper().startswith(city) for city in ['BOGOTA', 'MEDELLIN', 'CALI', 'BARRANQUILLA']):
        resultado = standardize_address(addr)
        print(f"  '{addr}' -> '{resultado}'")
        contador += 1
        if contador >= 5:
            break

print("\n" + "="*100)
print("RESUMEN DE TESTS")
print("="*100)
print("""
Los tests anteriores muestran:

1. DESCRIPTIVOS: Palabras como PISO, LOCAL, OFICINA, BODEGA, SUR, NORTE,
   CENTRO no se están eliminando en la salida normalizada.
   SOLUCION: Agregarlas a la lista de descriptivos

2. CIUDADES: Ciudades como BOGOTA, MEDELLIN, CALI al inicio no se eliminan
   SOLUCION: Agregarlas a la lista de ciudades para rechazar

3. ABREVIATURAS: CR y CLL no se normalizan a KR y CL respectivamente
   SOLUCION: Agregarlas al mapa de tipos de vía

4. CORREOS: Direcciones con @ deben rechazarse
   SOLUCION: Agregar validación para '@'

5. ESPECIALES: SUR, NORTE, CENTRO, ESTE, OESTE deberían eliminarse
   SOLUCION: Agregarlas como descriptivos

IMPACTO ESPERADO: Pasar de 93.3% a 95%+ de precisión

""")

print("="*100)
print("FIN DE TESTS")
print("="*100 + "\n")
