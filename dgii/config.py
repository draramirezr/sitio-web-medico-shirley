"""DGII environment URLs (TesteCF / CerteCF / eCF)."""

from __future__ import annotations

import os
from typing import Dict


AMBIENTES = {
    "PRUEBAS": "testecf",
    "CERTIFICACION": "certecf",
    "PRODUCCION": "ecf",
}


def get_ambiente() -> str:
    raw = (os.getenv("DGII_AMBIENTE") or "PRUEBAS").strip().upper()
    if raw in ("TEST", "TESTECF", "PRECERT"):
        return "PRUEBAS"
    if raw in ("CERT", "CERTECF"):
        return "CERTIFICACION"
    if raw in ("PROD", "PRODUCTION", "ECF"):
        return "PRODUCCION"
    if raw not in AMBIENTES:
        return "PRUEBAS"
    return raw


def get_urls(ambiente: str | None = None) -> Dict[str, str]:
    amb = (ambiente or get_ambiente()).upper()
    slug = AMBIENTES.get(amb, AMBIENTES["PRUEBAS"])
    base = f"https://ecf.dgii.gov.do/{slug}"
    return {
        "ambiente": amb,
        "slug": slug,
        "autenticacion": f"{base}/autenticacion",
        "semilla": f"{base}/autenticacion/api/autenticacion/semilla",
        "validar_semilla": f"{base}/autenticacion/api/autenticacion/validarsemilla",
        "recepcion": f"{base}/recepcion",
        "recepcion_api": f"{base}/recepcion/api/facturaselectronicas",
        "recepcion_help": f"{base}/recepcion/help/index.html",
        "consulta_trackid": f"{base}/consultaresultado/api/consultas/estado",
        "consultaresultado": f"{base}/consultaresultado",
    }


def cert_dir() -> str:
    path = (os.getenv("DGII_CERT_DIR") or "").strip()
    if path:
        return path
    # Default: private folder next to app (never commit contents)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, "private", "dgii_certs")
