#include <stdio.h>
#include <inttypes.h>
#include <string.h>

#include "NTT15_Kara1_helper.h"

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

void NTT_15(uint32_t *A, uint32_t N, uint32_t phi, uint32_t q) {
    uint32_t i;
    uint32_t j;
    uint32_t k;

    uint32_t add_temp;
    uint64_t sub_temp;
    uint32_t phi_temp;

    // Stage 0 - 14
    for (k = 0; k < 15; k++) {
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

void Kara_1(uint32_t *a_2, uint32_t *a_3, uint32_t q) {

    // Stage 0
    a_3[0] = a_2[0];
    a_3[1] = (a_2[0] + a_2[1]) % q;
    a_3[2] = a_2[1];

}

void Ele_wise_Mult(uint32_t *A_6561, uint32_t *B_6561, uint32_t *C_6561, uint32_t Kara_6561, uint32_t q) {
    uint32_t i;

    uint64_t C_temp;

    for (i = 0; i < Kara_6561; i++) {
        C_temp = (uint64_t)A_6561[i] * B_6561[i];
        C_6561[i] = C_temp % q;
    }

}

void Inv_Kara_1(uint32_t *C_2, uint32_t *C_3, uint32_t q) {

    uint32_t x[3] = {0};

    // Stage 0
    x[0] = C_3[0];
    x[1] = (C_3[1]+q+q - C_3[0] - C_3[2]) % q; 
    x[2] = C_3[2];
    memset(C_3, 0, 3 * sizeof(uint32_t));
    C_3[0] = x[0];
    C_3[1] = x[1];
    C_3[2] = x[2];

    // concat 3 to 2
    C_2[0] = (C_3[0]+C_3[2]) % q;
    C_2[1] = C_3[1];
    
}

void Inv_NTT_15(uint32_t *C, uint32_t N, uint32_t phi_inv, uint32_t inv_2, uint32_t q) {
    uint32_t i;
    uint32_t j;
    uint32_t k;

    uint32_t phi_inv_temp;
    uint64_t mult_temp;
    uint32_t mult_mod_temp;
    uint64_t C_temp;
    
    // Stage 0 - 14
    for (k = 0; k < 15; k++) {
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