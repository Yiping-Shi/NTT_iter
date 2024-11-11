import math
import random
from NTT_Kara_helper import *

# Parameter Definition
N       = 16
K       = 8
q       = 193
psi     = 8
psi_inv = 169
phi     = 64
phi_inv = 190

inv_2 = modinv(2, q)
print("inv_2: ", inv_2)
print("\n\r")

# -----------------------------------
print("********** Start Init **********")
# A = list(range(N))
# B = list(range(N))
# A = [1] * N
# B = [1] * N
A = [random.randint(0, q-1) for _ in range(N)]
B = [random.randint(0, q-1) for _ in range(N)]
print("A: ", A)
print("B: ", B)
print("********** End Init **********")
print("\n\r")

# -----------------------------------
print("********** Start Nega_conv **********")
A_nega = [0] * N
B_nega = [0] * N
for i in range(N):
    A_nega[i] = (A[i] * ((psi**i)%q)) % q
    B_nega[i] = (B[i] * ((psi**i)%q)) % q
print("A_nega: ", A_nega)
print("B_nega: ", B_nega)
print("********** End Nega_conv **********")
print("\n\r")

# -----------------------------------
print("********** Start NTT **********")
A_ntt_pre_stage = NTT3_Kara1_pre_stage(A_nega, q, phi)
B_ntt_pre_stage = NTT3_Kara1_pre_stage(B_nega, q, phi)
print("A_ntt_pre_stage: ", A_ntt_pre_stage)
print("B_ntt_pre_stage: ", B_ntt_pre_stage)
print("********** End NTT **********")
print("\n\r")

# -----------------------------------
print("********** Start Element-wise Mult **********")
C = [0] * int(N*3/2)
for i in range(int(N*3/2)):
    C[i] = (A_ntt_pre_stage[i] * B_ntt_pre_stage[i]) % q
print("C: ", C)
print("********** End Element-wise Mult **********")
print("\n\r")

# -----------------------------------
print("********** Start INTT **********")
C_intt_pre_stage = Kara1_INTT3_pre_stage(C, q, phi_inv, inv_2)
print("C_intt_pre_stage: ", C_intt_pre_stage)
print("********** End INTT **********")
print("\n\r")

# -----------------------------------
print("********** Start inv_Nega_conv **********")
C = [0] * N
for i in range(N):
    C[i] = (C_intt_pre_stage[i] * ((psi_inv**i)%q)) % q
print("C: ", C)
print("********** End inv_Nega_conv **********")
print("\n\r")

# -----------------------------------
print("********** Start Verification **********")
Base_temp = [0] * (2*N-1)
for i in range(N):
    for j in range(N):
        Base_temp[i+j] += A[i] * B[j] % q
        # Base_temp[i+j] %= q
print("Base_temp: ", Base_temp)
Base = [0] * N
for i in range(N):
    Base[i] = Base_temp[i] % q
for i in range(N, 2*N-1):
    Base[i-N] = (Base[i-N] - Base_temp[i]) % q
print("Base: ", Base)

if C == Base:
    print("Verification Passed! 😊😊😊😊😊")
else:
    print("Verification Failed! 😢😢😢😢😢")
print("********** End Verification **********")