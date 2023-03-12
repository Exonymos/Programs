#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TITLE_LENGTH 50
#define FILE_NAME "EpisodeList.txt"

// Function declarations
void display_menu();
void add_show();
void update_watched();
void rename_show();
void show_contents();

int main() {
    int choice;
    do {
        display_menu();
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                add_show();
                break;
            case 2:
                update_watched();
                break;
            case 3:
                rename_show();
                break;
            case 4:
                show_contents();
                break;
            case 5:
                printf("Goodbye!\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 5);

    return 0;
}

void display_menu() {
    printf("\nMenu:\n");
    printf("1. Add a new Movie/TV Show\n");
    printf("2. Update watched episodes\n");
    printf("3. Rename a Movie/TV Show\n");
    printf("4. Show the contents of the file\n");
    printf("5. Quit\n");
    printf("Enter your choice: ");
}

void add_show() {
    char title[MAX_TITLE_LENGTH];
    int total_episodes, watched_episodes;
    printf("Enter the title of the Movie/TV Show: ");
    scanf(" %[^\n]", title);
    printf("Enter the total number of episodes: ");
    scanf("%d", &total_episodes);
    printf("Enter the number of episodes watched: ");
    scanf("%d", &watched_episodes);

    FILE *fp = fopen(FILE_NAME, "a");
    if (fp == NULL) {
        printf("Error opening file.\n");
        return;
    }
    fprintf(fp, "\"%s\"\nTotal number of episodes: %d\nWatched episodes: %d\n", title, total_episodes, watched_episodes);
    fclose(fp);

    printf("Added \"%s\" to the list.\n", title);
}

void update_watched() {
    char title[MAX_TITLE_LENGTH];
    int watched_episodes;
    printf("Choose a Movie/TV Show to update:\n");
    FILE *fp = fopen(FILE_NAME, "r");
    if (fp == NULL) {
        printf("Error opening file.\n");
        return;
    }
    char line[100];
    int count = 1;
    while (fgets(line, 100, fp) != NULL) {
        if (count % 4 == 1) {
            printf("%d. %s\n", count / 4 + 1, line + 1);
        }
        count++;
    }
    fclose(fp);
    int choice;
    printf("Enter your choice: ");
    scanf("%d", &choice);
    printf("Enter the number of episodes watched: ");
    scanf("%d", &watched_episodes);

    fp = fopen(FILE_NAME, "r");
    FILE *temp_fp = fopen("temp.txt", "w");
    if (fp == NULL || temp_fp == NULL) {
        printf("Error opening file.\n");
        return;
    }
    count = 1;
    while (fgets(line, 100, fp) != NULL) {
        if (count % 4 == 3 && (count / 4 + 1) == choice) {
            fprintf(temp_fp, "Watched episodes: %d\n", watched_episodes);
        } else {
            fprintf(temp_fp, "%s", line);
        }
        count++;
    }
    fclose(fp);
    fclose(temp_fp);

    // Replace the original file with the updated version
    remove(FILE_NAME);
    rename("temp.txt", FILE_NAME);

    printf("Updated \"%s\" with %d watched episodes.\n", title, watched_episodes);
}

void rename_show() {
    char title[MAX_TITLE_LENGTH], new_title[MAX_TITLE_LENGTH];
    printf("Choose a Movie/TV Show to rename:\n");
    FILE *fp = fopen(FILE_NAME, "r");
    if (fp == NULL) {
        printf("Error opening file.\n");
        return;
    }
    char line[100];
    int count = 1;
    while (fgets(line, 100, fp) != NULL) {
        if (count % 4 == 1) {
            printf("%d. %s\n", count / 4 + 1, line + 1);
        }
        count++;
    }
    fclose(fp);
    int choice;
    printf("Enter your choice: ");
    scanf("%d", &choice);
    printf("Enter the new title: ");
    scanf(" %[^\n]", new_title);

    fp = fopen(FILE_NAME, "r");
    FILE *temp_fp = fopen("temp.txt", "w");
    if (fp == NULL || temp_fp == NULL) {
        printf("Error opening file.\n");
        return;
    }
    count = 1;
    while (fgets(line, 100, fp) != NULL) {
        if (count % 4 == 1 && (count / 4 + 1) == choice) {
            fprintf(temp_fp, "\"%s\"\n", new_title);
        } else {
            fprintf(temp_fp, "%s", line);
        }
        count++;
    }
    fclose(fp);
    fclose(temp_fp);

    // Replace the original file with the updated version
    remove(FILE_NAME);
    rename("temp.txt", FILE_NAME);

    printf("Renamed \"%s\" to \"%s\".\n", title, new_title);
}

void show_contents() {
    FILE *fp = fopen(FILE_NAME, "r");
    if (fp == NULL) {
        printf("Error opening file.\n");
        return;
    }
    char line[100];
    while (fgets(line, 100, fp) != NULL) {
        printf("%s", line);
    }
    fclose(fp);
}