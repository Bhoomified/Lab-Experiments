#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LEN 1024

// Helper function to safely clear leftover characters in stdin buffer
void clear_input_buffer(void) {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

// Transforms text in-place by shifting alphabetic characters by 'shift' positions
void shift_cipher(char *text, int shift) {
    // Normalize shift to stay within [0, 25]
    shift = (shift % 26 + 26) % 26;

    for (int i = 0; text[i] != '\0'; i++) {
        if (isupper((unsigned char)text[i])) {
            text[i] = (char)(((text[i] - 'A' + shift) % 26) + 'A');
        } else if (islower((unsigned char)text[i])) {
            text[i] = (char)(((text[i] - 'a' + shift) % 26) + 'a');
        }
        // Non-alphabetic characters (digits, spaces, punctuation) remain unchanged
    }
}

int main(void) {
    char text[MAX_LEN];
    int choice = 0;
    int shift = 0;

    while (1) {
        printf("\n=====================================\n");
        printf("       Shift-by-N Substitution       \n");
        printf("=====================================\n");
        printf("1. Encrypt Text\n");
        printf("2. Decrypt Text\n");
        printf("3. Exit\n");
        printf("Choose an option (1-3): ");

        if (scanf("%d", &choice) != 1) {
            printf("\n[!] Invalid input. Please enter a number (1-3).\n");
            clear_input_buffer();
            continue;
        }

        // Exit condition
        if (choice == 3) {
            printf("\nExiting cipher program. Goodbye!\n");
            break;
        }

        // Validate menu choice
        if (choice != 1 && choice != 2) {
            printf("\n[!] Invalid selection. Please choose 1, 2, or 3.\n");
            clear_input_buffer();
            continue;
        }

        // Read shift value (n)
        printf("Enter shift key (n): ");
        if (scanf("%d", &shift) != 1) {
            printf("\n[!] Invalid integer for shift.\n");
            clear_input_buffer();
            continue;
        }

        // Clear trailing newline left by scanf before calling fgets
        clear_input_buffer();

        // Read the target text
        printf("Enter text: ");
        if (fgets(text, sizeof(text), stdin) == NULL) {
            printf("\n[!] Error reading text input.\n");
            continue;
        }

        // Strip trailing newline character stored by fgets
        text[strcspn(text, "\r\n")] = '\0';

        // Apply shift: forward for encryption, backward for decryption
        int effective_shift = (choice == 1) ? shift : -shift;
        shift_cipher(text, effective_shift);

        printf("-------------------------------------\n");
        printf("Output: %s\n", text);
        printf("-------------------------------------\n");
    }

    return 0;
}