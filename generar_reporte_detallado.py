#!/usr/bin/env python
# -*- coding: utf-8 -*-
from normalizar_direcciones import standardize_address

# Casos de prueba variados (algunos deben procesarse, otros no)
test_cases = [
    # Formato TIPO NUM NUM (debe procesarse)
    ("Calle 123 #45-67", "DEBE PROCESAR", "Calle simple con guiones"),
    ("Cra 7 No. 34-56", "DEBE PROCESAR", "Carrera con No."),
    ("AV 9 # 45 - 23", "DEBE PROCESAR", "Avenida con guiones"),
    ("Diagonal 10 56 89", "DEBE PROCESAR", "Diagonal sin símbolos"),
    ("Transversal 3 No. 25-15", "DEBE PROCESAR", "Transversal"),
    
    # Solo números sin tipo de vía (PATRÓN 2)
    ("123 456", "DEBE PROCESAR", "Solo números sin tipo"),
    ("50 10 20", "DEBE PROCESAR", "Solo números 3 componentes"),
    
    # Con ciudades (debe limpiar ciudad y procesar)
    ("BOGOTA - Calle 50 # 10-20", "DEBE PROCESAR", "Con ciudad"),
    ("Medellín Cra 7 34 56", "DEBE PROCESAR", "Con ciudad integrada"),
    
    # Coordenadas GPS (DEBE RECHAZAR)
    ("10.123456  -74.654321", "NO PROCESAR", "Coordenadas GPS"),
    ("10.123456, -74.654321", "NO PROCESAR", "Coordenadas GPS con coma"),
    
    # Valores vacíos o inválidos (DEBE RECHAZAR)
    ("", "NO PROCESAR", "Vacío"),
    ("NaN", "NO PROCESAR", "NaN"),
    ("none", "NO PROCESAR", "none"),
    ("00", "NO PROCESAR", "00"),
    
    # Descripciones sin dirección clara (DEBE RECHAZAR)
    ("Vereda El Palmar", "NO PROCESAR", "Solo vereda sin números"),
    ("Barrio Centro", "NO PROCESAR", "Solo barrio sin números"),
    ("Calle", "NO PROCESAR", "Solo tipo de vía sin números"),
    
    # Con apartamento/piso (debe limpiar descriptivo y procesar)
    ("Cra 7 No. 34-56 apt 2", "DEBE PROCESAR", "Con apto (limpia apto)"),
    ("Calle 50 #10-20 Piso 3", "DEBE PROCESAR", "Con piso"),
    ("Avenida 9 45 23 Apto 5B", "DEBE PROCESAR", "Con apto alfanumérico"),
    
    # Casos complejos
    ("Calle 1 Apto 5", "DEBE PROCESAR", "Calle simple con apto"),
    ("Pasaje las Flores 12 34", "DEBE PROCESAR", "Pasaje con palabras"),
    ("Via Circunvalar 5 67", "DEBE PROCESAR", "Vía circunvalar"),
    
    # Casos con sufijos
    ("Calle 123 bis 45-67", "FLEXIBLE", "Con sufijo BIS"),
    ("Diagonal 10 A 56 89", "FLEXIBLE", "Con sufijo A"),
    
    # Casos anómalos que NO deben procesarse
    ("Información no disponible", "NO PROCESAR", "Texto descriptivo"),
    ("Ver documento anexo", "NO PROCESAR", "Instrucción"),
    ("Zona Industrial", "NO PROCESAR", "Solo zona"),
    ("123456789012345", "NO PROCESAR", "Un único número muy largo"),
]

# Separar resultados por categoría
deberia_procesar_pero_no = []
no_deberia_procesar_pero_si = []
correctos = []

for entrada, categoria, descripcion in test_cases:
    salida = standardize_address(entrada)
    procesada = salida != ""
    
    if categoria == "DEBE PROCESAR":
        if procesada:
            correctos.append((entrada, salida, descripcion, "OK"))
        else:
            deberia_procesar_pero_no.append((entrada, salida, descripcion))
    elif categoria == "NO PROCESAR":
        if not procesada:
            correctos.append((entrada, salida, descripcion, "OK"))
        else:
            no_deberia_procesar_pero_si.append((entrada, salida, descripcion))

