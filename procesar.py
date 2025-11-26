import pandas as pd
from normalizar_direcciones import standardize_address

# Procesar el archivo
df = pd.read_excel("direcciones.xlsx")
print(f"✓ Archivo cargado: {len(df)} filas")
print(f"✓ Columnas: {list(df.columns)}")

# Normalizar
df["Direccion Estandarizada"] = df["Direccion"].apply(standardize_address)

# Estadísticas
total = len(df)
procesadas = (df["Direccion Estandarizada"] != '').sum()

print(f"\n✓ Procesadas: {procesadas}/{total} ({100*procesadas/total:.1f}%)")
print(f"\n✓ Primeros 5 resultados:")
for i in range(min(5, len(df))):
    print(f"  {i+1}. {df['Direccion'].iloc[i]} -> {df['Direccion Estandarizada'].iloc[i]}")

# Guardar
df.to_excel("direcciones_normalizadas.xlsx", index=False)
print(f"\n✓ Archivo guardado: direcciones_normalizadas.xlsx")
