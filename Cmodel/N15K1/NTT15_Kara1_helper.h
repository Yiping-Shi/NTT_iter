#ifndef __NTT15_KARA1_HELPER_H__
#define __NTT15_KARA1_HELPER_H__

#include <inttypes.h>

extern void Nega_conv(uint32_t *A, uint32_t N, uint32_t psi, uint32_t q);

extern void NTT_15(uint32_t *A, uint32_t N, uint32_t phi, uint32_t q);

extern void Kara_1(uint32_t *a_2, uint32_t *a_3, uint32_t q);

extern void Ele_wise_Mult(uint32_t *A_6561, uint32_t *B_6561, uint32_t *C_6561, uint32_t Kara_6561, uint32_t q);

extern void Inv_Kara_1(uint32_t *C_2, uint32_t *C_3, uint32_t q);

extern void Inv_NTT_15(uint32_t *C, uint32_t N, uint32_t phi_inv, uint32_t inv_2, uint32_t q);

#endif /* __NTT15_KARA1_HELPER_H__ */