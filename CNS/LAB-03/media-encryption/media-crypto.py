from pathlib import Path
import struct

from Crypto.Cipher import AES, DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


# ============================================================
# CONFIGURATION
# ============================================================

CHUNK_SIZE = 64 * 1024       # 64 KB
MAGIC = b"MC01"

AES_ALGORITHM = b"A"
DES_ALGORITHM = b"D"


# ============================================================
# KEY INPUT
# ============================================================

def get_aes_key():
    """
    Get an AES key using numeric digits only.

    AES-128 -> 16 digits
    AES-192 -> 24 digits
    AES-256 -> 32 digits
    """

    while True:

        print("\nChoose AES key size:")
        print("1. AES-128 (16 digits)")
        print("2. AES-192 (24 digits)")
        print("3. AES-256 (32 digits)")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            required_length = 16
            key_size_name = "AES-128"

        elif choice == "2":
            required_length = 24
            key_size_name = "AES-192"

        elif choice == "3":
            required_length = 32
            key_size_name = "AES-256"

        else:
            print("Invalid choice.")
            continue

        key_input = input(
            f"Enter a {required_length}-digit numeric key: "
        ).strip()

        if not key_input.isdigit():
            print("Invalid key! Digits only.")
            continue

        if len(key_input) != required_length:
            print(
                f"Invalid key length! "
                f"{key_size_name} requires "
                f"exactly {required_length} digits."
            )
            continue

        return key_input.encode("ascii")


def get_des_key():
    """
    Get an 8-digit numeric DES key.
    """

    while True:

        key_input = input(
            "\nEnter an 8-digit numeric DES key: "
        ).strip()

        if not key_input.isdigit():
            print("Invalid key! Digits only.")
            continue

        if len(key_input) != 8:
            print(
                "Invalid key length! "
                "DES requires exactly 8 digits."
            )
            continue

        return key_input.encode("ascii")


# ============================================================
# FILE VALIDATION
# ============================================================

def validate_input_file(file_path):
    """
    Check whether the input path exists and is a file.
    """

    path = Path(file_path).expanduser()

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Path is not a regular file: {path}"
        )

    return path


# ============================================================
# OUTPUT PATH HANDLING
# ============================================================

def get_output_path(default_path):
    """
    Ask the user for an output path.
    Press Enter to use the default.
    """

    print(
        f"\nDefault output file:\n{default_path}"
    )

    user_input = input(
        "Enter output path or press Enter for default: "
    ).strip()

    if user_input:
        output_path = Path(user_input).expanduser()
    else:
        output_path = Path(default_path)

    if output_path.exists():

        overwrite = input(
            f"\n{output_path} already exists. "
            "Overwrite? (y/n): "
        ).strip().lower()

        if overwrite != "y":
            raise FileExistsError(
                "Output file already exists. "
                "Choose a different name."
            )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return output_path


# ============================================================
# HEADER
# ============================================================

def create_header(
    algorithm,
    key_length,
    original_filename,
    iv
):
    """
    Create a small metadata header.

    Header contains:
        MAGIC
        algorithm
        key length
        IV length
        original filename length
        original filename
        IV

    The key itself is NEVER stored.
    """

    filename_bytes = (
        original_filename.encode("utf-8")
    )

    if len(filename_bytes) > 65535:
        raise ValueError(
            "Filename is too long."
        )

    header = (
        MAGIC
        + algorithm
        + bytes([key_length])
        + bytes([len(iv)])
        + struct.pack(
            ">H",
            len(filename_bytes)
        )
        + filename_bytes
        + iv
    )

    return header


