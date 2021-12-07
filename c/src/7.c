/* NOTE: this program sometimes segfaults
 but i can't replicate in gdb
 so *shrug* */

#include "aoc.h"
#include <string.h>
#include <stdlib.h>

static const AocLevel LEVEL = {2021, 7};

static const char TEST_DATA[] = "16,1,2,0,4,2,7,1,2,14";

static size_t parse(const char* inp, uint16_t data[static 1024]) {
    size_t inp_len = strlen(inp);
    char* inp_copy = malloc(inp_len + 1);
    memcpy(inp_copy, inp, inp_len + 1);

    int i = 0;
    char* token = strtok(inp_copy, ",");
    do {
        data[i++] = (uint16_t)atoi(token);
    } while((token = strtok(NULL, ",")));
    return (size_t)i;
}

static uint16_t mean(uint16_t data[static 1024], size_t n) {
    double sum = 0;
    for (int i = 0; i < n; i++) {
        sum += (double)data[i];
    }

    double avg = sum/n;
    return (uint16_t)(avg+0.5);
}

static int64_t sol1(const char* inp) {
    uint16_t data[1024];
    size_t n = parse(inp, data);


    int min_total_fuel = INT_MAX;
    for (uint16_t center = 0; center < UINT16_MAX; center++) {
        int total_fuel = 0;
        for (int i = 0; i < n; i++) {
            total_fuel += data[i] > center ? (int)(data[i] - center) : (int)(center - data[i]);
        }

        if (min_total_fuel > total_fuel)
            min_total_fuel = total_fuel;
    }

    return min_total_fuel;
}


// returns 1 + 2 + 3 + 4 + ... + n
//
// proof
// f(x) = x
// x = integral(f, x-1/2 to x+1/2)
// sum to n = sum(integral(f, x-1/2 to x+1/2))
//          = integral(f, 1/2, n+1/2)
//
// F(x) = 1/2 x^2 + c
// sum to n = 1/2(n+1/2)^2 - 1/2(1/2)^2 = 1/2(n+1/2)^2 - 1/8
static int64_t tri(int n) {
    double nd = (double)n;
    return (int64_t)(0.5 * (nd+0.5)*(nd+0.5) - 0.125);
}


static  int64_t sol2(const char* inp) {
    uint16_t data[1024];
    size_t n = parse(inp, data);


    int64_t min_total_fuel = INT_MAX;
    for (uint16_t center = 0; center < UINT16_MAX; center++) {
        int64_t total_fuel = 0;
        for (int i = 0; i < n; i++) {
            total_fuel += tri(data[i] > center ? (int)(data[i] - center) : (int)(center - data[i]));
        }

        if (min_total_fuel > total_fuel)
            min_total_fuel = total_fuel;
    }

    return min_total_fuel;
}

int main(void) {
    uint16_t buf[1024];

    aoc_debug(LEVEL, sol1, TEST_DATA, 37);
    aoc_debug(LEVEL, sol2, TEST_DATA, 168);
}