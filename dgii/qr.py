"""QR de Representación Impresa (RI) del e-CF — consulta timbre DGII."""

from __future__ import annotations

from io import BytesIO
from typing import Any, Dict, Optional
from urllib.parse import quote


_AMBIENTE_PATH = {
    "PRUEBAS": "testecf",
    "TESTECF": "testecf",
    "CERTIFICACION": "certecf",
    "CERTECF": "certecf",
    "PRODUCCION": "ecf",
    "ECF": "ecf",
}


def _q(value) -> str:
    return quote(str(value or "").strip(), safe="")


def consultatimbre_url(
    *,
    ambiente: str,
    rnc_emisor: str,
    rnc_comprador: str,
    encf: str,
    fecha_emision: str,
    monto_total: str,
    fecha_firma: str,
    codigo_seguridad: str,
) -> str:
    path = _AMBIENTE_PATH.get((ambiente or "PRUEBAS").strip().upper(), "testecf")
    encf_u = (encf or "").strip().upper()
    parts = [
        f"rncemisor={_q(rnc_emisor)}",
    ]
    if rnc_comprador and not encf_u.startswith("E43") and not encf_u.startswith("E47"):
        parts.append(f"RncComprador={_q(rnc_comprador)}")
    parts.extend([
        f"encf={_q(encf)}",
        f"fechaemision={_q(fecha_emision)}",
        f"montototal={_q(monto_total)}",
        f"fechafirma={_q(fecha_firma)}",
        f"codigoseguridad={_q(codigo_seguridad)}",
    ])
    return f"https://ecf.dgii.gov.do/{path}/consultatimbre?" + "&".join(parts)


def qr_png_bytes(url: str, scale: int = 4) -> bytes:
    import segno

    qr = segno.make(url, error="M")
    buf = BytesIO()
    qr.save(buf, kind="png", scale=scale, border=1)
    return buf.getvalue()


def timbre_from_envio(envio: Optional[Dict[str, Any]]) -> Optional[Dict[str, str]]:
    if not envio:
        return None
    xml = envio.get("xml_firmado") or envio.get("xml_signed") or ""
    ambiente = (envio.get("ambiente") or "PRUEBAS").strip()
    fields: Dict[str, str] = {}
    if xml:
        try:
            from dgii.ecf_builder import extract_timbre_fields

            raw = xml.encode("utf-8") if isinstance(xml, str) else xml
            fields = extract_timbre_fields(raw)
        except Exception:
            fields = {}
    codigo = (fields.get("codigo_seguridad") or envio.get("codigo_seguridad") or "").strip()
    encf = (fields.get("encf") or envio.get("encf") or "").strip()
    if not codigo or not encf or codigo == "000000":
        return None
    if not fields.get("fecha_firma") or not fields.get("rnc_emisor"):
        return None
    url = consultatimbre_url(
        ambiente=ambiente,
        rnc_emisor=fields.get("rnc_emisor") or "",
        rnc_comprador=fields.get("rnc_comprador") or "",
        encf=encf,
        fecha_emision=fields.get("fecha_emision") or "",
        monto_total=fields.get("monto_total") or "",
        fecha_firma=fields.get("fecha_firma") or "",
        codigo_seguridad=codigo,
    )
    return {
        "url": url,
        "codigo_seguridad": codigo,
        "encf": encf,
        "ambiente": ambiente,
        "rnc_emisor": fields.get("rnc_emisor") or "",
        "fecha_emision": fields.get("fecha_emision") or "",
        "monto_total": fields.get("monto_total") or "",
        "fecha_firma": fields.get("fecha_firma") or "",
    }
