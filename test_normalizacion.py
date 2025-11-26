import sys
sys.path.insert(0, 'c:\\Users\\Juan\\Documents\\Lorena')

from normalizar_direcciones import standardize_address, normalize_via_type

# Casos de prueba típicos
test_cases = [
    # (entrada, descripción esperada)
    ("Calle 123 #45-67", "dirección calle simple"),
    ("Cra 7 No. 34-56 apt 2", "carrera con apto"),
    ("AV 9 # 45 - 23", "avenida con guiones"),
    ("Diagonal 10 bis 56 - 89", "diagonal con BIS"),
    ("10.123456  -74.654321", "coordenadas GPS"),
    ("BOGOTA - Calle 50 # 10-20", "con ciudad"),
    ("Transversal 3 No. 25-15", "transversal"),
    ("Vereda El Palmar", "solo vereda"),
    ("Calle 1 Apto 5", "calle con apto"),
    ("", "vacío"),
    ("NaN", "NaN"),
    ("Pasaje las Flores 12 34", "pasaje"),
    ("123 456", "solo números sin tipo"),
    ("Via Circunvalar 5 67", "vía circunvalar"),
]

print("=" * 80)
print("PRUEBAS DE NORMALIZACIÓN DE DIRECCIONES")
print("=" * 80)

for entrada, descripcion in test_cases:
    resultado = standardize_address(entrada)
    estado = "✓" if resultado != "" else "Ø"
    print(f"{estado} [{descripcion}]")
    print(f"  Entrada:  '{entrada}'")
    print(f"  Salida:   '{resultado}'")
    print()

print("=" * 80)
print("PRUEBAS DE NORMALIZACIÓN DE TIPOS DE VÍA")
print("=" * 80)

via_tests = [
    ("Calle", "CL"),
    ("CLL", "CL"),
    ("Carrera", "KR"),
    ("KRA", "KR"),
    ("Avenida", "AV"),
    ("Diagonal", "DG"),
    ("TV", "TV"),
    ("PASAJE", "PASAJE"),
    ("VIA", "VIA"),
]

for entrada, esperado in via_tests:
    resultado = normalize_via_type(entrada)
    match = "✓" if resultado == esperado else "✗"
    print(f"{match} {entrada:15} -> {resultado:10} (esperado: {esperado})")

print("\n" + "=" * 80)
print("FIN DE PRUEBAS")
print("=" * 80)
