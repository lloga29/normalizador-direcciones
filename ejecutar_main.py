#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os
import sys
from normalizar_direcciones import standardize_address

# Usar el archivo local
input_file = "direcciones.xlsx"
output_file = "direcciones_normalizadas.xlsx"
column_name = "Direccion"

try:
    if not os.path.exists(input_file):
        print(f"ERROR: El archivo {input_file} no existe")
        sys.exit(1)
    
    print(f"📂 Leyendo archivo: {input_file}")
    df = pd.read_excel(input_file)
    
    print(f"📊 Columnas encontradas: {list(df.columns)}")
    print(f"📈 Total de filas: {len(df)}")
    
    if column_name not in df.columns:
        print(f"ERROR: La columna '{column_name}' no existe")
        print(f"Columnas disponibles: {list(df.columns)}")
        sys.exit(1)
    
    print(f"\n⏳ Procesando {len(df)} direcciones...")
    df["Direccion Estandarizada"] = df[column_name].apply(standardize_address)
    
    # Estadísticas
    total = len(df)
    procesadas = (df["Direccion Estandarizada"] != '').sum()
    rechazadas = total - procesadas
    
    print(f"\n✅ RESULTADOS:")
    print(f"   Direcciones procesadas: {procesadas}/{total} ({100*procesadas/total:.1f}%)")
    print(f"   Direcciones rechazadas: {rechazadas}/{total} ({100*rechazadas/total:.1f}%)")
    
    # Mostrar primeros ejemplos
    print(f"\n📋 Primeros 10 ejemplos:")
    for i, row in df.head(10).iterrows():
        orig = str(row[column_name])[:40]
        norm = str(row["Direccion Estandarizada"])[:40]
        print(f"   {i+1}. '{orig}' -> '{norm}'")
    
    # Guardar
    df.to_excel(output_file, index=False)
    print(f"\n💾 Archivo generado: {output_file}")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
