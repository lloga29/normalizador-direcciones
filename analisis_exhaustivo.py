#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ANALISIS EXHAUSTIVO DE VARIABLES Y PATRONES
Identifica todas las variables, palabras clave y patrones en direcciones
para configurar reglas adicionales
"""

import pandas as pd
import re
from collections import Counter, defaultdict

print("\n" + "="*100)
print("ANALISIS EXHAUSTIVO - IDENTIFICACION DE VARIABLES Y PATRONES EN DIRECCIONES")
print("="*100)

# Cargar ambos archivos
print("\n[1] Cargando archivos...")
df_prueba = pd.read_excel("direcciones.xlsx")
df_nits = pd.read_excel("Nits_ciudad.xlsx")

print(f"    [OK] Prueba: {len(df_prueba)} registros")
print(f"    [OK] Nits_ciudad: {len(df_nits)} registros")

# Combinar para análisis
all_addresses = pd.concat([
    df_prueba['Direccion'],
    df_nits['Direccion']
], ignore_index=True).dropna()

print(f"    [OK] Total para analizar: {len(all_addresses)} direcciones")

# ============================================================================
# PASO 1: PALABRAS MAS FRECUENTES
# ============================================================================
print("\n" + "="*100)
print("[2] PALABRAS MAS FRECUENTES EN TODAS LAS DIRECCIONES")
print("="*100)

all_words = []
for addr in all_addresses:
    palabras = addr.upper().split()
    all_words.extend(palabras)

contador_palabras = Counter(all_words)
print("\nTop 50 palabras mas comunes:")
for idx, (palabra, count) in enumerate(contador_palabras.most_common(50), 1):
    pct = (count / len(all_addresses) * 100)
    print(f"  {idx:2}. {palabra:20} - {count:5} veces ({pct:5.2f}%)")

# ============================================================================
# PASO 2: PATRONES CON NUMEROS
# ============================================================================
print("\n" + "="*100)
print("[3] ANALISIS DE PATRONES CON NUMEROS")
print("="*100)

numero_pattern = re.compile(r'\d+')
patrones_con_numeros = []
patrones_sin_numeros = []

for addr in all_addresses:
    if numero_pattern.search(addr):
        patrones_con_numeros.append(addr)
    else:
        patrones_sin_numeros.append(addr)

print(f"\nDirecciones CON numeros: {len(patrones_con_numeros)} ({100*len(patrones_con_numeros)/len(all_addresses):.1f}%)")
print(f"Direcciones SIN numeros: {len(patrones_sin_numeros)} ({100*len(patrones_sin_numeros)/len(all_addresses):.1f}%)")

print("\n--- Primeras 15 direcciones SIN numeros (potencial RECHAZA) ---")
for i, addr in enumerate(patrones_sin_numeros[:15], 1):
    print(f"  {i:2}. {addr}")

# ============================================================================
# PASO 3: PALABRAS QUE PUEDEN SER DESCRIPTIVOS
# ============================================================================
print("\n" + "="*100)
print("[4] POSIBLES DESCRIPTIVOS (palabras despues de numeros)")
print("="*100)

palabras_post_numero = Counter()
for addr in patrones_con_numeros:
    # Encontrar posición de números
    tokens = addr.upper().split()
    for i, token in enumerate(tokens):
        if numero_pattern.search(token) and i < len(tokens) - 1:
            siguiente = tokens[i + 1]
            # Excluir números y caracteres especiales puros
            if not numero_pattern.match(siguiente) and len(siguiente) > 1:
                palabras_post_numero[siguiente] += 1

print("\nPalabras frecuentes DESPUES de numeros (posibles descriptivos/sufijos):")
for palabra, count in palabras_post_numero.most_common(40):
    pct = (count / len(patrones_con_numeros) * 100)
    print(f"  {palabra:20} - {count:4} veces ({pct:5.2f}%)")

# ============================================================================
# PASO 5: ABREVIATURAS NO RECONOCIDAS
# ============================================================================
print("\n" + "="*100)
print("[5] ABREVIATURAS POTENCIALES NO RECONOCIDAS")
print("="*100)

# Tipos de vía conocidos
tipos_conocidos = {'CL', 'CLL', 'CALLE', 'KR', 'KRA', 'CARRERA', 'AV', 'AVD', 'AVENIDA', 
                   'DG', 'DIAGONAL', 'TV', 'TRANSV', 'TRANSVERSAL', 'VDA', 'VEREDA', 
                   'VIA', 'PASAJE', 'AC'}

abreviaturas_nuevas = Counter()
for addr in all_addresses:
    palabras = addr.upper().split()
    for palabra in palabras:
        # Si contiene letras pero no es muy larga y no está en conocidos
        if 2 <= len(palabra) <= 6 and palabra not in tipos_conocidos:
            # Filtrar números puros
            if re.match(r'^[A-Z]+$', palabra):
                abreviaturas_nuevas[palabra] += 1

print("\nAbreviaturas potenciales (2-6 caracteres, solo letras):")
for abrev, count in abreviaturas_nuevas.most_common(50):
    pct = (count / len(all_addresses) * 100)
    if count > 5:  # Solo mostrar si aparecen mas de 5 veces
        print(f"  {abrev:10} - {count:4} veces ({pct:5.2f}%)")

# ============================================================================
# PASO 6: SIMBOLOS Y CARACTERES ESPECIALES
# ============================================================================
print("\n" + "="*100)
print("[6] SIMBOLOS Y CARACTERES ESPECIALES")
print("="*100)

simbolos = Counter()
for addr in all_addresses:
    for char in addr:
        if not char.isalnum() and not char.isspace():
            simbolos[char] += 1

print("\nSimbolos mas frecuentes:")
for simbolo, count in simbolos.most_common(20):
    print(f"  '{simbolo}' - {count:5} veces")

# ============================================================================
# PASO 7: PREFIJOS COMUNES
# ============================================================================
print("\n" + "="*100)
print("[7] PREFIJOS COMUNES (primeras palabras)")
print("="*100)

primeras_palabras = Counter()
for addr in all_addresses:
    palabras = addr.upper().split()
    if len(palabras) > 0:
        primeras_palabras[palabras[0]] += 1

print("\nPrimeras palabras mas frecuentes (posibles prefijos/ciudades):")
for palabra, count in primeras_palabras.most_common(40):
    pct = (count / len(all_addresses) * 100)
    print(f"  {palabra:25} - {count:5} veces ({pct:5.2f}%)")

# ============================================================================
# PASO 8: ULTIMAS PALABRAS
# ============================================================================
print("\n" + "="*100)
print("[8] ULTIMAS PALABRAS (posibles sufijos/complementos)")
print("="*100)

ultimas_palabras = Counter()
for addr in all_addresses:
    palabras = addr.upper().split()
    if len(palabras) > 0:
        ultimas_palabras[palabras[-1]] += 1

print("\nUltimas palabras mas frecuentes:")
for palabra, count in ultimas_palabras.most_common(40):
    pct = (count / len(all_addresses) * 100)
    print(f"  {palabra:25} - {count:5} veces ({pct:5.2f}%)")

# ============================================================================
# PASO 9: LONGITUD DE DIRECCIONES
# ============================================================================
print("\n" + "="*100)
print("[9] ESTADISTICAS DE LONGITUD")
print("="*100)

longitudes = [len(addr.split()) for addr in all_addresses]
print(f"\nPalabras por direccion:")
print(f"  Minimo: {min(longitudes)}")
print(f"  Maximo: {max(longitudes)}")
print(f"  Promedio: {sum(longitudes)/len(longitudes):.1f}")
print(f"  Mediana: {sorted(longitudes)[len(longitudes)//2]}")

longitud_counter = Counter(longitudes)
print("\nDistribucion de longitud (palabras):")
for length in sorted(longitud_counter.keys())[:15]:
    count = longitud_counter[length]
    pct = (count / len(all_addresses) * 100)
    bar = "#" * int(pct / 2)
    print(f"  {length:2} palabras: {count:6} ({pct:5.2f}%) {bar}")

# ============================================================================
# PASO 10: PATRONES DE NUMEROS
# ============================================================================
print("\n" + "="*100)
print("[10] PATRONES DE NUMEROS")
print("="*100)

# Contar cuántos números por dirección
numeros_por_addr = []
for addr in patrones_con_numeros:
    numeros = numero_pattern.findall(addr)
    numeros_por_addr.append(len(numeros))

num_counter = Counter(numeros_por_addr)
print(f"\nNumeros por direccion (en direcciones con numeros):")
for count in sorted(num_counter.keys()):
    freq = num_counter[count]
    pct = (freq / len(patrones_con_numeros) * 100)
    print(f"  {count} numeros: {freq:6} veces ({pct:5.2f}%)")

# ============================================================================
# PASO 11: PALABRAS POTENCIALMENTE PROBLEMATICAS
# ============================================================================
print("\n" + "="*100)
print("[11] PALABRAS POTENCIALMENTE PROBLEMATICAS")
print("="*100)

palabras_problematicas = []
for addr in all_addresses:
    palabras = addr.upper().split()
    for palabra in palabras:
        # Palabras que son principalmente letras pero contienen números
        if re.search(r'[A-Z]', palabra) and re.search(r'\d', palabra):
            palabras_problematicas.append(palabra)

problematica_counter = Counter(palabras_problematicas)
print("\nPalabras MIXTAS (letras + numeros) mas comunes:")
for palabra, count in problematica_counter.most_common(30):
    print(f"  {palabra:15} - {count:4} veces")

# ============================================================================
# EXPORTAR REPORTE
# ============================================================================
print("\n" + "="*100)
print("[EXPORTANDO REPORTES...]")
print("="*100)

with open("ANALISIS_VARIABLES.txt", "w", encoding="utf-8") as f:
    f.write("="*100 + "\n")
    f.write("ANALISIS EXHAUSTIVO DE VARIABLES Y PATRONES\n")
    f.write("="*100 + "\n\n")
    
    f.write("RESUMEN GENERAL:\n")
    f.write(f"  Total direcciones analizadas: {len(all_addresses):,}\n")
    f.write(f"  Con numeros: {len(patrones_con_numeros):,}\n")
    f.write(f"  Sin numeros: {len(patrones_sin_numeros):,}\n\n")
    
    f.write("POSIBLES DESCRIPTIVOS A AGREGAR:\n")
    for palabra, count in palabras_post_numero.most_common(20):
        f.write(f"  - {palabra} ({count} veces)\n")
    
    f.write("\n\nABREVIATURAS NO RECONOCIDAS:\n")
    for abrev, count in abreviaturas_nuevas.most_common(20):
        if count > 5:
            f.write(f"  - {abrev} ({count} veces)\n")
    
    f.write("\n\nPREFIJOS COMUNES A EVALUAR:\n")
    for palabra, count in primeras_palabras.most_common(20):
        f.write(f"  - {palabra} ({count} veces)\n")

print("\n[OK] Reporte exportado a: ANALISIS_VARIABLES.txt")

print("\n" + "="*100)
print("ANALISIS COMPLETADO")
print("="*100 + "\n")
