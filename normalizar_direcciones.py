import pandas as pd
import re
import os

def normalize_via_type(s: str) -> str:
    """
    Normaliza el tipo de vía a abreviaturas estándar.
    """
    s_upper = s.upper()
    
    # Mapeo de tipos de vía
    if s_upper in ['CALLE', 'CLL', 'CL', 'CALL', 'AC','ACL']:
        return 'CL'
    elif s_upper in ['CARRERA', 'CRA', 'KRA', 'KR', 'CARR', 'AK', 'K']:
        return 'KR'
    elif s_upper in ['AVENIDA', 'AV', 'AVD', 'AVDA', 'AVE']:
        return 'AV'
    elif s_upper in ['DIAGONAL', 'DG', 'DIAG']:
        return 'DG'
    elif s_upper in ['TRANSVERSAL', 'TV', 'TRANSV', 'TR']:
        return 'TV'
    else:
        return s_upper


def standardize_address(address: str) -> str:
    """
    Estandariza direcciones colombianas a formato: TIPO NUM NUM [NUM]
    Estrategia:
    1. Limpia símbolos y descriptivos
    2. Busca patrón TIPO_VIA + NUMEROS
    3. Si no encuentra tipo de vía, toma los primeros números como si fuera una calle
    4. Rechaza valores que parecen ser coordenadas GPS
    """
    if pd.isna(address):
        return ''
    
    s = str(address).strip()
    if not s or s.lower() in ['nan', '00', 'none', '']:
        return ''
    
    original = s
    s = s.upper()
    
    # RECHAZO RÁPIDO: Si tiene muchas coordenadas GPS (patrones como "10.123456  74.654321")
    # Cuenta cuántos números decimales hay
    decimal_count = len(re.findall(r'\d+\.\d+', s))
    if decimal_count >= 2:  # Probablemente son coordenadas GPS
        return ''
    
    # Reemplazar símbolos comunes por espacios
    s = re.sub(r'[#\-,;.()]+', ' ', s)
    
    # Eliminar números que parecen coordenadas GPS (muchos decimales)
    s = re.sub(r'\b\d+\.\d{5,}\b', ' ', s)
    
    # Reemplazar variaciones de "No." o "Nº"
    s = re.sub(r'\b(N[OÓº°]|NO|NR|NUM)\b', ' ', s, flags=re.IGNORECASE)
    
    # Eliminar palabras descriptivas (PERO NO VIA)
    descriptivos = r'\b(LOCAL|LOCALES|L\d+|CENTRO|COMERCIAL|COMERCIAR|PISO|APTO|APT|APARTAMENTO|OFICINA|OF|INTERIOR|INT|BODEGA|CASA|EDIFICIO|ED|ATRIO|TORRE|TO|BLOQUE|BL|BLQ|MZ|MANZANA|BARRIO|CONJUNTO|CONJ|ETAPA|PARQUE|TERMINAL|PUENTE|AEREO|SUR|NORTE|ESTE|OESTE|COSTADO|FRENTE|ESQUINA|ESQ|LAS|LOS|LA|LD|LOTE|LOTES|FASE|MODULO|MOD|SUBLOTE|SECTOR|SECT|KM|KILOMETRO|KILOMETROS|DEL|DE|EN|BODEGAS|ARTURO|CUMPLIDO|TOLU|PARCELAS|COTA|ES|DIRECCION|A|MTS|ADELANTE|PEAJE|PUERTAS|DON|DIEGO|LLANOGRANDE|ACOPI|ACACIAS|RANSA|COLFRIGOS|SUBA|CALI|MIECO|ERNESTO|CORTIZZOS|CAMILA|DAZA|ADMINISTRATIVO|ACTUAL|AENIDA)\b'
    s = re.sub(descriptivos, ' ', s, flags=re.IGNORECASE)
    
    # Eliminar ciudades/lugares
    ciudades = r'\b(BOGOTA|CALI|MEDELLIN|BARRANQUILLA|CARTAGENA|SIN CIUDAD|SINCELEJO|YUMBO|CHIA|FUNZA|COTA|IBAGUE|PEREIRA|MANIZALES|BUCARAMANGA|SANTA MARTA|VALLEDUPAR|RIONEGRO|CAJICA|MADRID|FACATATIVA|SOACHA|VILLAVICENCIO|DUITAMA|SOGAMOSO|TUNJA|GIRARDOTA|SABANETA|ENVIGADO|SONSON|RIOHACHA|GALAP|ZOFIA|FRANCA|CIUDAD|CART|MERCADO|ZONA|AERO|COMPLEJO|INDUSTRIAL|COMERCIAL|CIC|JARDIN|SOTANO|BUENAVISTA|AEROPUERTO|AEREOPUERTO|AEREROPUERTO|AEROPUERTI|CARGO)\b'
    s = re.sub(ciudades, ' ', s, flags=re.IGNORECASE)
    
    # Compactar espacios
    s = re.sub(r'\s+', ' ', s).strip()
    
    if not s or len(s) < 1:
        return ''
    
    # PATRÓN 1: Buscar TIPO_VIA explícito + NUMEROS (flexible con espacios)
    # Permite múltiples espacios y captura hasta 4 componentes numéricos
    pattern_con_tipo = r'\b(CALLE|CLL|CL|CALL|CARRERA|CRA|KRA|KR|AK|K|AVENIDA|AV|AVD|AVDA|AVE|DIAGONAL|DG|DIAG|TRANSVERSAL|TV|TRANSV|TR|AC|CIRCULAR|CIRC|PASAJE|PAS|PASEO|PEATONAL|PTE|PERIF|CTRA|VEREDA|VDA|VIA)\s+([A-Z0-9]+)\s+([A-Z0-9]+)(?:\s+([A-Z0-9]+))?(?:\s+([A-Z0-9]+))?'
    
    match = re.search(pattern_con_tipo, s, re.IGNORECASE)
    
    if match:
        via_type = normalize_via_type(match.group(1))
        num1 = match.group(2)
        num2 = match.group(3)
        num3 = match.group(4) if match.group(4) else ''
        num4 = match.group(5) if match.group(5) else ''
        
        # VALIDACIÓN: Verificar que al menos uno de los componentes sea principalmente numérico
        # Esto evita procesar "VEREDA EL PALMAR" como si fuera una dirección válida
        has_numbers = (re.match(r'\d', num1) or re.match(r'\d', num2) or 
                      (num3 and re.match(r'\d', num3)))
        
        if has_numbers:
            # Retornar máximo 3 componentes (tipo + 2 ó 3 números)
            if num3:
                return f"{via_type} {num1} {num2} {num3}"
            else:
                return f"{via_type} {num1} {num2}"
    
    # PATRÓN 2: Si no encuentra tipo explícito, busca al menos 2 bloques numéricos
    # pero SOLO si parecen direcciones, no coordenadas
    pattern_numeros = r'^([A-Z0-9]+)\s+([A-Z0-9]+)(?:\s+([A-Z0-9]+))?'
    match2 = re.search(pattern_numeros, s)
    
    if match2:
        num1 = match2.group(1)
        num2 = match2.group(2)
        num3 = match2.group(3) if match2.group(3) else ''
        
        # Solo retornar si:
        # 1. Los primeros 2 componentes son principalmente numéricos
        # 2. NO tienen más de 10 dígitos (eso sería datos raros/GPS)
        if (re.match(r'\d', num1) and re.match(r'\d', num2) and
            len(num1) <= 10 and len(num2) <= 10):
            if num3:
                return f"{num1} {num2} {num3}"
            else:
                return f"{num1} {num2}"
    
    return ''


def main():
    input_file = "Nits_ciudad.xlsx"
    output_file = "Nits_ciudad_normalizadas.xlsx"
    column_name = "Direccion"  # cambia si tu columna tiene otro nombre

    # Validar que el archivo de entrada existe
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"El archivo de entrada no existe: {input_file}")

    print(f"Leyendo archivo: {input_file}")
    df = pd.read_excel(input_file)

    if column_name not in df.columns:
        raise ValueError(f"La columna '{column_name}' no existe en el archivo de entrada.")

    print(f"Procesando {len(df)} direcciones...")
    df["Direccion Estandarizada"] = df[column_name].apply(standardize_address)
    
    # Mostrar estadísticas
    total = len(df)
    procesadas = (df["Direccion Estandarizada"] != '').sum()
    print(f"Direcciones procesadas exitosamente: {procesadas}/{total} ({procesadas/total*100:.1f}%)")

    df.to_excel(output_file, index=False)
    print(f"Archivo generado: {output_file}")


if __name__ == "__main__":
    main()
