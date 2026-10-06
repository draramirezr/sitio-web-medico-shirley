"""HTTP client for DGII authentication and réception ping."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import requests

from .config import get_urls

DEFAULT_TIMEOUT = 45


class DgiiClientError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, body: str = ""):
        self.status_code = status_code
        self.body = body or ""
        detail = message
        if self.body:
            snippet = self.body.replace("\n", " ").strip()
            if snippet and snippet not in detail:
                detail = f"{message} · {snippet[:240]}"
        super().__init__(detail)


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
            if resp.status_code < 500:
                return True, f"Recepción alcanzable ({url}) HTTP {resp.status_code}"
            last_err = f"HTTP {resp.status_code} en {url}"
        except requests.RequestException as e:
            last_err = str(e)
            continue
    return False, f"No se pudo alcanzar el servicio de recepción DGII: {last_err}"


def autenticar(ambiente: Optional[str], p12_bytes: bytes, passphrase: str) -> str:
    """Obtiene token JWT: semilla → firma → validarSemilla."""
    from .xml_sign import sign_semilla_xml

    semilla = obtener_semilla(ambiente)
    firmada = sign_semilla_xml(semilla, p12_bytes, passphrase)
    data = validar_semilla(firmada, ambiente)
    token = data.get("token")
    if not token:
        raise DgiiClientError("Autenticación DGII sin token")
    return token


def enviar_ecf(
    signed_xml: bytes,
    filename: str,
    token: str,
    ambiente: Optional[str] = None,
) -> Dict[str, Any]:
    """POST recepción e-CF. Retorna dict con trackId."""
    urls = get_urls(ambiente)
    files = {"xml": (filename, signed_xml, "application/xml")}
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": f"Bearer {token}",
    }
    try:
        resp = requests.post(
            urls["recepcion_api"],
            files=files,
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
        )
    except requests.RequestException as e:
        raise DgiiClientError(f"No se pudo enviar e-CF a DGII: {e}") from e

    if resp.status_code not in (200, 201, 202):
        raise DgiiClientError(
            f"Recepción e-CF HTTP {resp.status_code}",
            status_code=resp.status_code,
            body=(resp.text or "")[:1000],
        )

    data: Dict[str, Any] = {}
    try:
        data = resp.json() if resp.content else {}
    except ValueError:
        text = (resp.text or "").strip()
        data = {"trackId": text, "raw": True}

    track = None
    if isinstance(data, dict):
        track = data.get("trackId") or data.get("TrackId") or data.get("trackid")
    if not track:
        raise DgiiClientError(
            "DGII no devolvió TrackId",
            status_code=resp.status_code,
            body=(resp.text or "")[:1000],
        )
    data["trackId"] = track
    return data


def consultar_estado_trackid(track_id: str, token: str, ambiente: Optional[str] = None) -> Dict[str, Any]:
    urls = get_urls(ambiente)
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    try:
        resp = requests.get(
            urls["consulta_trackid"],
            params={"trackid": track_id},
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
        )
    except requests.RequestException as e:
        raise DgiiClientError(f"No se pudo consultar estado e-CF: {e}") from e

    if resp.status_code != 200:
        raise DgiiClientError(
            f"Consulta estado HTTP {resp.status_code}",
            status_code=resp.status_code,
            body=(resp.text or "")[:800],
        )
    try:
        return resp.json() if resp.content else {}
    except ValueError:
        return {"estado": (resp.text or "").strip(), "raw": True}
