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
A = list(range(N))
print("A: ", A)
print("********** End Init **********")
print("\n\r")

# -----------------------------------
print("********** Start NTT **********")
A_ntt = ntt_ct_std2rev(A, N, 2, q)
print("A_ntt: ", A_ntt)
print("\n\r")

A_stage_1 = ntt_ct_std2rev_stage_1(A, N, 2, q)
print("A_stage_1: ", A_stage_1)
print("\n\r")

A_stage_2 = ntt_ct_std2rev_stage_2(A_stage_1, N, 2, q)
print("A_stage_2: ", A_stage_2)
print("\n\r")

A_stage_3 = ntt_ct_std2rev_stage_3(A_stage_2, N, 2, q)
print("A_stage_3: ", A_stage_3)
print("\n\r")

A_stage_4 = ntt_ct_std2rev_stage_4(A_stage_3, N, 2, q)
print("A_stage_4: ", A_stage_4)
print("\n\r")

# -----------------------------------
print("********** Start Verification **********")
if A_ntt == A_stage_4:
    print("Verification: Passed! 😊😊😊😊😊")
else:
    print("Verification: Failed! 😢😢😢😢😢")