"""XMLDSig enveloped signing compatible with DGII (TesteCF / e-CF).

DGII's official Java sample uses:
  - CanonicalizationMethod: Inclusive C14N 1.0
  - Reference transforms: only enveloped-signature
  - DigestMethod: SHA-256
  - SignatureMethod: RSA-SHA256

Pretty-printed whitespace in the seed XML must be removed before signing;
otherwise DGII returns HTTP 400 \"Firma del certificado invalida\".
"""

from __future__ import annotations

import base64
import hashlib
from typing import Any

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from lxml import etree

DS_NS = "http://www.w3.org/2000/09/xmldsig#"
C14N_INCLUSIVE = "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
RSA_SHA256 = "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
SHA256 = "http://www.w3.org/2001/04/xmlenc#sha256"
ENVELOPED = "http://www.w3.org/2000/09/xmldsig#enveloped-signature"


def sign_enveloped(root: etree._Element, key: Any, cert: x509.Certificate) -> bytes:
    """Sign XML with enveloped XMLDSig as required by DGII."""
    try:
        return _sign_enveloped_dgii(root, key, cert)
    except Exception as err:
        raise RuntimeError(f"No se pudo firmar XML: {err}") from err


def _strip_whitespace_nodes(elem: etree._Element) -> None:
    """Drop indentation/whitespace-only text nodes (breaks DGII digest)."""
    for el in elem.iter():
        if el.text is not None and not el.text.strip():
            el.text = None
        if el.tail is not None and not el.tail.strip():
            el.tail = None


def _c14n_inclusive(node: etree._Element) -> bytes:
    return etree.tostring(node, method="c14n", exclusive=False, with_comments=False)


def _sign_enveloped_dgii(root: etree._Element, key: Any, cert: x509.Certificate) -> bytes:
    # Re-parse to a clean tree and remove pretty-print whitespace from DGII seed
    doc = etree.fromstring(etree.tostring(root))
    _strip_whitespace_nodes(doc)

    nsmap = {"ds": DS_NS}
    signature = etree.Element(f"{{{DS_NS}}}Signature", nsmap=nsmap)
    signed_info = etree.SubElement(signature, f"{{{DS_NS}}}SignedInfo")
    etree.SubElement(
        signed_info,
        f"{{{DS_NS}}}CanonicalizationMethod",
        Algorithm=C14N_INCLUSIVE,
    )
    etree.SubElement(
        signed_info,
        f"{{{DS_NS}}}SignatureMethod",
        Algorithm=RSA_SHA256,
    )
    # URI="" → whole document; only enveloped transform (matches DGII Java sample)
    reference = etree.SubElement(signed_info, f"{{{DS_NS}}}Reference", URI="")
    transforms = etree.SubElement(reference, f"{{{DS_NS}}}Transforms")
    etree.SubElement(transforms, f"{{{DS_NS}}}Transform", Algorithm=ENVELOPED)
    etree.SubElement(reference, f"{{{DS_NS}}}DigestMethod", Algorithm=SHA256)

    # Digest of document without Signature, Inclusive C14N (default after enveloped)
    digest = hashlib.sha256(_c14n_inclusive(doc)).digest()
    etree.SubElement(reference, f"{{{DS_NS}}}DigestValue").text = base64.b64encode(digest).decode("ascii")

    # Attach Signature (without SignatureValue yet) so SignedInfo has correct ns context
    doc.append(signature)
    si_c14n = _c14n_inclusive(signed_info)
    signature_bytes = key.sign(si_c14n, padding.PKCS1v15(), hashes.SHA256())

    sig_value = etree.Element(f"{{{DS_NS}}}SignatureValue")
    sig_value.text = base64.b64encode(signature_bytes).decode("ascii")
    # Insert SignatureValue after SignedInfo
    signed_info.addnext(sig_value)

    key_info = etree.SubElement(signature, f"{{{DS_NS}}}KeyInfo")
    x509_data = etree.SubElement(key_info, f"{{{DS_NS}}}X509Data")
    der = cert.public_bytes(serialization.Encoding.DER)
    etree.SubElement(x509_data, f"{{{DS_NS}}}X509Certificate").text = base64.b64encode(der).decode("ascii")

    # Compact UTF-8 XML (no pretty print / no BOM)
    return etree.tostring(doc, encoding="utf-8", xml_declaration=True)
