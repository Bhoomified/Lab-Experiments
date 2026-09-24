from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


# ============================================================
# AES KEY INPUT
# ============================================================

def get_aes_key():
    """
    Get a numeric AES key from the user.

    Supported key sizes:
        128-bit -> 16 digits
        192-bit -> 24 digits
        256-bit -> 32 digits

    The user only enters digits.
    The program converts them to bytes internally.
    """

    while True:

        print("\nChoose AES key size:")
        print("1. AES-128 (16 digits)")
        print("2. AES-192 (24 digits)")
        print("3. AES-256 (32 digits)")
        print("4. Generate a random AES key")

        choice = input("\nEnter your choice: ").strip()

        # ----------------------------------------------------
        # AES-128
        # ----------------------------------------------------

        if choice == "1":

            required_length = 16

            key_input = input(
                "Enter a 16-digit numeric AES key: "
            ).strip()

            if not key_input.isdigit():
                print("Invalid key! Enter digits only.")
                continue

            if len(key_input) != required_length:
                print(
                    "Invalid key length!"
                    "\nAES-128 requires exactly 16 digits."
                )
                continue

            return key_input.encode("ascii")

        # ----------------------------------------------------
        # AES-192
        # ----------------------------------------------------

        elif choice == "2":

            required_length = 24

            key_input = input(
                "Enter a 24-digit numeric AES key: "
            ).strip()

            if not key_input.isdigit():
                print("Invalid key! Enter digits only.")
                continue

            if len(key_input) != required_length:
                print(
                    "Invalid key length!"
                    "\nAES-192 requires exactly 24 digits."
                )
                continue

            return key_input.encode("ascii")

        # ----------------------------------------------------
        # AES-256
        # ----------------------------------------------------

        elif choice == "3":

            required_length = 32

            key_input = input(
                "Enter a 32-digit numeric AES key: "
            ).strip()

            if not key_input.isdigit():
                print("Invalid key! Enter digits only.")
                continue

            if len(key_input) != required_length:
                print(
                    "Invalid key length!"
                    "\nAES-256 requires exactly 32 digits."
                )
                continue

            return key_input.encode("ascii")

        # ----------------------------------------------------
        # RANDOM KEY
        # ----------------------------------------------------

        elif choice == "4":

            print("\nChoose random key size:")
            print("1. AES-128")
            print("2. AES-192")
            print("3. AES-256")

            random_choice = input(
                "Enter your choice: "
            ).strip()

            if random_choice == "1":
                return get_random_bytes(16)

            elif random_choice == "2":
                return get_random_bytes(24)

            elif random_choice == "3":
                return get_random_bytes(32)

            else:
                print("Invalid choice.")

        else:
            print("Invalid choice. Please select 1-4.")


# ============================================================
# AES ENCRYPTION
# ============================================================

def aes_encrypt(plaintext, key):
    """
    Encrypt plaintext using AES-CBC.
    """

    # AES block size = 16 bytes
    iv = get_random_bytes(AES.block_size)

    # PKCS#7 padding
    padded_plaintext = pad(
        plaintext,
        AES.block_size
    )

    # Create AES-CBC cipher
    cipher = AES.new(
        key,
        AES.MODE_CBC,
        iv
    )

    # Encrypt
    ciphertext = cipher.encrypt(
        padded_plaintext
    )

    return iv, ciphertext


# ============================================================
# AES DECRYPTION
# ============================================================

def aes_decrypt(ciphertext, key, iv):
    """
    Decrypt AES-CBC ciphertext and remove padding.
    """

    cipher = AES.new(
        key,
        AES.MODE_CBC,
        iv
    )

    # Decrypt
    padded_plaintext = cipher.decrypt(
        ciphertext
    )

    # Validate and remove padding
    plaintext = unpad(
        padded_plaintext,
        AES.block_size
    )

    return plaintext


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_result(
    plaintext,
    key,
    iv,
    ciphertext,
    decrypted
):

    print("\n" + "=" * 60)
    print("              AES ENCRYPTION")
    print("=" * 60)

    print("\nOriginal Plaintext:")
    print(plaintext.decode("utf-8"))

    print("\nKey (Hex):")
    print(key.hex())

    print("\nKey Length:")
    print(f"{len(key) * 8} bits")

    print("\nInitialization Vector (IV):")
    print(iv.hex())

    print("\nCiphertext (Hex):")
    print(ciphertext.hex())

    print("\n" + "=" * 60)
    print("              AES DECRYPTION")
    print("=" * 60)

    print("\nDecrypted Plaintext:")
    print(decrypted.decode("utf-8"))

    print("\n" + "=" * 60)
    print("              VERIFICATION")
    print("=" * 60)

    if plaintext == decrypted:

        print("\nSUCCESS ✅")
        print("Original Plaintext == Decrypted Plaintext")

    else:

        print("\nFAILED ❌")
        print("Original Plaintext != Decrypted Plaintext")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("             AES CRYPTOGRAPHY LAB")
    print("=" * 60)

    while True:

        print("\n1. Encrypt and Decrypt")
        print("2. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if choice == "2":
            print("\nExiting AES program...")
            break

        # ----------------------------------------------------
        # INVALID OPTION
        # ----------------------------------------------------

        if choice != "1":
            print(
                "\nInvalid choice. Please select 1 or 2."
            )
            continue

        # ----------------------------------------------------
        # PLAINTEXT
        # ----------------------------------------------------

        message = input(
            "\nEnter plaintext: "
        )

        # Convert user text to bytes
        plaintext = message.encode("utf-8")

        try:

            # ------------------------------------------------
            # KEY
            # ------------------------------------------------

            key = get_aes_key()

            # ------------------------------------------------
            # ENCRYPTION
            # ------------------------------------------------

            iv, ciphertext = aes_encrypt(
                plaintext,
                key
            )

            # ------------------------------------------------
            # DECRYPTION
            # ------------------------------------------------

            decrypted = aes_decrypt(
                ciphertext,
                key,
                iv
            )

            # ------------------------------------------------
            # DISPLAY
            # ------------------------------------------------

            display_result(
                plaintext,
                key,
                iv,
                ciphertext,
                decrypted
            )

        except ValueError as error:

            print(
                "\nEncryption/Decryption Error:"
            )

            print(error)

        except Exception as error:

            print(
                "\nUnexpected Error:"
            )

            print(error)


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    main()