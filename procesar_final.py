#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import sys
from normalizar_direcciones import standardize_address

# Procesar el archivo Excel
input_file = "direcciones.xlsx"
output_file = "direcciones_normalizadas.xlsx"

try:
    # Procesar
    df = pd.read_excel(input_file)
    df["Direccion Estandarizada"] = df["Direccion"].apply(standardize_address)
    
    # Estadísticas
    total = len(df)
    procesadas = (df["Direccion Estandarizada"] != '').sum()
    rechazadas = total - procesadas
    
    # Guardar a archivo de log
    with open("reporte_procesamiento.txt", "w", encoding="utf-8") as f:
        f.write("=" * 100 + "\n")
        f.write("PROCESAMIENTO DE ARCHIVO EXCEL\n")
        f.write("=" * 100 + "\n\n")
        
        f.write(f"✓ Archivo cargado: {len(df)} filas\n")
        f.write(f"✓ Columnas: {list(df.columns)}\n\n")
        
        f.write("✅ RESULTADOS:\n")
        f.write(f"   Total de direcciones:         {total}\n")
        f.write(f"   Procesadas exitosamente:      {procesadas} ({100*procesadas/total:.1f}%)\n")
        f.write(f"   Rechazadas/No procesadas:     {rechazadas} ({100*rechazadas/total:.1f}%)\n\n")
        
        f.write("📋 PRIMEROS 15 EJEMPLOS:\n")
        f.write("-" * 100 + "\n")
        for i in range(min(15, len(df))):
            orig = str(df["Direccion"].iloc[i])[:50]
            norm = str(df["Direccion Estandarizada"].iloc[i])[:50]
            status = "✓" if norm else "✗"
            f.write(f"{i+1:2d}. {status} '{orig}' -> '{norm}'\n")
        
        f.write("\n⚠️  EJEMPLOS DE DIRECCIONES RECHAZADAS (primeras 10):\n")
        f.write("-" * 100 + "\n")
        rechazadas_df = df[df["Direccion Estandarizada"] == ""]
        for i, (idx, row) in enumerate(rechazadas_df.head(10).iterrows()):
            orig = str(row["Direccion"])[:70]
            f.write(f"{i+1:2d}. '{orig}'\n")
        
        f.write("\n" + "=" * 100 + "\n")
    
    # Guardar Excel
    df.to_excel(output_file, index=False)
    
    print("✓ Procesamiento completado exitosamente")
    print("✓ Reporte guardado en: reporte_procesamiento.txt")
    print("✓ Excel guardado en: " + output_file)

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
