"""XMLDSig enveloped signing without depending on broken OpenSSL.verify imports.

Tries signxml first; falls back to a cryptography + lxml implementation.
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
C14N_EXCL = "http://www.w3.org/2001/10/xml-exc-c14n#"
RSA_SHA256 = "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
SHA256 = "http://www.w3.org/2001/04/xmlenc#sha256"
ENVELOPED = "http://www.w3.org/2000/09/xmldsig#enveloped-signature"


def sign_enveloped(root: etree._Element, key: Any, cert: x509.Certificate) -> bytes:
    try:
        from signxml import XMLSigner, methods

        signer = XMLSigner(
            method=methods.enveloped,
            signature_algorithm="rsa-sha256",
            digest_algorithm="sha256",
            c14n_algorithm=C14N_EXCL,
        )
        signed = signer.sign(root, key=key, cert=cert, always_add_key_value=True)
        return etree.tostring(signed, encoding="utf-8", xml_declaration=True)
    except Exception as primary_err:
        try:
            return _sign_enveloped_fallback(root, key, cert)
        except Exception as fallback_err:
            raise RuntimeError(
                f"No se pudo firmar XML (signxml: {primary_err}; fallback: {fallback_err})"
            ) from fallback_err


def _c14n(node: etree._Element) -> bytes:
    return etree.tostring(node, method="c14n", exclusive=True, with_comments=False)


def _sign_enveloped_fallback(root: etree._Element, key: Any, cert: x509.Certificate) -> bytes:
    """Minimal enveloped XMLDSig (RSA-SHA256) compatible with common DGII validators."""
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

    # Digest of document without Signature (enveloped): canonicalize current doc
    digest = hashlib.sha256(_c14n(doc)).digest()
    etree.SubElement(reference, f"{{{DS_NS}}}DigestValue").text = base64.b64encode(digest).decode("ascii")

    # Temporary attach SignedInfo structure for signing bytes
    # Compute SignatureValue over canonical SignedInfo
    si_c14n = _c14n(signed_info)
    signature_bytes = key.sign(si_c14n, padding.PKCS1v15(), hashes.SHA256())
    etree.SubElement(signature, f"{{{DS_NS}}}SignatureValue").text = base64.b64encode(signature_bytes).decode("ascii")

    key_info = etree.SubElement(signature, f"{{{DS_NS}}}KeyInfo")
    x509_data = etree.SubElement(key_info, f"{{{DS_NS}}}X509Data")
    der = cert.public_bytes(serialization.Encoding.DER)
    etree.SubElement(x509_data, f"{{{DS_NS}}}X509Certificate").text = base64.b64encode(der).decode("ascii")

    doc.append(signature)

    # Recompute digest AFTER knowing signature is separate — enveloped transform excludes Signature.
    # Standard approach: digest the document with Signature removed for digest calculation first,
    # which we already did on `doc` before append. Good.

    # But SignedInfo was built before SignatureValue; Reference digest was of doc without Signature.
    # After append, we must NOT change DigestValue. SignatureValue already computed over SignedInfo.
    # However SignedInfo's DigestValue was set before we had final Signature node — correct for enveloped.

    return etree.tostring(doc, encoding="utf-8", xml_declaration=True)
