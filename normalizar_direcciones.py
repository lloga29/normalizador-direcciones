import os
import re
from typing import Optional

import pandas as pd

# --- Tipos de vía normalizados y variantes conocidas ---
VIA_NORMALIZATION = {
    # Calles / carreras
    "CALLE": "CL",
    "CLL": "CL",
    "CL": "CL",
    "CALL": "CL",
    "AC": "CL",
    "ACL": "CL",
    "CARRERA": "KR",
    "CRA": "KR",
    "KRA": "KR",
    "KR": "KR",
    "CARR": "KR",
    "AK": "KR",
    "K": "KR",
    "ACR": "KR",
    # Avenidas
    "AVENIDA": "AV",
    "AENIDA": "AV",
    "AV": "AV",
    "AVD": "AV",
    "AVDA": "AV",
    "AVE": "AV",
    # Diagonales / transversales
    "DIAGONAL": "DG",
    "DG": "DG",
    "DIAG": "DG",
    "TRANSVERSAL": "TV",
    "TRANSV": "TV",
    "TR": "TV",
    "TRV": "TV",
    "TV": "TV",
    # Circunvalares
    "CIRCUNVALAR": "CIRC",
    "CIRCUNV": "CIRC",
    "CIRCUNVAL": "CIRC",
    "CIRCULAR": "CIRC",
    "CIRC": "CIRC",
    # Otros tipos
    "PASAJE": "PS",
    "PAS": "PS",
    "PASEO": "PS",
    "PEATONAL": "PS",
    "PTE": "PS",
    "PERIF": "PS",
    "CTRA": "PS",
    "VEREDA": "VDA",
    "VDA": "VDA",
    "VIA": "VIA",
}

# --- Listas de control y patrones reutilizables ---
CITY_NAMES = [
    "ACACIAS",
    "AGUACHICA",
    "AGUAZUL",
    "ANAPOIMA",
    "ANSERMA",
    "APARTADO",
    "ARMENIA",
    "BARANOA",
    "BARBOSA",
    "BARRANCABERMEJA",
    "BARRANQUILLA",
    "BELEN DE UMBRIA",
    "BELLO",
    "BOGOTA",
    "BOLIVAR",
    "BRICENO",
    "BUCARAMANGA",
    "BUENAVENTURA",
    "BUGA",
    "CAJICA",
    "CALARCA",
    "CALDAS",
    "CALI",
    "CAMPOALEGRE",
    "CARTAGENA",
    "CARTAGO",
    "CAUCASIA",
    "CERETE",
    "CHAPARRAL",
    "CHIA",
    "CHINCHINA",
    "CHIQUINQUIRA",
    "CIENAGA",
    "CODAZZI",
    "COPACABANA",
    "COTA",
    "CUCUNUBA",
    "CUCUTA",
    "DOSQUEBRADAS",
    "DUITAMA",
    "ENVIGADO",
    "ESPINAL",
    "FACATATIVA",
    "FLANDES",
    "FLORENCIA",
    "FLORIDA",
    "FLORIDABLANCA",
    "FUNDACION",
    "FUNZA",
    "FUSAGASUGA",
    "GALAPA",
    "GARZON",
    "GIRARDOT",
    "GIRARDOTA",
    "GIRON",
    "GRANADA",
    "GUARNE",
    "GUAYMARAL",
    "IBAGUE",
    "IPIALES",
    "ITAGUI",
    "JAMUNDI",
    "LA CALERA",
    "LA CEJA",
    "LA DORADA",
    "LA ESTRELLA",
    "LA MESA",
    "LA PINTADA",
    "LA VEGA",
    "LEBRIJA",
    "MADRID",
    "MALAMBO",
    "MANIZALES",
    "MANIZALEZ",
    "MANZANARES",
    "MARINILLA",
    "MARIQUITA",
    "MARSELLA",
    "MEDELLIN",
    "MELGAR",
    "MONTELIBANO",
    "MONTENEGRO",
    "MONTERIA",
    "MONTERREY",
    "MOSQUERA",
    "NEIRA",
    "NEIVA",
    "OCANA",
    "PAIPA",
    "PALMIRA",
    "PALONEGRO",
    "PAMPLONA",
    "PASTO",
    "PEREIRA",
    "PIEDECUESTA",
    "PITALITO",
    "PLANETA RICA",
    "POPAYAN",
    "PUERTO COLOMBIA",
    "PUERTO GAITAN",
    "PUERTO LOPEZ",
    "QUIMBAYA",
    "RIOHACHA",
    "RIONEGRO",
    "RIOSUCIO",
    "RISARALDA",
    "SABANALARGA",
    "SABANETA",
    "SALGAR",
    "SAN GIL",
    "SANTA BARBARA",
    "SANTA MARIA",
    "SANTA MARTA",
    "SANTA ROSA DE CABAL",
    "SANTANDER DE QUILICHAO",
    "SIBATE",
    "SINCELEJO",
    "SOACHA",
    "SOGAMOSO",
    "SOLEDAD",
    "SOPO",
    "TENJO",
    "TOCANCIPA",
    "TULUA",
    "TUNJA",
    "TURBACO",
    "TURBO",
    "UBATE",
    "URABA",
    "VALLEDUPAR",
    "VILLA DE LEYVA",
    "VILLA DEL ROSARIO",
    "VILLA MARIA",
    "VILLAVICENCIO",
    "VILLETA",
    "YARUMAL",
    "YOPAL",
    "YUMBO",
    "ZARAGOZA",
    "ZIPAQUIRA",
]

