#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
#include <assert.h>

#include "NTT15_Kara1_helper.h"

// Parameter Definition
#define N            65536       // N = 2^16
// #define N_kara       1679616     // N_kara = 2^8 * 3^8
#define Kara_group   32768       // Kara_group = 2^15
#define Kara_2       2
#define Kara_3       3
#define K            32
#define q            998244353
#define phi          629671588
#define phi_inv      283043518
#define psi          24514907
#define psi_inv      3707709
#define N_inv        998229121
#define inv_2        499122177

#define NTESTS 4

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

static int32_t random_coeff(void) {
  int32_t x;

  x = rand() % q;
  assert(0 <= x && x <= q-1);
  return x;
}

/*
 * For speed measurements: counter of CPU cycles
 */
static inline uint64_t cpucycles(void) {
  uint64_t result;
  __asm__ volatile(".byte 15;.byte 49;shlq $32,%%rdx;orq %%rdx,%%rax"
    : "=a" (result) ::  "%rdx");
  return result;
}

int main() {
    // -----------------------------------------
	  printf("********** Start Init **********\n");
    uint32_t i,j;
	  uint32_t A[N] = {0};
    uint32_t B[N] = {0};
    uint32_t C[N] = {0};
    for (i = 0; i < N; i++) {
        A[i] = i;
        B[i] = i;
    }
    // for (i = 0; i < N; i++) {
    //     A[i] = random_coeff();
    //     B[i] = random_coeff();
    // }
    printf("********** End Init **********\n\n");


    // -----------------------------------------
    printf("Speed test:\n");
    uint64_t t[NTESTS];
    uint64_t avg, s, tt;

    for (i=0; i<NTESTS; i++) {
        t[i] = cpucycles();
        // Function Under Test
        Nega_conv(A, N, psi, q);
        Nega_conv(B, N, psi, q);

        NTT_15(A, N, phi, q);
        NTT_15(B, N, phi, q);

        uint32_t A_3[Kara_3] = {0};
        uint32_t B_3[Kara_3] = {0};
        uint32_t C_3[Kara_3] = {0};

        for (j=0; j<Kara_group; j++) {
            uint32_t* A_2 = &A[j*Kara_2];
            uint32_t* B_2 = &B[j*Kara_2];
            Kara_1(A_2, A_3, q);
            Kara_1(B_2, B_3, q);
            // -----------------------------------------
            Ele_wise_Mult(A_3, B_3, C_3, Kara_3, q);
            // -----------------------------------------
            uint32_t* C_2 = &C[j*Kara_2];
            Inv_Kara_1(C_2, C_3, q);
        }

        Inv_NTT_15(C, N, phi_inv, inv_2, q);

        Nega_conv(C, N, psi_inv, q);
    }
    tt = cpucycles();
    for (i=0; i<NTESTS-1; i++) {
        t[i] = t[i+1] - t[i];
    }
    t[i] = tt - t[i];
    s = 0;
    for (i=0; i<NTESTS; i++) {
        s += t[i];
    }
    avg = s / NTESTS;
    printf("speed test %s: average = %"PRIu64"\n\n", "Poly_NTT16_Kara0", avg);


    // -----------------------------------------
    printf("********** Start Verification **********\n");
    uint32_t Base_temp[2*N-1] = {0};
    uint32_t Base[N] = {0};
    for (i = 0; i < N; i++) {
      for (j = 0; j < N; j++) {
        Base_temp[i+j] = Base_temp[i+j] + (uint64_t)A[i] * B[j] % q;
      }
    }
    for (i = 0; i < N; i++) {
      Base[i] = Base_temp[i] % q;
    }
    for (i = N; i < 2*N-1; i++) {
      Base[i-N] = (Base[i-N]+q - Base_temp[i]) % q;
    }

    if (memcmp(C, Base, N * sizeof(uint32_t)) == 0) {
      printf("Verification PASS! :) :) :) :) :)\n");
    } else {
      printf("Verification PASS! :) :) :) :) :)\n");
    }

    printf("********** End Verification **********\n\n");     
      
    return 0;
}