def read_header(file):
    """
    Read and validate the encrypted-file header.
    """

    magic = file.read(4)

    if magic != MAGIC:
        raise ValueError(
            "Invalid encrypted file format."
        )

    algorithm = file.read(1)

    if algorithm not in (
        AES_ALGORITHM,
        DES_ALGORITHM
    ):
        raise ValueError(
            "Unknown encryption algorithm."
        )

    key_length_data = file.read(1)

    if len(key_length_data) != 1:
        raise ValueError(
            "Corrupted encrypted file."
        )

    key_length = key_length_data[0]

    iv_length_data = file.read(1)

    if len(iv_length_data) != 1:
        raise ValueError(
            "Corrupted encrypted file."
        )

    iv_length = iv_length_data[0]

    filename_length_data = file.read(2)

    if len(filename_length_data) != 2:
        raise ValueError(
            "Corrupted encrypted file."
        )

    filename_length = struct.unpack(
        ">H",
        filename_length_data
    )[0]

    filename_bytes = file.read(
        filename_length
    )

    if len(filename_bytes) != filename_length:
        raise ValueError(
            "Corrupted encrypted file."
        )

    iv = file.read(iv_length)

    if len(iv) != iv_length:
        raise ValueError(
            "Corrupted encrypted file."
        )

    original_filename = (
        filename_bytes.decode("utf-8")
    )

    return (
        algorithm,
        key_length,
        original_filename,
        iv
    )


# ============================================================
# AES FILE ENCRYPTION
# ============================================================

def encrypt_file_aes(
    input_path,
    output_path,
    key
):
    """
    Encrypt any binary file using AES-CBC.

    The file is processed in chunks.
    """

    iv = get_random_bytes(
        AES.block_size
    )

    header = create_header(
        AES_ALGORITHM,
        len(key),
        input_path.name,
        iv
    )

    cipher = AES.new(
        key,
        AES.MODE_CBC,
        iv
    )

    with open(
        input_path,
        "rb"
    ) as source, open(
        output_path,
        "wb"
    ) as destination:

        destination.write(header)

        buffer = b""

        while True:

            chunk = source.read(
                CHUNK_SIZE
            )

            if not chunk:
                break

            buffer += chunk

            full_length = (
                len(buffer)
                // AES.block_size
            ) * AES.block_size

            if full_length > 0:

                process_data = (
                    buffer[:full_length]
                )

                buffer = (
                    buffer[full_length:]
                )

                encrypted = cipher.encrypt(
                    process_data
                )

                destination.write(
                    encrypted
                )

        # Apply padding to the final remainder
        padded_final = pad(
            buffer,
            AES.block_size
        )

        encrypted_final = cipher.encrypt(
            padded_final
        )

        destination.write(
            encrypted_final
        )


# ============================================================
# DES FILE ENCRYPTION
# ============================================================

def encrypt_file_des(
    input_path,
    output_path,
    key
):
    """
    Encrypt any binary file using DES-CBC.

    The file is processed in chunks.
    """

    iv = get_random_bytes(
        DES.block_size
    )

    header = create_header(
        DES_ALGORITHM,
        len(key),
        input_path.name,
        iv
    )

    cipher = DES.new(
        key,
        DES.MODE_CBC,
        iv
    )

    with open(
        input_path,
        "rb"
    ) as source, open(
        output_path,
        "wb"
    ) as destination:

        destination.write(header)

        buffer = b""

        while True:

            chunk = source.read(
                CHUNK_SIZE
            )

            if not chunk:
                break

            buffer += chunk

            full_length = (
                len(buffer)
                // DES.block_size
            ) * DES.block_size

            if full_length > 0:

                process_data = (
                    buffer[:full_length]
                )

                buffer = (
                    buffer[full_length:]
                )

                encrypted = cipher.encrypt(
                    process_data
                )

                destination.write(
                    encrypted
                )

        # Apply padding to final remainder
        padded_final = pad(
            buffer,
            DES.block_size
        )

        encrypted_final = cipher.encrypt(
            padded_final
        )

        destination.write(
            encrypted_final
        )


# ============================================================
# AES FILE DECRYPTION
# ============================================================

