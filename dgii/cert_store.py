"""Secure PKCS#12 storage and passphrase encryption."""

from __future__ import annotations

import base64
import hashlib
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Tuple

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography import x509

from .config import cert_dir


@dataclass
class CertInfo:
    fingerprint_sha256: str
    not_after: datetime
    subject: str
    issuer: str


def _fernet() -> Fernet:
    secret = (os.getenv("DGII_CERT_SECRET") or os.getenv("SECRET_KEY") or "dgii-dev-secret").strip()
    digest = hashlib.sha256(secret.encode("utf-8")).digest()
    key = base64.urlsafe_b64encode(digest)
    return Fernet(key)


def encrypt_passphrase(passphrase: str) -> str:
    return _fernet().encrypt(passphrase.encode("utf-8")).decode("utf-8")


def decrypt_passphrase(token: str) -> str:
    try:
        return _fernet().decrypt(token.encode("utf-8")).decode("utf-8")
    except InvalidToken as e:
        raise ValueError("No se pudo descifrar la contraseña del certificado. Revisa DGII_CERT_SECRET/SECRET_KEY.") from e


def ensure_cert_dir() -> str:
    path = cert_dir()
    os.makedirs(path, exist_ok=True)
    return path


def load_pkcs12(p12_bytes: bytes, passphrase: str) -> Tuple[object, x509.Certificate, list]:
    password = passphrase.encode("utf-8") if passphrase is not None else None
    try:
        key, cert, additional = pkcs12.load_key_and_certificates(p12_bytes, password)
    except Exception as e:
        raise ValueError(f"Certificado PKCS#12 inválido o contraseña incorrecta: {e}") from e
    if key is None or cert is None:
        raise ValueError("El archivo PKCS#12 no contiene clave privada y certificado.")
    return key, cert, additional or []


def inspect_pkcs12(p12_bytes: bytes, passphrase: str) -> CertInfo:
    _key, cert, _extra = load_pkcs12(p12_bytes, passphrase)
    fp = cert.fingerprint(hashlib.sha256()).hex().upper()
    # Format fingerprint as AA:BB:...
    fingerprint = ":".join(fp[i : i + 2] for i in range(0, len(fp), 2))
    not_after = cert.not_valid_after_utc if hasattr(cert, "not_valid_after_utc") else cert.not_valid_after.replace(tzinfo=timezone.utc)
    subject = cert.subject.rfc4514_string()
    issuer = cert.issuer.rfc4514_string()
    return CertInfo(
        fingerprint_sha256=fingerprint,
        not_after=not_after,
        subject=subject,
        issuer=issuer,
    )


def save_pkcs12_file(p12_bytes: bytes, filename: str = "emisor.p12") -> str:
    directory = ensure_cert_dir()
    # Normalize extension
    lower = filename.lower()
    if not (lower.endswith(".p12") or lower.endswith(".pfx")):
        filename = "emisor.p12"
    safe_name = "emisor" + (".pfx" if lower.endswith(".pfx") else ".p12")
    path = os.path.join(directory, safe_name)
    with open(path, "wb") as f:
        f.write(p12_bytes)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def read_pkcs12_file(path: str) -> bytes:
    if not path or not os.path.isfile(path):
        raise FileNotFoundError("No hay certificado almacenado.")
    with open(path, "rb") as f:
        return f.read()


def format_not_after(dt: Optional[datetime]) -> str:
    if not dt:
        return "No disponible"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
