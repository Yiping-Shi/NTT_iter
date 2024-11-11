import random
from Poly_NTT_helper_ct2gs import *

# Parameter Definition
# N        = 16
# K        = 14    # 2^14 = 16384
# q        = 12289
# psi      = 1212
# phi      = 6553  # phi = pow(psi, 2, q)
# psi_inv  = 2545
# phi_inv  = 722
# n_inv    = 11521
# -------
N        = 16
K        = 8
q        = 193
psi      = 8
phi      = 64
psi_inv  = 169
phi_inv  = 190
n_inv    = 181

# -----------------------------------
print("********** Start Init **********")
A = list(range(N))
B = list(range(N))
# A = [random.randint(0, q-1) for _ in range(N)]
# B = [random.randint(0, q-1) for _ in range(N)]
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
print("********** Start NTT **********")
A_ntt = ntt_ct_std2rev(A_nega_conv, N, phi, q)
B_ntt = ntt_ct_std2rev(B_nega_conv, N, phi, q)
print("A_ntt: ", A_ntt)
print("B_ntt: ", B_ntt)
print("********** End NTT **********")
print("\n\r")

# -----------------------------------
print("********** Start Element_wise_Mult **********")
C_ntt = mul_array_elementwise(A_ntt, B_ntt, N, q)
print("C_ntt: ", C_ntt)
print("********** End Element_wise_Mult **********")
print("\n\r")

# -----------------------------------
print("********** Start Inverse NTT **********")
# C_ntt = indexReverse(C_ntt, int(math.log(N, 2)))
# print("C_ntt(rev_std): ", C_ntt)
C = intt_gs_rev2std(C_ntt, N, phi_inv, q)
print("C: ", C)
# C = indexReverse(C, int(math.log(N, 2)))
# print("C(rev_std): ", C)
print("********** End Inverse NTT **********")
print("\n\r")

# -----------------------------------
print("********** Start Nega_conv_psi_inv **********")
C_nega_conv = nega_conv_mul_array(C, N, psi_inv, q)
result = [0] * N
for i in range(N):
    result[i] = (C_nega_conv[i] * n_inv) % q
print("Result: ", result)
print("********** End Nega_conv_psi_inv **********")
print("\n\r")

# -----------------------------------
print("********** Start Baseline-Verification **********")
n = len(A) + len(B) - 1
temp = [0] * n
baseline = [0] * N

for i in range(N):
    for j in range(N):
        temp[i+j] += (A[i] * B[j]) % q

for i in range(N):
    baseline[i] = temp[i] % q
for i in range(N, n):
    baseline[i-N] = (baseline[i-N] - temp[i]) % q 
    
print("Baseline: ", baseline)
if result == baseline:
    print("Verification: Passed! 😊😊😊😊😊")
else:
    print("Verification: Failed! 😢😢😢😢😢")
print("********** End Baseline-Verification **********")