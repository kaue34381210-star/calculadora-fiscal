"""
Alíquotas internas de ICMS por UF (2024).
"""

ICMS_POR_UF = {
    "AC": 0.17, "AL": 0.17, "AP": 0.18, "AM": 0.20, "BA": 0.19,
    "CE": 0.20, "DF": 0.20, "ES": 0.17, "GO": 0.17, "MA": 0.20,
    "MT": 0.17, "MS": 0.17, "MG": 0.18, "PA": 0.17, "PB": 0.18,
    "PR": 0.19, "PE": 0.20, "PI": 0.21, "RJ": 0.20, "RN": 0.18,
    "RS": 0.17, "RO": 0.17, "RR": 0.17, "SC": 0.17, "SP": 0.18,
    "SE": 0.19, "TO": 0.20,
}

def get_aliquota_icms(uf: str) -> float:
    return ICMS_POR_UF.get(uf.upper(), 0.18)
