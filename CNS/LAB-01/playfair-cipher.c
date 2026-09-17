#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LEN 2048

// Helper to flush leftover characters from standard input
void clear_input_buffer(void) {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

// -----------------------------------------------------------------------------
// 1. Matrix Generation
// -----------------------------------------------------------------------------

// Builds a 5x5 Playfair matrix from the keyword (merging 'J' into 'I')
void build_matrix(const char *key, char matrix[5][5]) {
    int used[26] = {0};
    used['J' - 'A'] = 1; // 'J' is merged into 'I'

    int row = 0, col = 0;

    // First, insert unique characters from the key
    for (int i = 0; key[i] != '\0'; i++) {
        if (!isalpha((unsigned char)key[i])) continue;

        char ch = (char)toupper((unsigned char)key[i]);
        if (ch == 'J') ch = 'I';

        if (!used[ch - 'A']) {
            used[ch - 'A'] = 1;
            matrix[row][col++] = ch;
            if (col == 5) {
                col = 0;
                row++;
            }
        }
    }

    // Next, fill the remaining slots with unused letters of the alphabet
    for (char ch = 'A'; ch <= 'Z'; ch++) {
        if (!used[ch - 'A']) {
            used[ch - 'A'] = 1;
            matrix[row][col++] = ch;
            if (col == 5) {
                col = 0;
                row++;
            }
        }
    }
}

// Displays the 5x5 key matrix in a neat format
void print_matrix(char matrix[5][5]) {
    printf("\n--- 5x5 Playfair Key Matrix ---\n");
    for (int r = 0; r < 5; r++) {
        printf("       ");
        for (int c = 0; c < 5; c++) {
            if (matrix[r][c] == 'I') {
                printf("I/J ");
            } else {
                printf(" %c  ", matrix[r][c]);
            }
        }
        printf("\n");
    }
    printf("-------------------------------\n");
}

// Finds the row and column coordinates of a character in the matrix
void find_position(char matrix[5][5], char ch, int *row, int *col) {
    if (ch == 'J') ch = 'I';
    for (int r = 0; r < 5; r++) {
        for (int c = 0; c < 5; c++) {
            if (matrix[r][c] == ch) {
                *row = r;
                *col = c;
                return;
            }
        }
    }
}

// -----------------------------------------------------------------------------
// 2. Text Preparation & Digraph Splitting
// -----------------------------------------------------------------------------

// Prompts the user for an alternative filler if standard 'X' cannot be used
char get_alternative_filler(char forbidden) {
    char alt = '\0';
    while (1) {
        printf("[!] Conflict: Letter '%c' collides with default filler 'X'.\n", forbidden);
        printf("    Enter an alternative filler letter (e.g., Q or Z): ");
        
        char line[64];
        if (fgets(line, sizeof(line), stdin) != NULL) {
            line[strcspn(line, "\r\n")] = '\0';
            if (strlen(line) > 0 && isalpha((unsigned char)line[0])) {
                alt = (char)toupper((unsigned char)line[0]);
                if (alt == 'J') alt = 'I';
                if (alt != forbidden && alt != 'X') {
                    return alt;
                }
            }
        }
        printf("    Invalid choice. Must be a single letter different from '%c' and 'X'.\n", forbidden);
    }
}

// Cleans input and pairs into valid digraphs
void prepare_plaintext(const char *input, char *prepared) {
    char raw[MAX_LEN];
    int raw_len = 0;

    // 1. Filter only alphabetic letters, uppercase them, and map J -> I
    for (int i = 0; input[i] != '\0'; i++) {
        if (isalpha((unsigned char)input[i])) {
            char ch = (char)toupper((unsigned char)input[i]);
            raw[raw_len++] = (ch == 'J') ? 'I' : ch;
        }
    }
    raw[raw_len] = '\0';

    // 2. Form digraphs, handling double letters and odd lengths
    int p_idx = 0;
    char default_filler = 'X';
    char active_alt_filler = '\0';

    for (int i = 0; i < raw_len; ) {
        char first = raw[i];
        char second;

        if (i + 1 < raw_len) {
            second = raw[i + 1];

            if (first == second) {
                // Double letter collision
                char filler = default_filler;
                if (first == default_filler) {
                    if (active_alt_filler == '\0') {
                        active_alt_filler = get_alternative_filler(first);
                    }
                    filler = active_alt_filler;
                }
                prepared[p_idx++] = first;
                prepared[p_idx++] = filler;
                i++; // Only consume the first letter
            } else {
                prepared[p_idx++] = first;
                prepared[p_idx++] = second;
                i += 2;
            }
        } else {
            // Odd ending letter
            char filler = default_filler;
            if (first == default_filler) {
                if (active_alt_filler == '\0') {
                    active_alt_filler = get_alternative_filler(first);
                }
                filler = active_alt_filler;
            }
            prepared[p_idx++] = first;
            prepared[p_idx++] = filler;
            i++;
        }
    }
    prepared[p_idx] = '\0';
}

// -----------------------------------------------------------------------------
// 3. Playfair Cipher Core Logic
// -----------------------------------------------------------------------------

// mode = 1 for Encrypt, mode = -1 for Decrypt
void playfair_transform(char matrix[5][5], const char *input, char *output, int mode) {
    int len = strlen(input);
    int step = (mode == 1) ? 1 : 4; // Adding 4 is equivalent to subtracting 1 modulo 5

    for (int i = 0; i < len; i += 2) {
        int r1, c1, r2, c2;
        find_position(matrix, input[i], &r1, &c1);
        find_position(matrix, input[i + 1], &r2, &c2);

        if (r1 == r2) {
            // Same Row -> Shift columns right (encrypt) or left (decrypt)
            output[i]     = matrix[r1][(c1 + step) % 5];
            output[i + 1] = matrix[r2][(c2 + step) % 5];
        } else if (c1 == c2) {
            // Same Column -> Shift rows down (encrypt) or up (decrypt)
            output[i]     = matrix[(r1 + step) % 5][c1];
            output[i + 1] = matrix[(r2 + step) % 5][c2];
        } else {
            // Rectangle / Box -> Swap columns
            output[i]     = matrix[r1][c2];
            output[i + 1] = matrix[r2][c1];
        }
    }
    output[len] = '\0';
}

// Formats text into space-separated digraph pairs (e.g., "HE LL OW OR LD")
void format_digraphs(const char *in, char *out) {
    int j = 0;
    for (int i = 0; in[i] != '\0'; i += 2) {
        out[j++] = in[i];
        out[j++] = in[i + 1];
        out[j++] = ' ';
    }
    if (j > 0) j--; // Remove trailing space
    out[j] = '\0';
}

// -----------------------------------------------------------------------------
// 4. Interactive Menu
// -----------------------------------------------------------------------------

int main(void) {
    char key[256];
    char text[MAX_LEN];
    char processed[MAX_LEN * 2];
    char output[MAX_LEN * 2];
    char formatted[MAX_LEN * 3];
    char matrix[5][5];
    int choice = 0;

    while (1) {
        printf("\n==============================================\n");
        printf("            Playfair Cipher Engine            \n");
        printf("==============================================\n");
        printf("1. Encrypt Message\n");
        printf("2. Decrypt Ciphertext\n");
        printf("3. Exit\n");
        printf("Select an option (1-3): ");

        if (scanf("%d", &choice) != 1) {
            printf("\n[!] Invalid selection. Enter 1, 2, or 3.\n");
            clear_input_buffer();
            continue;
        }

        if (choice == 3) {
            printf("\nExiting Playfair Cipher. Goodbye!\n");
            break;
        }

        if (choice != 1 && choice != 2) {
            printf("\n[!] Invalid choice. Please choose 1, 2, or 3.\n");
            clear_input_buffer();
            continue;
        }

        clear_input_buffer();

        // 1. Get Keyword
        printf("Enter keyword/keyphrase: ");
        if (fgets(key, sizeof(key), stdin) == NULL) continue;
        key[strcspn(key, "\r\n")] = '\0';

        // Build and display key matrix
        build_matrix(key, matrix);
        print_matrix(matrix);

        // 2. Encryption Workflow
        if (choice == 1) {
            printf("Enter plaintext: ");
            if (fgets(text, sizeof(text), stdin) == NULL) continue;
            text[strcspn(text, "\r\n")] = '\0';

            prepare_plaintext(text, processed);
            format_digraphs(processed, formatted);
            printf("\nPrepared Digraphs: %s\n", formatted);

            playfair_transform(matrix, processed, output, 1);
            format_digraphs(output, formatted);

            printf("----------------------------------------------\n");
            printf("Ciphertext       : %s\n", formatted);
            printf("Raw Ciphertext   : %s\n", output);
            printf("----------------------------------------------\n");
        } 
        // 3. Decryption Workflow
        else {
            printf("Enter ciphertext: ");
            if (fgets(text, sizeof(text), stdin) == NULL) continue;
            text[strcspn(text, "\r\n")] = '\0';

            // Filter ciphertext to alphabetic letters only
            int clean_len = 0;
            for (int i = 0; text[i] != '\0'; i++) {
                if (isalpha((unsigned char)text[i])) {
                    char ch = (char)toupper((unsigned char)text[i]);
                    processed[clean_len++] = (ch == 'J') ? 'I' : ch;
                }
            }
            processed[clean_len] = '\0';

            // Edge-case check: Playfair ciphertexts must be even in length
            if (clean_len % 2 != 0) {
                printf("\n[!] Error: Ciphertext has an odd number of letters (%d).\n", clean_len);
                printf("    Valid Playfair ciphertext must always consist of even pairs.\n");
                continue;
            }

            playfair_transform(matrix, processed, output, -1);
            format_digraphs(output, formatted);

            printf("----------------------------------------------\n");
            printf("Decrypted Digraphs : %s\n", formatted);
            printf("Raw Decrypted Text : %s\n", output);
            printf("----------------------------------------------\n");
            printf("(Note: Look for filler letters like 'X' or your chosen alternative)\n");
        }
    }

    return 0;
}