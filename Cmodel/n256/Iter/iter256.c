#include <assert.h>
#include <stdio.h>
#include <inttypes.h>

#include "iter256.h"

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
 * - n = 256    (Input length)
 * - m = 6561    (Output length)  
 * 
 * - output: a_pre = Iter(a) in length(n^1.5)
 */
void iter_preprocess_256(int32_t *a, int32_t *a_pre) {
    uint32_t i, j;
    int32_t x[6561];

    for (i=0; i<6561; i++) {
        x[i] = 0;
    }

    // Stage 0
    // Group num  = 1
    // Group size = 256
    for (j=0; j<1; j++) {
        for (i=0; i<128; i++) {
            x[j*384+i]      = a[j*256+i];
            x[j*384+i+128]  = a[j*256+i] + a[j*256+i+128];
            x[j*384+i+256]  = a[j*256+i+128];
        }
    }


    // Stage 1
    // Group num  = 3
    // Group size = 128
    for (j=0; j<3; j++) {
        for (i=0; i<64; i++) {
            a_pre[j*192+i]      = x[j*128+i];
            a_pre[j*192+i+64]   = x[j*128+i] + x[j*128+i+64];
            a_pre[j*192+i+128]  = x[j*128+i+64];
        }
    }

    // Stage 2
    // Group num  = 9
    // Group size = 64
    for (j=0; j<9; j++) {
        for (i=0; i<32; i++) {
            x[j*96+i]     = a_pre[j*64+i];
            x[j*96+i+32]  = a_pre[j*64+i] + a_pre[j*64+i+32];
            x[j*96+i+64]  = a_pre[j*64+i+32];
        }
    }

    // Stage 3
    // Group num  = 27
    // Group size = 32
    for (j=0; j<27; j++) {
        for (i=0; i<16; i++) {
            a_pre[j*48+i]     = x[j*32+i];
            a_pre[j*48+i+16]  = x[j*32+i] + x[j*32+i+16];
            a_pre[j*48+i+32]  = x[j*32+i+16];
        }
    }

    // Stage 4
    // Group num  = 81
    // Group size = 16
    for (j=0; j<81; j++) {
        for (i=0; i<8; i++) {
            x[j*24+i]     = a_pre[j*16+i];
            x[j*24+i+8]   = a_pre[j*16+i] + a_pre[j*16+i+8];
            x[j*24+i+16]  = a_pre[j*16+i+8];
        }
    }

    // Stage 5
    // Group num  = 243
    // Group size = 8
    for (j=0; j<243; j++) {
        for (i=0; i<4; i++) {
            a_pre[j*12+i]    = x[j*8+i];
            a_pre[j*12+i+4]  = x[j*8+i] + x[j*8+i+4];
            a_pre[j*12+i+8]  = x[j*8+i+4];
        }
    }

    // Stage 6
    // Group num  = 729
    // Group size = 4
    for (j=0; j<729; j++) {
        for (i=0; i<2; i++) {
            x[j*6+i]    = a_pre[j*4+i];
            x[j*6+i+2]  = a_pre[j*4+i] + a_pre[j*4+i+2];
            x[j*6+i+4]  = a_pre[j*4+i+2];
        }
    }

    // Stage 7
    // Group num  = 2187
    // Group size = 2
    for (j=0; j<2187; j++) {
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
 * - n = 6561    (Input length)
 * - m = 511    (Output length)  
 * 
 * - output: c_post = Iter(c_pre)
 */
void iter_postprocess_256(int32_t *c_pre, int32_t *c_post) {
    uint32_t i, j, k;
    int32_t x[6561];
    int32_t y[6561];

    for (i=0; i<6561; i++) {
        x[i] = 0;
        y[i] = 0;
    }

    // ****************
    // Stage 0
    // Group num  = 2187
    // Group size = 3

    // Stage 0 - 0: Substract
    for (i=0; i<6561; i++) {
        x[i] = c_pre[i];
    }
    for (i=0; i<2187; i++) {
        for (k=0; k<1; k++) {
            x[i*3+1+k] -= (c_pre[i*3+k] + c_pre[i*3+2+k]);
        }
    }
    // Stage 0 - 1: Concat
    for (i=0; i<6561; i++) {
        y[i] = 0;
    }
    for (i=0; i<2187; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<1; k++) {
                y[i*3+j+k] += x[i*3+j+k];
            }
        }
    }

    // ****************
    // Stage 1
    // Group num  = 729
    // Group size = 9

    // Stage 1 - 0: Substract
    for (i=0; i<6561; i++) {
        x[i] = y[i];
    }
    for (i=0; i<729; i++) {
        for (k=0; k<3; k++) {
            x[i*9+3+k] -= (y[i*9+k] + y[i*9+6+k]);
        }
    }
    // Stage 1 - 1: Concat
    for (i=0; i<6561; i++) {
        y[i] = 0;
    }
    for (i=0; i<729; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<3; k++) {
                y[i*7+j*2+k] += x[i*9+j*3+k];
            }
        }
    }

    
    // ****************
    // Stage 2
    // Group num  = 243
    // Group size = 21

    // Stage 2 - 0: Substract
    for (i=0; i<6561; i++) {
        x[i] = y[i];
    }
    for (i=0; i<243; i++) {
        for (k=0; k<7; k++) {
            x[i*21+7+k] -= (y[i*21+k] + y[i*21+14+k]);
        }
    }
    // Stage 2 - 1: Concat
    for (i=0; i<6561; i++) {
        y[i] = 0;
    }
    for (i=0; i<243; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<7; k++) {
                y[i*15+j*4+k] += x[i*21+j*7+k];
            }
        }
    }


    // ****************
    // Stage 3
    // Group num  = 81
    // Group size = 45

    // Stage 3 - 0: Substract
    for (i=0; i<6561; i++) {
        x[i] = y[i];
    }
    for (i=0; i<81; i++) {
        for (k=0; k<15; k++) {
            x[i*45+15+k] -= (y[i*45+k] + y[i*45+30+k]);
        }
    }
    // Stage 3 - 1: Concat
    for (i=0; i<6561; i++) {
        y[i] = 0;
    }
    for (i=0; i<81; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<15; k++) {
                y[i*31+j*8+k] += x[i*45+j*15+k];
            }
        }
    }


    // ****************
    // Stage 4
    // Group num  = 27
    // Group size = 93

    // Stage 4 - 0: Substract
    for (i=0; i<6561; i++) {
        x[i] = y[i];
    }
    for (i=0; i<27; i++) {
        for (k=0; k<31; k++) {
            x[i*93+31+k] -= (y[i*93+k] + y[i*93+62+k]);
        }
    }
    // Stage 4 - 1: Concat
    for (i=0; i<6561; i++) {
        y[i] = 0;
    }
    for (i=0; i<27; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<31; k++) {
                y[i*63+j*16+k] += x[i*93+j*31+k];
            }
        }
    }

    // ****************
    // Stage 5
    // Group num  = 9
    // Group size = 189

    // Stage 5 - 0: Substract
    for (i=0; i<6561; i++) {
        x[i] = y[i];
    }
    for (i=0; i<9; i++) {
        for (k=0; k<63; k++) {
            x[i*189+63+k] -= (y[i*189+k] + y[i*189+126+k]);
        }
    }
    // Stage 5 - 1: Concat
    for (i=0; i<6561; i++) {
        y[i] = 0;
    }
    for (i=0; i<9; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<63; k++) {
                y[i*127+j*32+k] += x[i*189+j*63+k];
            }
        }
    }

    // ****************
    // Stage 6
    // Group num  = 3
    // Group size = 381

    // Stage 6 - 0: Substract
    for (i=0; i<6561; i++) {
        x[i] = y[i];
    }
    for (i=0; i<3; i++) {
        for (k=0; k<127; k++) {
            x[i*381+127+k] -= (y[i*381+k] + y[i*381+254+k]);
        }
    }
    // Stage 6 - 1: Concat
    for (i=0; i<6561; i++) {
        y[i] = 0;
    }
    for (i=0; i<3; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<127; k++) {
                y[i*255+j*64+k] += x[i*381+j*127+k];
            }
        }
    }

    // ****************
    // Stage 7
    // Group num  = 1
    // Group size = 765

    // Stage 7 - 0: Substract
    for (i=0; i<6561; i++) {
        x[i] = y[i];
    }
    for (i=0; i<1; i++) {
        for (k=0; k<255; k++) {
            x[i*765+255+k] -= (y[i*765+k] + y[i*765+510+k]);
        }
    }
    // Stage 7 - 1: Concat
    for (i=0; i<1; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<255; k++) {
                c_post[i*511+j*128+k] += x[i*765+j*255+k];
            }
        }
    }
}


/*
 * Postprocess: apply mod(X^n+1) to c_post
 *
 * - input: c_post[0 ... n-1] in standard order
 * - n = 511    (Input length)
 * - m = 256    (Output length)  
 * 
 * - output: c = concat(c_post)
 */
void iter_concat_256(int32_t *c_post, int32_t *c) {
    uint32_t i;

    // assert(n == 511);
    // assert(m == 256);

    for (i=0; i<256; i++) {
        c[i] = c_post[i];
    }
    for (i=0; i<255; i++) {
        c[i] = c[i] - c_post[i+256];
    }

}

/*
 * Elementwise product: c[i] = a[i] * b[i]
 * - all arrays are 32bit integers of size n
 */
void elementwise_product(int32_t *c, uint32_t n, const int32_t *a, const int32_t *b) {
  uint32_t i;

  for (i=0; i<n; i++) {
    c[i] = (a[i] * b[i]);
  }
}