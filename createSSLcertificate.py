from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

# Generate the PRIVATE KEY
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Create the autosign CERTIFICATE => COMPILE THAT WITH YOUR INFORMATIONS
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"YourCountry"), #es FR (France)
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"YourProvince"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"YourCity"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"MyOrg"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
])

cert = x509.CertificateBuilder().subject_name(subject)\
    .issuer_name(issuer)\
    .public_key(key.public_key())\
    .serial_number(x509.random_serial_number())\
    .not_valid_before(datetime.datetime.now())\
    .not_valid_after(datetime.datetime.now() + datetime.timedelta(days=365))\
    .add_extension(x509.SubjectAlternativeName([x509.DNSName(u"localhost")]), critical=False)\
    .sign(key, hashes.SHA256())

# Save the private key
with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))

# Save the certificate
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("\nCERTIFICATE AND KEY GENERATED WITH SUCCESS")