DEPARTMENTS = [
    "ANTIOQUIA",
    "ATLANTICO",
    "CUNDINAMARCA",
    "VALLE",
    "SANTANDER",
    "CASANARE",
]

DESCRIPTIVE_WORDS = [
    # Ubicación y complementos
    "LOCAL",
    "LOCALES",
    "L\\d+",
    "CENTRO",
    "COMERCIAL",
    "COMERCIAR",
    "PISO",
    "PISOS",
    "APTO",
    "APT",
    "APARTAMENTO",
    "OFICINA",
    "OF",
    "OFC",
    "OFI",
    "INTERIOR",
    "INT",
    "BODEGA",
    "BOD",
    "BODEGAS",
    "CASA",
    "EDIFICIO",
    "ED",
    "TORRE",
    "TO",
    "BLOQUE",
    "BLQ",
    "MZ",
    "MANZANA",
    "BARRIO",
    "CONJUNTO",
    "CONJ",
    "ETAPA",
    "PARQUE",
    "TERMINAL",
    "PUENTE",
    "COSTADO",
    "FRENTE",
    "ESQUINA",
    "ESQ",
    "LAS",
    "LOS",
    "LA",
    "LD",
    "LOTE",
    "LOTES",
    "FASE",
    "MODULO",
    "MOD",
    "SUBLOTE",
    "SECTOR",
    "SECT",
    "SECCION",
    "KILOMETRO",
    "KILOMETROS",
    "DEL",
    "DE",
    "EN",
    "ARTURO",
    "CUMPLIDO",
    "TOLU",
    "PARCELAS",
    "COTA",
    "ES",
    "DIRECCION",
    "DIR",
    "MTS",
    "METROS",
    "ADELANTE",
    "PEAJE",
    "PUERTAS",
    "DON",
    "DIEGO",
    "LLANOGRANDE",
    "ACACIAS",
    "RANSA",
    "COLFRIGOS",
    "SUBA",
    "CALI",
    "MIECO",
    "ERNESTO",
    "CORTIZZOS",
    "CAMILA",
    "DAZA",
    "ADMINISTRATIVO",
    "NRO",
    "TRADE",
    "PARK",
    "SIBERIA",
    "VIAL",
    "BRICENO",
    "PALERMO",
    "ANILLO",
    "GIRON",
    "LC",
    "LOC",
    "LI",
    "DG",
    "BA",
    "CD",
    "PI",
    "PZ",
    "BD",
    "AL",
    "TRV",
    "BOG",
    "PS",
    "LT",
    "LO",
    "IN",
    "AP",
    "CON",
    "AN",
    "BDG",
    "PAGINA",
    "LINCA",
    "NIVEL",
    "ACOPI",
    "ACTUAL",
    "SOLEDAD",
    "AGOSTO",
    "POR",
    "ENTRE",
    "EDIF",
    "ANTIOQUIA",
    "ATLANTICO",
    "DORADO",
    "BOYACA",
    "AMERICAS",
    "BOLIVAR",
    "MULTIPLAZA",
    "ROSITA",
    "BURBUJA",
    "TAQUILLA",
    "SEDE",
    "ADM",
    "ADMINISTRACION",
    "FINCA",
    "ZONA",
    "FRANCA",
    "COMPLEJO",
    "INDUSTRIAL",
    "LOGISTICO",
    "PARQUEADERO",
    "ENTRADA",
]

