from normalizar_direcciones import standardize_address
import re

# Caso problemático
entrada = "Vereda El Palmar"

print("=" * 80)
print(f"ANÁLISIS DETALLADO: '{entrada}'")
print("=" * 80)

# Simular paso a paso lo que hace la función
s = str(entrada).strip().upper()
print(f"1. Original en mayúsculas: '{s}'")

# Reemplazar símbolos
s = re.sub(r'[#\-,;.()]+', ' ', s)
print(f"2. Después de limpiar símbolos: '{s}'")

# Eliminar decimales
s = re.sub(r'\b\d+\.\d{5,}\b', ' ', s)
print(f"3. Después de limpiar decimales: '{s}'")

# Reemplazar NO, Nº, etc
s = re.sub(r'\b(N[OÓº°]|NO|NR|NUM)\b', ' ', s, flags=re.IGNORECASE)
print(f"4. Después de limpiar No./Nº: '{s}'")

# Eliminar descriptivos
descriptivos = r'\b(LOCAL|LOCALES|L\d+|CENTRO|COMERCIAL|COMERCIAR|PISO|APTO|APT|APARTAMENTO|OFICINA|OF|INTERIOR|INT|BODEGA|CASA|EDIFICIO|ED|ATRIO|TORRE|TO|BLOQUE|BL|BLQ|MZ|MANZANA|BARRIO|CONJUNTO|CONJ|ETAPA|PARQUE|TERMINAL|PUENTE|AEREO|SUR|NORTE|ESTE|OESTE|COSTADO|FRENTE|ESQUINA|ESQ|LAS|LOS|LA|LD|LOTE|LOTES|FASE|MODULO|MOD|SUBLOTE|SECTOR|SECT|KM|KILOMETRO|KILOMETROS|DEL|DE|EN|BODEGAS|ARTURO|CUMPLIDO|TOLU|PARCELAS|COTA|ES|DIRECCION|A|MTS|ADELANTE|PEAJE|PUERTAS|DON|DIEGO|LLANOGRANDE)\b'
s = re.sub(descriptivos, ' ', s, flags=re.IGNORECASE)
print(f"5. Después de limpiar descriptivos: '{s}'")

# Eliminar ciudades
ciudades = r'\b(BOGOTA|CALI|MEDELLIN|BARRANQUILLA|CARTAGENA|SIN CIUDAD|SINCELEJO|YUMBO|CHIA|FUNZA|COTA|IBAGUE|PEREIRA|MANIZALES|BUCARAMANGA|SANTA MARTA|VALLEDUPAR|RIONEGRO|CAJICA|MADRID|FACATATIVA|SOACHA|VILLAVICENCIO|DUITAMA|SOGAMOSO|TUNJA|GIRARDOTA|SABANETA|ENVIGADO|SONSON|RIOHACHA|GALAP|ZOFIA|FRANCA|CIUDAD|CART|MERCADO|ZONA|AERO|COMPLEJO|INDUSTRIAL|COMERCIAL|CIC|JARDIN|SOTANO|BUENAVISTA)\b'
s = re.sub(ciudades, ' ', s, flags=re.IGNORECASE)
print(f"6. Después de limpiar ciudades: '{s}'")

# Compactar espacios
s = re.sub(r'\s+', ' ', s).strip()
print(f"7. Después de compactar espacios: '{s}'")

# Buscar patrón CON TIPO de vía
pattern_con_tipo = r'\b(CALLE|CLL|CL|CALL|CARRERA|CRA|KRA|KR|AK|K|AVENIDA|AV|AVD|AVDA|AVE|DIAGONAL|DG|DIAG|TRANSVERSAL|TV|TRANSV|TR|AC|CIRCULAR|CIRC|PASAJE|PAS|PASEO|PEATONAL|PTE|PERIF|CTRA|VEREDA|VDA|VIA)\s+([A-Z0-9]+)\s+([A-Z0-9]+)(?:\s+([A-Z0-9]+))?(?:\s+([A-Z0-9]+))?'
match = re.search(pattern_con_tipo, s, re.IGNORECASE)
print(f"\n8. ¿Coincide con PATRÓN 1 (TIPO_VIA + NÚMEROS)? {bool(match)}")
if match:
    print(f"   Grupos: {match.groups()}")

# Buscar patrón SIN TIPO (solo números)
pattern_numeros = r'^([A-Z0-9]+)\s+([A-Z0-9]+)(?:\s+([A-Z0-9]+))?'
match2 = re.search(pattern_numeros, s)
print(f"\n9. ¿Coincide con PATRÓN 2 (SIN TIPO, solo números)? {bool(match2)}")
if match2:
    print(f"   Grupos: {match2.groups()}")
    num1 = match2.group(1)
    num2 = match2.group(2)
    patron_digito = r'\d'
    es_num1_digito = bool(re.match(patron_digito, num1))
    es_num2_digito = bool(re.match(patron_digito, num2))
    print(f"   num1='{num1}' ¿empieza con dígito? {es_num1_digito}")
    print(f"   num2='{num2}' ¿empieza con dígito? {es_num2_digito}")

# Resultado final
resultado = standardize_address(entrada)
print(f"\n10. Resultado final: '{resultado}'")
print("\n⚠️  El problema es que VEREDA quedó con EL PALMAR, ambos parecen componentes válidos.")
print("    Se detecta como PATRÓN 1 (VEREDA + EL + PALMAR).")
