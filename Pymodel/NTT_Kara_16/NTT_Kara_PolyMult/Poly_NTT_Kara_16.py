import random
from Poly_NTT_Kara_helper import *

# Parameter Definition
N        = 16
K        = 14    # 2^14 = 16384
q        = 12289
psi      = 1212
phi      = 6553  # phi = pow(psi, 2, q)
psi_inv  = 2545
phi_inv  = 722
n_inv    = 11521

# -----------------------------------
print("********** Start Init **********")
# A = list(range(N))
# B = list(range(N))
A = [1,1,1,1, 1,1,1,1, 0,0,0,0, 0,0,0,0]
B = [1,1,1,1, 1,1,1,1, 0,0,0,0, 0,0,0,0]
print("A: ", A)
print("B: ", B)
print("********** End Init **********")
print("\n\r")

# -----------------------------------
print("********** Start Nega_conv_psi **********")
A_nega_conv = nega_conv_mul_array(A, N, psi, q)
B_nega_conv = nega_conv_mul_array(B, N, psi, q)
print("A_nega_conv: ", A_nega_conv)
print("B_nega_conv: ", B_nega_conv)
print("********** End Nega_conv_psi **********")
print("\n\r")

# -----------------------------------
# +++++++++++++++++++++++++++++++++++
print("********** Start NTT Stage by Stage **********")
print("Start Stage 1:")
A_stage_1 = ntt_ct_std2rev_stage_1(A_nega_conv, N, phi, q)
B_stage_1 = ntt_ct_std2rev_stage_1(B_nega_conv, N, phi, q)
print("A_stage_1: ", A_stage_1)
print("B_stage_1: ", B_stage_1)
print("\n\r")

print("Start Stage 2:")
A_stage_2 = ntt_ct_std2rev_stage_2(A_stage_1, N, phi, q)
B_stage_2 = ntt_ct_std2rev_stage_2(B_stage_1, N, phi, q)
print("A_stage_2: ", A_stage_2)
print("B_stage_2: ", B_stage_2)
print("\n\r")

print("Start Stage 3:")
A_stage_3 = ntt_ct_std2rev_stage_3(A_stage_2, N, phi, q)
B_stage_3 = ntt_ct_std2rev_stage_3(B_stage_2, N, phi, q)
print("A_stage_3: ", A_stage_3)
print("B_stage_3: ", B_stage_3)
print("\n\r")

print("Start Stage 4:")
A_stage_4 = ntt_ct_std2rev_stage_4(A_stage_3, N, phi, q)
B_stage_4 = ntt_ct_std2rev_stage_4(B_stage_3, N, phi, q)
print("A_stage_4: ", A_stage_4)
print("B_stage_4: ", B_stage_4)
print("\n\r")

# print("Replace NTT-Stage 4 with Karatsuba-Preprocessing")
# A_Kara_pre = karatsuba_preprocess(A_stage_3, N, q)
# B_Kara_pre = karatsuba_preprocess(B_stage_3, N, q)
# print("A_Kara_pre: ", A_Kara_pre)
# print("B_Kara_pre: ", B_Kara_pre)
# print("\n\r")

print("********** End NTT Stage by Stage **********")
print("\n\r")

# -----------------------------------
print("********** Start Element_wise_Mult **********")
C_ntt = mul_array_elementwise(A_stage_4, B_stage_4, N, q)
print("C_ntt: ", C_ntt)
# C_Kara_pre = mul_array_elementwise(A_Kara_pre, B_Kara_pre, len(A_Kara_pre), q)
# print("C_Kara_pre: ", C_Kara_pre)
print("********** End Element_wise_Mult **********")
print("\n\r")

# -----------------------------------
# +++++++++++++++++++++++++++++++++++
print("********** Start Inverse NTT Stage by Stage **********")
print("Start Stage 1:")
C_stage_1 = intt_ct_rev2std_stage_1(C_ntt, N, phi_inv, q)
print("C_stage_1: ", C_stage_1)
print("\n\r")

# print("Replace Inverse NTT-Stage 1 with Karatsuba-Postprocessing")
# C_Kara_post = karatsuba_postprocess(C_Kara_pre, N, q)
# print("C_Kara_post: ", C_Kara_post)
# print("\n\r")

print("Start Stage 2:")
C_stage_2 = intt_ct_rev2std_stage_2(C_stage_1, N, phi_inv, q)
print("C_stage_2: ", C_stage_2)
print("\n\r")

print("Start Stage 3:")
C_stage_3 = intt_ct_rev2std_stage_3(C_stage_2, N, phi_inv, q)
print("C_stage_3: ", C_stage_3)
print("\n\r")

print("Start Stage 4:")
C_stage_4 = intt_ct_rev2std_stage_4(C_stage_3, N, phi_inv, q)
print("C_stage_4: ", C_stage_4)
print("\n\r")

print("********** End Inverse NTT Stage by Stage **********")
print("\n\r")

# -----------------------------------
print("********** Start Nega_conv_psi_inv **********")
C_nega_conv = nega_conv_mul_array(C_stage_4, N, psi_inv, q)
result = [0] * N
for i in range(N):
    result[i] = (C_nega_conv[i] * n_inv) % q
print("Result: ", result)
print("********** End Nega_conv_psi_inv **********")
print("\n\r")