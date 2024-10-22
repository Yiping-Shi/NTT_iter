/*
 * Tests for naive iter64
 */

#include <windows.h>

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#include "iter16.h"

#define Q 1047525377

/*
 * Print array of size n
 */
static void print_array(FILE *f, int32_t *a, int32_t n) {
    uint32_t i, k;

    k = 0;
    for (i=0; i<n; i++) {
        if (k == 0) fprintf(f, "  ");
        fprintf(f, "%5"PRId32, a[i]);
        k ++;
        if (k == 16) {
            fprintf(f, "\n");
            k = 0;
        } else {
            fprintf(f, " ");
        }
    }
    if (k > 0) {
        fprintf(f, "\n");
    }
}


/*
 * Polynomial multiplication
 *
 */
void iter16_product(int32_t *c, int32_t *a, int32_t *b, int32_t *a_pre, int32_t *b_pre, int32_t *c_pre, int32_t *c_post) {
    uint32_t i;

    iter_preprocess_16(a, a_pre);

    iter_preprocess_16(b, b_pre);

    elementwise_product(c_pre, 81, a_pre, b_pre, Q);

    iter_postprocess_16(c_pre, c_post);
    
    iter_concat_16(c_post, c);
}


/*
 * Normalize all elements: make sure 0 <= a[i] < Q
 */

int all_non_negative(int32_t *a, uint32_t n) {
    uint32_t i;

    for (i = 0; i < n; i++) {
        if (a[i] < 0) {
            return 0;  
        }
    }
    return 1;

}

static void iter_normalize(int32_t *a, uint32_t n) {
    uint32_t i;

    while (!all_non_negative(a, n)) {
        for (i=0; i<n; i++) {
            if (a[i] < 0) a[i] += Q;
        }
    }

}


// *********************************************************
int main(void) {
    int32_t a[16];
    int32_t b[16];
    int32_t c[16];

    int32_t a_pre[81];
    int32_t b_pre[81];
    int32_t c_pre[81];
    int32_t c_post[31];
    
    for (int i=0; i<16; i++) {
        a[i] = i;
        b[i] = i;
    }

    for (int i=0; i<81; i++) {
        a_pre[i] = 0;
        b_pre[i] = 0;
        c_pre[i] = 0;
    }

    for (int i=0; i<31; i++) {
        c_post[i] = 0;
    }

    printf("a:\n");
    print_array(stdout, a, 16);

    printf("b:\n");
    print_array(stdout, b, 16);

    // product
    iter16_product(c, a, b, a_pre, b_pre, c_pre, c_post);
    printf("c(before norm):\n");
    print_array(stdout, c, 16);

    iter_normalize(c, 16);

    printf("c:\n");
    print_array(stdout, c, 16);

    return 0;
}