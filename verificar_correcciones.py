from normalizar_direcciones import standardize_address

# Casos clave a verificar
casos = [
    ("AC 26 68C 61", "AC debe ser CL"),
    ("AC 63 97 10", "AC simple debe ser CL"),
    ("AEROPUERTO", "AEROPUERTO debe rechazarse"),
    ("AEREOPUERTO", "AEREOPUERTO debe rechazarse"),
    ("ACACIAS AV 23 27 14", "ACACIAS debe limpiarse"),
    ("ACOPI CL 15 N 35 75 L4", "ACOPI debe limpiarse"),
]

print("=" * 80)
print("VERIFICACIÓN DE CORRECCIONES")
print("=" * 80)
print()

for entrada, descripcion in casos:
    resultado = standardize_address(entrada)
    print(f"✓ {descripcion}")
    print(f"  Entrada:  '{entrada}'")
    print(f"  Salida:   '{resultado}'")
    print()

print("=" * 80)
