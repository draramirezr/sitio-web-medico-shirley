"""HTTP client for DGII authentication and réception ping."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import requests

from .config import get_urls

DEFAULT_TIMEOUT = 45


class DgiiClientError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, body: str = ""):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


def obtener_semilla(ambiente: Optional[str] = None) -> bytes:
    urls = get_urls(ambiente)
    try:
        resp = requests.get(
            urls["semilla"],
            headers={"Accept": "application/xml, text/xml, */*"},
            timeout=DEFAULT_TIMEOUT,
        )
    except requests.RequestException as e:
        raise DgiiClientError(f"No se pudo conectar a DGII (semilla): {e}") from e
    if resp.status_code != 200:
        raise DgiiClientError(
            f"DGII semilla respondió HTTP {resp.status_code}",
            status_code=resp.status_code,
            body=(resp.text or "")[:500],
        )
    if not (resp.content or b"").strip():
        raise DgiiClientError("DGII devolvió semilla vacía")
    return resp.content


def validar_semilla(signed_xml: bytes, ambiente: Optional[str] = None) -> Dict[str, Any]:
    urls = get_urls(ambiente)
    files = {
        "xml": ("semilla_firmada.xml", signed_xml, "application/xml"),
    }
    try:
        resp = requests.post(
            urls["validar_semilla"],
            files=files,
            headers={"Accept": "application/json, text/plain, */*"},
            timeout=DEFAULT_TIMEOUT,
        )
    except requests.RequestException as e:
        raise DgiiClientError(f"No se pudo conectar a DGII (validar semilla): {e}") from e

    if resp.status_code not in (200, 201):
        raise DgiiClientError(
            f"DGII validarSemilla respondió HTTP {resp.status_code}",
            status_code=resp.status_code,
            body=(resp.text or "")[:800],
        )

    token = None
    data: Dict[str, Any] = {}
    try:
        data = resp.json() if resp.content else {}
        if isinstance(data, dict):
            token = data.get("token") or data.get("Token") or data.get("access_token")
    except ValueError:
        # Algunas respuestas vienen como texto plano (JWT)
        text = (resp.text or "").strip()
        if text and text.count(".") >= 2:
            token = text
            data = {"token": token, "raw": True}

    if not token:
        raise DgiiClientError(
            "DGII no devolvió token JWT en validarSemilla",
            status_code=resp.status_code,
            body=(resp.text or "")[:800],
        )
    data["token"] = token
    return data


def ping_recepcion(token: Optional[str] = None, ambiente: Optional[str] = None) -> Tuple[bool, str]:
    """
    Verifica conectividad al servicio de recepción (sin enviar e-CF).
    Intenta help/index.html; si falla, HEAD/GET a la base recepción.
    """
    urls = get_urls(ambiente)
    headers = {"Accept": "text/html, application/json, */*"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    last_err = "sin respuesta"
    for url in (urls["recepcion_help"], urls["recepcion"]):
        try:
            resp = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
            # 200/401/403/404 con TLS OK = canal vivo (401/403 implica auth, no caída de red)
            if resp.status_code < 500:
                return True, f"Recepción alcanzable ({url}) HTTP {resp.status_code}"
            last_err = f"HTTP {resp.status_code} en {url}"
        except requests.RequestException as e:
            last_err = str(e)
            continue
    return False, f"No se pudo alcanzar el servicio de recepción DGII: {last_err}"
