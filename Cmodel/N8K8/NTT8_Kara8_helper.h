#ifndef __NTT8_KARA8_HELPER_H__
#define __NTT8_KARA8_HELPER_H__

#include <inttypes.h>

extern void Nega_conv(uint32_t *A, uint32_t N, uint32_t psi, uint32_t q);

extern void NTT_8(uint32_t *A, uint32_t N, uint32_t phi, uint32_t q);

extern void Kara_8(uint32_t *a_256, uint32_t *a_6561, uint32_t q);

extern void Ele_wise_Mult(uint32_t *A_6561, uint32_t *B_6561, uint32_t *C_6561, uint32_t Kara_6561, uint32_t q);

extern void Inv_Kara_8(uint32_t *C_256, uint32_t *C_6561, uint32_t q);

extern void Inv_NTT_8(uint32_t *C, uint32_t N, uint32_t phi_inv, uint32_t inv_2, uint32_t q);

#endif /* __NTT8_KARA8_HELPER_H__ */