SPACE_RE = re.compile(r"\s+")
COORD_RE = re.compile(r"\b\d+\.\d{5,}\b|\b\d+\.\d+\s*[NSEOW]\b", re.IGNORECASE)
PHONE_RE = re.compile(r"\b\d{7,}\b")
NO_TOKEN_RE = re.compile(r"\b(N[O0]|NO|NR|NUM)\b", re.IGNORECASE)
NUM_SINGLE_CARDINAL_RE = re.compile(r"\b([0-9]+)\s+([NSEO])\s+([0-9]+)\b", re.IGNORECASE)
STUCK_TYPES_RE = re.compile(r"\b(AV|AK|CR|CL|KR|TV|DG|CIRC)(CL|CR|KR|AV|AK|TV|DG|CIRC)\b", re.IGNORECASE)
TYPE_WITH_NUMBER_RE = re.compile(r"(CR|CL|AV|KR|AK|TV|DG|CIRC)(\d)", re.IGNORECASE)
NUMBER_LETTER_RE = re.compile(r"(\d+[A-Z])(\d)")
CARDINAL_STUCK_RE = re.compile(r"(\d+[A-Z]?)(SUR|NORTE|ESTE|OESTE)", re.IGNORECASE)
BSUR_RE = re.compile(r"\b(\d+[A-Z]?)\s+B\s+(SUR|NORTE|ESTE|OESTE)\b", re.IGNORECASE)
SYMBOL_RE = re.compile(r"[#\-,;.()]+")
CITY_PATTERN = re.compile(rf"\b({'|'.join(map(re.escape, CITY_NAMES))})\b", re.IGNORECASE)
DEPT_PATTERN = re.compile(rf"\b({'|'.join(map(re.escape, DEPARTMENTS))})\b", re.IGNORECASE)
DESCRIPTIVE_PATTERN = re.compile(rf"\b({'|'.join(DESCRIPTIVE_WORDS)})\b", re.IGNORECASE)
AEROPUERTO_TYPO_RE = re.compile(r"\b(AEREOPUERTO|AEREROPUERTO|AEROPUERTI|CARGO)\b", re.IGNORECASE)
VIA_TYPE_PATTERN = r"(?:CALLE|CLL|CL|CALL|CARRERA|CRA|KRA|KR|AK|K|AVENIDA|AENIDA|AV|AVD|AVDA|AVE|DIAGONAL|DG|DIAG|TRANSVERSAL|TRAVERSAL|TRANVERSAL|TRANSVERSA|TRANSVERAL|TRANSVESAL|TV|TRANSV|TR|AC|ACL|ACR|CIRCULAR|CIRCUNVALAR|CIRCUNV|CIRC|PASAJE|PAS|PASEO|PEATONAL|PTE|PERIF|CTRA|VEREDA|VDA|VIA)"
CARDINAL_NORMALIZATION = {
    "NOR": "NORTE",
    "NORT": "NORTE",
    "NORTE": "NORTE",
    "SUR": "SUR",
    "ESTE": "ESTE",
    "OESTE": "OESTE",
    "OCC": "OESTE",
    "OCCIDENTE": "OESTE",
    "BIS": "BIS",
}
CARDINAL_PATTERN = r"(?:NORTE|NOR|NORT|SUR|ESTE|OESTE|OCC|OCCIDENTE|BIS)"


def normalize_via_type(token: str) -> str:
    return VIA_NORMALIZATION.get(token.upper(), token.upper())


def clean_basic(address: str) -> str:
    if pd.isna(address):
        return ""
    s = str(address).strip()
    if not s or s.lower() in {"nan", "none", "00"}:
        return ""
    s = s.upper()
    s = COORD_RE.sub(" ", s)
    s = SPACE_RE.sub(" ", s).strip()
    return s


def remove_noise(text: str) -> str:
    text = PHONE_RE.sub(" ", text)
    text = STUCK_TYPES_RE.sub(r"\1 \2", text)
    text = TYPE_WITH_NUMBER_RE.sub(r"\1 \2", text)
    text = NUMBER_LETTER_RE.sub(r"\1 \2", text)
    text = CARDINAL_STUCK_RE.sub(r"\1 \2", text)
    text = BSUR_RE.sub(r"\1 BIS \2", text)
    text = SYMBOL_RE.sub(" ", text)
    text = NO_TOKEN_RE.sub(" ", text)
    text = NUM_SINGLE_CARDINAL_RE.sub(r"\1 \3", text)
    text = DESCRIPTIVE_PATTERN.sub(" ", text)
    text = CITY_PATTERN.sub(" ", text)
    text = DEPT_PATTERN.sub(" ", text)
    text = SPACE_RE.sub(" ", text).strip()
    return text


