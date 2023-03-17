#include <stdio.h>

int main()
{
    char me[20];

    printf("What is your name?");
    scanf("%s", &me);
    printf("Darn glad to meet you, %s!\n",me);
}