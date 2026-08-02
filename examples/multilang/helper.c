/* helper.c — Example C file for run_c() demo */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    printf("Hello from C!\n");
    printf("C version: %s\n", __STDC_VERSION__ ? "C11+" : "C99");

    /* Calculate sum 1..100 */
    int sum = 0;
    for (int i = 1; i <= 100; i++) {
        sum += i;
    }
    printf("Sum 1..100 = %d\n", sum);

    /* Factorial */
    long long fact = 1;
    for (int i = 1; i <= 20; i++) fact *= i;
    printf("20! = %lld\n", fact);

    /* Current time */
    time_t t = time(NULL);
    printf("Time: %s", ctime(&t));

    return 0;
}
