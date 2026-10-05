"""Sign e-CF XML documents (enveloped XMLDSig)."""

from __future__ import annotations

from typing import Union

from lxml import etree

from .cert_store import load_pkcs12
from .xmldsig_util import sign_enveloped


def sign_ecf_xml(ecf_xml: Union[str, bytes], p12_bytes: bytes, passphrase: str) -> bytes:
    if isinstance(ecf_xml, str):
        xml_bytes = ecf_xml.encode("utf-8")
    else:
        xml_bytes = ecf_xml

    key, cert, _additional = load_pkcs12(p12_bytes, passphrase)
    root = etree.fromstring(xml_bytes)
    return sign_enveloped(root, key=key, cert=cert)
