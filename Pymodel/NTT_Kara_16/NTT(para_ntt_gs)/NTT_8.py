import math
from NTT_helper import *

# Parameter Definition
N       = 8
K       = 8
q       = 241
psi     = 44
psi_inv = 126
w       = 8
w_inv   = 211


# -----------------------------------
print("********** Start Init **********")
A = list(range(N))
B = list(range(N))
print("A: ", A)
print("B: ", B)
print("********** End Init **********")

# -----------------------------------
print("********** Start NTT **********")
A_ntt = IterativeForwardNTT(A,q,w)
B_ntt = IterativeForwardNTT(B,q,w)
print("A_ntt: ", A_ntt)
print("B_ntt: ", B_ntt)
print("********** End NTT **********")

# -----------------------------------
print("********** Start BitReverse **********")
A_rev = indexReverse(A_ntt,int(math.log(N,2)))
B_rev = indexReverse(B_ntt,int(math.log(N,2)))
print("A_rev: ", A_rev)
print("B_rev: ", B_rev)
print("********** End BitReverse **********")
    
# -----------------------------------
print("********** Start INTT **********")
A_rec = IterativeInverseNTT(A_rev,q,w_inv)
B_rec = IterativeInverseNTT(B_rev,q,w_inv)
print("A_rec: ", A_rec)
print("B_rec: ", B_rec)
print("********** End INTT **********")
    
# -----------------------------------
print("********** Start BitReverse **********")
A_res = indexReverse(A_rec,int(math.log(N,2)))
B_res = indexReverse(B_rec,int(math.log(N,2)))
print("A_res: ", A_res)
print("B_res: ", B_res)
print("********** End BitReverse **********")
