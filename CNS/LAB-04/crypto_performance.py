
import time
import statistics

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.asymmetric import padding


# Number of times each operation is tested
ITERATIONS = 10


# ============================================================
# RSA PERFORMANCE
# ============================================================

def benchmark_rsa():
    key_generation_times = []
    encryption_times = []
    decryption_times = []

    message = b"Hello Cyber Security"

    for _ in range(ITERATIONS):

        # RSA Key Generation
        start = time.perf_counter()

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        public_key = private_key.public_key()

        end = time.perf_counter()
        key_generation_times.append((end - start) * 1000)

        # RSA Encryption
        start = time.perf_counter()

        encrypted = public_key.encrypt(
            message,
            # OAEP padding is used for secure RSA encryption
            __import__(
                "cryptography.hazmat.primitives.asymmetric.padding",
                fromlist=["OAEP"]
            ).OAEP(
                mgf=__import__(
                    "cryptography.hazmat.primitives.asymmetric.padding",
                    fromlist=["MGF1"]
                ).MGF1(
                    algorithm=hashes.SHA256()
                ),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        end = time.perf_counter()
        encryption_times.append((end - start) * 1000)

        # RSA Decryption
        start = time.perf_counter()

        private_key.decrypt(
            encrypted,
            __import__(
                "cryptography.hazmat.primitives.asymmetric.padding",
                fromlist=["OAEP"]
            ).OAEP(
                mgf=__import__(
                    "cryptography.hazmat.primitives.asymmetric.padding",
                    fromlist=["MGF1"]
                ).MGF1(
                    algorithm=hashes.SHA256()
                ),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        end = time.perf_counter()
        decryption_times.append((end - start) * 1000)

    return (
        statistics.mean(key_generation_times),
        statistics.mean(encryption_times),
        statistics.mean(decryption_times)
    )


# ============================================================
# PKI PERFORMANCE
# ============================================================

def benchmark_pki():
    ca_key_times = []
    certificate_times = []
    verification_times = []

    for _ in range(ITERATIONS):

        # Generate CA key
        start = time.perf_counter()

        ca_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        end = time.perf_counter()
        ca_key_times.append((end - start) * 1000)

        # Create CA certificate
        start = time.perf_counter()

        subject = issuer = x509.Name([
            x509.NameAttribute(
                NameOID.COUNTRY_NAME, "IN"
            ),
            x509.NameAttribute(
                NameOID.ORGANIZATION_NAME,
                "Cyber Security Lab"
            ),
            x509.NameAttribute(
                NameOID.COMMON_NAME,
                "Lab CA"
            )
        ])

        ca_certificate = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(ca_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(
                __import__("datetime").datetime.now()
            )
            .not_valid_after(
                __import__("datetime").datetime.now()
                + __import__("datetime").timedelta(days=365)
            )
            .add_extension(
                x509.BasicConstraints(
                    ca=True,
                    path_length=None
                ),
                critical=True
            )
            .sign(
                ca_key,
                hashes.SHA256()
            )
        )

        # Create user key
        user_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # Create CSR
        user_subject = x509.Name([
            x509.NameAttribute(
                NameOID.COUNTRY_NAME, "IN"
            ),
            x509.NameAttribute(
                NameOID.ORGANIZATION_NAME,
                "Cyber Security Lab"
            ),
            x509.NameAttribute(
                NameOID.COMMON_NAME,
                "User"
            )
        ])

        csr = (
            x509.CertificateSigningRequestBuilder()
            .subject_name(user_subject)
            .sign(
                user_key,
                hashes.SHA256()
            )
        )

        # CA signs user certificate
        start = time.perf_counter()

        user_certificate = (
            x509.CertificateBuilder()
            .subject_name(csr.subject)
            .issuer_name(ca_certificate.subject)
            .public_key(csr.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(
                __import__("datetime").datetime.now()
            )
            .not_valid_after(
                __import__("datetime").datetime.now()
                + __import__("datetime").timedelta(days=365)
            )
            .sign(
                ca_key,
                hashes.SHA256()
            )
        )

        end = time.perf_counter()
        certificate_times.append((end - start) * 1000)

        # Verify certificate signature
        start = time.perf_counter()

        ca_certificate.public_key().verify(
    user_certificate.signature,
    user_certificate.tbs_certificate_bytes,
    padding.PKCS1v15(),
    user_certificate.signature_hash_algorithm
)

        end = time.perf_counter()
        verification_times.append((end - start) * 1000)

    return (
        statistics.mean(ca_key_times),
        statistics.mean(certificate_times),
        statistics.mean(verification_times)
    )


# ============================================================
# DIFFIE-HELLMAN PERFORMANCE
# ============================================================

def benchmark_diffie_hellman():
    key_generation_times = []
    exchange_times = []

    for _ in range(ITERATIONS):

        # Generate DH parameters
        start = time.perf_counter()

        parameters = dh.generate_parameters(
            generator=2,
            key_size=2048
        )

        end = time.perf_counter()

        parameter_time = (end - start) * 1000

        # Alice key generation
        start = time.perf_counter()

        alice_private = parameters.generate_private_key()
        alice_public = alice_private.public_key()

        # Bob key generation
        bob_private = parameters.generate_private_key()
        bob_public = bob_private.public_key()

        end = time.perf_counter()

        key_generation_times.append(
            parameter_time + ((end - start) * 1000)
        )

        # Shared secret calculation
        start = time.perf_counter()

        alice_shared = alice_private.exchange(
            bob_public
        )

        bob_shared = bob_private.exchange(
            alice_public
        )

        end = time.perf_counter()

        exchange_times.append(
            (end - start) * 1000
        )

        # Check both secrets match
        if alice_shared != bob_shared:
            raise Exception(
                "Diffie-Hellman shared keys do not match!"
            )

    return (
        statistics.mean(key_generation_times),
        statistics.mean(exchange_times)
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

print("=" * 70)
print("       CRYPTOGRAPHIC ALGORITHM PERFORMANCE ANALYSIS")
print("=" * 70)

print("\nNumber of iterations:", ITERATIONS)

print("\nRunning RSA benchmark...")
rsa_results = benchmark_rsa()

print("Running PKI benchmark...")
pki_results = benchmark_pki()

print("Running Diffie-Hellman benchmark...")
dh_results = benchmark_diffie_hellman()


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 70)
print("                    PERFORMANCE RESULTS")
print("=" * 70)

print(
    f"\n{'Algorithm':<20}"
    f"{'Key Generation':>18}"
    f"{'Main Operation':>18}"
    f"{'Verification/Decrypt':>22}"
)

print("-" * 70)

print(
    f"{'RSA':<20}"
    f"{rsa_results[0]:>15.3f} ms"
    f"{rsa_results[1]:>15.3f} ms"
    f"{rsa_results[2]:>19.3f} ms"
)

print(
    f"{'PKI':<20}"
    f"{pki_results[0]:>15.3f} ms"
    f"{pki_results[1]:>15.3f} ms"
    f"{pki_results[2]:>19.3f} ms"
)

print(
    f"{'Diffie-Hellman':<20}"
    f"{dh_results[0]:>15.3f} ms"
    f"{dh_results[1]:>15.3f} ms"
    f"{'N/A':>22}"
)

print("-" * 70)

print("\nNote:")
print("• RSA measures key generation, encryption and decryption.")
print("• PKI measures CA key generation, certificate signing and verification.")
print("• Diffie-Hellman measures parameter/key generation and shared-secret exchange.")

print("\nPerformance analysis completed successfully!")
