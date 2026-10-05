"""Sign DGII seed XML with PKCS#12 (XMLDSig enveloped)."""

from __future__ import annotations

from typing import Union

from lxml import etree
from signxml import XMLSigner, methods

from .cert_store import load_pkcs12


def sign_semilla_xml(semilla_xml: Union[str, bytes], p12_bytes: bytes, passphrase: str) -> bytes:
    """
    Firma la semilla XML de autenticación DGII con el certificado del emisor.
    Retorna XML firmado (bytes, UTF-8).
    """
    if isinstance(semilla_xml, str):
        xml_bytes = semilla_xml.encode("utf-8")
    else:
        xml_bytes = semilla_xml

    key, cert, additional = load_pkcs12(p12_bytes, passphrase)
    root = etree.fromstring(xml_bytes)

    signer = XMLSigner(
        method=methods.enveloped,
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256",
        c14n_algorithm="http://www.w3.org/2001/10/xml-exc-c14n#",
    )
    # Prefer exclusive C14N commonly accepted by DGII stacks
    signed = signer.sign(root, key=key, cert=cert, always_add_key_value=True)
    return etree.tostring(signed, encoding="utf-8", xml_declaration=True)
