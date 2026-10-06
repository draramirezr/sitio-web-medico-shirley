"""Build DGII e-CF XML (types 31, 32, 45) for medical invoices (ITBIS exento)."""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, List, Optional
from xml.etree.ElementTree import Element, SubElement, tostring

from lxml import etree


# Traditional NCF prefix → TipoeCF
_PREFIX_TO_TIPO = {
    "B01": 31,  # Crédito fiscal
    "B02": 32,  # Consumo
    "B14": 45,  # Gubernamental
    "B15": 44,  # Régimen especial
    "E31": 31,
    "E32": 32,
    "E45": 45,
    "E44": 44,
}


def _money(value) -> str:
    d = Decimal(str(value or 0)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return f"{d:.2f}"


def _fecha_dd_mm_yyyy(value) -> str:
    if value is None:
        d = date.today()
    elif isinstance(value, datetime):
        d = value.date()
    elif isinstance(value, date):
        d = value
    else:
        s = str(value).strip()[:10]
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                d = datetime.strptime(s, fmt).date()
                break
            except ValueError:
                continue
        else:
            d = date.today()
    return d.strftime("%d-%m-%Y")


def fecha_hora_firma_now() -> str:
    """DGII FechaHoraFirma: dd-MM-yyyy HH:mm:ss (hora local aproximada)."""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def map_tipoe_cf(ncf_prefijo: str, ncf_tipo: str = "") -> int:
    p = (ncf_prefijo or "").strip().upper()
    for key, tipo in _PREFIX_TO_TIPO.items():
        if p.startswith(key):
            return tipo
    t = (ncf_tipo or "").upper()
    if "GUBERNAMENTAL" in t:
        return 45
    if "CONSUMO" in t:
        return 32
    if "FISCAL" in t:
        return 31
    return 31


def build_encf(tipoe_cf: int, secuencia: int) -> str:
    """eNCF = E + tipoeCF(2) + secuencia(10)."""
    return f"E{int(tipoe_cf):02d}{int(secuencia):010d}"


def secuencia_from_ncf_completo(ncf_completo: str, prefijo: str) -> int:
    raw = (ncf_completo or "").strip().upper()
    pref = (prefijo or "").strip().upper()
    if pref and raw.startswith(pref):
        digits = raw[len(pref) :]
    elif raw.startswith("E") and len(raw) >= 13:
        digits = raw[3:]
    else:
        digits = "".join(ch for ch in raw if ch.isdigit())
    try:
        return int(digits or "0")
    except ValueError:
        return 0


def build_ecf_xml(
    *,
    tipoe_cf: int,
    encf: str,
    fecha_emision,
    emisor: Dict[str, str],
    comprador: Dict[str, str],
    items: List[Dict[str, Any]],
    monto_total,
    fecha_vencimiento_secuencia: str = "31-12-2026",
    fecha_hora_firma: Optional[str] = None,
) -> bytes:
    """
    Construye XML ECF para servicios exentos (IndicadorFacturacion=4).
    Incluye campos que DGII suele exigir en recepción (formas de pago, FechaHoraFirma).
    """
    total = _money(monto_total)
    root = Element("ECF")
    encabezado = SubElement(root, "Encabezado")
    SubElement(encabezado, "Version").text = "1.0"

    id_doc = SubElement(encabezado, "IdDoc")
    SubElement(id_doc, "TipoeCF").text = str(int(tipoe_cf))
    SubElement(id_doc, "eNCF").text = encf
    if tipoe_cf != 32:
        SubElement(id_doc, "FechaVencimientoSecuencia").text = fecha_vencimiento_secuencia
    # 0 = envío normal inmediato (1=diferido/contingencia)
    SubElement(id_doc, "IndicadorEnvioDiferido").text = "0"
    if tipoe_cf == 32:
        SubElement(id_doc, "IndicadorMontoGravado").text = "0"
    SubElement(id_doc, "TipoIngresos").text = "01"
    SubElement(id_doc, "TipoPago").text = "1"  # Contado

    # Obligatorio/condicional frecuente con TipoPago=1
    tabla_fp = SubElement(id_doc, "TablaFormasPago")
    forma = SubElement(tabla_fp, "FormaDePago")
    SubElement(forma, "FormaPago").text = "1"  # Efectivo / transferencia genérica
    SubElement(forma, "MontoPago").text = total

    em = SubElement(encabezado, "Emisor")
    SubElement(em, "RNCEmisor").text = str(emisor.get("rnc") or "").strip()
    SubElement(em, "RazonSocialEmisor").text = (emisor.get("razon_social") or "").strip()[:150]
    SubElement(em, "DireccionEmisor").text = (emisor.get("direccion") or "Santo Domingo Este").strip()[:100]
    municipio = (emisor.get("municipio") or "010101").strip()  # código genérico si no hay
    provincia = (emisor.get("provincia") or "010000").strip()
    if emisor.get("municipio"):
        SubElement(em, "Municipio").text = municipio
    if emisor.get("provincia"):
        SubElement(em, "Provincia").text = provincia
    SubElement(em, "FechaEmision").text = _fecha_dd_mm_yyyy(fecha_emision)

    comp = SubElement(encabezado, "Comprador")
    SubElement(comp, "RNCComprador").text = str(comprador.get("rnc") or "").strip()
    SubElement(comp, "RazonSocialComprador").text = (comprador.get("razon_social") or "").strip()[:150]

    totales = SubElement(encabezado, "Totales")
    SubElement(totales, "MontoExento").text = total
    SubElement(totales, "MontoTotal").text = total

    detalles = SubElement(root, "DetallesItems")
    for idx, it in enumerate(items, start=1):
        item = SubElement(detalles, "Item")
        SubElement(item, "NumeroLinea").text = str(idx)
        SubElement(item, "IndicadorFacturacion").text = "4"  # Exento
        nombre = (it.get("nombre") or "Servicio medico").strip()[:80]
        SubElement(item, "NombreItem").text = nombre
        SubElement(item, "IndicadorBienoServicio").text = "2"  # Servicio
        cant = it.get("cantidad", 1)
        precio = it.get("precio", it.get("monto", 0))
        monto = it.get("monto", precio)
        SubElement(item, "CantidadItem").text = _money(cant)
        SubElement(item, "UnidadMedida").text = str(it.get("unidad_medida") or "43")
        SubElement(item, "PrecioUnitarioItem").text = _money(precio)
        SubElement(item, "MontoItem").text = _money(monto)

    # Debe existir ANTES de la firma digital
    SubElement(root, "FechaHoraFirma").text = fecha_hora_firma or fecha_hora_firma_now()

    rough = tostring(root, encoding="utf-8")
    parsed = etree.fromstring(rough)
    return etree.tostring(parsed, encoding="utf-8", xml_declaration=True)


def extract_codigo_seguridad(signed_xml: bytes) -> str:
    """DGII: primeros 6 caracteres del SignatureValue."""
    root = etree.fromstring(signed_xml)
    ns = {"ds": "http://www.w3.org/2000/09/xmldsig#"}
    nodes = root.xpath("//ds:SignatureValue", namespaces=ns)
    if not nodes:
        nodes = root.xpath("//*[local-name()='SignatureValue']")
    if not nodes or not (nodes[0].text or "").strip():
        return "000000"
    return (nodes[0].text or "").strip().replace("\n", "").replace(" ", "")[:6]


def extract_motivos_respuesta(respuesta: Any) -> List[str]:
    """Normalize DGII consulta/recepción payload into human-readable rejection reasons."""
    if not respuesta:
        return []
    if isinstance(respuesta, str):
        return [respuesta] if respuesta.strip() else []
    if not isinstance(respuesta, dict):
        return [str(respuesta)]

    out: List[str] = []
    for key in ("mensajes", "Mensajes", "motivos", "Motivos", "errores", "Errores"):
        msgs = respuesta.get(key)
        if isinstance(msgs, list):
            for m in msgs:
                if isinstance(m, dict):
                    val = m.get("valor") or m.get("Valor") or m.get("mensaje") or m.get("descripcion") or m.get("Detalle")
                    cod = m.get("codigo") or m.get("Codigo") or ""
                    if val:
                        out.append(f"{cod}: {val}".strip(": "))
                    else:
                        out.append(str(m))
                else:
                    out.append(str(m))
        elif isinstance(msgs, str) and msgs.strip():
            out.append(msgs)
    for key in ("mensaje", "Mensaje", "detalle", "Detalle", "error", "Error"):
        val = respuesta.get(key)
        if val and str(val) not in out:
            out.append(str(val))
    return out