def decrypt_file_aes(
    input_path,
    output_path,
    key,
    iv,
    original_filename
):
    """
    Decrypt an AES encrypted binary file.
    """

    if len(key) != 16 and \
       len(key) != 24 and \
       len(key) != 32:

        raise ValueError(
            "Invalid AES key length."
        )

    if len(iv) != AES.block_size:
        raise ValueError(
            "Invalid AES IV."
        )

    cipher = AES.new(
        key,
        AES.MODE_CBC,
        iv
    )

    with open(
        input_path,
        "rb"
    ) as source, open(
        output_path,
        "wb"
    ) as destination:

        # Skip header
        read_header(source)

        buffer = b""

        while True:

            chunk = source.read(
                CHUNK_SIZE
            )

            if not chunk:
                break

            buffer += chunk

            # Keep the final block untouched
            # until EOF for padding validation.
            if len(buffer) >= (
                2 * AES.block_size
            ):

                process_length = (
                    (
                        len(buffer)
                        - AES.block_size
                    )
                    // AES.block_size
                ) * AES.block_size

                process_data = (
                    buffer[:process_length]
                )

                buffer = (
                    buffer[process_length:]
                )

                decrypted = cipher.decrypt(
                    process_data
                )

                destination.write(
                    decrypted
                )

        if len(buffer) != AES.block_size:
            raise ValueError(
                "Invalid AES ciphertext."
            )

        final_decrypted = cipher.decrypt(
            buffer
        )

        final_plaintext = unpad(
            final_decrypted,
            AES.block_size
        )

        destination.write(
            final_plaintext
        )


# ============================================================
# DES FILE DECRYPTION
# ============================================================

def decrypt_file_des(
    input_path,
    output_path,
    key,
    iv,
    original_filename
):
    """
    Decrypt a DES encrypted binary file.
    """

    if len(key) != 8:
        raise ValueError(
            "DES key must be 8 bytes."
        )

    if len(iv) != DES.block_size:
        raise ValueError(
            "Invalid DES IV."
        )

    cipher = DES.new(
        key,
        DES.MODE_CBC,
        iv
    )

    with open(
        input_path,
        "rb"
    ) as source, open(
        output_path,
        "wb"
    ) as destination:

        # Skip header
        read_header(source)

        buffer = b""

        while True:

            chunk = source.read(
                CHUNK_SIZE
            )

            if not chunk:
                break

            buffer += chunk

            if len(buffer) >= (
                2 * DES.block_size
            ):

                process_length = (
                    (
                        len(buffer)
                        - DES.block_size
                    )
                    // DES.block_size
                ) * DES.block_size

                process_data = (
                    buffer[:process_length]
                )

                buffer = (
                    buffer[process_length:]
                )

                decrypted = cipher.decrypt(
                    process_data
                )

                destination.write(
                    decrypted
                )

        if len(buffer) != DES.block_size:
            raise ValueError(
                "Invalid DES ciphertext."
            )

        final_decrypted = cipher.decrypt(
            buffer
        )

        final_plaintext = unpad(
            final_decrypted,
            DES.block_size
        )

        destination.write(
            final_plaintext
        )


# ============================================================
# ENCRYPTION MENU
# ============================================================

def encrypt_mode():

    print("\n" + "=" * 60)
    print("                 FILE ENCRYPTION")
    print("=" * 60)

    print("\nChoose algorithm:")
    print("1. AES")
    print("2. DES")

    algorithm_choice = input(
        "\nEnter choice: "
    ).strip()

    if algorithm_choice not in (
        "1",
        "2"
    ):
        print("Invalid algorithm choice.")
        return

    input_name = input(
        "\nEnter path of image/audio/video file: "
    ).strip()

    try:

        input_path = validate_input_file(
            input_name
        )

    except (
        FileNotFoundError,
        ValueError
    ) as error:

        print(f"\nError: {error}")
        return

    # --------------------------------------------------------
    # AES
    # --------------------------------------------------------

    if algorithm_choice == "1":

        key = get_aes_key()

        output_default = (
            str(input_path) + ".aes"
        )

        output_path = get_output_path(
            output_default
        )

        try:

            encrypt_file_aes(
                input_path,
                output_path,
                key
            )

            print(
                "\nAES encryption completed successfully!"
            )

            print(
                f"Encrypted file:\n{output_path}"
            )

            print(
                "\nKeep the numeric key safe. "
                "The key is NOT stored in the encrypted file."
            )

        except Exception as error:

            print(
                f"\nEncryption failed: {error}"
            )

    # --------------------------------------------------------
    # DES
    # --------------------------------------------------------

    else:

        key = get_des_key()

        output_default = (
            str(input_path) + ".des"
        )

        output_path = get_output_path(
            output_default
        )

        try:

            encrypt_file_des(
                input_path,
                output_path,
                key
            )

            print(
                "\nDES encryption completed successfully!"
            )

            print(
                f"Encrypted file:\n{output_path}"
            )

            print(
                "\nKeep the numeric key safe. "
                "The key is NOT stored in the encrypted file."
            )

        except Exception as error:

            print(
                f"\nEncryption failed: {error}"
            )


