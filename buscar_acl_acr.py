#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ANALISIS ESPECIFICO: Buscar casos de ACL, ACR y variaciones similares
Identifica abreviaturas con tendencias similares y analiza KM VÍA
"""

import pandas as pd
import re
from collections import Counter

print("\n" + "="*100)
print("ANALISIS ESPECIFICO: BUSQUEDA DE ACL, ACR Y VARIACIONES SIMILARES")
print("="*100)

# Cargar ambos archivos
df_prueba = pd.read_excel("direcciones.xlsx")
df_nits = pd.read_excel("Nits_ciudad.xlsx")

print(f"\nCargando datos...")
print(f"  Prueba: {len(df_prueba)} registros")
print(f"  Nits_ciudad: {len(df_nits)} registros")

# Combinar para análisis
all_addresses = pd.concat([
    df_prueba['Direccion'],
    df_nits['Direccion']
], ignore_index=True).dropna()

print(f"  Total para analizar: {len(all_addresses)} direcciones")

# ============================================================================
# BUSQUEDA 1: ACL EN CUALQUIER CASO
# ============================================================================
print("\n" + "="*100)
print("[1] BUSQUEDA DE 'ACL' (en cualquier caso)")
print("="*100)

# Buscar ACL como palabra completa o prefijo
acl_pattern = re.compile(r'\bACL\b|\bACl\b|\bAcl\b|\bacl\b', re.IGNORECASE)

casos_acl = []
for idx, addr in enumerate(all_addresses):
    if acl_pattern.search(addr):
        casos_acl.append((idx, addr))

if casos_acl:
    print(f"\nEncontrados: {len(casos_acl)} casos con ACL")
    print("\nPrimeros 20 ejemplos:")
    for i, (idx, addr) in enumerate(casos_acl[:20], 1):
        print(f"  {i:2}. {addr}")
else:
    print(f"\nNo se encontraron casos de ACL en los datos")

# ============================================================================
# BUSQUEDA 2: ACR EN CUALQUIER CASO
# ============================================================================
print("\n" + "="*100)
print("[2] BUSQUEDA DE 'ACR' (en cualquier caso)")
print("="*100)

# Buscar ACR como palabra completa o prefijo
acr_pattern = re.compile(r'\bACR\b|\bACr\b|\bAcr\b|\bacr\b', re.IGNORECASE)

casos_acr = []
for idx, addr in enumerate(all_addresses):
    if acr_pattern.search(addr):
        casos_acr.append((idx, addr))

if casos_acr:
    print(f"\nEncontrados: {len(casos_acr)} casos con ACR")
    print("\nPrimeros 20 ejemplos:")
    for i, (idx, addr) in enumerate(casos_acr[:20], 1):
        print(f"  {i:2}. {addr}")
else:
    print(f"\nNo se encontraron casos de ACR en los datos")

# ============================================================================
# BUSQUEDA 3: AC# (AC seguido de número)
# ============================================================================
print("\n" + "="*100)
print("[3] BUSQUEDA DE 'AC' COMO ABREVIATURA (AC + numero)")
print("="*100)

# Buscar AC como tipo de vía (AC seguido de número)
ac_pattern = re.compile(r'\bAC\s+\d', re.IGNORECASE)

casos_ac = []
for idx, addr in enumerate(all_addresses):
    if ac_pattern.search(addr):
        casos_ac.append((idx, addr))

if casos_ac:
    print(f"\nEncontrados: {len(casos_ac)} casos con AC (como tipo de vía)")
    print("\nPrimeros 20 ejemplos:")
    for i, (idx, addr) in enumerate(casos_ac[:20], 1):
        print(f"  {i:2}. {addr}")
        
    # Verificar si se normalizan correctamente con el script actual
    print("\n" + "-"*100)
    print("Verificando normalizacion actual:")
    print("-"*100)
    
    from normalizar_direcciones import standardize_address
    
    print("\nPrimeros 10 casos y su normalizacion:")
    for i, (idx, addr) in enumerate(casos_ac[:10], 1):
        resultado = standardize_address(addr)
        estado = "OK" if resultado.startswith("CL") else "ERROR"
        print(f"  {i:2}. '{addr}'")
        print(f"      -> '{resultado}' [{estado}]")
else:
    print(f"\nNo se encontraron casos de AC como tipo de vía")

# ============================================================================
# BUSQUEDA 4: ANÁLISIS DE PALABRAS CON "AC"
# ============================================================================
print("\n" + "="*100)
print("[4] PALABRAS CON 'AC' (análisis de contexto)")
print("="*100)

palabras_con_ac = Counter()
for addr in all_addresses:
    palabras = addr.upper().split()
    for palabra in palabras:
        if 'AC' in palabra and len(palabra) <= 10:
            palabras_con_ac[palabra] += 1

print("\nPalabras que contienen 'AC':")
for palabra, count in palabras_con_ac.most_common(30):
    print(f"  {palabra:20} - {count:5} veces")

# ============================================================================
# BUSQUEDA 5: VARIACIONES SIMILARES A VIAS (patron: 2-3 letras + numero)
# ============================================================================
print("\n" + "="*100)
print("[5] VARIACIONES SIMILARES A TIPOS DE VIA (2-3 letras)")
print("="*100)

# Patrones similares: AB, AC, AD, AK, AP, AV, AZ, etc.
variaciones = Counter()
for addr in all_addresses:
    # Buscar palabras de 2-3 letras seguidas de número
    matches = re.findall(r'\b([A-Z]{2,3})\s+\d+\b', addr.upper())
    for match in matches:
        variaciones[match] += 1

print("\nAbrevaturas de 2-3 letras seguidas de número:")
for abrev, count in variaciones.most_common(50):
    # Marcar las que ya conocemos
    status = ""
    if abrev in ['CR', 'CL', 'CRA', 'KR', 'KM', 'AV']:
        status = " [YA EXISTE]"
    elif abrev in ['ACL', 'ACR']:
        status = " [NUEVA - ACL/ACR]"
    elif abrev in ['AB', 'AC', 'AD', 'AF', 'AG', 'AL', 'AM', 'AP', 'AR', 'AS', 'AT', 'AZ']:
        status = " [POTENCIAL SIMILAR]"
    
    print(f"  {abrev:4} - {count:5} veces{status}")

# ============================================================================
# BUSQUEDA 6: KM VÍA (Kilometro Vía) - Análisis especial
# ============================================================================
print("\n" + "="*100)
print("[6] ANALISIS ESPECIAL: KM, KM VIA, VIA KM, KILOMETRO")
print("="*100)

km_pattern = re.compile(r'K\.?M\.?\s*|KM\s+|\bVIA\s+KM\b|\bKILOMETRO\b', re.IGNORECASE)
via_km_pattern = re.compile(r'\bVIA\s+\d+|VÍA\s+\d+|VEREDA\s+\d+', re.IGNORECASE)

casos_km = []
casos_via_km = []

for idx, addr in enumerate(all_addresses):
    if km_pattern.search(addr):
        casos_km.append((idx, addr))
    if via_km_pattern.search(addr):
        casos_via_km.append((idx, addr))

print(f"\nCasos con KM, KM VÍA o KILOMETRO: {len(casos_km)}")
if len(casos_km) > 0:
    print("Primeros 15 ejemplos:")
    for i, (idx, addr) in enumerate(casos_km[:15], 1):
        print(f"  {i:2}. {addr}")

print(f"\nCasos con VÍA + número o VEREDA: {len(casos_via_km)}")
if len(casos_via_km) > 0:
    print("Primeros 15 ejemplos:")
    for i, (idx, addr) in enumerate(casos_via_km[:15], 1):
        print(f"  {i:2}. {addr}")

# ============================================================================
# BUSQUEDA 7: Palabras después de KM (análisis de complementos)
# ============================================================================
print("\n" + "="*100)
print("[7] PALABRAS DESPUÉS DE KM (análisis de complementos)")
print("="*100)

# Buscar lo que viene después de KM
km_context = Counter()
for addr in all_addresses:
    # Encontrar KM y capturar 3 palabras después
    matches = re.findall(r'KM[.]?\s+(\d+)\s+(.+?)(?=\s+(?:BOGOTA|MEDELLIN|CALI|LOCAL|PISO|APT|OFICINA|BODEGA|$))', addr.upper())
    for match in matches:
        if len(match) > 1:
            palabras_despues = match[1].split()[:3]
            for palabra in palabras_despues:
                if len(palabra) > 2:
                    km_context[palabra] += 1

print("\nPalabras frecuentes después de KM (que podrían ser complementos):")
for palabra, count in km_context.most_common(30):
    print(f"  {palabra:20} - {count:5} veces")

# ============================================================================
# BUSQUEDA 8: Estructura de direcciones con KM
# ============================================================================
print("\n" + "="*100)
print("[8] ESTRUCTURA DE DIRECCIONES KM (analisis para normalizacion)")
print("="*100)

km_estructuras = Counter()
for idx, addr in enumerate(casos_km[:100]):  # Analizar primeros 100 casos KM
    _, address = addr
    # Capturar estructura: KM + numero + estructura
    match = re.search(r'(KM[.]?\s+\d+[\w\s]*?)(?=\s+(?:BOGOTA|MEDELLIN|CALI|LOCAL|PISO|APT|OFICINA|BODEGA|\d{5}|$))', address.upper())
    if match:
        estructura = match.group(1).strip()
        km_estructuras[estructura] += 1

print("\nEstructuras encontradas con KM:")
for estructura, count in km_estructuras.most_common(20):
    print(f"  '{estructura}' - {count} veces")

print("\nAccion recomendada: Mantener estructura KM + numero, eliminar complementos")
print("Ejemplo: 'KM 5 VIA A BOGOTA LOCAL 2' -> 'KM 5 VIA A'")

# ============================================================================
# RESUMEN Y RECOMENDACIONES
# ============================================================================
print("\n" + "="*100)
print("[RESUMEN Y RECOMENDACIONES]")
print("="*100)

print("\nRESULTADOS PRINCIPALES:")
print(f"  Casos de ACL: {len(casos_acl)}")
print(f"  Casos de ACR: {len(casos_acr)}")
print(f"  Casos de AC (tipo vía): {len(casos_ac)}")
print(f"  Casos con KM/KM VÍA: {len(casos_km)}")
print(f"  Casos con VÍA + número: {len(casos_via_km)}")

print("\nVARIACIONES SIMILARES ENCONTRADAS:")
# Identificar abreviaturas nuevas que no son las conocidas
abrev_nuevas = set()
for abrev, count in variaciones.most_common(100):
    if count >= 10:  # Al menos 10 casos
        if abrev not in ['CR', 'CL', 'CRA', 'KR', 'KM', 'AV', 'AK', 'CD', 'PZ', 'TR']:
            abrev_nuevas.add(f"{abrev} ({count})")

if abrev_nuevas:
    print("  Abreviaturas nuevas con 10+ casos:")
    for abrev in sorted(abrev_nuevas):
        print(f"    - {abrev}")
else:
    print("  No se encontraron variaciones nuevas significativas")

print("\nRECOMENDACIONES:")
if len(casos_acl) > 0:
    print(f"  1. Agregar ACL -> CL (encontrado {len(casos_acl)} casos)")
if len(casos_acr) > 0:
    print(f"  2. Agregar ACR -> KR (encontrado {len(casos_acr)} casos)")
if len(casos_km) > 0:
    print(f"  3. Normalizar KM VÍA: mantener estructura, eliminar complementos")
    print(f"     Afecta: {len(casos_km)} casos")
    print(f"     Patrón: Eliminar BOGOTA, CALI, LOCAL, PISO, APT, etc. después de estructura KM")


# ============================================================================
# EXPORTAR REPORTE
# ============================================================================
print("\n" + "="*100)
print("[EXPORTANDO REPORTE...]")
print("="*100)

with open("ANALISIS_ACL_ACR.txt", "w", encoding="utf-8") as f:
    f.write("="*100 + "\n")
    f.write("ANALISIS ESPECIFICO: ACL, ACR, VARIACIONES SIMILARES Y KM VÍA\n")
    f.write("="*100 + "\n\n")
    
    f.write("RESUMEN EJECUTIVO:\n")
    f.write(f"  Casos de ACL encontrados: {len(casos_acl)}\n")
    f.write(f"  Casos de ACR encontrados: {len(casos_acr)}\n")
    f.write(f"  Casos de AC como tipo via: {len(casos_ac)}\n")
    f.write(f"  Casos con KM/KM VÍA: {len(casos_km)}\n")
    f.write(f"  Casos con VÍA + número: {len(casos_via_km)}\n\n")
    
    if len(casos_acl) > 0:
        f.write("CASOS DE ACL:\n")
        f.write("-"*100 + "\n")
        for i, (idx, addr) in enumerate(casos_acl[:30], 1):
            f.write(f"  {i}. {addr}\n")
        f.write("\n")
    
    if len(casos_acr) > 0:
        f.write("CASOS DE ACR:\n")
        f.write("-"*100 + "\n")
        for i, (idx, addr) in enumerate(casos_acr[:30], 1):
            f.write(f"  {i}. {addr}\n")
        f.write("\n")
    
    if len(casos_ac) > 0:
        f.write("CASOS DE AC (como tipo de vía):\n")
        f.write("-"*100 + "\n")
        for i, (idx, addr) in enumerate(casos_ac[:30], 1):
            f.write(f"  {i}. {addr}\n")
        f.write("\n")
    
    f.write("VARIACIONES SIMILARES (abreviaturas 2-3 letras):\n")
    f.write("-"*100 + "\n")
    for abrev, count in variaciones.most_common(50):
        if count >= 10:
            status = ""
            if abrev in ['CR', 'CL', 'CRA', 'KR', 'KM', 'AV']:
                status = " [YA EXISTE]"
            elif abrev in ['ACL', 'ACR']:
                status = " [NUEVA - ACL/ACR]"
            elif abrev in ['AB', 'AC', 'AD', 'AF', 'AG', 'AL', 'AM', 'AP', 'AR', 'AS', 'AT', 'AZ']:
                status = " [POTENCIAL SIMILAR]"
            f.write(f"  {abrev:4} - {count:5} veces{status}\n")
    f.write("\n")
    
    f.write("ANALISIS KM VÍA:\n")
    f.write("-"*100 + "\n")
    f.write(f"Total casos con KM: {len(casos_km)}\n")
    f.write(f"Total casos con VÍA + número: {len(casos_via_km)}\n\n")
    
    f.write("Ejemplos de direcciones KM:\n")
    for i, (idx, addr) in enumerate(casos_km[:20], 1):
        f.write(f"  {i}. {addr}\n")
    f.write("\n")
    
    f.write("Estructura de direcciones KM encontradas:\n")
    for estructura, count in km_estructuras.most_common(20):
        f.write(f"  '{estructura}' - {count} veces\n")
    f.write("\n")
    
    f.write("Palabras frecuentes después de KM (complementos a eliminar):\n")
    for palabra, count in km_context.most_common(20):
        f.write(f"  {palabra:20} - {count:5} veces\n")
    f.write("\n")
    
    f.write("="*100 + "\n")
    f.write("RECOMENDACIONES FINALES:\n")
    f.write("="*100 + "\n\n")
    
    recomendaciones = []
    
    if len(casos_acl) > 0:
        recomendaciones.append(f"1. AGREGAR ACL -> CL\n   Encontrado: {len(casos_acl)} casos\n   Prioridad: MEDIA\n")
    
    if len(casos_acr) > 0:
        recomendaciones.append(f"2. AGREGAR ACR -> KR\n   Encontrado: {len(casos_acr)} casos\n   Prioridad: MEDIA\n")
    
    if len(casos_ac) > 0:
        recomendaciones.append(f"3. VERIFICAR AC -> CL\n   Encontrado: {len(casos_ac)} casos\n   Estado: Verificar si normalizacion es correcta\n")
    
    abrev_nuevas_list = []
    for abrev, count in variaciones.most_common(100):
        if count >= 50:  # Solo si son significativas
            if abrev not in ['CR', 'CL', 'CRA', 'KR', 'KM', 'AV', 'AK', 'CD', 'PZ', 'TR', 'AC']:
                abrev_nuevas_list.append(f"{abrev} ({count})")
    
    if abrev_nuevas_list:
        recomendaciones.append(f"4. REVISAR VARIACIONES SIMILARES\n   Encontradas: {len(abrev_nuevas_list)}\n   " + "\n   ".join(abrev_nuevas_list[:5]) + "\n")
    
    if len(casos_km) > 0:
        recomendaciones.append(f"5. NORMALIZAR KM VÍA (ESPECIAL)\n   Encontrado: {len(casos_km)} casos\n   Accion: Mantener estructura base (KM + número + tipo vía)\n")
        recomendaciones.append("         Eliminar complementos: CIUDAD, LOCAL, PISO, APT, OFICINA, etc.\n")
        recomendaciones.append("   Ejemplo: 'KM 5 VIA A BOGOTA LOCAL 2' -> 'KM 5 VIA A'\n")
        recomendaciones.append("   Prioridad: IMPORTANTE\n")
    
    for rec in recomendaciones:
        f.write(rec + "\n")

print("\n[OK] Reporte exportado a: ANALISIS_ACL_ACR.txt")

print("\n" + "="*100)
print("ANALISIS COMPLETADO")
print("="*100 + "\n")
