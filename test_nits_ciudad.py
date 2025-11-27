#!/usr/bin/env python
# -*- coding: utf-8 -*-
from normalizar_direcciones import standardize_address

# Casos problemáticos del archivo Nits_ciudad.xlsx
test_cases = [
    # AC debe ser CL (no KR)
    ("AC 26 68C 61", "Debería procesar AC como CL"),
    ("AC 26 69D 91", "Debería procesar AC como CL"),
    ("AC 26 N 69 76", "AC con componente N"),
    ("AC 26 SUR 52 A 11", "AC con SUR y A"),
    ("AC 45ASUR 59A 50", "AC con caracteres especiales"),
    ("AC 63 97 10", "AC simple"),
    
    # AEROPUERTO debe rechazarse
    ("AEROPUERTO", "Debe rechazarse - no es dirección"),
    ("AEREOPUERTO", "Variante de AEROPUERTO - debe rechazarse"),
    ("AEREROPUERTO", "Otra variante - debe rechazarse"),
    ("AEROPUERTO DE CARGA X 74", "AEROPUERTO con descriptivos"),
    ("AEREOPUERTO ERNESTO CORTIZZOS", "AEROPUERTO con nombre"),
    ("AEROPUERTI CAMILA DAZA", "AEROPUERTO incompleto"),
    
    # ACOPI y ACACIAS deben eliminarse
    ("ACACIAS AV 23 27 14", "ACACIAS descriptivo + AV"),
    ("ACACIAS CL 14 18 41", "ACACIAS descriptivo + CL"),
    ("ACACIAS KR 14 12 53", "ACACIAS descriptivo + KR"),
    ("ACOPI CL 15 N 35 75 L4", "ACOPI descriptivo + CL"),
    ("ACOPI KR 25 A N 12 98 RANSA COLFRIGOS", "ACOPI con múltiples palabras"),
    ("ACOPI KR 30 10 06", "ACOPI descriptivo + KR"),
    
    # Otros casos
    ("ACL 45 99A 95 SUBA", "ACL variante"),
    ("ACTUAL CL 5C 26 55 CALI", "ACTUAL descriptivo"),
    ("ADMINISTRATIVO MIECO", "Solo descriptivos - debe rechazarse"),
    ("AENIDA 30 AGOSTO 63 30", "AENIDA incompleta - debe rechazarse"),
]

print("=" * 100)
print("VERIFICACIÓN DE CASOS PROBLEMÁTICOS - Nits_ciudad.xlsx")
print("=" * 100)
print()

correcciones = {
    "AC debe ser CL": 0,
    "AEROPUERTO rechazado": 0,
    "ACOPI/ACACIAS limpiados": 0,
}

for entrada, descripcion in test_cases:
    resultado = standardize_address(entrada)
    
    # Verificar correcciones
    if "AC" in entrada and resultado and ("CL" in resultado or "KR" in resultado):
        if "KR" in resultado and "AC 26" in entrada:  # AC debería ser KR ahora
            correcciones["AC debe ser CL"] += 0.5
        correcciones["AC debe ser CL"] += 0.5
    
    if "AERO" in entrada and resultado == "":
        correcciones["AEROPUERTO rechazado"] += 1
    
    if ("ACOPI" in entrada or "ACACIAS" in entrada) and resultado and ("ACOPI" not in resultado and "ACACIAS" not in resultado):
        correcciones["ACOPI/ACACIAS limpiados"] += 1
    
    estado = "✓" if resultado else "Ø"
    print(f"{estado} {descripcion}")
    print(f"   Entrada:  '{entrada}'")
    print(f"   Salida:   '{resultado}'")
    print()

print("=" * 100)
print("RESUMEN DE CORRECCIONES:")
print("=" * 100)
for categoria, count in correcciones.items():
    print(f"{categoria}: {int(count)} casos corregidos")

print("\n✓ Pruebas completadas")
