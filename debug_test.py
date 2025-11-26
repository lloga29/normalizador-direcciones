#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.getcwd())

try:
    from normalizar_direcciones import standardize_address
    
    # Prueba 1: Calle simple
    resultado1 = standardize_address("Calle 123 #45-67")
    print(f"Test 1 - Calle 123 #45-67: {resultado1}")
    
    # Prueba 2: Carrera con apto
    resultado2 = standardize_address("Cra 7 No. 34-56 apt 2")
    print(f"Test 2 - Cra 7 No. 34-56 apt 2: {resultado2}")
    
    # Prueba 3: Avenida
    resultado3 = standardize_address("AV 9 # 45 - 23")
    print(f"Test 3 - AV 9 # 45 - 23: {resultado3}")
    
    # Prueba 4: GPS (debe rechazar)
    resultado4 = standardize_address("10.123456  -74.654321")
    print(f"Test 4 - 10.123456  -74.654321 (GPS): '{resultado4}' (esperado: '')")
    
    # Prueba 5: Con ciudad
    resultado5 = standardize_address("BOGOTA - Calle 50 # 10-20")
    print(f"Test 5 - BOGOTA - Calle 50 # 10-20: {resultado5}")
    
    # Prueba 6: Solo números
    resultado6 = standardize_address("123 456")
    print(f"Test 6 - 123 456: {resultado6}")
    
    print("\n✓ Todas las pruebas ejecutadas correctamente")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
