#include <stdio.h>
#include <inttypes.h>
#include <string.h>

#include "NTT8_Kara8_helper.h"

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

uint32_t mod_exp(uint32_t base, uint32_t exp, uint32_t mod) {
    uint64_t result = 1;
    uint64_t base_mod = base % mod;

    while (exp > 0) {
        if (exp % 2 == 1) {
            result = (result * base_mod) % mod;
        }
        base_mod = (base_mod * base_mod) % mod;
        exp /= 2;
    }

    return (uint32_t)result;
}

void Nega_conv(uint32_t *A, uint32_t N, uint32_t psi, uint32_t q) {
    uint32_t i;

    uint32_t psi_temp;
    uint64_t A_temp;

    for (i = 0; i < N; i++) {
        psi_temp = mod_exp(psi, i, q);
        A_temp   = (uint64_t)A[i] * psi_temp;
        A[i]     = A_temp % q;
    }
    
}

void NTT_8(uint32_t *A, uint32_t N, uint32_t phi, uint32_t q) {
    uint32_t i;
    uint32_t j;
    uint32_t k;

    uint32_t add_temp;
    uint64_t sub_temp;
    uint32_t phi_temp;

    // Stage 0 - 7
    for (k = 0; k < 8; k++) {
        for (j = 0; j < (1<<k); j++) {
            for (i = 0; i < (N>>(k+1)); i++) {
                phi_temp = mod_exp(phi, (1<<k)*i, q);
                add_temp = A[i+j*(N>>k)] + A[i+j*(N>>k)+(N>>(k+1))];
                sub_temp = (uint64_t)(A[i+j*(N>>k)]+q - A[i+j*(N>>k)+(N>>(k+1))]) * phi_temp;

                A[i+j*(N>>k)]            = add_temp % q;
                A[i+j*(N>>k)+(N>>(k+1))] = sub_temp % q;
            }
        }
    }
}

void Kara_8(uint32_t *a_256, uint32_t *a_6561, uint32_t q) {
    uint32_t i;
    uint32_t j;

    uint32_t x[6561] = {0};

    // Stage 0
    for (j=0; j<1; j++) {
        for (i=0; i<128; i++) {
            x[j*384+i]      = a_256[j*256+i];
            x[j*384+i+128]  = (a_256[j*256+i] + a_256[j*256+i+128]) % q;
            x[j*384+i+256]  = a_256[j*256+i+128];
        }
    }
    // Stage 1
    for (j=0; j<3; j++) {
        for (i=0; i<64; i++) {
            a_6561[j*192+i]      = x[j*128+i];
            a_6561[j*192+i+64]   = (x[j*128+i] + x[j*128+i+64]) % q;
            a_6561[j*192+i+128]  = x[j*128+i+64];
        }
    }
    // Stage 2
    for (j=0; j<9; j++) {
        for (i=0; i<32; i++) {
            x[j*96+i]     = a_6561[j*64+i];
            x[j*96+i+32]  = (a_6561[j*64+i] + a_6561[j*64+i+32]) % q;
            x[j*96+i+64]  = a_6561[j*64+i+32];
        }
    }
    // Stage 3
    for (j=0; j<27; j++) {
        for (i=0; i<16; i++) {
            a_6561[j*48+i]     = x[j*32+i];
            a_6561[j*48+i+16]  = (x[j*32+i] + x[j*32+i+16]) % q;
            a_6561[j*48+i+32]  = x[j*32+i+16];
        }
    }
    // Stage 4
    for (j=0; j<81; j++) {
        for (i=0; i<8; i++) {
            x[j*24+i]     = a_6561[j*16+i];
            x[j*24+i+8]   = (a_6561[j*16+i] + a_6561[j*16+i+8]) % q;
            x[j*24+i+16]  = a_6561[j*16+i+8];
        }
    }
    // Stage 5
    for (j=0; j<243; j++) {
        for (i=0; i<4; i++) {
            a_6561[j*12+i]     = x[j*8+i];
            a_6561[j*12+i+4]   = (x[j*8+i] + x[j*8+i+4]) % q;
            a_6561[j*12+i+8]   = x[j*8+i+4];
        }
    }
    // Stage 6
    for (j=0; j<729; j++) {
        for (i=0; i<2; i++) {
            x[j*6+i]     = a_6561[j*4+i];
            x[j*6+i+2]   = (a_6561[j*4+i] + a_6561[j*4+i+2]) % q;
            x[j*6+i+4]   = a_6561[j*4+i+2];
        }
    }
    // Stage 7
    for (j=0; j<2187; j++) {
        for (i=0; i<1; i++) {
            a_6561[j*3+i]     = x[j*2+i];
            a_6561[j*3+i+1]   = (x[j*2+i] + x[j*2+i+1]) % q;
            a_6561[j*3+i+2]   = x[j*2+i+1];
        }
    }
}

