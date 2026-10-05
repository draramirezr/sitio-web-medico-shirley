"""Sign e-CF XML documents (enveloped XMLDSig)."""

from __future__ import annotations

from typing import Union

from lxml import etree
from signxml import XMLSigner, methods

from .cert_store import load_pkcs12


def sign_ecf_xml(ecf_xml: Union[str, bytes], p12_bytes: bytes, passphrase: str) -> bytes:
    if isinstance(ecf_xml, str):
        xml_bytes = ecf_xml.encode("utf-8")
    else:
        xml_bytes = ecf_xml

    key, cert, _additional = load_pkcs12(p12_bytes, passphrase)
    root = etree.fromstring(xml_bytes)
    signer = XMLSigner(
        method=methods.enveloped,
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256",
        c14n_algorithm="http://www.w3.org/2001/10/xml-exc-c14n#",
    )
    signed = signer.sign(root, key=key, cert=cert, always_add_key_value=True)
    return etree.tostring(signed, encoding="utf-8", xml_declaration=True)
