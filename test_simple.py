from normalizar_direcciones import standardize_address, normalize_via_type

# Casos de prueba
test_cases = [
    ("Calle 123 #45-67", "dirección calle simple"),
    ("Cra 7 No. 34-56 apt 2", "carrera con apto"),
    ("AV 9 # 45 - 23", "avenida con guiones"),
    ("10.123456  -74.654321", "coordenadas GPS"),
    ("BOGOTA - Calle 50 # 10-20", "con ciudad"),
    ("123 456", "solo números sin tipo"),
]

with open("resultados_test.txt", "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("PRUEBAS DE NORMALIZACIÓN DE DIRECCIONES\n")
    f.write("=" * 80 + "\n\n")
    
    for entrada, descripcion in test_cases:
        resultado = standardize_address(entrada)
        estado = "✓" if resultado != "" else "Ø"
        f.write(f"{estado} [{descripcion}]\n")
        f.write(f"  Entrada:  '{entrada}'\n")
        f.write(f"  Salida:   '{resultado}'\n\n")
    
    f.write("=" * 80 + "\n")
    f.write("PRUEBAS DE NORMALIZACIÓN DE TIPOS DE VÍA\n")
    f.write("=" * 80 + "\n\n")
    
    via_tests = [
        ("Calle", "CL"),
        ("CLL", "CL"),
        ("Carrera", "KR"),
        ("Avenida", "AV"),
        ("Diagonal", "DG"),
        ("TV", "TV"),
    ]
    
    for entrada, esperado in via_tests:
        resultado = normalize_via_type(entrada)
        match = "✓" if resultado == esperado else "✗"
        f.write(f"{match} {entrada:15} -> {resultado:10} (esperado: {esperado})\n")

print("Pruebas completadas. Resultados guardados en resultados_test.txt")
