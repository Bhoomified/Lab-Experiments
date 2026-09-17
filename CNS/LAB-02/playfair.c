#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define SIZE 5

// Convert character to uppercase
// Treat J as I
char normalize(char ch)
{
    ch = toupper(ch);

    if (ch == 'J')
        ch = 'I';

    return ch;
}

// Create 5x5 Playfair matrix
void createMatrix(char key[], char matrix[SIZE][SIZE])
{
    int used[26] = {0};
    int row = 0;
    int col = 0;

    // I and J are considered the same
    used['J' - 'A'] = 1;

    // First insert key characters
    for (int i = 0; key[i] != '\0'; i++)
    {
        if (isalpha(key[i]))
        {
            char ch = normalize(key[i]);
            int index = ch - 'A';

            if (!used[index])
            {
                matrix[row][col] = ch;
                used[index] = 1;

                col++;

                if (col == SIZE)
                {
                    col = 0;
                    row++;
                }
            }
        }
    }

    // Insert remaining alphabets
    for (char ch = 'A'; ch <= 'Z'; ch++)
    {
        if (ch == 'J')
            continue;

        int index = ch - 'A';

        if (!used[index])
        {
            matrix[row][col] = ch;
            used[index] = 1;

            col++;

            if (col == SIZE)
            {
                col = 0;
                row++;
            }
        }
    }
}

// Display matrix
void displayMatrix(char matrix[SIZE][SIZE])
{
    printf("\nPlayfair Matrix:\n");

    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            printf("%c ", matrix[i][j]);
        }

        printf("\n");
    }
}

// Find row and column of a character
void findPosition(char matrix[SIZE][SIZE],
                  char ch,
                  int *row,
                  int *col)
{
    ch = normalize(ch);

    for (int i = 0; i < SIZE; i++)
    {
        for (int j = 0; j < SIZE; j++)
        {
            if (matrix[i][j] == ch)
            {
                *row = i;
                *col = j;
                return;
            }
        }
    }
}

// Prepare plaintext into digrams
void prepareText(char input[], char output[])
{
    char temp[500];
    int n = 0;

    // Remove spaces and convert to uppercase
    for (int i = 0; input[i] != '\0'; i++)
    {
        if (isalpha(input[i]))
        {
            temp[n++] = normalize(input[i]);
        }
    }

    temp[n] = '\0';

    int i = 0;
    int j = 0;

    while (i < n)
    {
        // If last character is alone
        if (i == n - 1)
        {
            output[j++] = temp[i];
            output[j++] = 'X';
            i++;
        }

        // Repeated letters in same pair
        else if (temp[i] == temp[i + 1])
        {
            output[j++] = temp[i];
            output[j++] = 'X';
            i++;
        }

        // Normal pair
        else
        {
            output[j++] = temp[i];
            output[j++] = temp[i + 1];
            i += 2;
        }
    }

    output[j] = '\0';
}

// Encrypt one digram
void encryptPair(char a, char b,
                 char matrix[SIZE][SIZE])
{
    int row1, col1;
    int row2, col2;

    findPosition(matrix, a, &row1, &col1);
    findPosition(matrix, b, &row2, &col2);

    // RULE 1: Same row
    if (row1 == row2)
    {
        col1 = (col1 + 1) % SIZE;
        col2 = (col2 + 1) % SIZE;

        printf("%c%c",
               matrix[row1][col1],
               matrix[row2][col2]);
    }

    // RULE 2: Same column
    else if (col1 == col2)
    {
        row1 = (row1 + 1) % SIZE;
        row2 = (row2 + 1) % SIZE;

        printf("%c%c",
               matrix[row1][col1],
               matrix[row2][col2]);
    }

    // RULE 3: Rectangle
    else
    {
        printf("%c%c",
               matrix[row1][col2],
               matrix[row2][col1]);
    }
}

// Decrypt one digram
void decryptPair(char a, char b,
                 char matrix[SIZE][SIZE])
{
    int row1, col1;
    int row2, col2;

    findPosition(matrix, a, &row1, &col1);
    findPosition(matrix, b, &row2, &col2);

    // Same row
    if (row1 == row2)
    {
        col1 = (col1 - 1 + SIZE) % SIZE;
        col2 = (col2 - 1 + SIZE) % SIZE;

        printf("%c%c",
               matrix[row1][col1],
               matrix[row2][col2]);
    }

    // Same column
    else if (col1 == col2)
    {
        row1 = (row1 - 1 + SIZE) % SIZE;
        row2 = (row2 - 1 + SIZE) % SIZE;

        printf("%c%c",
               matrix[row1][col1],
               matrix[row2][col2]);
    }

    // Rectangle
    else
    {
        // Rectangle rule is the same for encryption/decryption
        printf("%c%c",
               matrix[row1][col2],
               matrix[row2][col1]);
    }
}

int main()
{
    char key[100];
    char text[500];
    char prepared[500];

    char matrix[SIZE][SIZE];

    int choice;

    printf("===== PLAYFAIR CIPHER =====\n");

    // Input key
    printf("\nEnter key: ");
    fgets(key, sizeof(key), stdin);

    key[strcspn(key, "\n")] = '\0';

    // Create matrix
    createMatrix(key, matrix);

    // Display matrix
    displayMatrix(matrix);

    // Menu
    printf("\n1. Encryption");
    printf("\n2. Decryption");

    printf("\n\nEnter your choice: ");
    scanf("%d", &choice);

    getchar();

    // Input text
    printf("Enter text: ");
    fgets(text, sizeof(text), stdin);

    text[strcspn(text, "\n")] = '\0';

    // Encryption
    if (choice == 1)
    {
        prepareText(text, prepared);

        printf("\nDigrams: ");

        for (int i = 0; prepared[i] != '\0'; i += 2)
        {
            printf("%c%c ", prepared[i], prepared[i + 1]);
        }

        printf("\nCipher text: ");

        for (int i = 0; prepared[i] != '\0'; i += 2)
        {
            encryptPair(prepared[i],
                        prepared[i + 1],
                        matrix);
        }

        printf("\n");
    }

    // Decryption
    else if (choice == 2)
    {
        int n = 0;

        // Clean ciphertext
        for (int i = 0; text[i] != '\0'; i++)
        {
            if (isalpha(text[i]))
            {
                prepared[n++] = normalize(text[i]);
            }
        }

        prepared[n] = '\0';

        if (n % 2 != 0)
        {
            printf("\nInvalid ciphertext!");
            printf("\nCiphertext must contain even number of letters.\n");
            return 1;
        }

        printf("\nPlain text: ");

        for (int i = 0; prepared[i] != '\0'; i += 2)
        {
            decryptPair(prepared[i],
                        prepared[i + 1],
                        matrix);
        }

        printf("\n");
    }

    else
    {
        printf("\nInvalid choice!\n");
    }

    return 0;
}