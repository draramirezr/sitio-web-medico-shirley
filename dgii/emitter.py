"""Emit e-CF for a generated invoice (Phase B)."""

from __future__ import annotations

import os
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
    resolve_fecha_vencimiento_secuencia,
    secuencia_from_ncf_completo,
)
from .ecf_sign import sign_ecf_xml


def dgii_emitir_habilitado() -> bool:
    """Auto-emit on invoice unless explicitly disabled."""
    raw = (os.getenv("DGII_EMITIR_AUTO") or "1").strip().lower()
    return raw not in ("0", "false", "no", "off")


def emitir_ecf_para_factura(
    *,
    cfg: Dict[str, Any],
    factura_id: int,
    ncf_row: Dict[str, Any],
    ncf_completo: str,
    fecha_factura,
    ars_row: Dict[str, Any],
    items: List[Dict[str, Any]],
    monto_total,
    fecha_vencimiento_secuencia: Optional[str] = None,
) -> Dict[str, Any]:
    """
    cfg: fila dgii_config (cert_path, passphrase_encrypted, ambiente, rnc_emisor, ...)
    Retorna dict con ok, track_id, encf, tipoe_cf, estado, codigo_seguridad, error, xml_signed (opcional).
    """
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

    tipoe = map_tipoe_cf(ncf_row.get("prefijo") or "", ncf_row.get("tipo") or "")
    seq = secuencia_from_ncf_completo(ncf_completo, ncf_row.get("prefijo") or "")
    if seq <= 0:
        seq = int(ncf_row.get("ultimo_numero") or 0) or 1
    encf = build_encf(tipoe, seq)
    ambiente = cfg.get("ambiente") or get_ambiente()

    comprador_rnc = str(ars_row.get("rnc") or "").strip()
    comprador_nombre = str(ars_row.get("nombre_ars") or "Comprador").strip()
    if tipoe == 32 and (not comprador_rnc or comprador_rnc in ("0", "00000000000")):
        comprador_rnc = "00000000000"
        comprador_nombre = comprador_nombre or "Consumidor Final"

    line_items = []
    if items:
        for it in items:
            nombre = it.get("nombre") or it.get("nombre_paciente") or it.get("servicio") or "Servicio medico"
            monto = it.get("monto") or it.get("precio") or 0
            line_items.append({
                "nombre": str(nombre)[:80],
                "cantidad": 1,
                "precio": monto,
                "monto": monto,
            })
    else:
        line_items = [{"nombre": "Servicios medicos", "cantidad": 1, "precio": monto_total, "monto": monto_total}]

    try:
        venc = resolve_fecha_vencimiento_secuencia(
            cfg_value=fecha_vencimiento_secuencia or cfg.get("fecha_vencimiento_secuencia"),
            env_value=os.getenv("DGII_FECHA_VENCIMIENTO_SEC"),
        )
    except ValueError as e:
        return {"ok": False, "error": str(e), "tipoe_cf": tipoe, "encf": encf, "ambiente": ambiente}

    try:
        p12 = read_pkcs12_file(cfg["cert_path"])
        passphrase = decrypt_passphrase(cfg["passphrase_encrypted"])
        xml_unsigned = build_ecf_xml(
            tipoe_cf=tipoe,
            encf=encf,
            fecha_emision=fecha_factura,
            emisor={"rnc": rnc, "razon_social": razon, "direccion": direccion},
            comprador={"rnc": comprador_rnc, "razon_social": comprador_nombre},
            items=line_items,
            monto_total=monto_total,
            fecha_vencimiento_secuencia=venc,
            ambiente=ambiente,
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
        error_text = "; ".join(motivos) if motivos else None
        if error_text:
            error_text = f"{error_text} (FechaVencimientoSecuencia enviada: {venc})"
        accepted = str(estado).lower() not in ("rechazado", "rejected", "error")

        return {
            "ok": accepted,
            "factura_id": factura_id,
            "tipoe_cf": tipoe,
            "encf": encf,
            "track_id": track_id,
            "codigo_seguridad": codigo,
            "estado": estado,
            "ambiente": ambiente,
            "fecha_vencimiento_secuencia": venc,
            "respuesta": estado_detalle,
            "error": error_text,
            "xml_signed": xml_signed.decode("utf-8", errors="replace"),
        }
    except Exception as e:
        return {
            "ok": False,
            "factura_id": factura_id,
            "tipoe_cf": tipoe,
            "encf": encf,
            "error": str(e),
            "ambiente": ambiente,
        }
