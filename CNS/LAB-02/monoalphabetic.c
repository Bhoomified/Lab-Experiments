#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define SIZE 26

// Function to check whether the key is valid
int isValidKey(char key[])
{
    int seen[26] = {0};

    if (strlen(key) != 26)
        return 0;

    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
            return 0;

        key[i] = toupper(key[i]);

        int index = key[i] - 'A';

        if (seen[index])
            return 0;

        seen[index] = 1;
    }

    return 1;
}

// Encryption function
void encrypt(char text[], char key[])
{
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isalpha(text[i]))
        {
            char ch = toupper(text[i]);

            // Find corresponding substitution
            text[i] = key[ch - 'A'];
        }
    }
}

// Decryption function
void decrypt(char text[], char key[])
{
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isalpha(text[i]))
        {
            char ch = toupper(text[i]);

            // Search the key to find original character
            for (int j = 0; j < SIZE; j++)
            {
                if (key[j] == ch)
                {
                    text[i] = 'A' + j;
                    break;
                }
            }
        }
    }
}

int main()
{
    char key[SIZE + 1];
    char text[500];
    int choice;

    printf("Enter 26-letter substitution key: ");
    scanf("%26s", key);

    // Validate key
    if (!isValidKey(key))
    {
        printf("Invalid key!\n");
        printf("Key must contain all 26 different alphabets.\n");
        return 1;
    }

    getchar(); // Remove newline left by scanf

    printf("\n1. Encrypt\n");
    printf("2. Decrypt\n");
    printf("Enter your choice: ");
    scanf("%d", &choice);

    getchar(); // Remove newline

    printf("Enter text: ");
    fgets(text, sizeof(text), stdin);

    if (choice == 1)
    {
        encrypt(text, key);
        printf("\nEncrypted text: %s", text);
    }
    else if (choice == 2)
    {
        decrypt(text, key);
        printf("\nDecrypted text: %s", text);
    }
    else
    {
        printf("Invalid choice!\n");
    }

    return 0;
}