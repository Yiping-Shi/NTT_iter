import time
import numpy as np
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

np.set_printoptions(linewidth=168)

start_time = time.time()
print("start_time: ", start_time)

# -----------------------------------
print("********** Start Init **********")
A = np.arange(N, dtype=np.int64)
B = np.arange(N, dtype=np.int64)
# A = np.random.randint(0, q, size=N, dtype=np.int64)
# B = np.random.randint(0, q, size=N, dtype=np.int64)
print("A[0:16]: ")
print(A[0:16])
print("B[0:16]: ")
print(B[0:16])
print("********** End Init **********")
print("\n\r")

# -----------------------------------
print("********** Start Nega_conv **********")
nega_conv_start_time = time.time()

indices = np.arange(N, dtype=np.int64)
# psi_powers = np.power(psi, indices, dtype=np.int64) % q
psi_powers = np.array([pow(psi, int(i), q) for i in indices], dtype=np.int64)

A_nega = (A * psi_powers) % q
B_nega = (B * psi_powers) % q
print("A_nega[0:16]: ")
print(A_nega[0:16])
print("B_nega[0:16]: ")
print(B_nega[0:16])

nega_conv_end_time = time.time()
print("Nega_conv Time: ", nega_conv_end_time - nega_conv_start_time)
print("********** End Nega_conv **********")
print("\n\r")


# -----------------------------------
print("********** Start NTT **********")
ntt_start_time = time.time()

A_ntt8 = NTT8(A_nega, q, phi)
B_ntt8 = NTT8(B_nega, q, phi)
print("A_ntt8[0:16]: ")
print(A_ntt8[0:16])
print("B_ntt8[0:16]: ")
print(B_ntt8[0:16])

ntt_end_time = time.time()
print("NTT Time: ", ntt_end_time - ntt_start_time)
print("********** End NTT **********")
print("\n\r")
# #### WRONG CMODEL ####
print("A_ntt8[240:256]: ")
print(A_ntt8[240:256])
print("A_ntt8[256:272]: ")
print(A_ntt8[256:272])

# -----------------------------------
print("********** Start Kara_Poly Kernel **********")
kara_start_time = time.time()

A_kara8   = np.zeros(6561, dtype=np.int64)
B_kara8   = np.zeros(6561, dtype=np.int64)
C_mult    = np.zeros(6561, dtype=np.int64)
C_block   = np.zeros(256, dtype=np.int64)
C_ikara8  = np.zeros(N, dtype=np.int64)

for i in range(256):
    A_block = A_ntt8[i*256:(i+1)*256]
    B_block = B_ntt8[i*256:(i+1)*256]
    
    # Karatsuba
    A_kara8 = Kara8(A_block, q)
    B_kara8 = Kara8(B_block, q)
    
    # Element-wise Multiplication
    C_mult = np.multiply(A_kara8, B_kara8) % q
    
    # Inverse Karatsuba
    C_block = Inv_Kara8(C_mult, q)
    
    C_ikara8[i*256:(i+1)*256] = C_block

print("C_ikara8[0:16]: ")
print(C_ikara8[0:16])

kara_end_time = time.time()
print("Karatsuba Time: ", kara_end_time - kara_start_time)
print("********** End Kara_Poly Kernel **********")
print("\n\r")

# -----------------------------------
print("********** Start Inv_NTT **********")
intt_start_time = time.time()

C_intt8 = Inv_NTT8(C_ikara8, q, phi_inv, inv_2)
print("C_intt8[0:16]: ")
print(C_intt8[0:16])

intt_end_time = time.time()
print("INTT Time: ", intt_end_time - intt_start_time)
print("********** End Inv_NTT **********")
print("\n\r")

# -----------------------------------
print("********** Start Inv_Nega_conv **********")
inv_nega_conv_start_time = time.time()

indices = np.arange(N, dtype=np.int64)
# psi_inv_powers = np.power(psi_inv, indices, dtype=np.int64) % q
psi_inv_powers = np.array([pow(psi_inv, int(i), q) for i in indices], dtype=np.int64)

C = (C_intt8 * psi_inv_powers) % q
print("C[0:16]: ")
print(C[0:16])

inv_nega_conv_end_time = time.time()
print("Inv_Nega_conv Time: ", inv_nega_conv_end_time - inv_nega_conv_start_time)
print("********** End Inv_Nega_conv **********")
print("\n\r")

# -----------------------------------
print("********** Start Verification **********")

Base_temp = np.zeros(2*N-1, dtype=np.int64)
for i in range(N):
    Base_temp[i:i+N] += (A[i]*B) % q
    # Base_temp[i+j] %= q
Base_temp %= q
Base = np.zeros(N, dtype=np.int64)
Base[:N] = Base_temp[:N]
Base[:N-1] -= Base_temp[N:]
Base %= q
print("Base[0:16]: ")
print(Base[0:16])

if np.array_equal(C, Base):
    print("Verification PASS! :) :) :) :) :)")
else:
    print("Verification FAIL! :( :( :( :( :(")
print("********** End Verification **********")
print("\n\r")

end_time = time.time()
print("end_time: ", end_time)
print("Execution Time: ", end_time - start_time)