void Ele_wise_Mult(uint32_t *A_6561, uint32_t *B_6561, uint32_t *C_6561, uint32_t Kara_6561, uint32_t q) {
    uint32_t i;

    uint64_t C_temp;

    for (i = 0; i < Kara_6561; i++) {
        C_temp = (uint64_t)A_6561[i] * B_6561[i];
        C_6561[i] = C_temp % q;
    }

}

void Inv_Kara_8(uint32_t *C_256, uint32_t *C_6561, uint32_t q) {
    uint32_t i;
    uint32_t j;
    uint32_t k;

    uint32_t x[6561] = {0};

    // Stage 0
    for (i=0; i<2187; i++) {
        for (k=0; k<1; k++) {
            x[i*3+k]   = C_6561[i*3+k];
            x[i*3+1+k] = (C_6561[i*3+1+k]+q+q - C_6561[i*3+k] - C_6561[i*3+2+k]) % q;
            x[i*3+2+k] = C_6561[i*3+2+k];
        }
    }
    memset(C_6561, 0, 6561 * sizeof(uint32_t));
    for (i=0; i<2187; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<1; k++) {
                C_6561[i*3+j+k] = (C_6561[i*3+j+k] + x[i*3+j+k]) % q;
            }
        }
    }
    // Stage 1
    for (i=0; i<729; i++) {
        for (k=0; k<3; k++) {
            x[i*9+k]   = C_6561[i*9+k];
            x[i*9+3+k] = (C_6561[i*9+3+k]+q+q - C_6561[i*9+k] - C_6561[i*9+6+k]) % q;
            x[i*9+6+k] = C_6561[i*9+6+k];
        }
    }
    memset(C_6561, 0, 6561 * sizeof(uint32_t));
    for (i=0; i<729; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<3; k++) {
                C_6561[i*7+j*2+k] = (C_6561[i*7+j*2+k] + x[i*9+j*3+k]) % q;
            }
        }
    }
    // Stage 2
    for (i=0; i<243; i++) {
        for (k=0; k<7; k++) {
            x[i*21+k]    = C_6561[i*21+k];
            x[i*21+7+k]  = (C_6561[i*21+7+k]+q+q - C_6561[i*21+k] - C_6561[i*21+14+k]) % q;
            x[i*21+14+k] = C_6561[i*21+14+k];
        }
    }
    memset(C_6561, 0, 6561 * sizeof(uint32_t));
    for (i=0; i<243; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<7; k++) {
                C_6561[i*15+j*4+k] = (C_6561[i*15+j*4+k] + x[i*21+j*7+k]) % q;
            }
        }
    }
    // Stage 3
    for (i=0; i<81; i++) {
        for (k=0; k<15; k++) {
            x[i*45+k]    = C_6561[i*45+k];
            x[i*45+15+k] = (C_6561[i*45+15+k]+q+q - C_6561[i*45+k] - C_6561[i*45+30+k]) % q;
            x[i*45+30+k] = C_6561[i*45+30+k];
        }
    }
    memset(C_6561, 0, 6561 * sizeof(uint32_t));
    for (i=0; i<81; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<15; k++) {
                C_6561[i*31+j*8+k] = (C_6561[i*31+j*8+k] + x[i*45+j*15+k]) % q;
            }
        }
    }
    // Stage 4
    for (i=0; i<27; i++) {
        for (k=0; k<31; k++) {
            x[i*93+k]    = C_6561[i*93+k];
            x[i*93+31+k] = (C_6561[i*93+31+k]+q+q - C_6561[i*93+k] - C_6561[i*93+62+k]) % q;
            x[i*93+62+k] = C_6561[i*93+62+k];
        }
    }
    memset(C_6561, 0, 6561 * sizeof(uint32_t));
    for (i=0; i<27; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<31; k++) {
                C_6561[i*63+j*16+k] = (C_6561[i*63+j*16+k] + x[i*93+j*31+k]) % q;
            }
        }
    }
    // Stage 5
    for (i=0; i<9; i++) {
        for (k=0; k<63; k++) {
            x[i*189+k]    = C_6561[i*189+k];
            x[i*189+63+k] = (C_6561[i*189+63+k]+q+q - C_6561[i*189+k] - C_6561[i*189+126+k]) % q;
            x[i*189+126+k] = C_6561[i*189+126+k];
        }
    }
    memset(C_6561, 0, 6561 * sizeof(uint32_t));
    for (i=0; i<9; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<63; k++) {
                C_6561[i*127+j*32+k] = (C_6561[i*127+j*32+k] + x[i*189+j*63+k]) % q;
            }
        }
    }
    // Stage 6
    for (i=0; i<3; i++) {
        for (k=0; k<127; k++) {
            x[i*381+k]    = C_6561[i*381+k];
            x[i*381+127+k] = (C_6561[i*381+127+k]+q+q - C_6561[i*381+k] - C_6561[i*381+254+k]) % q;
            x[i*381+254+k] = C_6561[i*381+254+k];
        }
    }
    memset(C_6561, 0, 6561 * sizeof(uint32_t));
    for (i=0; i<3; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<127; k++) {
                C_6561[i*255+j*64+k] = (C_6561[i*255+j*64+k] + x[i*381+j*127+k]) % q;
            }
        }
    }
    // Stage 7
    for (i=0; i<1; i++) {
        for (k=0; k<255; k++) {
            x[i*765+k]    = C_6561[i*765+k];
            x[i*765+255+k] = (C_6561[i*765+255+k]+q+q - C_6561[i*765+k] - C_6561[i*765+510+k]) % q;
            x[i*765+510+k] = C_6561[i*765+510+k];
        }
    }
    memset(C_6561, 0, 6561 * sizeof(uint32_t));
    for (i=0; i<1; i++) {
        for (j=0; j<3; j++) {
            for (k=0; k<255; k++) {
                C_6561[i*511+j*128+k] = (C_6561[i*511+j*128+k] + x[i*765+j*255+k]) % q;
            }
        }
    }

    // concat 511 to 256
    for (i=0; i<256; i++) {
        C_256[i] = C_6561[i];
    }
    for (i=0; i<255; i++) {
        C_256[i] = (C_256[i] + C_6561[i+256]) % q;
    }

}

void Inv_NTT_8(uint32_t *C, uint32_t N, uint32_t phi_inv, uint32_t inv_2, uint32_t q) {
    uint32_t i;
    uint32_t j;
    uint32_t k;

    uint32_t phi_inv_temp;
    uint64_t mult_temp;
    uint32_t mult_mod_temp;
    uint64_t C_temp;
    
    // Stage 0 - 7
    for (k = 0; k < 8; k++) {
        for (j = 0; j < (128>>k); j++) {
            for (i = 0; i < (256<<k); i++) {
                phi_inv_temp  = mod_exp(phi_inv, (128>>k)*i, q);
                mult_temp     = (uint64_t)C[i+j*(512<<k)+(256<<k)] * phi_inv_temp;
                mult_mod_temp = mult_temp % q;

                C[i+j*(512<<k)]          = (C[i+j*(512<<k)] + mult_mod_temp) % q;
                C[i+j*(512<<k)+(256<<k)] = (C[i+j*(512<<k)] - mult_mod_temp) % q;
            }
        }
        for (i = 0; i < N; i++) {
            C_temp = (uint64_t)C[i] * inv_2;
            C[i] = C_temp % q;
        }
    }

}