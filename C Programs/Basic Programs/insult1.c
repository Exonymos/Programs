#include <stdio.h>

int main()
{
    char jerk[20];

    printf("Name some jerk you know: ");
    gets(jerk);
    printf("Yeah, I think %s is a jerk, too.\n",jerk);
}