def normalize_cardinal(token: Optional[str]) -> Optional[str]:
    if not token:
        return None
    upper = token.upper()
    return CARDINAL_NORMALIZATION.get(upper, upper)


def parse_with_name(text: str) -> Optional[str]:
    pattern = re.compile(
        rf"\b({VIA_TYPE_PATTERN})\s+((?:[A-Z]+\s+){{1,3}}?)(\d+[A-Z]?)\s*(?:({CARDINAL_PATTERN})\s+)?(\d+[A-Z]?)(?:\s+(\d+[A-Z]?))?(?:\s+(\d+[A-Z]?))?",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if not match:
        return None
    via = normalize_via_type(match.group(1))
    name = match.group(2).strip()
    num1 = match.group(3)
    cardinal = normalize_cardinal(match.group(4))
    num2 = match.group(5)
    num3 = match.group(6) or ""
    num4 = match.group(7) or ""
    parts = [via]
    if name:
        parts.append(SPACE_RE.sub(" ", name.strip()))
    parts.append(num1)
    if cardinal:
        parts.append(cardinal)
    for piece in (num2, num3, num4):
        if piece:
            parts.append(piece)
    return " ".join(str(p) for p in parts if p)


def parse_with_type(text: str) -> Optional[str]:
    pattern = re.compile(
        rf"\b({VIA_TYPE_PATTERN})\s+([A-Z0-9]+)(?:\s+({CARDINAL_PATTERN}))?(?:\s+([A-Z0-9]+))?(?:\s+([A-Z0-9]+))?(?:\s+([A-Z0-9]+))?",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if not match:
        return None
    via = normalize_via_type(match.group(1))
    num1 = match.group(2)
    if not re.match(r"\d", num1):
        return None
    cardinal = normalize_cardinal(match.group(3))
    num2 = match.group(4) or ""
    num3 = match.group(5) or ""
    num4 = match.group(6) or ""
    parts = [via, num1]
    if cardinal:
        parts.append(cardinal)
    if num2:
        parts.append(num2)
    if num3:
        parts.append(num3)
    if num4:
        parts.append(num4)
    return " ".join(parts)


def parse_numbers_only(text: str) -> Optional[str]:
    pattern = re.compile(r"^([A-Z0-9]+)\s+([A-Z0-9]+)(?:\s+([A-Z0-9]+))?")
    match = pattern.search(text)
    if not match:
        return None
    num1, num2, num3 = match.group(1), match.group(2), match.group(3)
    if not (re.match(r"\d", num1) and re.match(r"\d", num2)):
        return None
    parts = [num1, num2]
    if num3 and len(num3) <= 10:
        parts.append(num3)
    return " ".join(parts)


def handle_aeropuerto(text: str) -> Optional[str]:
    if "AEROPUERTO" not in text and not AEROPUERTO_TYPO_RE.search(text):
        return None
    s = AEROPUERTO_TYPO_RE.sub("AEROPUERTO", text)
    s = re.sub(rf"^({ '|'.join(map(re.escape, CITY_NAMES)) })\s+", "", s, flags=re.IGNORECASE).strip()
    s = re.sub(r"\b(LOCAL|LOCALES|L\d+|MUELLE|PISO|PISOS|P\d+|BODEGA|BODEGAS|BOD|HANGAR|OFICINA|OF|ZONA|SALA|PUERTA|GATE|TERMINAL|MODULO|MOD)\b.*$", "", s, flags=re.IGNORECASE).strip()
    s = SPACE_RE.sub(" ", s).strip()
    return s or None


def handle_via(text: str) -> Optional[str]:
    if not re.search(r"\bVIA\b", text, re.IGNORECASE):
        return None
    s = re.sub(rf"^({ '|'.join(map(re.escape, CITY_NAMES)) })\s+", "", text, flags=re.IGNORECASE).strip()
    s = re.sub(r"\b(LOCAL|LOCALES|L\d+|MUELLE|PISO|PISOS|P\d+|BODEGA|BODEGAS|BOD|HANGAR|OFICINA|OF|ZONA|SALA|PUERTA|GATE|TERMINAL|MODULO|MOD|LOTE|SECTOR|COORDENADAS|UBICADO|UBICADA)\b.*$", "", s, flags=re.IGNORECASE).strip()
    s = SPACE_RE.sub(" ", s).strip()
    if len(s) <= 3:
        return None
    return s


def normalize_fragment(text: str) -> str:
    cleaned = remove_noise(text)
    if not cleaned:
        return ""
    return parse_with_name(cleaned) or parse_with_type(cleaned) or parse_numbers_only(cleaned) or cleaned


def handle_autopista(text: str) -> Optional[str]:
    base = re.sub(r"\bAUTO\s+PISTA\b", "AUTO", text, flags=re.IGNORECASE)
    base = re.sub(r"\bAUTOP\b", "AUTO", base, flags=re.IGNORECASE)
    match = re.search(r"\b(AUTOPISTA|AUT\.?|AUTO[A-Z]+|AUT[A-Z]+)\b", base, flags=re.IGNORECASE)
    if not match:
        return None
    before = base[: match.start()].strip()
    after = base[match.end() :].strip()
    # Si antes solo hay ciudad, elimínala
    if before and CITY_PATTERN.fullmatch(before):
        before = ""
    token = match.group(1).upper()
    aut_name = ""
    if token.startswith("AUTO") and len(token) > 4 and token not in {"AUTO", "AUTOPISTA"}:
        aut_name = token[4:]
    elif token.startswith("AUT") and len(token) > 3 and token not in {"AUT", "AUT.", "AUTOPISTA"}:
        aut_name = token[3:]
    if not aut_name and after:
        parts = after.split()
        aut_name = parts[0]
        after = " ".join(parts[1:]) if len(parts) > 1 else ""
    km_match = re.search(r"\b(?:KM|K\.M\.?|KILOMETRO)\s*([0-9]+(?:\.[0-9]+)?)", after, flags=re.IGNORECASE)
    km_clause = ""
    remainder = after
    if km_match:
        km_clause = f" KM {km_match.group(1)}"
        remainder = after[km_match.end() :].strip()
    norm_tail = normalize_fragment(remainder)
    parts = ["AUTOPISTA"]
    if aut_name:
        parts.append(aut_name)
    result = " ".join(parts)
    if km_clause:
        result += km_clause
    if norm_tail:
        result = f"{result} {norm_tail}"
    return result.strip() or None


def handle_km(text: str) -> Optional[str]:
    km_match = re.search(
        r"\b(?:KM|K\.M\.?|KILOMETRO)\s+(\d+[.\d]*)\s+(.+?)(?=\s+(?:BOGOTA|MEDELLIN|CALI|BARRANQUILLA|LOCAL|PISO|APT|OFICINA|BODEGA|ZONA|SOTANO|$))",
        text,
        flags=re.IGNORECASE,
    )
    if not km_match:
        return None
    km_num = km_match.group(1)
    remainder = km_match.group(2).strip()
    via_match = re.search(
        rf"\b({VIA_TYPE_PATTERN})\s+(.+)", remainder, flags=re.IGNORECASE
    )
    if via_match:
        via_type = normalize_via_type(via_match.group(1))
        via_num = via_match.group(2).strip().split()[0]
        return f"KM {km_num} {via_type} {via_num}"
    return f"KM {km_num}"


def standardize_address(address: str) -> str:
    s = clean_basic(address)
    if not s:
        return ""

    aeropuerto = handle_aeropuerto(s)
    if aeropuerto:
        return aeropuerto

    via = handle_via(s)
    if via:
        return via

    autopista = handle_autopista(s)
    if autopista:
        return autopista

    km_via = handle_km(s)
    if km_via:
        return km_via

    normalized = normalize_fragment(s)
    return normalized


def main() -> None:
    input_file = "Nits_ciudad.xlsx"
    output_file = "Nits_ciudad_normalizadas.xlsx"
    column_name = "Direccion"
    output_column = "Direccion Estandarizada"

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"El archivo de entrada no existe: {input_file}")

    print(f"Leyendo archivo: {input_file}")
    df = pd.read_excel(input_file)

    if column_name not in df.columns:
        raise ValueError(f"La columna '{column_name}' no existe en el archivo de entrada.")

    if output_column in df.columns:
        print(f"Advertencia: la columna '{output_column}' ya existe y será reemplazada.")

    print(f"Procesando {len(df)} direcciones...")
    df[output_column] = df[column_name].apply(standardize_address)

    total = len(df)
    procesadas = (df[output_column] != "").sum()
    print(f"Direcciones procesadas exitosamente: {procesadas}/{total} ({procesadas/total*100:.1f}%)")

    df.to_excel(output_file, index=False)
    print(f"Archivo generado: {output_file}")


if __name__ == "__main__":
    main()
