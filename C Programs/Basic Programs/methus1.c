#include <stdio.h>

int main()
{
    int diff;
    int methus;
    int you;
    char years[8];

    printf("How old are you?");
    gets(years);
    you=atoi(years);
    
    methus=969;

    diff=methus-you;

    printf("You are %i years younger than Methuselah.\n",diff);
}