#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MOD 26

// Find GCD
int gcd(int a, int b)
{
    while (b != 0)
    {
        int temp = b;
        b = a % b;
        a = temp;
    }

    return a;
}

// Find modular inverse of a under modulo 26
int modInverse(int a)
{
    a = a % MOD;

    for (int x = 1; x < MOD; x++)
    {
        if ((a * x) % MOD == 1)
            return x;
    }

    return -1;
}

// Convert character to number
int charToNum(char ch)
{
    return toupper(ch) - 'A';
}

// Convert number to character
char numToChar(int num)
{
    return (num % MOD + MOD) % MOD + 'A';
}

// Encrypt plaintext
void encrypt(char text[], int key[2][2])
{
    int length = strlen(text);

    // Remove non-alphabetic characters
    char clean[500];
    int j = 0;

    for (int i = 0; i < length; i++)
    {
        if (isalpha(text[i]))
        {
            clean[j++] = toupper(text[i]);
        }
    }

    clean[j] = '\0';

    // Add X if length is odd
    if (j % 2 != 0)
    {
        clean[j++] = 'X';
        clean[j] = '\0';
    }

    printf("\nEncrypted text: ");

    for (int i = 0; i < j; i += 2)
    {
        int p1 = charToNum(clean[i]);
        int p2 = charToNum(clean[i + 1]);

        int c1 = (key[0][0] * p1 + key[0][1] * p2) % MOD;
        int c2 = (key[1][0] * p1 + key[1][1] * p2) % MOD;

        printf("%c%c", numToChar(c1), numToChar(c2));
    }

    printf("\n");
}

// Decrypt ciphertext
void decrypt(char text[], int key[2][2])
{
    int det;

    // Calculate determinant
    det = key[0][0] * key[1][1] -
          key[0][1] * key[1][0];

    det = (det % MOD + MOD) % MOD;

    // Find modular inverse of determinant
    int detInverse = modInverse(det);

    if (detInverse == -1)
    {
        printf("\nKey matrix cannot be inverted modulo 26.\n");
        return;
    }

    // Calculate inverse matrix
    int inverse[2][2];

    inverse[0][0] = key[1][1] * detInverse;
    inverse[0][1] = -key[0][1] * detInverse;
    inverse[1][0] = -key[1][0] * detInverse;
    inverse[1][1] = key[0][0] * detInverse;

    // Apply modulo 26
    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            inverse[i][j] =
                (inverse[i][j] % MOD + MOD) % MOD;
        }
    }

    int length = strlen(text);

    printf("\nDecrypted text: ");

    for (int i = 0; i < length; i += 2)
    {
        int c1 = charToNum(text[i]);
        int c2 = charToNum(text[i + 1]);

        int p1 = (inverse[0][0] * c1 +
                  inverse[0][1] * c2) % MOD;

        int p2 = (inverse[1][0] * c1 +
                  inverse[1][1] * c2) % MOD;

        printf("%c%c", numToChar(p1), numToChar(p2));
    }

    printf("\n");
}

int main()
{
    int key[2][2];
    char text[500];
    int choice;

    printf("===== HILL CIPHER =====\n");

    printf("\nEnter the 2x2 key matrix:\n");

    printf("Enter key[0][0]: ");
    scanf("%d", &key[0][0]);

    printf("Enter key[0][1]: ");
    scanf("%d", &key[0][1]);

    printf("Enter key[1][0]: ");
    scanf("%d", &key[1][0]);

    printf("Enter key[1][1]: ");
    scanf("%d", &key[1][1]);

    // Normalize key values
    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            key[i][j] =
                (key[i][j] % MOD + MOD) % MOD;
        }
    }

    // Check determinant
    int det = key[0][0] * key[1][1] -
              key[0][1] * key[1][0];

    det = (det % MOD + MOD) % MOD;

    if (gcd(det, MOD) != 1)
    {
        printf("\nInvalid key matrix!\n");
        printf("The determinant must be relatively prime to 26.\n");
        return 1;
    }

    printf("\n1. Encrypt");
    printf("\n2. Decrypt");

    printf("\n\nEnter your choice: ");
    scanf("%d", &choice);

    getchar();

    printf("Enter text: ");
    fgets(text, sizeof(text), stdin);

    // Remove newline
    text[strcspn(text, "\n")] = '\0';

    if (choice == 1)
    {
        encrypt(text, key);
    }
    else if (choice == 2)
    {
        // Remove non-alphabetic characters for decryption
        char clean[500];
        int j = 0;

        for (int i = 0; text[i] != '\0'; i++)
        {
            if (isalpha(text[i]))
            {
                clean[j++] = toupper(text[i]);
            }
        }

        clean[j] = '\0';

        if (j % 2 != 0)
        {
            printf("\nCiphertext must contain an even number of letters.\n");
            return 1;
        }

        decrypt(clean, key);
    }
    else
    {
        printf("\nInvalid choice!\n");
    }

    return 0;
}