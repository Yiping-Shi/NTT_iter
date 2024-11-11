import math
from NTT_helper import *

# Parameter Definition
N       = 16
K       = 8
q       = 193
psi     = 8
psi_inv = 169
phi     = 64
phi_inv = 190

inv_2 = modinv(2, q)
inv_4 = modinv(4, q)
inv_8 = modinv(8, q)
N_inv = modinv(N, q)
print("inv_2: ", inv_2)
print("inv_4: ", inv_4)
print("inv_8: ", inv_8)
print("N_inv: ", N_inv)
print("\n\r")

# -----------------------------------
print("********** Start Init **********")
A = list(range(N))
# B = list(range(N))
print("A: ", A)
# print("B: ", B)
print("********** End Init **********")
print("\n\r")

# -----------------------------------
print("********** Start NTT **********")
A_ntt = IterativeForwardNTT(A,q,phi)
# B_ntt = IterativeForwardNTT(B,q,phi)
print("A_ntt: ", A_ntt)
# print("B_ntt: ", B_ntt)
print("\n\r")

A_ntt_pre_stage = NTT_pre_stage(A, q, phi)
print("A_ntt_pre_stage: ", A_ntt_pre_stage)

print("********** End NTT **********")
print("\n\r")

# -----------------------------------
print("********** Start INTT **********")
A_intt_pre_stage = INTT_pre_stage(A_ntt_pre_stage, q, phi_inv, inv_2)
print("A_intt_pre_stage: ", A_intt_pre_stage)

for i in range(N):
    A_intt_pre_stage[i] = (A_intt_pre_stage[i] * inv_2) % q
print("A_intt_pre_stage: ", A_intt_pre_stage)

print("********** End INTT **********")
print("\n\r")

