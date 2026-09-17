import string


ALPHABET = string.ascii_uppercase


def is_valid_key(key):
    key = key.upper()

    return (
        len(key) == 26
        and all(ch.isalpha() for ch in key)
        and len(set(key)) == 26
    )


def encrypt(text, key):
    result = ""

    for ch in text:
        if ch.isalpha():
            ch = ch.upper()
            result += key[ord(ch) - ord('A')]
        else:
            result += ch

    return result


def decrypt(text, key):
    result = ""

    for ch in text:
        if ch.isalpha():
            ch = ch.upper()

            # Find the position of ciphertext character
            index = key.index(ch)

            result += chr(ord('A') + index)
        else:
            result += ch

    return result


print("===== MONOALPHABETIC CIPHER =====")

key = input("\nEnter 26-letter substitution key: ").upper()

if not is_valid_key(key):
    print("\nInvalid key!")
    print("Key must contain all 26 different alphabets.")
    exit()

print("\n1. Encrypt")
print("2. Decrypt")

choice = int(input("\nEnter your choice: "))

text = input("Enter text: ")

if choice == 1:
    encrypted = encrypt(text, key)
    print("\nEncrypted text:", encrypted)

elif choice == 2:
    decrypted = decrypt(text, key)
    print("\nDecrypted text:", decrypted)

else:
    print("\nInvalid choice!")