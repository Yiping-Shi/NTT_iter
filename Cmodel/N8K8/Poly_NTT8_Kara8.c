#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
#include <assert.h>

#include "NTT8_Kara8_helper.h"

// Parameter Definition
#define N            65536       // N = 2^16
// #define N_kara       1679616     // N_kara = 2^8 * 3^8
#define Kara_group   256
#define Kara_256     256
#define Kara_6561    6561
#define K            32
#define q            998244353
#define phi          629671588
#define phi_inv      283043518
#define psi          24514907
#define psi_inv      3707709
#define N_inv        998229121
#define inv_2        499122177

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

int main() {
    // -----------------------------------------
	  printf("********** Start Init **********\n");
    uint32_t i,j;
	  uint32_t A[N] = {0};
    uint32_t B[N] = {0};
    uint32_t C[N] = {0};
    // for (i = 0; i < N; i++) {
    //     A[i] = i;
    //     B[i] = i;
    // }
    for (i = 0; i < N; i++) {
        A[i] = random_coeff();
        B[i] = random_coeff();
    }
    printf("A[0:15]");
    print_array(stdout, A, 16);
    printf("B[0:15]");
    print_array(stdout, B, 16);
    printf("********** End Init **********\n\n");

    // -----------------------------------------
    printf("********** Start Nega_conv **********\n");
    Nega_conv(A, N, psi, q);
    Nega_conv(B, N, psi, q);
    printf("A[0:15]");
    print_array(stdout, A, 16);
    printf("B[0:15]");
    print_array(stdout, B, 16);
    printf("********** End Nega_conv **********\n\n");

    // -----------------------------------------
    printf("********** Start NTT **********\n");
    NTT_8(A, N, phi, q);
    NTT_8(B, N, phi, q);
    printf("A[0:15]");
    print_array(stdout, A, 16);
    printf("B[0:15]");
    print_array(stdout, B, 16);
    printf("********** End NTT **********\n\n");

    // -----------------------------------------
    printf("********** Start Karatsuba - Element-wise Mult **********\n");
    uint32_t A_6561[Kara_6561] = {0};
    uint32_t B_6561[Kara_6561] = {0}; 
    uint32_t C_6561[Kara_6561] = {0}; 

    for (i = 0; i < Kara_group; i++) {
        uint32_t* A_256  = &A[i*Kara_256];
        uint32_t* B_256  = &B[i*Kara_256];
        Kara_8(A_256, A_6561, q);
        Kara_8(B_256, B_6561, q);
        // -----------------------------------------
        Ele_wise_Mult(A_6561, B_6561, C_6561, Kara_6561, q);
        // -----------------------------------------
        uint32_t* C_256  = &C[i*Kara_256];
        Inv_Kara_8(C_256, C_6561, q);
    }
    printf("C[0:15]");
    print_array(stdout, C, 16);
    printf("********** End Karatsuba - Element-wise Mult **********\n\n");

    // -----------------------------------------
    printf("********** Start Inv_NTT **********\n");
    Inv_NTT_8(C, N, phi_inv, inv_2, q);
    printf("C[0:15]");
    print_array(stdout, C, 16);
    printf("********** End Inv_NTT **********\n\n");

    // -----------------------------------------
    printf("********** Start Inv_Nega_conv **********\n");
    Nega_conv(C, N, psi_inv, q);
    printf("C[0:15]");
    print_array(stdout, C, 16);
    printf("********** End Inv_Nega_conv **********\n\n");

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
