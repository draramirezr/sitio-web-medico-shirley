"""XMLDSig enveloped signing compatible with DGII (TesteCF / e-CF).

- Semilla auth XML: Signature as last child only (no FechaHoraFirma).
- e-CF XML: FechaHoraFirma must precede Signature (DGII XSD).
Inclusive C14N 1.0 + enveloped-only reference (DGII Java sample).
"""

from __future__ import annotations

import base64
import hashlib
from datetime import datetime
from typing import Any, Optional

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
    for el in elem.iter():
        if el.text is not None and not el.text.strip():
            el.text = None
        if el.tail is not None and not el.tail.strip():
            el.tail = None


def _c14n_inclusive(node: etree._Element) -> bytes:
    return etree.tostring(node, method="c14n", exclusive=False, with_comments=False)


def _local(tag: Any) -> str:
    if tag is None:
        return ""
    try:
        return etree.QName(tag).localname
    except Exception:
        return str(tag).split("}")[-1]


def _is_ecf_document(doc: etree._Element) -> bool:
    return _local(doc.tag) == "ECF"


def _prepare_ecf_before_digest(doc: etree._Element) -> None:
    """Move/create FechaHoraFirma as last child before signing ECF."""
    fhf: Optional[etree._Element] = None
    for child in list(doc):
        if _local(child.tag) == "FechaHoraFirma":
            fhf = child
            break
        if _local(child.tag) == "Signature":
            doc.remove(child)
    if fhf is None:
        fhf = etree.Element("FechaHoraFirma")
        fhf.text = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        doc.append(fhf)
    else:
        doc.remove(fhf)
        doc.append(fhf)


def _sign_enveloped_dgii(root: etree._Element, key: Any, cert: x509.Certificate) -> bytes:
    doc = etree.fromstring(etree.tostring(root))
    _strip_whitespace_nodes(doc)

    # ECF only: finalize FechaHoraFirma position BEFORE digest
    if _is_ecf_document(doc):
        _prepare_ecf_before_digest(doc)

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
    reference = etree.SubElement(signed_info, f"{{{DS_NS}}}Reference", URI="")
    transforms = etree.SubElement(reference, f"{{{DS_NS}}}Transforms")
    etree.SubElement(transforms, f"{{{DS_NS}}}Transform", Algorithm=ENVELOPED)
    etree.SubElement(reference, f"{{{DS_NS}}}DigestMethod", Algorithm=SHA256)

    digest = hashlib.sha256(_c14n_inclusive(doc)).digest()
    etree.SubElement(reference, f"{{{DS_NS}}}DigestValue").text = base64.b64encode(digest).decode("ascii")

    # Append Signature as final child (after FechaHoraFirma on ECF; alone on Semilla)
    doc.append(signature)

    si_c14n = _c14n_inclusive(signed_info)
    signature_bytes = key.sign(si_c14n, padding.PKCS1v15(), hashes.SHA256())

    sig_value = etree.Element(f"{{{DS_NS}}}SignatureValue")
    sig_value.text = base64.b64encode(signature_bytes).decode("ascii")
    signed_info.addnext(sig_value)

    key_info = etree.SubElement(signature, f"{{{DS_NS}}}KeyInfo")
    x509_data = etree.SubElement(key_info, f"{{{DS_NS}}}X509Data")
    der = cert.public_bytes(serialization.Encoding.DER)
    etree.SubElement(x509_data, f"{{{DS_NS}}}X509Certificate").text = base64.b64encode(der).decode("ascii")

    return etree.tostring(doc, encoding="utf-8", xml_declaration=True)
