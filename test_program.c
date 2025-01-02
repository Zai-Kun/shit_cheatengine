#include <stdio.h>

int main()
{
    int x = 10;
    int y = 10;

    printf("x: %i, y: %i\n", x, y);

    printf("let's change x to something else: ");
    scanf("%i", &x);
    getchar();

    while (1)
    {
        printf("Value: %i\nPointer: %p\n", x, &x);
        getchar();
    }
}