# Generar reporte detallado
with open("reporte_detallado.txt", "w", encoding="utf-8") as f:
    f.write("=" * 120 + "\n")
    f.write("REPORTE DETALLADO DE PRUEBAS\n")
    f.write("=" * 120 + "\n\n")
    
    # Sección 1: Direcciones que DEBÍAN procesarse pero NO se procesaron
    f.write("🔴 SECCIÓN 1: DIRECCIONES QUE DEBÍAN PROCESARSE PERO NO SE PROCESARON\n")
    f.write("-" * 120 + "\n")
    if deberia_procesar_pero_no:
        f.write(f"Total: {len(deberia_procesar_pero_no)} casos\n\n")
        for i, (entrada, salida, descripcion) in enumerate(deberia_procesar_pero_no, 1):
            f.write(f"{i}. DESCRIPCIÓN: {descripcion}\n")
            f.write(f"   ENTRADA:    '{entrada}'\n")
            f.write(f"   SALIDA:     '{salida}' (VACÍA - ERROR)\n")
            f.write(f"   ANÁLISIS:   Esta dirección debería haber sido procesada pero fue rechazada.\n\n")
    else:
        f.write("✓ NO HAY CASOS - Todas las direcciones que debían procesarse fueron procesadas.\n\n")
    
    # Sección 2: Direcciones que NO DEBÍAN procesarse pero SÍ se procesaron
    f.write("\n" + "=" * 120 + "\n")
    f.write("🔴 SECCIÓN 2: DIRECCIONES QUE NO DEBÍAN PROCESARSE PERO SÍ SE PROCESARON\n")
    f.write("-" * 120 + "\n")
    if no_deberia_procesar_pero_si:
        f.write(f"Total: {len(no_deberia_procesar_pero_si)} casos\n\n")
        for i, (entrada, salida, descripcion) in enumerate(no_deberia_procesar_pero_si, 1):
            f.write(f"{i}. DESCRIPCIÓN: {descripcion}\n")
            f.write(f"   ENTRADA:    '{entrada}'\n")
            f.write(f"   SALIDA:     '{salida}' (DEBERÍA ESTAR VACÍA - ERROR)\n")
            f.write(f"   ANÁLISIS:   Esta dirección no válida fue procesada cuando debería haber sido rechazada.\n\n")
    else:
        f.write("✓ NO HAY CASOS - No hubo direcciones inválidas procesadas.\n\n")
    
    # Resumen
    f.write("\n" + "=" * 120 + "\n")
    f.write("📊 RESUMEN EJECUTIVO\n")
    f.write("-" * 120 + "\n")
    f.write(f"Casos correctos:                                  {len(correctos)}\n")
    f.write(f"Casos que debían procesarse pero no lo fueron:   {len(deberia_procesar_pero_no)}\n")
    f.write(f"Casos que no debían procesarse pero sí lo fueron: {len(no_deberia_procesar_pero_si)}\n")
    f.write(f"\nPRECISIÓN TOTAL: {len(correctos)}/{len(test_cases)} ({100*len(correctos)/len(test_cases):.1f}%)\n")
    f.write("=" * 120 + "\n")

# Mostrar en consola
print("=" * 120)
print("REPORTE DETALLADO DE PRUEBAS")
print("=" * 120)

print("\n🔴 SECCIÓN 1: DIRECCIONES QUE DEBÍAN PROCESARSE PERO NO SE PROCESARON")
print("-" * 120)
if deberia_procesar_pero_no:
    print(f"Total: {len(deberia_procesar_pero_no)} casos\n")
    for i, (entrada, salida, descripcion) in enumerate(deberia_procesar_pero_no, 1):
        print(f"{i}. DESCRIPCIÓN: {descripcion}")
        print(f"   ENTRADA:    '{entrada}'")
        print(f"   SALIDA:     '{salida}' (VACÍA - ERROR)")
        print()
else:
    print("✓ NO HAY CASOS - Todas las direcciones que debían procesarse fueron procesadas.\n")

print("\n" + "=" * 120)
print("🔴 SECCIÓN 2: DIRECCIONES QUE NO DEBÍAN PROCESARSE PERO SÍ SE PROCESARON")
print("-" * 120)
if no_deberia_procesar_pero_si:
    print(f"Total: {len(no_deberia_procesar_pero_si)} casos\n")
    for i, (entrada, salida, descripcion) in enumerate(no_deberia_procesar_pero_si, 1):
        print(f"{i}. DESCRIPCIÓN: {descripcion}")
        print(f"   ENTRADA:    '{entrada}'")
        print(f"   SALIDA:     '{salida}' (DEBERÍA ESTAR VACÍA - ERROR)")
        print()
else:
    print("✓ NO HAY CASOS - No hubo direcciones inválidas procesadas.\n")

print("=" * 120)
print("📊 RESUMEN")
print("-" * 120)
print(f"Casos correctos:                                  {len(correctos)}")
print(f"Casos que debían procesarse pero no lo fueron:   {len(deberia_procesar_pero_no)}")
print(f"Casos que no debían procesarse pero sí lo fueron: {len(no_deberia_procesar_pero_si)}")
print(f"\nPRECISIÓN TOTAL: {len(correctos)}/{len(test_cases)} ({100*len(correctos)/len(test_cases):.1f}%)")
print("=" * 120)

print("\n✓ Reporte guardado en: reporte_detallado.txt")
