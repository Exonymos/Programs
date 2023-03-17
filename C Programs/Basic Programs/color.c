#include <stdio.h>

int main()
{
    char name[20];
    char color[20];

    printf("What is you name?");
    scanf("%s",name);
    printf("What is you favorite color?");
    scanf("%s",color);
    printf("%s's favorite color is %s\n",name,color);
}