#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAX 500

// Create alphabetical order of key
void getOrder(char key[], int order[], int n)
{
    for (int i = 0; i < n; i++)
    {
        order[i] = 0;

        for (int j = 0; j < n; j++)
        {
            if (key[j] < key[i])
            {
                order[i]++;
            }
            else if (key[j] == key[i] && j < i)
            {
                order[i]++;
            }
        }
    }
}

// Encryption
void encrypt(char text[], char key[])
{
    int keyLen = strlen(key);
    int textLen = strlen(text);

    char clean[MAX];
    int n = 0;

    // Remove spaces and keep alphabets
    for (int i = 0; i < textLen; i++)
    {
        if (isalpha(text[i]))
        {
            clean[n++] = toupper(text[i]);
        }
    }

    clean[n] = '\0';

    // Calculate number of rows
    int rows = (n + keyLen - 1) / keyLen;

    // Create matrix
    char matrix[rows][keyLen];

    int index = 0;

    // Fill matrix row-wise
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < keyLen; j++)
        {
            if (index < n)
            {
                matrix[i][j] = clean[index++];
            }
            else
            {
                matrix[i][j] = 'X';
            }
        }
    }

    // Find column order
    int order[keyLen];

    getOrder(key, order, keyLen);

    printf("\nMatrix:\n");

    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < keyLen; j++)
        {
            printf("%c ", matrix[i][j]);
        }
        printf("\n");
    }

    printf("\nEncrypted text: ");

    // Read columns according to key order
    for (int number = 0; number < keyLen; number++)
    {
        for (int col = 0; col < keyLen; col++)
        {
            if (order[col] == number)
            {
                for (int row = 0; row < rows; row++)
                {
                    printf("%c", matrix[row][col]);
                }

                break;
            }
        }
    }

    printf("\n");
}

// Decryption
void decrypt(char cipher[], char key[])
{
    int keyLen = strlen(key);
    int cipherLen = strlen(cipher);

    char clean[MAX];
    int n = 0;

    // Remove spaces
    for (int i = 0; i < cipherLen; i++)
    {
        if (isalpha(cipher[i]))
        {
            clean[n++] = toupper(cipher[i]);
        }
    }

    clean[n] = '\0';

    if (n % keyLen != 0)
    {
        printf("\nInvalid ciphertext length.\n");
        printf("Ciphertext length must be divisible by key length.\n");
        return;
    }

    int rows = n / keyLen;

    char matrix[rows][keyLen];

    int order[keyLen];

    getOrder(key, order, keyLen);

    int index = 0;

    // Fill columns according to key order
    for (int number = 0; number < keyLen; number++)
    {
        for (int col = 0; col < keyLen; col++)
        {
            if (order[col] == number)
            {
                for (int row = 0; row < rows; row++)
                {
                    matrix[row][col] = clean[index++];
                }

                break;
            }
        }
    }

    printf("\nDecrypted text: ");

    // Read row-wise
    for (int row = 0; row < rows; row++)
    {
        for (int col = 0; col < keyLen; col++)
        {
            printf("%c", matrix[row][col]);
        }
    }

    printf("\n");
}

int main()
{
    char key[MAX];
    char text[MAX];
    int choice;

    printf("===== COLUMNAR TRANSPOSITION CIPHER =====\n");

    printf("\nEnter key: ");
    scanf("%s", key);

    // Convert key to uppercase
    for (int i = 0; key[i] != '\0'; i++)
    {
        key[i] = toupper(key[i]);
    }

    printf("\n1. Encryption");
    printf("\n2. Decryption");

    printf("\n\nEnter your choice: ");
    scanf("%d", &choice);

    getchar();

    printf("Enter text: ");
    fgets(text, sizeof(text), stdin);

    text[strcspn(text, "\n")] = '\0';

    if (choice == 1)
    {
        encrypt(text, key);
    }
    else if (choice == 2)
    {
        decrypt(text, key);
    }
    else
    {
        printf("\nInvalid choice!\n");
    }

    return 0;
}