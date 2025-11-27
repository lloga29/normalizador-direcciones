import pandas as pd
import re
import os

def normalize_via_type(s: str) -> str:
    """
    Normaliza el tipo de vía a abreviaturas estándar.
    """
    s_upper = s.upper()
    
    # Mapeo de tipos de vía - ACTUALIZADO: ACL->CL, ACR->KR
    if s_upper in ['CALLE', 'CLL', 'CL', 'CALL', 'AC', 'ACL']:
        return 'CL'
    elif s_upper in ['CARRERA', 'CRA', 'KRA', 'KR', 'CARR', 'AK', 'K', 'ACR']:
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
    5. ESPECIAL: Normaliza KM VÍA manteniendo estructura base, eliminando complementos
    6. ESPECIAL: Normaliza direcciones de AUTOPISTAS (AUT, AUTO, etc.) manteniendo estructura
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
    
    # ===== MANEJO ESPECIAL PARA AUTOPISTAS =====
    # Detectar si comienza con AUT, AUTO, AUT., AUTOMÁTICO, etc.
    # Manejo especial para variantes: AUTO (con espacio), AUTOXXXXXX (pegado), AUTONORTE, etc.
    
    # Primero eliminar ciudades al inicio si van seguidas de autopista
    s = re.sub(r'^(BOGOTA|CALI|MEDELLIN|BARRANQUILLA|CHIA|FUNZA|COTA|RIONEGRO|BUCARAMANGA|SOLEDAD)\s+(?=(?:AUTOPISTA|AUT\.?|AUTO(?:P|PISTA)?|AUTO[A-Z]+|AUT[A-Z]+))', '', s, flags=re.IGNORECASE).strip()
    
    # Luego limpiar errores de escritura: AUTO PISTA -> AUTO, AUTOP -> AUTO
    s = re.sub(r'\bAUTO\s+PISTA\b', 'AUTO', s, flags=re.IGNORECASE)
    s = re.sub(r'\bAUTOP\b', 'AUTO', s, flags=re.IGNORECASE)
    
    # Detectar si es una autopista (AUT, AUTO, AUTOPISTA)
    aut_check = re.match(r'^(?:AUTOPISTA|AUT\.?|AUTO(?:PISTA)?\.?|AUTO[A-Z]+|AUT[A-Z]+)', s, re.IGNORECASE)
    
    if aut_check:
        # Es una dirección de autopista
        aut_name = None
        resto_aut = None
        
        # Primer intento: capturar AUTOPISTA. o AUT. o AUTO. (con punto o palabra completa)
        prefijo_match = re.match(r'^(AUTOPISTA\.?|AUT\.|AUTO\.)\s*(.+)$', s, re.IGNORECASE)
        if prefijo_match:
            resto_aut = prefijo_match.group(2).strip()
        else:
            # Segundo intento: capturar AUTO[PALABRAS] o AUT[PALABRAS] (pegado sin espacios)
            prefijo_match = re.match(r'^(AUTO[A-Z]+|AUT[A-Z]+)\s*(.+)?$', s, re.IGNORECASE)
            if prefijo_match:
                aut_prefix = prefijo_match.group(1)
                resto_aut = prefijo_match.group(2)
                
                # Extraer el nombre de la autopista desde el prefijo pegado
                # Ej: AUTONORTE -> NORTE, AUTOMEDELLIN -> MEDELLIN, AUTOMED -> MED
                if aut_prefix.upper().startswith('AUTO'):
                    aut_name = aut_prefix[4:]  # Quitar "AUTO"
                elif aut_prefix.upper().startswith('AUT'):
                    aut_name = aut_prefix[3:]  # Quitar "AUT"
                
                # Si no hay resto, solo retornar el nombre de la autopista
                if not resto_aut:
                    return f"AUTOPISTA {aut_name}"
            else:
                # Tercer intento: capturar AUTOPISTA o AUTO o AUT seguido de espacio
                prefijo_match = re.match(r'^(AUTOPISTA|AUTO|AUT)\s+(.+)$', s, re.IGNORECASE)
                if prefijo_match:
                    resto_aut = prefijo_match.group(2).strip()
        
        # Si tenemos resto_aut pero no aut_name (casos con espacio), extraer el nombre
        if resto_aut and not aut_name:
            # Extraer solo la primera palabra como nombre de la autopista
            palabras = resto_aut.split()
            if palabras:
                aut_name = palabras[0]
                resto_aut = ' '.join(palabras[1:]) if len(palabras) > 1 else ''
        
        # Si tenemos resto_aut, procesarlo
        if resto_aut:
            # Si no tenemos aut_name, extraerlo de resto_aut
            if not aut_name:
                # Buscar patrón de KM primero para extraer el nombre
                km_in_aut_pattern = re.compile(r'^(.+?)(?:KM|K\.M\.?|KILOMETRO)\s*(\d+[.\d]*)\s*(.+)?', re.IGNORECASE)
                km_in_aut = km_in_aut_pattern.search(resto_aut)
                
                if km_in_aut:
                    aut_name = km_in_aut.group(1).strip()
                else:
                    # Extraer primeras palabras como nombre
                    nombre_pattern = re.compile(r'^([A-Z]+(?:\s+[A-Z]+)?)(?:\s+|$)', re.IGNORECASE)
                    nombre_match = nombre_pattern.match(resto_aut)
                    aut_name = nombre_match.group(1).strip() if nombre_match else resto_aut
            
            # Buscar patrón de KM dentro (incluyendo casos como "4KM" sin espacio)
            km_in_aut_pattern = re.compile(r'(?:(\d+)\s*(?:KM|K\.M\.?|KILOMETRO)|(?:KM|K\.M\.?|KILOMETRO)\s*(\d+[.\d]*))\s*(.+)?', re.IGNORECASE)
            km_in_aut = km_in_aut_pattern.search(resto_aut)
            
            if km_in_aut:
                # Tiene formato: [NOMBRE_AUTOPISTA] KM [numero] [resto]
                km_num = km_in_aut.group(1) if km_in_aut.group(1) else km_in_aut.group(2)
                resto_km = km_in_aut.group(3).strip() if km_in_aut.group(3) else ''
                
                # Limpiar resto_km de descriptivos
                resto_km = re.sub(r'\b(BOGOTA|CALI|MEDELLIN|LOCAL|BODEGA|PISO|PARQUE|COSTADO|GLORIETA|SIBERIA|PARCELAS)\b', '', resto_km, flags=re.IGNORECASE).strip()
                resto_km = re.sub(r'\s+', ' ', resto_km).strip()
                
                # Buscar tipo de vía en lo que sigue después del KM
                if resto_km:
                    via_pattern = re.compile(r'\b(CALLE|CLL|CL|CALL|CARRERA|CRA|KRA|KR|AK|K|AVENIDA|AV|AVD|AVDA|AVE|DIAGONAL|DG|DIAG|TRANSVERSAL|TV|TRANSV|TR|AC|ACL|ACR|PASAJE|PAS|PASEO|VEREDA|VDA|VIA)\b', re.IGNORECASE)
                    via_match = via_pattern.search(resto_km)
                    
                    if via_match:
                        via_type = normalize_via_type(via_match.group(1))
                        return f"AUTOPISTA {aut_name} KM {km_num} {via_type}"
                    else:
                        return f"AUTOPISTA {aut_name} KM {km_num}"
                else:
                    return f"AUTOPISTA {aut_name} KM {km_num}"
            else:
                # No tiene KM, buscar si tiene números o tipo de vía
                # Eliminar complementos y descriptivos del resto (múltiples pasadas)
                resto_limpio = resto_aut
                
                # Primera pasada: eliminar todas las palabras descriptivas
                descriptivos_aut = r'\b(NO|N|NUM|NR|NUMERO|GLORIETA|SIBERIA|CENTRO|COMERCIAL|EMPRESARIAL|ENTRADA|COSTADO|INTERIOR|CRUCE|CONECTOR|BOGOTA|CALI|MEDELLIN|LOCAL|BODEGA|PISO|ZONA|OFICINA|LOTE|MODULO|BD|BOD|BG|OFC|LC|LOC|ENT|INT|PARQUE|BODEGAS|TERMINALES?|COORDEN|COORD|SOBRE|VEREDA|SUR|NORTE|ESTE|OESTE)\b'
                for _ in range(2):  # Dos pasadas para asegurar limpieza
                    resto_limpio = re.sub(descriptivos_aut, ' ', resto_limpio, flags=re.IGNORECASE)
                
                resto_limpio = resto_limpio.strip()
                resto_limpio = re.sub(r'\s+', ' ', resto_limpio).strip()
                
                # Reemplazar símbolos por espacios
                resto_limpio = re.sub(r'[#\-\.]+', ' ', resto_limpio)
                resto_limpio = re.sub(r'\s+', ' ', resto_limpio).strip()
                
                # Buscar patrón: [TIPO] [num] [num] o directamente números
                if resto_limpio:
                    via_pattern = re.compile(r'\b(CALLE|CLL|CL|CALL|CARRERA|CRA|KRA|KR|AK|K|AVENIDA|AV|AVD|AVDA|AVE|DIAGONAL|DG|DIAG|TRANSVERSAL|TV|TRANSV|TR|AC|ACL|ACR|PASAJE|PAS|PASEO)\s+([A-Z0-9]+)\s+([A-Z0-9]+)', re.IGNORECASE)
                    via_match = via_pattern.search(resto_limpio)
                    
                    if via_match:
                        via_type = normalize_via_type(via_match.group(1))
                        num1 = via_match.group(2).strip().split()[0]
                        num2 = via_match.group(3).strip().split()[0]
                        return f"AUTOPISTA {aut_name} {via_type} {num1} {num2}"
                    else:
                        # Buscar solo números
                        numeros = re.findall(r'\b\d+(?:[A-Z]?)(?:\.\d+)?\b', resto_limpio)
                        if len(numeros) >= 2:
                            return f"AUTOPISTA {aut_name} {numeros[0]} {numeros[1]}"
                        elif len(numeros) == 1:
                            return f"AUTOPISTA {aut_name} {numeros[0]}"
            
            # Si llegamos aquí sin retornar, solo retornar el nombre de la autopista
            return f"AUTOPISTA {aut_name}" if aut_name else ""
    
    # ===== MANEJO ESPECIAL PARA KM VÍA =====
    # Detectar si es una dirección de KM VÍA (formato: ... KM <numero> VIA/VEREDA ... CIUDAD ...)
    km_pattern = re.compile(r'^(.*?)(?:KM|K\.M\.?|KILOMETRO)\s+(\d+[.\d]*)\s+(.+?)(?=\s+(?:BOGOTA|MEDELLIN|CALI|BARRANQUILLA|LOCAL|PISO|APT|OFICINA|BODEGA|ZONA|SOTANO|$))', re.IGNORECASE)
    km_match = km_pattern.search(s)
    
    if km_match:
        # Es una dirección de KM VÍA
        km_num = km_match.group(2)
        resto_despues_km = km_match.group(3).strip()
        
        # Buscar el tipo de vía después del KM
        via_pattern = re.compile(r'\b(CALLE|CLL|CL|CALL|CARRERA|CRA|KRA|KR|AK|K|AVENIDA|AV|AVD|AVDA|AVE|DIAGONAL|DG|DIAG|TRANSVERSAL|TV|TRANSV|TR|AC|ACL|ACR|PASAJE|PAS|PASEO|VEREDA|VDA|VIA)\s+(.+)', re.IGNORECASE)
        via_match = via_pattern.search(resto_despues_km)
        
        if via_match:
            via_type = normalize_via_type(via_match.group(1))
            via_numero = via_match.group(2).strip().split()[0]  # Tomar solo el primer elemento
            return f"KM {km_num} {via_type} {via_numero}"
        else:
            # Solo KM + número, sin tipo de vía claro
            return f"KM {km_num}"
    
    # Reemplazar símbolos comunes por espacios
    s = re.sub(r'[#\-,;.()]+', ' ', s)
    
    # Eliminar números que parecen coordenadas GPS (muchos decimales)
    s = re.sub(r'\b\d+\.\d{5,}\b', ' ', s)
    
    # Reemplazar variaciones de "No." o "Nº"
    s = re.sub(r'\b(N[OÓº°]|NO|NR|NUM)\b', ' ', s, flags=re.IGNORECASE)
    
    # Eliminar palabras descriptivas - ACTUALIZADO CON NUEVAS VARIACIONES
    descriptivos = r'\b(LOCAL|LOCALES|L\d+|CENTRO|COMERCIAL|COMERCIAR|PISO|APTO|APT|APARTAMENTO|OFICINA|OF|OFC|OFI|INTERIOR|INT|BODEGA|BOD|BODEGAS|CASA|EDIFICIO|ED|ATRIO|TORRE|TO|BLOQUE|BL|BLQ|MZ|MANZANA|BARRIO|CONJUNTO|CONJ|ETAPA|PARQUE|TERMINAL|PUENTE|AEREO|SUR|NORTE|ESTE|OESTE|COSTADO|FRENTE|ESQUINA|ESQ|LAS|LOS|LA|LD|LOTE|LOTES|FASE|MODULO|MOD|SUBLOTE|SECTOR|SECT|KM|KILOMETRO|KILOMETROS|DEL|DE|EN|BODEGAS|ARTURO|CUMPLIDO|TOLU|PARCELAS|COTA|ES|DIRECCION|A|MTS|ADELANTE|PEAJE|PUERTAS|DON|DIEGO|LLANOGRANDE|ACOPI|ACACIAS|RANSA|COLFRIGOS|SUBA|CALI|MIECO|ERNESTO|CORTIZZOS|CAMILA|DAZA|ADMINISTRATIVO|ACTUAL|AENIDA|NRO|TRADE|PARK|SIBERIA|VIAL|BRICENO|PALERMO|ANILLO|VEREDA|VDA|GIRON|VIA|AUTOPISTA|LC|LOC|DG|BA|CD|PI|PZ|BIS|BD|AL|TRV|BOG|PS|LT|LO|IN|AP|CON|AN|BDG|PAGINA|LINCA|NIVEL)\b'
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
    pattern_con_tipo = r'\b(CALLE|CLL|CL|CALL|CARRERA|CRA|KRA|KR|AK|K|AVENIDA|AV|AVD|AVDA|AVE|DIAGONAL|DG|DIAG|TRANSVERSAL|TV|TRANSV|TR|AC|ACL|ACR|CIRCULAR|CIRC|PASAJE|PAS|PASEO|PEATONAL|PTE|PERIF|CTRA|VEREDA|VDA|VIA)\s+([A-Z0-9]+)\s+([A-Z0-9]+)(?:\s+([A-Z0-9]+))?(?:\s+([A-Z0-9]+))?'
    
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
