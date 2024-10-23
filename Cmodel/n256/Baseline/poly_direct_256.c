/*
 * Direct Polynomial Multiplication
 * O(n^2)
 */

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#define Q 601381537

/*
 * Print array of size n
 */
static void print_array(FILE *f, int64_t *a, int32_t n) {
  uint32_t i, k;

  k = 0;
  for (i=0; i<n; i++) {
    if (k == 0) fprintf(f, "  ");
    fprintf(f, "%5"PRId64, a[i]);
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
 * Direct polynomial multiplication
 * c_pre = a * b
 */
void direct_256(int64_t *c_pre, int64_t *a, int64_t *b) {
    uint32_t i, j;

    for (i=0; i<256; i++) {
        for (j=0; j<256; j++) {
            c_pre[i+j] += a[i] * b[j];
        }
    }
}

/*
 * Concatenate c_pre to c
 */
void direct_concat_256(int64_t *c_pre, int64_t *c) {
    uint32_t i;

    for (i=0; i<256; i++) {
        c[i] = c_pre[i];
    }
    for (i=0; i<255; i++) {
        c[i] = c[i] - c_pre[i+256];
    }
}

/*
 * Normalize all elements: make sure 0 <= a[i] < Q
 */

int all_non_negative_256(int64_t *a) {
    uint32_t i;

    for (i = 0; i < 256; i++) {
        if (a[i] < 0) {
            return 0;  
        }
    }
    return 1;

}

static void direct_normalize_256(int64_t *a) {
    uint32_t i;

    while (!all_non_negative_256(a)) {
        for (i=0; i<256; i++) {
            if (a[i] < 0) a[i] += Q;
        }
    }

}

/*
 * Direct polynomial multiplication
 * c = a * b
 */
void direct256_product(int64_t *c, int64_t *c_pre, int64_t *a, int64_t *b) {
    uint32_t i;
    
    for (i=0; i<256; i++) {
        a[i] = i;
        b[i] = i;
        c[i] = 0;   
    }
    for (i=0; i<511; i++) {
        c_pre[i] = 0;
    }  
    direct_256(c_pre, a, b);
    printf("c_pre:\n");
    print_array(stdout, c_pre, 511);
    direct_concat_256(c_pre, c);
    printf("c(before norm):\n");
    print_array(stdout, c, 256);
    direct_normalize_256(c);   
}

// ******************************************
int main(void) {
    int64_t a[256];
    int64_t b[256];
    int64_t c[256];
    int64_t c_pre[511];

    uint32_t n;
    uint32_t i;

    n = 256;

    for (i=0; i<n; i++) {
        a[i] = i;
        b[i] = i;
        c[i] = 0;   
    }
    for (i=0; i<511; i++) {
        c_pre[i] = 0;
    }

    printf("a:\n");
    print_array(stdout, a, n);

    printf("b:\n");
    print_array(stdout, b, n);

    direct256_product(c, c_pre, a, b);

    printf("c:\n");
    print_array(stdout, c, n);

    return 0;    
}