"""Automated DGII Phase-A test battery after certificate upload."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .cert_store import inspect_pkcs12, read_pkcs12_file
from .client import DgiiClientError, obtener_semilla, ping_recepcion, validar_semilla
from .config import get_ambiente
from .xml_sign import sign_semilla_xml


def _step(name: str, ok: bool, detail: str = "") -> Dict[str, Any]:
    return {"name": name, "ok": bool(ok), "detail": detail or ("OK" if ok else "Falló")}


def run_dgii_pruebas(
    p12_bytes: Optional[bytes] = None,
    passphrase: Optional[str] = None,
    cert_path: Optional[str] = None,
    ambiente: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Ejecuta:
      1) Certificado legible
      2) Semilla DGII
      3) Firma de semilla
      4) Token JWT
      5) Conexión recepción
    """
    amb = ambiente or get_ambiente()
    steps: List[Dict[str, Any]] = []
    started = datetime.now(timezone.utc).isoformat()

    # Resolve PKCS#12 bytes
    try:
        if p12_bytes is None:
            if not cert_path:
                raise ValueError("No hay certificado para probar.")
            p12_bytes = read_pkcs12_file(cert_path)
        if passphrase is None:
            raise ValueError("Falta la contraseña del certificado.")
    except Exception as e:
        steps.append(_step("Certificado legible", False, str(e)))
        return {
            "ok": False,
            "ambiente": amb,
            "started_at": started,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "steps": steps,
        }

    # 1) Certificate readable
    try:
        info = inspect_pkcs12(p12_bytes, passphrase)
        steps.append(
            _step(
                "Certificado legible",
                True,
                f"Huella {info.fingerprint_sha256[:29]}… · vence {info.not_after.date().isoformat()}",
            )
        )
        cert_meta = {
            "fingerprint": info.fingerprint_sha256,
            "not_after": info.not_after.isoformat(),
            "subject": info.subject,
        }
    except Exception as e:
        steps.append(_step("Certificado legible", False, str(e)))
        return {
            "ok": False,
            "ambiente": amb,
            "started_at": started,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "steps": steps,
        }

    # 2) Semilla
    semilla = None
    try:
        semilla = obtener_semilla(amb)
        steps.append(_step("Semilla DGII", True, f"Recibida ({len(semilla)} bytes)"))
    except DgiiClientError as e:
        detail = str(e)
        if e.body:
            detail += f" · {e.body[:200]}"
        steps.append(_step("Semilla DGII", False, detail))
        steps.append(_step("Firma de semilla", False, "Omitida (sin semilla)"))
        steps.append(_step("Token obtenido", False, "Omitido"))
        steps.append(_step("Conexión recepción", False, "Omitida"))
        return _finish(False, amb, started, steps, cert_meta)

    # 3) Sign seed
    signed = None
    try:
        signed = sign_semilla_xml(semilla, p12_bytes, passphrase)
        steps.append(_step("Firma de semilla", True, f"XML firmado ({len(signed)} bytes)"))
    except Exception as e:
        steps.append(_step("Firma de semilla", False, str(e)))
        steps.append(_step("Token obtenido", False, "Omitido (sin firma)"))
        steps.append(_step("Conexión recepción", False, "Omitida"))
        return _finish(False, amb, started, steps, cert_meta)

    # 4) Validate seed → token
    token = None
    try:
        auth = validar_semilla(signed, amb)
        token = auth.get("token")
        steps.append(_step("Token obtenido", True, "JWT recibido de DGII"))
    except DgiiClientError as e:
        detail = str(e)
        if e.body:
            detail += f" · {e.body[:240]}"
        steps.append(_step("Token obtenido", False, detail))
        # Still try recepción without token
        ok_ping, msg = ping_recepcion(None, amb)
        steps.append(_step("Conexión recepción", ok_ping, msg))
        return _finish(False, amb, started, steps, cert_meta)

    # 5) Reception ping
    ok_ping, msg = ping_recepcion(token, amb)
    steps.append(_step("Conexión recepción", ok_ping, msg))

    all_ok = all(s["ok"] for s in steps)
    return _finish(all_ok, amb, started, steps, cert_meta)


def _finish(ok: bool, amb: str, started: str, steps: List[Dict[str, Any]], cert_meta: Optional[Dict] = None) -> Dict[str, Any]:
    return {
        "ok": ok,
        "ambiente": amb,
        "started_at": started,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "steps": steps,
        "cert": cert_meta or {},
    }
