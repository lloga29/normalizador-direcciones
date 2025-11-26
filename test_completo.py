#!/usr/bin/env python
# -*- coding: utf-8 -*-
from normalizar_direcciones import standardize_address

# Casos de prueba variados (algunos deben procesarse, otros no)
test_cases = [
    # Formato TIPO NUM NUM (debe procesarse)
    ("Calle 123 #45-67", "DEBE PROCESAR - Calle simple con guiones"),
    ("Cra 7 No. 34-56", "DEBE PROCESAR - Carrera con No."),
    ("AV 9 # 45 - 23", "DEBE PROCESAR - Avenida con guiones"),
    ("Diagonal 10 56 89", "DEBE PROCESAR - Diagonal sin símbolos"),
    ("Transversal 3 No. 25-15", "DEBE PROCESAR - Transversal"),
    
    # Solo números sin tipo de vía (PATRÓN 2)
    ("123 456", "DEBE PROCESAR - Solo números sin tipo"),
    ("50 10 20", "DEBE PROCESAR - Solo números 3 componentes"),
    
    # Con ciudades (debe limpiar ciudad y procesar)
    ("BOGOTA - Calle 50 # 10-20", "DEBE PROCESAR - Con ciudad"),
    ("Medellín Cra 7 34 56", "DEBE PROCESAR - Con ciudad integrada"),
    
    # Coordenadas GPS (DEBE RECHAZAR)
    ("10.123456  -74.654321", "NO PROCESAR - Coordenadas GPS"),
    ("10.123456, -74.654321", "NO PROCESAR - Coordenadas GPS con coma"),
    
    # Valores vacíos o inválidos (DEBE RECHAZAR)
    ("", "NO PROCESAR - Vacío"),
    ("NaN", "NO PROCESAR - NaN"),
    ("none", "NO PROCESAR - none"),
    ("00", "NO PROCESAR - 00"),
    
    # Descripciones sin dirección clara (DEBE RECHAZAR)
    ("Vereda El Palmar", "NO PROCESAR - Solo vereda sin números"),
    ("Barrio Centro", "NO PROCESAR - Solo barrio sin números"),
    ("Calle", "NO PROCESAR - Solo tipo de vía sin números"),
    
    # Con apartamento/piso (debe limpiar descriptivo y procesar)
    ("Cra 7 No. 34-56 apt 2", "DEBE PROCESAR - Con apto (limpia apto)"),
    ("Calle 50 #10-20 Piso 3", "DEBE PROCESAR - Con piso"),
    ("Avenida 9 45 23 Apto 5B", "DEBE PROCESAR - Con apto alfanumérico"),
    
    # Casos complejos
    ("Calle 1 Apto 5", "DEBE PROCESAR - Calle simple con apto"),
    ("Pasaje las Flores 12 34", "DEBE PROCESAR - Pasaje con palabras"),
    ("Via Circunvalar 5 67", "DEBE PROCESAR - Vía circunvalar"),
    
    # Casos con sufijos
    ("Calle 123 bis 45-67", "PUEDE PROCESAR - Con sufijo BIS"),
    ("Diagonal 10 A 56 89", "PUEDE PROCESAR - Con sufijo A"),
    
    # Casos anómalos que NO deben procesarse
    ("Información no disponible", "NO PROCESAR - Texto descriptivo"),
    ("Ver documento anexo", "NO PROCESAR - Instrucción"),
    ("Zona Industrial", "NO PROCESAR - Solo zona"),
    ("123456789012345", "NO PROCESAR - Un único número muy largo"),
]

# Ejecutar pruebas
resultado = []
procesadas_ok = 0
rechazadas_ok = 0
procesadas_mal = 0
rechazadas_mal = 0

print("=" * 100)
print("PRUEBAS COMPLETAS DE NORMALIZACIÓN DE DIRECCIONES")
print("=" * 100)
print()

for entrada, descripcion in test_cases:
    salida = standardize_address(entrada)
    procesada = salida != ""
    
    # Determinar si el resultado es correcto
    if "DEBE PROCESAR" in descripcion:
        if procesada:
            estado = "✓ OK"
            procesadas_ok += 1
        else:
            estado = "✗ ERROR"
            procesadas_mal += 1
    elif "NO PROCESAR" in descripcion:
        if not procesada:
            estado = "✓ OK"
            rechazadas_ok += 1
        else:
            estado = "✗ ERROR"
            rechazadas_mal += 1
    else:  # PUEDE PROCESAR
        estado = "? FLEXIBLE"
    
    # Mostrar resultado
    print(f"{estado}")
    print(f"  Descripción: {descripcion}")
    print(f"  Entrada:     '{entrada}'")
    print(f"  Salida:      '{salida}'")
    print()

# Resumen
print("=" * 100)
print("RESUMEN DE PRUEBAS")
print("=" * 100)
print(f"✓ Direcciones que DEBÍAN procesarse y SÍ se procesaron:        {procesadas_ok}")
print(f"✗ Direcciones que DEBÍAN procesarse pero NO se procesaron:    {procesadas_mal}")
print(f"✓ Direcciones que NO DEBÍAN procesarse y efectivamente NO lo fueron: {rechazadas_ok}")
print(f"✗ Direcciones que NO DEBÍAN procesarse pero SÍ se procesaron: {rechazadas_mal}")
print()

total_correcto = procesadas_ok + rechazadas_ok
total_esperado = procesadas_ok + procesadas_mal + rechazadas_ok + rechazadas_mal
porcentaje = (total_correcto / total_esperado * 100) if total_esperado > 0 else 0

print(f"PRECISIÓN TOTAL: {total_correcto}/{total_esperado} ({porcentaje:.1f}%)")
print("=" * 100)

# Guardar resultados en archivo
with open("resultados_completos.txt", "w", encoding="utf-8") as f:
    f.write("RESUMEN DE PRUEBAS\n")
    f.write("=" * 100 + "\n")
    f.write(f"✓ Direcciones que DEBÍAN procesarse y SÍ se procesaron:        {procesadas_ok}\n")
    f.write(f"✗ Direcciones que DEBÍAN procesarse pero NO se procesaron:    {procesadas_mal}\n")
    f.write(f"✓ Direcciones que NO DEBÍAN procesarse y NO lo fueron:        {rechazadas_ok}\n")
    f.write(f"✗ Direcciones que NO DEBÍAN procesarse pero SÍ se procesaron: {rechazadas_mal}\n")
    f.write(f"\nPRECISIÓN TOTAL: {total_correcto}/{total_esperado} ({porcentaje:.1f}%)\n")

print("\n✓ Resultados guardados en: resultados_completos.txt")
