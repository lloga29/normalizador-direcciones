#!/usr/bin/env python
# -*- coding: utf-8 -*-
from normalizar_direcciones import standardize_address

print("\n" + "=" * 120)
print("VERIFICACIÓN FINAL DEL SCRIPT DE NORMALIZACIÓN")
print("=" * 120 + "\n")

# Casos críticos a verificar
test_cases = [
    ("Calle 123 #45-67", "CL 123 45 67", "Dirección con tipo y números"),
    ("123 456", "123 456", "Solo números sin tipo"),
    ("10.123456  -74.654321", "", "Coordenadas GPS - debe rechazar"),
    ("Vereda El Palmar", "", "Solo vereda sin números - debe rechazar"),
    ("BOGOTA - Calle 50 # 10-20", "CL 50 10 20", "Con ciudad - debe limpiarla"),
    ("Cra 7 No. 34-56 apt 2", "KR 7 34 56", "Con apto - debe limpiarlo"),
]

print("CASOS CRÍTICOS:")
print("-" * 120)

todos_correctos = True
for entrada, esperado, descripcion in test_cases:
    resultado = standardize_address(entrada)
    correcto = resultado == esperado
    estado = "✓" if correcto else "✗"
    
    print(f"{estado} {descripcion}")
    print(f"   Entrada:   '{entrada}'")
    print(f"   Esperado:  '{esperado}'")
    print(f"   Resultado: '{resultado}'")
    
    if not correcto:
        todos_correctos = False
        print(f"   ⚠️  ERROR: Resultado no coincide")
    print()

print("=" * 120)
if todos_correctos:
    print("✅ TODOS LOS CASOS CRÍTICOS PASARON")
else:
    print("❌ ALGUNOS CASOS FALLARON")
print("=" * 120)