# ============================================================
# DECRYPTION MODE
# ============================================================

def decrypt_mode():

    print("\n" + "=" * 60)
    print("                 FILE DECRYPTION")
    print("=" * 60)

    encrypted_name = input(
        "\nEnter path of encrypted file: "
    ).strip()

    try:

        encrypted_path = validate_input_file(
            encrypted_name
        )

    except (
        FileNotFoundError,
        ValueError
    ) as error:

        print(f"\nError: {error}")
        return

    try:

        # ----------------------------------------------------
        # Read metadata
        # ----------------------------------------------------

        with open(
            encrypted_path,
            "rb"
        ) as encrypted_file:

            (
                algorithm,
                stored_key_length,
                original_filename,
                iv
            ) = read_header(
                encrypted_file
            )

        print(
            f"\nOriginal filename: "
            f"{original_filename}"
        )

        # ----------------------------------------------------
        # AES
        # ----------------------------------------------------

        if algorithm == AES_ALGORITHM:

            print(
                "\nDetected algorithm: AES"
            )

            if stored_key_length == 16:
                print(
                    "Expected key size: AES-128"
                )

            elif stored_key_length == 24:
                print(
                    "Expected key size: AES-192"
                )

            elif stored_key_length == 32:
                print(
                    "Expected key size: AES-256"
                )

            else:
                raise ValueError(
                    "Invalid stored AES key length."
                )

            key = get_aes_key()

            if len(key) != stored_key_length:

                raise ValueError(
                    "Key size does not match "
                    "the encrypted file."
                )

            output_default = (
                encrypted_path.parent
                / f"decrypted_{original_filename}"
            )

            output_path = get_output_path(
                output_default
            )

            decrypt_file_aes(
                encrypted_path,
                output_path,
                key,
                iv,
                original_filename
            )

        # ----------------------------------------------------
        # DES
        # ----------------------------------------------------

        elif algorithm == DES_ALGORITHM:

            print(
                "\nDetected algorithm: DES"
            )

            if stored_key_length != 8:
                raise ValueError(
                    "Invalid stored DES key length."
                )

            key = get_des_key()

            if len(key) != stored_key_length:

                raise ValueError(
                    "Key size does not match "
                    "the encrypted file."
                )

            output_default = (
                encrypted_path.parent
                / f"decrypted_{original_filename}"
            )

            output_path = get_output_path(
                output_default
            )

            decrypt_file_des(
                encrypted_path,
                output_path,
                key,
                iv,
                original_filename
            )

        else:

            raise ValueError(
                "Unsupported algorithm."
            )

        print(
            "\nDecryption completed successfully!"
        )

        print(
            f"Decrypted file:\n{output_path}"
        )

    except ValueError as error:

        print(
            f"\nDecryption failed:"
            f"\n{error}"
        )

    except Exception as error:

        print(
            f"\nUnexpected error:"
            f"\n{error}"
        )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    print("=" * 60)
    print("        AES / DES MEDIA FILE ENCRYPTION")
    print("=" * 60)

    print(
        "\nSupported files:"
        "\n- Images"
        "\n- Audio"
        "\n- Video"
        "\n- Documents"
        "\n- Any other binary file"
    )

    while True:

        print("\n" + "-" * 60)
        print("1. Encrypt File")
        print("2. Decrypt File")
        print("3. Exit")
        print("-" * 60)

        choice = input(
            "\nEnter choice: "
        ).strip()

        if choice == "1":

            encrypt_mode()

        elif choice == "2":

            decrypt_mode()

        elif choice == "3":

            print(
                "\nExiting..."
            )
            break

        else:

            print(
                "\nInvalid choice."
            )


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    main()