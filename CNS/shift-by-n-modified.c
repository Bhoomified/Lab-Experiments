#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LEN 2048
#define DICT_PATH "/usr/share/dict/words"
#define HASH_TABLE_SIZE 500009

// --- 1. macOS Dictionary Hash Table ---

typedef struct Node {
    char *word;
    struct Node *next;
} Node;

static Node *hash_table[HASH_TABLE_SIZE] = {NULL};

// Fast djb2 hash function
static unsigned long hash_string(const char *str) {
    unsigned long hash = 5381;
    int c;
    while ((c = (unsigned char)*str++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash % HASH_TABLE_SIZE;
}

// Load words into memory
int load_system_dictionary(const char *filepath) {
    FILE *fp = fopen(filepath, "r");
    if (!fp) {
        perror("Error opening system dictionary");
        return 0;
    }

    char line[128];
    size_t loaded_count = 0;

    while (fgets(line, sizeof(line), fp)) {
        line[strcspn(line, "\r\n")] = '\0';
        if (line[0] == '\0') continue;

        for (int i = 0; line[i]; i++) {
            line[i] = (char)tolower((unsigned char)line[i]);
        }

        unsigned long idx = hash_string(line);
        Node *newNode = (Node *)malloc(sizeof(Node));
        if (!newNode) {
            fprintf(stderr, "Memory allocation failure.\n");
            fclose(fp);
            return 0;
        }

        newNode->word = strdup(line);
        newNode->next = hash_table[idx];
        hash_table[idx] = newNode;
        loaded_count++;
    }

    fclose(fp);
    printf("[i] Loaded %zu words from %s\n", loaded_count, filepath);
    return 1;
}

// Legitimate standard 2-letter English words to prevent dictionary false positives
static int is_common_two_letter_word(const char *w) {
    static const char *valid_two[] = {
        "am", "an", "as", "at", "be", "by", "do", "go", "he", "if",
        "in", "is", "it", "me", "my", "no", "of", "on", "or", "so",
        "to", "up", "us", "we"
    };
    int count = sizeof(valid_two) / sizeof(valid_two[0]);
    for (int i = 0; i < count; i++) {
        if (strcmp(w, valid_two[i]) == 0) return 1;
    }
    return 0;
}

// O(1) dictionary word lookup with validation guards
int is_valid_word(const char *word) {
    size_t len = strlen(word);
    if (len == 0) return 0;

    // Single-letter words only 'a' or 'i'
    if (len == 1) {
        char c = (char)tolower((unsigned char)word[0]);
        return (c == 'a' || c == 'i');
    }

    // Convert candidate to lower case
    char lower[128];
    if (len >= sizeof(lower)) len = sizeof(lower) - 1;
    for (size_t i = 0; i < len; i++) {
        lower[i] = (char)tolower((unsigned char)word[i]);
    }
    lower[len] = '\0';

    // Guard against uncommon 2-letter words listed in dictionary
    if (len == 2 && !is_common_two_letter_word(lower)) {
        return 0;
    }

    unsigned long idx = hash_string(lower);
    Node *curr = hash_table[idx];
    while (curr) {
        if (strcmp(curr->word, lower) == 0) {
            return 1;
        }
        curr = curr->next;
    }
    return 0;
}

// --- 2. Cipher Logic & Word Extraction ---

void clear_input_buffer(void) {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

// Standard Shift-by-N
void shift_cipher(const char *input, char *output, int shift) {
    shift = (shift % 26 + 26) % 26;

    for (int i = 0; input[i] != '\0'; i++) {
        if (isupper((unsigned char)input[i])) {
            output[i] = (char)(((input[i] - 'A' + shift) % 26) + 'A');
        } else if (islower((unsigned char)input[i])) {
            output[i] = (char)(((input[i] - 'a' + shift) % 26) + 'a');
        } else {
            output[i] = input[i];
        }
    }
    output[strlen(input)] = '\0';
}

// Counts total alphabetic words in a string
int count_total_words(const char *text) {
    char copy[MAX_LEN];
    strncpy(copy, text, sizeof(copy) - 1);
    copy[sizeof(copy) - 1] = '\0';

    int words = 0;
    const char *delimiters = " \t\r\n.,;:!?\"'()[]{}<>-/";
    char *token = strtok(copy, delimiters);

    while (token != NULL) {
        // Only count tokens containing letters
        int has_alpha = 0;
        for (int i = 0; token[i]; i++) {
            if (isalpha((unsigned char)token[i])) {
                has_alpha = 1;
                break;
            }
        }
        if (has_alpha) words++;
        token = strtok(NULL, delimiters);
    }
    return words;
}

// Counts how many tokens match the dictionary
int count_recognized_words(const char *candidate) {
    char copy[MAX_LEN];
    strncpy(copy, candidate, sizeof(copy) - 1);
    copy[sizeof(copy) - 1] = '\0';

    int matched_words = 0;
    const char *delimiters = " \t\r\n.,;:!?\"'()[]{}<>-/";
    char *token = strtok(copy, delimiters);

    while (token != NULL) {
        if (is_valid_word(token)) {
            matched_words++;
        }
        token = strtok(NULL, delimiters);
    }
    return matched_words;
}

// Auto-decrypt with EARLY EXIT when full match is found
int auto_decrypt(const char *ciphertext, char *best_plaintext) {
    int total_words = count_total_words(ciphertext);
    int best_shift = -1;
    int max_matches = 0;
    char temp[MAX_LEN];

    printf("\n[~] Target total word count: %d\n", total_words);
    printf("[~] Testing shifts n = 1 to 25...\n");

    for (int n = 1; n < 26; n++) {
        shift_cipher(ciphertext, temp, -n);
        int matches = count_recognized_words(temp);

        printf("  Testing key n = %2d -> [%2d/%2d valid words] | Preview: \"%.30s%s\"\n",
               n, matches, total_words, temp, strlen(temp) > 30 ? "..." : "");

        if (matches > max_matches) {
            max_matches = matches;
            best_shift = n;
            strcpy(best_plaintext, temp);
        }

        // EARLY EXIT: As soon as every word in the sentence is validated, stop immediately!
        if (total_words > 0 && matches == total_words) {
            printf("\n[!] 100%% of words verified in macOS dictionary. Halting search early at n = %d.\n", n);
            return n;
        }
    }

    return (max_matches > 0) ? best_shift : -1;
}

// --- 3. Main Loop ---

int main(void) {
    if (!load_system_dictionary(DICT_PATH)) {
        fprintf(stderr, "Aborting: Dictionary could not be loaded.\n");
        return 1;
    }

    char text[MAX_LEN];
    char result[MAX_LEN];
    int choice = 0;
    int shift = 0;

    while (1) {
        printf("\n==============================================\n");
        printf("  macOS System-Dictionary Shift Cipher Engine  \n");
        printf("==============================================\n");
        printf("1. Encrypt Text (with key n)\n");
        printf("2. Auto-Decrypt Text (no key needed)\n");
        printf("3. Exit\n");
        printf("Select option (1-3): ");

        if (scanf("%d", &choice) != 1) {
            printf("\n[!] Invalid input.\n");
            clear_input_buffer();
            continue;
        }

        if (choice == 3) {
            printf("\nExiting. Goodbye!\n");
            break;
        }

        if (choice != 1 && choice != 2) {
            printf("\n[!] Please select 1, 2, or 3.\n");
            clear_input_buffer();
            continue;
        }

        if (choice == 1) {
            printf("Enter shift key (n): ");
            if (scanf("%d", &shift) != 1) {
                printf("\n[!] Invalid integer.\n");
                clear_input_buffer();
                continue;
            }
            clear_input_buffer();

            printf("Enter plaintext: ");
            if (fgets(text, sizeof(text), stdin) == NULL) continue;
            text[strcspn(text, "\r\n")] = '\0';

            shift_cipher(text, result, shift);
            printf("\n----------------------------------------------\n");
            printf("Ciphertext: %s\n", result);
            printf("----------------------------------------------\n");

        } else {
            clear_input_buffer();
            printf("Enter ciphertext to crack: ");
            if (fgets(text, sizeof(text), stdin) == NULL) continue;
            text[strcspn(text, "\r\n")] = '\0';

            int detected_key = auto_decrypt(text, result);

            printf("\n----------------------------------------------\n");
            if (detected_key != -1) {
                printf("[✓] SUCCESS!\n");
                printf("Identified Shift (n): %d\n", detected_key);
                printf("Recovered Plaintext : %s\n", result);
            } else {
                printf("[X] Failed to validate any shift against the dictionary.\n");
            }
            printf("----------------------------------------------\n");
        }
    }

    return 0;
}