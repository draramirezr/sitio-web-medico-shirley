"""Emit e-CF tipo 34 (Nota de Crédito)."""

from __future__ import annotations

import os
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from .cert_store import decrypt_passphrase, read_pkcs12_file
from .client import DgiiClientError, autenticar, consultar_estado_trackid, enviar_ecf
from .config import get_ambiente
from .ecf_builder import (
    build_ecf_xml,
    build_encf,
    extract_codigo_seguridad,
    extract_motivos_respuesta,
    map_tipoe_cf,
    secuencia_from_ncf_completo,
)
from .ecf_sign import sign_ecf_xml


def _indicador_nota_credito(fecha_factura_original) -> int:
    """0 si la factura original tiene ≤30 días; 1 si es mayor (DGII)."""
    if fecha_factura_original is None:
        return 0
    if isinstance(fecha_factura_original, datetime):
        d0 = fecha_factura_original.date()
    elif isinstance(fecha_factura_original, date):
        d0 = fecha_factura_original
    else:
        s = str(fecha_factura_original).strip()[:10]
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                d0 = datetime.strptime(s, fmt).date()
                break
            except ValueError:
                continue
        else:
            return 0
    dias = (date.today() - d0).days
    return 1 if dias > 30 else 0


def emitir_ecf_nota_credito(
    *,
    cfg: Dict[str, Any],
    nota_credito_id: int,
    ncf_row: Dict[str, Any],
    ncf_completo: str,
    fecha_nota,
    fecha_factura_original,
    encf_factura_original: str,
    ars_row: Dict[str, Any],
    items: List[Dict[str, Any]],
    monto_total,
    codigo_modificacion: int,
    razon_modificacion: str,
) -> Dict[str, Any]:
    if not cfg or not cfg.get("cert_path") or not cfg.get("passphrase_encrypted"):
        return {"ok": False, "skipped": True, "error": "Sin certificado DGII configurado"}

    rnc = (cfg.get("rnc_emisor") or os.getenv("DGII_RNC_EMISOR") or "").strip()
    razon = (cfg.get("razon_social_emisor") or os.getenv("DGII_RAZON_SOCIAL") or "Dra. Shirley Ramirez").strip()
    direccion = (
        cfg.get("direccion_emisor")
        or os.getenv("DGII_DIRECCION_EMISOR")
        or "Santo Domingo Este, Republica Dominicana"
    ).strip()
    if not rnc:
        return {"ok": False, "error": "Falta RNC emisor en configuración DGII"}

    tipoe = 34
    if map_tipoe_cf(ncf_row.get("prefijo") or "", ncf_row.get("tipo") or "") != 34:
        # Secuencia maestra debe ser E34/B04; emitimos siempre TipoeCF 34.
        pass
    seq = secuencia_from_ncf_completo(ncf_completo, ncf_row.get("prefijo") or "")
    if seq <= 0:
        seq = int(ncf_row.get("ultimo_numero") or 0) or 1
    encf = build_encf(tipoe, seq)
    ambiente = cfg.get("ambiente") or get_ambiente()

    comprador_rnc = str(ars_row.get("rnc") or "").strip()
    comprador_nombre = str(ars_row.get("nombre_ars") or "Comprador").strip()

    line_items = []
    for it in items or []:
        line_items.append({
            "nombre": str(it.get("nombre") or "Ajuste servicio medico")[:80],
            "cantidad": 1,
            "precio": it.get("monto") or 0,
            "monto": it.get("monto") or 0,
        })
    if not line_items:
        line_items = [{"nombre": "Nota de credito", "cantidad": 1, "precio": monto_total, "monto": monto_total}]

    indicador = _indicador_nota_credito(fecha_factura_original)
    referencia = {
        "ncf_modificado": encf_factura_original,
        "fecha_ncf_modificado": fecha_factura_original,
        "codigo_modificacion": int(codigo_modificacion),
        "razon_modificacion": (razon_modificacion or "Ajuste por nota de credito")[:250],
    }

    try:
        p12 = read_pkcs12_file(cfg["cert_path"])
        passphrase = decrypt_passphrase(cfg["passphrase_encrypted"])
        xml_unsigned = build_ecf_xml(
            tipoe_cf=tipoe,
            encf=encf,
            fecha_emision=fecha_nota,
            emisor={"rnc": rnc, "razon_social": razon, "direccion": direccion},
            comprador={"rnc": comprador_rnc, "razon_social": comprador_nombre},
            items=line_items,
            monto_total=monto_total,
            fecha_vencimiento_secuencia="",
            ambiente=ambiente,
            informacion_referencia=referencia,
            indicador_nota_credito=indicador,
        )
        xml_signed = sign_ecf_xml(xml_unsigned, p12, passphrase)
        codigo = extract_codigo_seguridad(xml_signed)
        token = autenticar(ambiente, p12, passphrase)
        filename = f"{rnc}{encf}.xml"
        recv = enviar_ecf(xml_signed, filename, token, ambiente)
        track_id = recv.get("trackId")
        estado = "ENVIADO"
        estado_detalle = recv
        try:
            estado_detalle = consultar_estado_trackid(track_id, token, ambiente)
            estado = (
                estado_detalle.get("estado")
                or estado_detalle.get("Estado")
                or estado_detalle.get("status")
                or "ENVIADO"
            )
        except DgiiClientError:
            pass

        motivos = extract_motivos_respuesta(estado_detalle)
        accepted = str(estado).lower() not in ("rechazado", "rejected", "error")
        error_text = None
        if not accepted and motivos:
            error_text = "; ".join(motivos)
        elif not accepted:
            error_text = "Rechazado por DGII (nota de credito)"

        return {
            "ok": accepted,
            "nota_credito_id": nota_credito_id,
            "tipoe_cf": tipoe,
            "encf": encf,
            "track_id": track_id,
            "codigo_seguridad": codigo,
            "estado": estado,
            "ambiente": ambiente,
            "respuesta": estado_detalle,
            "error": error_text,
            "xml_signed": xml_signed.decode("utf-8", errors="replace"),
            "indicador_nota_credito": indicador,
        }
    except Exception as e:
        return {
            "ok": False,
            "nota_credito_id": nota_credito_id,
            "tipoe_cf": tipoe,
            "encf": encf,
            "error": str(e),
            "ambiente": ambiente,
        }