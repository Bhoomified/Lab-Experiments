from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


# ============================================================
# KEY INPUT
# ============================================================

def get_des_key():
    """
    Takes an 8-digit numeric key from the user.

    Example:
        12345678

    The program automatically converts it into bytes.
    The user does NOT need to know ASCII values.
    """

    while True:
        key_input = input(
            "\nEnter an 8-digit numeric DES key: "
        ).strip()

        # Must contain digits only
        if not key_input.isdigit():
            print("Invalid key! Enter digits only.")
            continue

        # DES requires 8 bytes.
        # Since each entered character is one digit,
        # 8 digits -> 8 bytes.
        if len(key_input) != 8:
            print(
                "Invalid key length!"
                "\nDES requires exactly 8 digits."
            )
            continue

        # Convert digit characters to bytes automatically
        key = key_input.encode("ascii")

        return key


# ============================================================
# DES ENCRYPTION
# ============================================================

def des_encrypt(plaintext, key):
    """
    Encrypt plaintext using DES in CBC mode.
    """

    # DES block size = 8 bytes
    iv = get_random_bytes(DES.block_size)

    # PKCS#7 padding
    padded_plaintext = pad(
        plaintext,
        DES.block_size
    )

    # Create DES-CBC cipher
    cipher = DES.new(
        key,
        DES.MODE_CBC,
        iv
    )

    # Encrypt
    ciphertext = cipher.encrypt(
        padded_plaintext
    )

    return iv, ciphertext


# ============================================================
# DES DECRYPTION
# ============================================================

def des_decrypt(ciphertext, key, iv):
    """
    Decrypt DES-CBC ciphertext and remove padding.
    """

    # Create the same DES-CBC cipher
    cipher = DES.new(
        key,
        DES.MODE_CBC,
        iv
    )

    # Decrypt
    padded_plaintext = cipher.decrypt(
        ciphertext
    )

    # Remove and validate PKCS#7 padding
    plaintext = unpad(
        padded_plaintext,
        DES.block_size
    )

    return plaintext


# ============================================================
# DISPLAY
# ============================================================

def display_result(
    plaintext,
    key,
    iv,
    ciphertext,
    decrypted
):
    """
    Display encryption/decryption results.
    """

    print("\n" + "=" * 60)
    print("              DES ENCRYPTION")
    print("=" * 60)

    print("\nOriginal Plaintext:")
    print(plaintext.decode("utf-8"))

    print("\nNumeric Key Entered:")
    print(key.decode("ascii"))

    print("\nKey in Hex:")
    print(key.hex())

    print("\nInitialization Vector (IV):")
    print(iv.hex())

    print("\nCiphertext (Hex):")
    print(ciphertext.hex())

    print("\n" + "=" * 60)
    print("              DES DECRYPTION")
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
    print("             DES CRYPTOGRAPHY LAB")
    print("=" * 60)

    while True:

        print("\n1. Encrypt and Decrypt")
        print("2. Exit")

        choice = input("\nEnter your choice: ").strip()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if choice == "2":
            print("\nExiting DES program...")
            break

        # ----------------------------------------------------
        # INVALID OPTION
        # ----------------------------------------------------

        if choice != "1":
            print("\nInvalid choice. Please select 1 or 2.")
            continue

        # ----------------------------------------------------
        # PLAINTEXT
        # ----------------------------------------------------

        message = input(
            "\nEnter plaintext: "
        )

        # Convert text to bytes
        plaintext = message.encode("utf-8")

        # ----------------------------------------------------
        # KEY
        # ----------------------------------------------------

        key = get_des_key()

        try:

            # ------------------------------------------------
            # ENCRYPTION
            # ------------------------------------------------

            iv, ciphertext = des_encrypt(
                plaintext,
                key
            )

            # ------------------------------------------------
            # DECRYPTION
            # ------------------------------------------------

            decrypted = des_decrypt(
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