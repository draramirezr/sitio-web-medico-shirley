"""Load legacy PKCS#12 (RC2-40 / 3DES) that OpenSSL 3 cryptography rejects."""

from __future__ import annotations

import hashlib
import hmac as _hmac
from typing import List, Tuple

from asn1crypto import pkcs12 as a12
from asn1crypto.pkcs12 import AuthenticatedSafe, SafeContents
from cryptography.hazmat.primitives.serialization import (
    BestAvailableEncryption,
    NoEncryption,
    load_der_private_key,
)
from cryptography.hazmat.primitives.serialization.pkcs12 import serialize_key_and_certificates
from cryptography import x509
from Crypto.Cipher import ARC2, DES3
from Crypto.Util.Padding import unpad


def _bmp_password(password: str) -> bytes:
    # RFC 7292: BMPString + NUL
    return (password or "").encode("utf-16-be") + b"\x00\x00"


def _pkcs12_kdf(password: bytes, salt: bytes, iterations: int, id_byte: int, out_len: int) -> bytes:
    """PKCS#12 key derivation (RFC 7292 Appendix B)."""
    v = 64  # SHA-1 block size for this scheme
    diversifier = bytes([id_byte]) * v

    def _expand(data: bytes) -> bytes:
        if not data:
            return b""
        return (data * ((v // len(data)) + 1))[:v]

    d_salt = _expand(salt)
    d_pass = _expand(password)
    i_vec = bytearray(d_salt + d_pass)

    result = b""
    while len(result) < out_len:
        a = hashlib.sha1(diversifier + bytes(i_vec)).digest()
        for _ in range(iterations - 1):
            a = hashlib.sha1(a).digest()
        result += a

        b = (a * ((v // len(a)) + 1))[:v]
        b_int = int.from_bytes(b, "big") + 1
        for j in range(0, len(i_vec), v):
            chunk = int.from_bytes(i_vec[j : j + v], "big") + b_int
            i_vec[j : j + v] = (chunk % (1 << (v * 8))).to_bytes(v, "big")
    return result[:out_len]


def _pbe_decrypt(alg_name: str, params: dict, encrypted: bytes, password: bytes) -> bytes:
    salt = params["salt"]
    iterations = int(params["iterations"])
    if alg_name in ("pbewithshaand40bitrc2cbc", "pkcs12_sha1_rc2_40"):
        key = _pkcs12_kdf(password, salt, iterations, 1, 5)  # 40-bit
        iv = _pkcs12_kdf(password, salt, iterations, 2, 8)
        cipher = ARC2.new(key, ARC2.MODE_CBC, iv=iv, effective_keylen=40)
        return unpad(cipher.decrypt(encrypted), 8)
    if alg_name in ("pbewithshaand3keytripledes_cbc", "pkcs12_sha1_tripledes_3key"):
        key = _pkcs12_kdf(password, salt, iterations, 1, 24)
        iv = _pkcs12_kdf(password, salt, iterations, 2, 8)
        cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
        return unpad(cipher.decrypt(encrypted), 8)
    raise ValueError(f"Algoritmo PKCS#12 no soportado: {alg_name}")


def _verify_mac(p12: a12.Pfx, password: bytes) -> bool:
    mac_data = p12["mac_data"]
    if not mac_data:
        return True
    salt = mac_data["mac_salt"].native
    iterations = mac_data["iterations"].native if mac_data["iterations"] else 1
    digest_algo = mac_data["mac"]["digest_algorithm"]["algorithm"].native
    expected = mac_data["mac"]["digest"].native
    hashmod = getattr(hashlib, digest_algo, None)
    if hashmod is None:
        return True
    key = _pkcs12_kdf(password, salt, iterations, 3, hashmod().digest_size)
    content = p12["auth_safe"]["content"].native
    actual = _hmac.new(key, content, hashmod).digest()
    return _hmac.compare_digest(actual, expected)


def load_pkcs12_legacy(p12_bytes: bytes, passphrase: str) -> Tuple[object, x509.Certificate, list]:
    password = _bmp_password(passphrase or "")
    p12 = a12.Pfx.load(p12_bytes)
    if not _verify_mac(p12, password):
        raise ValueError("Contraseña incorrecta (MAC PKCS#12 no válida).")

    safe = AuthenticatedSafe.load(p12["auth_safe"]["content"].native)
    key = None
    certs: List[x509.Certificate] = []

    for ci in safe:
        ctype = ci["content_type"].native
        if ctype == "data":
            contents = SafeContents.load(ci["content"].native)
            for sc in contents:
                if sc["bag_id"].native == "pkcs8_shrouded_key_bag":
                    bag = sc["bag_value"]
                    alg = bag["encryption_algorithm"]["algorithm"].native
                    params = bag["encryption_algorithm"]["parameters"].native
                    encrypted = bag["encrypted_data"].native
                    der_key = _pbe_decrypt(alg, params, encrypted, password)
                    key = load_der_private_key(der_key, password=None)
        elif ctype == "encrypted_data":
            ed = ci["content"]
            eci = ed["encrypted_content_info"]
            alg = eci["content_encryption_algorithm"]["algorithm"].native
            params = eci["content_encryption_algorithm"]["parameters"].native
            encrypted = eci["encrypted_content"].native
            decrypted = _pbe_decrypt(alg, params, encrypted, password)
            contents = SafeContents.load(decrypted)
            for sc in contents:
                if sc["bag_id"].native == "cert_bag":
                    cert_bag = sc["bag_value"]
                    if cert_bag["cert_id"].native == "x509":
                        der = cert_bag["cert_value"].native
                        certs.append(x509.load_der_x509_certificate(der))

    if key is None or not certs:
        raise ValueError("El PKCS#12 legacy no contiene clave y certificado X.509.")

    leaf = certs[0]
    try:
        pub = key.public_key().public_numbers()
        for c in certs:
            try:
                if c.public_key().public_numbers() == pub:
                    leaf = c
                    break
            except Exception:
                continue
    except Exception:
        pass
    additional = [c for c in certs if c != leaf]
    return key, leaf, additional


def modernize_pkcs12(p12_bytes: bytes, passphrase: str) -> bytes:
    """Re-export as modern AES PKCS#12 so future loads work without RC2."""
    key, cert, additional = load_pkcs12_legacy(p12_bytes, passphrase)
    pwd = (passphrase or "").encode("utf-8")
    enc = BestAvailableEncryption(pwd) if pwd else NoEncryption()
    return serialize_key_and_certificates(
        name=b"emisor",
        key=key,
        cert=cert,
        cas=additional,
        encryption_algorithm=enc,
    )
