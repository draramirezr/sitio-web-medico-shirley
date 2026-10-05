"""XMLDSig enveloped signing with cryptography + lxml (no signxml/pyOpenSSL)."""

from __future__ import annotations

import base64
import hashlib
from typing import Any

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from lxml import etree

DS_NS = "http://www.w3.org/2000/09/xmldsig#"
C14N_EXCL = "http://www.w3.org/2001/10/xml-exc-c14n#"
RSA_SHA256 = "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
SHA256 = "http://www.w3.org/2001/04/xmlenc#sha256"
ENVELOPED = "http://www.w3.org/2000/09/xmldsig#enveloped-signature"


def sign_enveloped(root: etree._Element, key: Any, cert: x509.Certificate) -> bytes:
    """Sign XML with enveloped XMLDSig (RSA-SHA256)."""
    try:
        return _sign_enveloped(root, key, cert)
    except Exception as err:
        raise RuntimeError(f"No se pudo firmar XML: {err}") from err


def _c14n(node: etree._Element) -> bytes:
    return etree.tostring(node, method="c14n", exclusive=True, with_comments=False)


def _sign_enveloped(root: etree._Element, key: Any, cert: x509.Certificate) -> bytes:
    doc = etree.fromstring(etree.tostring(root))
    nsmap = {"ds": DS_NS}

    signature = etree.Element(f"{{{DS_NS}}}Signature", nsmap=nsmap)
    signed_info = etree.SubElement(signature, f"{{{DS_NS}}}SignedInfo")
    etree.SubElement(
        signed_info,
        f"{{{DS_NS}}}CanonicalizationMethod",
        Algorithm=C14N_EXCL,
    )
    etree.SubElement(
        signed_info,
        f"{{{DS_NS}}}SignatureMethod",
        Algorithm=RSA_SHA256,
    )
    reference = etree.SubElement(signed_info, f"{{{DS_NS}}}Reference", URI="")
    transforms = etree.SubElement(reference, f"{{{DS_NS}}}Transforms")
    etree.SubElement(transforms, f"{{{DS_NS}}}Transform", Algorithm=ENVELOPED)
    etree.SubElement(transforms, f"{{{DS_NS}}}Transform", Algorithm=C14N_EXCL)
    etree.SubElement(reference, f"{{{DS_NS}}}DigestMethod", Algorithm=SHA256)

    # Digest document before appending Signature (enveloped transform excludes it).
    digest = hashlib.sha256(_c14n(doc)).digest()
    etree.SubElement(reference, f"{{{DS_NS}}}DigestValue").text = base64.b64encode(digest).decode("ascii")

    si_c14n = _c14n(signed_info)
    signature_bytes = key.sign(si_c14n, padding.PKCS1v15(), hashes.SHA256())
    etree.SubElement(signature, f"{{{DS_NS}}}SignatureValue").text = base64.b64encode(signature_bytes).decode("ascii")

    key_info = etree.SubElement(signature, f"{{{DS_NS}}}KeyInfo")
    x509_data = etree.SubElement(key_info, f"{{{DS_NS}}}X509Data")
    der = cert.public_bytes(serialization.Encoding.DER)
    etree.SubElement(x509_data, f"{{{DS_NS}}}X509Certificate").text = base64.b64encode(der).decode("ascii")

    doc.append(signature)
    return etree.tostring(doc, encoding="utf-8", xml_declaration=True)
