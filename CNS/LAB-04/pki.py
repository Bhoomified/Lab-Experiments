from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta


# Generate RSA private key
def generate_key():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )


# Create a self-signed CA certificate
def create_ca_certificate(ca_key, ca_name):
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Cyber Security Lab"),
        x509.NameAttribute(NameOID.COMMON_NAME, ca_name),
    ])

    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now())
        .not_valid_after(datetime.now() + timedelta(days=365))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True
        )
        .sign(ca_key, hashes.SHA256())
    )

    return certificate


# Create CSR for the user
def create_csr(user_key, user_name):
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Cyber Security Lab"),
        x509.NameAttribute(NameOID.COMMON_NAME, user_name),
    ])

    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(subject)
        .sign(user_key, hashes.SHA256())
    )

    return csr


# CA signs the user's certificate
def sign_certificate(csr, ca_certificate, ca_key):
    certificate = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_certificate.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now())
        .not_valid_after(datetime.now() + timedelta(days=365))
        .sign(ca_key, hashes.SHA256())
    )

    return certificate


# Verify certificate
def verify_certificate(certificate, ca_certificate):
    try:
        if certificate.issuer != ca_certificate.subject:
            return False

        ca_certificate.public_key().verify(
            certificate.signature,
            certificate.tbs_certificate_bytes,
            certificate.signature_hash_algorithm
        )

        return True

    except Exception:
        return False


# ---------------- MAIN PROGRAM ----------------

print("========== PKI DEMONSTRATION ==========")

# Dynamic input
ca_name = input("Enter Certificate Authority name: ")
user_name = input("Enter user name: ")

print("\nGenerating CA private key...")
ca_key = generate_key()

print("Creating self-signed CA certificate...")
ca_certificate = create_ca_certificate(ca_key, ca_name)

print("Generating user private key...")
user_key = generate_key()

print("Creating Certificate Signing Request (CSR)...")
csr = create_csr(user_key, user_name)

print("CA signing user certificate...")
user_certificate = sign_certificate(
    csr,
    ca_certificate,
    ca_key
)

# Save CA private key
with open("ca_private_key.pem", "wb") as file:
    file.write(
        ca_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        )
    )

# Save user private key
with open("user_private_key.pem", "wb") as file:
    file.write(
        user_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        )
    )

# Save CA certificate
with open("ca_certificate.pem", "wb") as file:
    file.write(
        ca_certificate.public_bytes(
            serialization.Encoding.PEM
        )
    )

# Save user certificate
with open("user_certificate.pem", "wb") as file:
    file.write(
        user_certificate.public_bytes(
            serialization.Encoding.PEM
        )
    )

# Verify certificate
valid = verify_certificate(
    user_certificate,
    ca_certificate
)

print("\n========== PKI DETAILS ==========")
print("Certificate Authority :", ca_name)
print("User                  :", user_name)
print("Certificate Issuer    :", user_certificate.issuer)
print("Certificate Subject   :", user_certificate.subject)
print("Certificate Algorithm :", user_certificate.signature_hash_algorithm.name)

print("\nCertificate Verification:")
if valid:
    print("VALID - Certificate trusted by the CA")
else:
    print("INVALID - Certificate verification failed")

print("\nGenerated Files:")
print("1. ca_private_key.pem")
print("2. ca_certificate.pem")
print("3. user_private_key.pem")
print("4. user_certificate.pem")

print("\nPKI execution completed successfully!")