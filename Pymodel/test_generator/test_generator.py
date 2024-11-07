
# Copyright 2020
# Ahmet Can Mert <ahmetcanmert@sabanciuniv.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from math import log,ceil
from random import randint

from generate_prime import *
from helper import *

# Test Generator for N-pt NTT/INTT with P Processing Element

# -------------------------------------------------------------------------- TXT
PRM_TXT       = open("D:/FHE/IDEA/NTT_iter/Pymodel/test_generator/test/PARAM.txt","w")
NTT_DIN_TXT   = open("D:/FHE/IDEA/NTT_iter/Pymodel/test_generator/test/NTT_DIN.txt","w")
NTT_DOUT_TXT  = open("D:/FHE/IDEA/NTT_iter/Pymodel/test_generator/test/NTT_DOUT.txt","w")
INTT_DIN_TXT  = open("D:/FHE/IDEA/NTT_iter/Pymodel/test_generator/test/INTT_DIN.txt","w")
INTT_DOUT_TXT = open("D:/FHE/IDEA/NTT_iter/Pymodel/test_generator/test/INTT_DOUT.txt","w")
W_TXT         = open("D:/FHE/IDEA/NTT_iter/Pymodel/test_generator/test/W.txt","w")
WINV_TXT      = open("D:/FHE/IDEA/NTT_iter/Pymodel/test_generator/test/WINV.txt","w")
# -------------------------------------------------------------------------- TXT

# Pre-defined parameter set
PC = 0 # 0: generate parameters / 1: use pre-defined parameter set

# Number of Processing Elements
P = 1

# Generate parameters
q       = 0
psi     = 0
psi_inv = 0
w       = 0
w_inv   = 0
n_inv   = 0

if PC:
    N, K, q, psi = 1024, 19, 520193, 98

    psi_inv = modinv(psi,q)
    w       = pow(psi,2,q)
    w_inv   = modinv(w,q)

    R       = 2**((int(log(N,2))+1) * int(ceil((1.0*K)/(1.0*((int(log(N,2))+1))))))
    n_inv   = modinv(N,q)
    PE      = P*2
else:
    # Input parameters
    # N, K = 16, 8
    N, K = 8, 8
    # -----------------------
    # N      : 16
    # K      : 8
    # PE     : 1
    # q      : 193
    # psi    : 8
    # psi_inv: 169
    # w      : 64
    # w_inv  : 190
    # n_inv  : 181
    # log(R) : 10
    # -----------------------
    while(1):
        q = generate_large_prime(K)
        # check q = 1 (mod 2n or n)
        while (not ((q % (2*N)) == 1)):
            q = generate_large_prime(K)

        # generate NTT parameters
        for i in range(2,q-1):
            if pow(i,2*N,q) == 1:
                if pow(i,N,q) == (q-1):
                    pru = [i**x % q for x in range(1,2*N)]
                    if not(1 in pru):
                        psi     = i
                        psi_inv = modinv(i,q)
                        w       = pow(psi,2,q)
                        w_inv   = modinv(w,q)
                        break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            continue
        break

    # q       = 193
    # psi     = 8
    # psi_inv = 169
    # w       = 64
    # w_inv   = 190
    # # n_inv   = 181
    
    R     = 2**((int(log(N,2))+1) * int(ceil((1.0*K)/(1.0*((int(log(N,2))+1))))))
    n_inv = modinv(N,q)
    PE    = P*2
    

# Print parameters
print("-----------------------")
print("N      : {}".format(N))
print("K      : {}".format(K))
print("PE     : {}".format(P))
print("q      : {}".format(q))
print("psi    : {}".format(psi))
print("psi_inv: {}".format(psi_inv))
print("w      : {}".format(w))
print("w_inv  : {}".format(w_inv))
print("n_inv  : {}".format(n_inv))
print("log(R) : {}".format(int(log(R,2))))
print("-----------------------")

# --------------------------------------------------------------------------

PRM_TXT.write(hex(N          ).replace("L","")[2:].ljust(20)+"\n")
PRM_TXT.write(hex(q          ).replace("L","")[2:].ljust(20)+"\n")
PRM_TXT.write(hex(w          ).replace("L","")[2:].ljust(20)+"\n")
PRM_TXT.write(hex(w_inv      ).replace("L","")[2:].ljust(20)+"\n")
PRM_TXT.write(hex(psi        ).replace("L","")[2:].ljust(20)+"\n")
PRM_TXT.write(hex(psi_inv    ).replace("L","")[2:].ljust(20)+"\n")
PRM_TXT.write(hex((n_inv*R)%q).replace("L","")[2:].ljust(20)+"\n")
PRM_TXT.write(hex(R          ).replace("L","")[2:].ljust(20)+"\n")

PRM_TXT.write("// Input order:\n")

PRM_TXT.write("// N\n")
PRM_TXT.write("// q\n")
PRM_TXT.write("// w\n")
PRM_TXT.write("// w_inv\n")
PRM_TXT.write("// psi\n")
PRM_TXT.write("// psi_inv\n")
PRM_TXT.write("// n_inv\n")
PRM_TXT.write("// R\n")
PRM_TXT.write("// \n")
PRM_TXT.write("// K :"+str(K)+"\n")
PRM_TXT.write("// PE:"+str(P)+"\n")

# --------------------------------------------------------------------------

# NTT/INTT operation
# A = [randint(0,q-1) for _ in range(N)]
A = list(range(N))

A_ntt = IterativeForwardNTT(A,q,w,R)
A_rev = indexReverse(A_ntt,int(log(N,2)))
A_rec = IterativeInverseNTT(A_rev,q,w_inv,R)
A_res = indexReverse(A_rec,int(log(N,2)))

# Sanity Check
if sum([abs(x-y) for x,y in zip(A,A_res)]) == 0:
    print("Sanity Check: NTT operation is correct.")
else:
    print("Sanity Check: Check your math with NTT/INTT operation.")

# Print input/output to txt (normal input - bit-reversed output)
for i in range(N):
    NTT_DIN_TXT.write(hex(A[i]).replace("L","")[2:]+"\n")
    NTT_DOUT_TXT.write(hex(A_ntt[i]).replace("L","")[2:]+"\n")

for i in range(N):
    INTT_DIN_TXT.write(hex(A_rev[i]).replace("L","")[2:]+"\n")
    INTT_DOUT_TXT.write(hex(A_rec[i]).replace("L","")[2:]+"\n")

# Print TWs to txt
for j in range(int(log(N, 2))):
    for k in range(1 if (((N//PE)>>j) < 1) else ((N//PE)>>j)):
        for i in range(P):
            w_pow = (((P<<j)*k + (i<<j)) % (N//2))
            W_TXT.write(hex(((w**w_pow % q) * R) % q).replace("L","")[2:]+"\n")
            WINV_TXT.write(hex(((w_inv**w_pow % q) * R) % q).replace("L","")[2:]+"\n")

# --------------------------------------------------------------------------
