#include <assert.h>
#include <stdio.h>
#include <inttypes.h>

#include "iter16.h"

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
 * Preprocess: apply forward Iter to a
 *
 * - input: a[0 ... n-1] in standard order
 * - n = 16    (Input length)
 * - m = 81    (Output length)  
 * - q = 12289
 * 
 * - output: a_pre = Iter(a) in length(n^1.5)
 */
void iter_preprocess_16(int32_t *a, int32_t *a_pre) {
    uint32_t i, j;
    int32_t x[81];
    uint64_t t0, t1;

    for (i=0; i<81; i++) {
        x[i] = 0;
    }

    // Stage 0
    // Group num  = 1
    // Group size = 16
    for (j=0; j<1; j++) {
        for (i=0; i<8; i++) {
            x[j*24+i]     = a[j*16+i];
            x[j*24+i+8]   = a[j*16+i] + a[j*16+i+8];
            x[j*24+i+16]  = a[j*16+i+8];
        }
    }

    // Stage 1
    // Group num  = 3
    // Group size = 8
    for (j=0; j<3; j++) {
        for (i=0; i<4; i++) {
            a_pre[j*12+i]    = x[j*8+i];
            a_pre[j*12+i+4]  = x[j*8+i] + x[j*8+i+4];
            a_pre[j*12+i+8]  = x[j*8+i+4];
        }
    }

    // Stage 2
    // Group num  = 9
    // Group size = 4
    for (j=0; j<9; j++) {
        for (i=0; i<2; i++) {
            x[j*6+i]    = a_pre[j*4+i];
            x[j*6+i+2]  = a_pre[j*4+i] + a_pre[j*4+i+2];
            x[j*6+i+4]  = a_pre[j*4+i+2];
        }
    }

    // Stage 3
    // Group num  = 27
    // Group size = 2
    for (j=0; j<27; j++) {
        for (i=0; i<1; i++) {
            a_pre[j*3+i]    = x[j*2+i];
            a_pre[j*3+i+1]  = x[j*2+i] + x[j*2+i+1];
            a_pre[j*3+i+2]  = x[j*2+i+1];
        }
    }

}

/*
 * Postprocess: apply inverse Iter to c_pre
 *
 * - input: c_pre[0 ... n-1] in standard order
 * - n = 81    (Input length)
 * - m = 31    (Output length)  
 * 
 * - output: c_post = Iter(c_pre)
 */
void iter_postprocess_16(int32_t *c_pre, int32_t *c_post) {
    uint32_t i, j, k;
    int32_t x[81];
    int32_t y[81];

    for (i=0; i<81; i++) {
        x[i] = 0;
        y[i] = 0;
    }

    // ****************
    // Stage 0
    // Group num  = 27
    // Group size = 3

    // Stage 0 - 0: Substract
    for (i=0; i<81; i++) {
        x[i] = c_pre[i];
    }
    for (i=0; i<27; i++) {
        for (k=0; k<1; k++) {
            x[i*3+1+k] -= (c_pre[i*3+k] + c_pre[i*3+2+k]);
        }
    }
    // Stage 0 - 1: Concat
    for (i=0; i<81; i++) {
        y[i] = 0;
    }
    for (i=0; i<27; i++) {
        for (j=0; j<1; j++) {
            for (k=0; k<3; k++) {
                y[i*3+j+k] += x[i*3+j+k];
            }
        }
    }

    // ****************
    // Stage 1
    // Group num  = 9
    // Group size = 9

    // Stage 1 - 0: Substract
    for (i=0; i<81; i++) {
        x[i] = y[i];
    }
    for (i=0; i<9; i++) {
        for (k=0; k<3; k++) {
            x[i*9+3+k] -= (y[i*9+k] + y[i*9+6+k]);
        }
    }
    // Stage 1 - 1: Concat
    for (i=0; i<81; i++) {
        y[i] = 0;
    }
    for (i=0; i<9; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<3; k++) {
                y[i*7+j*2+k] += x[i*9+j*3+k];
            }
        }
    }
    
    // ****************
    // Stage 2
    // Group num  = 3
    // Group size = 21

    // Stage 2 - 0: Substract
    for (i=0; i<81; i++) {
        x[i] = y[i];
    }
    for (i=0; i<3; i++) {
        for (k=0; k<7; k++) {
            x[i*21+7+k] -= (y[i*21+k] + y[i*21+14+k]);
        }
    }
    // Stage 2 - 1: Concat
    for (i=0; i<81; i++) {
        y[i] = 0;
    }
    for (i=0; i<3; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<7; k++) {
                y[i*15+j*4+k] += x[i*21+j*7+k];
            }
        }
    }


    // ****************
    // Stage 3
    // Group num  = 1
    // Group size = 45

    // Stage 3 - 0: Substract
    for (i=0; i<81; i++) {
        x[i] = y[i];
    }
    for (i=0; i<1; i++) {
        for (k=0; k<15; k++) {
            x[i*45+15+k] -= (y[i*45+k] + y[i*45+30+k]);
        }
    }

    // Stage 3 - 1: Concat
    for (i=0; i<1; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<15; k++) {
                c_post[i*31+j*8+k] += x[i*45+j*15+k];
            }
        }
    }
}


/*
 * Postprocess: apply mod(X^n+1) to c_post
 *
 * - input: c_post[0 ... n-1] in standard order
 * - n = 31    (Input length)
 * - m = 16    (Output length)  
 * 
 * - output: c = concat(c_post)
 */
void iter_concat_16(int32_t *c_post, int32_t *c) {
    uint32_t i;

    // assert(n == 31);
    // assert(m == 16);

    for (i=0; i<16; i++) {
        c[i] = c_post[i];
    }
    for (i=0; i<15; i++) {
        c[i] = c[i] - c_post[i+16];
    }

}

/*
 * Elementwise product: c[i] = a[i] * b[i]
 * - all arrays are 32bit integers of size n
 */
void elementwise_product(int32_t *c, uint32_t n, const int32_t *a, const int32_t *b, int32_t q) {
  uint32_t i;

  for (i=0; i<n; i++) {
    c[i] = (a[i] * b[i]) % q;
  }
}