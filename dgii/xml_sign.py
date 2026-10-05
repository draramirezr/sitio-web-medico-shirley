"""Sign DGII seed XML with PKCS#12 (XMLDSig enveloped)."""

from __future__ import annotations

from typing import Union

from lxml import etree

from .cert_store import load_pkcs12
from .xmldsig_util import sign_enveloped


def sign_semilla_xml(semilla_xml: Union[str, bytes], p12_bytes: bytes, passphrase: str) -> bytes:
    """
    Firma la semilla XML de autenticación DGII con el certificado del emisor.
    Retorna XML firmado (bytes, UTF-8).
    """
    if isinstance(semilla_xml, str):
        xml_bytes = semilla_xml.encode("utf-8")
    else:
        xml_bytes = semilla_xml

    key, cert, _additional = load_pkcs12(p12_bytes, passphrase)
    root = etree.fromstring(xml_bytes)
    return sign_enveloped(root, key=key, cert=cert)
