import math
import random
import time
from NTT8_Kara8_helper import *

# Parameter Definition
N       =  65536
K       =  32
q       =  998244353
phi     =  629671588
phi_inv =  283043518
psi     =  24514907
psi_inv =  3707709
N_inv   =  998229121
inv_2   =  499122177

start_time = time.time()
print("start_time: ", start_time)

# -----------------------------------
print("********** Start Init **********")
A = list(range(N))
B = list(range(N))
# A = [1] * (N // 2) + [0] * (N // 2)
# B = [1] * (N // 2) + [0] * (N // 2)
# A = [random.randint(0, q-1) for _ in range(N)]
# B = [random.randint(0, q-1) for _ in range(N)]
print("A[0:16]: ", A[0:16])
print("B[0:16]: ", B[0:16])
print("********** End Init **********")
print("\n\r")

# -----------------------------------
print("********** Start Nega_conv **********")
nega_conv_start_time = time.time()
A_nega = [0] * N
B_nega = [0] * N
for i in range(N):
    A_nega[i] = (A[i] * ((psi**i)%q)) % q
    B_nega[i] = (B[i] * ((psi**i)%q)) % q
    if (i%8192==0):
        print("i", i)
print("A_nega[0:16]: ", A_nega[0:16])
print("B_nega[0:16]: ", B_nega[0:16])
nega_conv_end_time = time.time()
print("Nega_conv Time: ", nega_conv_end_time - nega_conv_start_time)
print("********** End Nega_conv **********")
print("\n\r")

# -----------------------------------
print("********** Start NTT **********")
ntt_start_time = time.time()
A_ntt8 = NTT8(A_nega, q, phi)
B_ntt8 = NTT8(B_nega, q, phi)
print("A_ntt8[0:16]: ", A_ntt8[0:16])
print("B_ntt8[0:16]: ", B_ntt8[0:16])
ntt_end_time = time.time()
print("NTT Time: ", ntt_end_time - ntt_start_time)
print("********** End NTT **********")
print("\n\r")

# -----------------------------------
print("********** Start Karatsuba **********")
kara_start_time = time.time()
# A_kara8 = Kara8(A_ntt8, q)
# B_kara8 = Kara8(B_ntt8, q)
A_kara8 = [0] * (3**8)
B_kara8 = [0] * (3**8)
for i in range(256):
    A_kara8[i*6561:(i+1)*6561] = Kara8(A_ntt8[i*256:(i+1)*256], q)
    B_kara8[i*6561:(i+1)*6561] = Kara8(B_ntt8[i*256:(i+1)*256], q)
    if (i%16 == 0):
        print("Kara_group_i: ", i)
print("A_kara8[0:16]: ", A_kara8[0:16])
print("B_kara8[0:16]: ", B_kara8[0:16])
kara_end_time = time.time()
print("Karatsuba Time: ", kara_end_time - kara_start_time)
print("********** End Karatsuba **********")
print("\n\r")

# -----------------------------------
print("********** Start Element-wise Mult **********")
ele_wise_start_time = time.time()
C_mult = [0] * int(6561*256)
for i in range(int(6561*256)):
    C_mult[i] = (A_kara8[i] * B_kara8[i]) % q
print("C_mult[0:16]: ", C_mult[0:16])
ele_wise_end_time = time.time()
print("Element-wise Multiplication Time: ", ele_wise_end_time - ele_wise_start_time)
print("********** End Element-wise Mult **********")
print("\n\r")

# -----------------------------------
print("********** Start Inv_Karatsuba **********")
ikara_start_time = time.time()
# C_ikara8 = Inv_Kara8(C_mult, q)
C_ikara8 = [0] * 256
for i in range(256):
    C_ikara8[i*256:(i+1)*256] = Inv_Kara8(C_mult[i*6561:(i+1)*6561], q)
    if (i%16 == 0):
        print("Inv_Kara_group_i: ", i)
print("C_ikara8[0:16]: ", C_ikara8[0:16])
ikara_end_time = time.time()
print("Inv_Karatsuba Time: ", ikara_end_time - ikara_start_time)
print("********** End Inv_Karatsuba **********")
print("\n\r")

# -----------------------------------
print("********** Start INTT **********")
intt_start_time = time.time()
C_intt8 = INTT8(C_ikara8, q, phi_inv, inv_2)
print("C_intt8[0:16]: ", C_intt8[0:16])
intt_end_time = time.time()
print("INTT Time: ", intt_end_time - intt_start_time)
print("********** End INTT **********")
print("\n\r")

# -----------------------------------
print("********** Start inv_Nega_conv **********")
inv_nega_conv_start_time = time.time()
C = [0] * N
for i in range(N):
    C[i] = (C_intt8[i] * ((psi_inv**i)%q)) % q
print("C[0:16]: ", C[0:16])
inv_nega_conv_end_time = time.time()
print("Inv_Nega_conv Time: ", inv_nega_conv_end_time - inv_nega_conv_start_time)
print("********** End inv_Nega_conv **********")
print("\n\r")

# -----------------------------------
print("********** Start Verification **********")
Base_temp = [0] * (2*N-1)
for i in range(N):
    for j in range(N):
        Base_temp[i+j] += A[i] * B[j] % q
        # Base_temp[i+j] %= q
Base = [0] * N
for i in range(N):
    Base[i] = Base_temp[i] % q
for i in range(N, 2*N-1):
    Base[i-N] = (Base[i-N] - Base_temp[i]) % q
print("Base[0:16]: ", Base[0:16])

if C == Base:
    print("Verification PASS! :) :) :) :) :)")
else:
    print("Verification FAIL! :( :( :( :( :(")
print("********** End Verification **********")
print("\n\r")

end_time = time.time()
print("end_time: ", end_time)
print("Execution Time: ", end_time - start_time)