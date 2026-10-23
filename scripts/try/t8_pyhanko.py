"""T8: pyHanko seals a generated PDF; a validator flags an edit made after sealing.
   uv run --no-project --with pyhanko==0.38.0 --with weasyprint==70.0 python scripts/try/t8_pyhanko.py"""
import datetime
import io
import tempfile
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko.sign import signers
from pyhanko.sign.validation import validate_pdf_signature
from pyhanko_certvalidator import ValidationContext
from weasyprint import HTML

tmp = Path(tempfile.mkdtemp())
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "realestate POC demonstration seal")])
now = datetime.datetime.now(datetime.timezone.utc)
cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key())
        .serial_number(x509.random_serial_number()).not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=30))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(key, hashes.SHA256()))
(tmp / "key.pem").write_bytes(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                                serialization.NoEncryption()))
(tmp / "cert.pem").write_bytes(cert.public_bytes(serialization.Encoding.PEM))

pdf = HTML(string="<h1>DEMONSTRATION contract draft</h1><p>Purchase price: $625,000.</p>").write_pdf()
signer = signers.SimpleSigner.load(str(tmp / "key.pem"), str(tmp / "cert.pem"))
out = io.BytesIO()
signers.sign_pdf(IncrementalPdfFileWriter(io.BytesIO(pdf)), signers.PdfSignatureMetadata(field_name="Seal"),
                 signer=signer, output=out)
sealed = out.getvalue()

from pyhanko.keys import load_cert_from_pemder  # noqa: E402

vc = ValidationContext(trust_roots=[load_cert_from_pemder(str(tmp / "cert.pem"))])


def check(data: bytes) -> str:
    sig = PdfFileReader(io.BytesIO(data)).embedded_signatures[0]
    st = validate_pdf_signature(sig, vc)
    return f"intact={st.intact} valid={st.valid} coverage={st.coverage.name}"


print("sealed  :", check(sealed))
idx = sealed.find(b"625,000")
if idx < 0:  # text is compressed in the content stream; flip a byte inside the signed range instead
    idx = len(sealed) // 3
tampered = bytearray(sealed)
tampered[idx] = (tampered[idx] + 1) % 256
try:
    res = check(bytes(tampered))
except Exception as e:  # a reader may refuse the damaged file outright, which also flags the edit
    res = f"refused: {type(e).__name__}"
print("tampered:", res)
ok = "intact=True" in check(sealed) and "intact=True" not in res
print("T8", "PASS" if ok else "FAIL")
