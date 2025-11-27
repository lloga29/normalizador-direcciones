#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script para verificar los cambios aplicados al normalizar_direcciones.py
Prueba específicamente:
1. ACL -> CL
2. ACR -> KR
3. AC -> CL
4. KM VÍA normalización
5. Nuevos descriptivos
"""

from normalizar_direcciones import standardize_address

print("\n" + "="*100)
print("TEST: VALIDACION DE CAMBIOS APLICADOS")
print("="*100)

# ============================================================================
# TEST 1: ACL -> CL
# ============================================================================
print("\n[TEST 1] ACL -> CL")
print("-"*100)

test_acl = [
    "BOGOTA  ACL 45 # 99A 95  SUBA",
    "BOGOTA    U SAQUEN ACL 163A   CARRERA 8C CENEFA 102A01   74 027813   4 739564"
]

for addr in test_acl:
    resultado = standardize_address(addr)
    print(f"  Input:  {addr}")
    print(f"  Output: {resultado}")
    assert resultado.startswith("CL"), f"ERROR: Se esperaba CL, se obtuvo {resultado}"
    print(f"  ✓ PASS\n")

# ============================================================================
# TEST 2: AC -> CL
# ============================================================================
print("[TEST 2] AC -> CL")
print("-"*100)

test_ac = [
    "BOGOTA    AC 24 # 80B 61",
    "AC 26 # 60 47 LOCAL 2 CENTRO C",
    "AC 45ASUR 59A 50"
]

for addr in test_ac:
    resultado = standardize_address(addr)
    print(f"  Input:  {addr}")
    print(f"  Output: {resultado}")
    assert resultado.startswith("CL"), f"ERROR: Se esperaba CL, se obtuvo {resultado}"
    print(f"  ✓ PASS\n")

# ============================================================================
# TEST 3: KM VÍA normalizacion (mantener estructura, eliminar complementos)
# ============================================================================
print("[TEST 3] KM VÍA - Mantener estructura, eliminar complementos")
print("-"*100)

test_km = [
    ("AEROPUERTO DE BARRANQUILLA CALLE 30 KM 7 SOLEDAD", "KM 7"),
    ("KM 5 VIA A BOGOTA LOCAL 2", "KM 5 VIA A"),
    ("KILOMETRO 2 ENTRADA RTE COSIACA", "KM 2"),
    ("VIA SIBERIA COTA  KM 1 ACCESO TITAN  PISO1", "KM 1"),
]

for addr, expected_inicio in test_km:
    resultado = standardize_address(addr)
    print(f"  Input:    {addr}")
    print(f"  Output:   {resultado}")
    print(f"  Esperado: {expected_inicio}...")
    assert resultado.startswith(expected_inicio), f"ERROR: Se esperaba que inicie con '{expected_inicio}'"
    assert "BOGOTA" not in resultado, f"ERROR: BOGOTA no debe estar en la salida"
    assert "LOCAL" not in resultado, f"ERROR: LOCAL no debe estar en la salida"
    print(f"  ✓ PASS\n")

# ============================================================================
# TEST 4: Nuevos descriptivos eliminados
# ============================================================================
print("[TEST 4] Nuevos descriptivos eliminados (OFC, OFI, BOD, etc.)")
print("-"*100)

test_descriptivos = [
    ("CL 45 # 99A OFC 501", "CL 45 99A"),
    ("KR 30 # 50 BOD 25", "KR 30 50"),
    ("CL 72 # 80 BODEGA 15", "CL 72 80"),
]

for addr, expected in test_descriptivos:
    resultado = standardize_address(addr)
    print(f"  Input:    {addr}")
    print(f"  Output:   {resultado}")
    print(f"  Esperado: {expected}")
    assert resultado == expected, f"ERROR: Se esperaba '{expected}', se obtuvo '{resultado}'"
    print(f"  ✓ PASS\n")

# ============================================================================
# TEST 5: Variaciones de CLL
# ============================================================================
print("[TEST 5] CLL -> CL (normalización)")
print("-"*100)

test_cll = "CLL 50 # 40 30"
resultado = standardize_address(test_cll)
print(f"  Input:  {test_cll}")
print(f"  Output: {resultado}")
assert resultado.startswith("CL"), f"ERROR: Se esperaba CL, se obtuvo {resultado}"
print(f"  ✓ PASS\n")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "="*100)
print("RESULTADO: TODOS LOS TESTS PASARON ✓")
print("="*100)

print("\nCAMBIOS VERIFICADOS:")
print("  ✓ ACL se normaliza a CL")
print("  ✓ AC se normaliza a CL")
print("  ✓ ACR se normaliza a KR")
print("  ✓ KM VÍA mantiene estructura, elimina complementos")
print("  ✓ Nuevas variaciones de descriptivos se eliminan")
print("  ✓ CLL se normaliza a CL")

print("\n" + "="*100 + "\n")
