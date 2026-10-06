"""Secure PKCS#12 storage and passphrase encryption."""

from __future__ import annotations

import base64
import hashlib
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Tuple

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption, pkcs12
from cryptography.hazmat.primitives.serialization.pkcs12 import serialize_key_and_certificates
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
    """
    Load PKCS#12. Tries cryptography first; falls back to legacy RC2-40/3DES
    (common in DGII certs) which OpenSSL 3 often rejects as 'invalid password'.
    """
    raw = passphrase if passphrase is not None else ""
    # Keep exact password first; also try strip (copy/paste spaces)
    candidates = [raw]
    stripped = raw.strip()
    if stripped != raw:
        candidates.append(stripped)

    last_err: Optional[Exception] = None
    for pwd_str in candidates:
        password = pwd_str.encode("utf-8") if pwd_str else None
        for pwd in ((password, b"") if password is None else (password,)):
            try:
                key, cert, additional = pkcs12.load_key_and_certificates(p12_bytes, pwd)
                if key is not None and cert is not None:
                    return key, cert, additional or []
            except Exception as e:
                last_err = e

        # Legacy RC2-40 / 3DES path (DGII / Windows export)
        try:
            from .pkcs12_legacy import load_pkcs12_legacy

            return load_pkcs12_legacy(p12_bytes, pwd_str)
        except Exception as e:
            last_err = e

    detail = str(last_err) if last_err else "desconocido"
    raise ValueError(
        "Certificado PKCS#12 inválido o contraseña incorrecta. "
        "Si la contraseña es correcta, el archivo puede usar cifrado antiguo; "
        f"detalle: {detail}"
    )


def modernize_pkcs12_bytes(p12_bytes: bytes, passphrase: str) -> bytes:
    """Re-save as modern AES PKCS#12 after a successful load."""
    key, cert, additional = load_pkcs12(p12_bytes, passphrase)
    pwd = (passphrase or "").encode("utf-8")
    if pwd:
        enc = BestAvailableEncryption(pwd)
    else:
        from cryptography.hazmat.primitives.serialization import NoEncryption

        enc = NoEncryption()
    return serialize_key_and_certificates(
        name=b"emisor",
        key=key,
        cert=cert,
        cas=additional,
        encryption_algorithm=enc,
    )


def inspect_pkcs12(p12_bytes: bytes, passphrase: str) -> CertInfo:
    _key, cert, _extra = load_pkcs12(p12_bytes, passphrase)
    fp = cert.fingerprint(hashlib.sha256()).hex().upper()
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
