#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from normalizar_direcciones import standardize_address

# Procesar el archivo Excel
input_file = "direcciones.xlsx"
output_file = "direcciones_normalizadas.xlsx"

print("=" * 100)
print("PROCESAMIENTO DE ARCHIVO EXCEL")
print("=" * 100)

df = pd.read_excel(input_file)
print(f"\n✓ Archivo cargado: {len(df)} filas")
print(f"✓ Columnas encontradas: {list(df.columns)}")

# Normalizar
print(f"\n⏳ Normalizando direcciones...")
df["Direccion Estandarizada"] = df["Direccion"].apply(standardize_address)

# Estadísticas
total = len(df)
procesadas = (df["Direccion Estandarizada"] != '').sum()
rechazadas = total - procesadas

print(f"\n✅ RESULTADOS DE PROCESAMIENTO:")
print(f"   Total de direcciones:          {total}")
print(f"   Procesadas exitosamente:       {procesadas} ({100*procesadas/total:.1f}%)")
print(f"   Rechazadas/No procesadas:      {rechazadas} ({100*rechazadas/total:.1f}%)")

# Mostrar primeros 15 ejemplos
print(f"\n📋 PRIMEROS 15 EJEMPLOS:")
print("-" * 100)
for i in range(min(15, len(df))):
    orig = str(df["Direccion"].iloc[i])[:50]
    norm = str(df["Direccion Estandarizada"].iloc[i])[:50]
    status = "✓" if norm else "✗"
    print(f"{i+1:2d}. {status} '{orig}' -> '{norm}'")

# Mostrar ejemplos de direcciones rechazadas
print(f"\n⚠️  EJEMPLOS DE DIRECCIONES RECHAZADAS (primeras 10):")
print("-" * 100)
rechazadas_df = df[df["Direccion Estandarizada"] == ""]
for i, (idx, row) in enumerate(rechazadas_df.head(10).iterrows()):
    orig = str(row["Direccion"])[:70]
    print(f"{i+1:2d}. '{orig}'")

# Guardar resultado
df.to_excel(output_file, index=False)
print(f"\n💾 Archivo generado exitosamente: {output_file}")
print("=" * 100)
