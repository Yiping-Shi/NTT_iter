import math

# Parameter Definition
N       = 16
K       = 8
q       = 193
psi     = 8
psi_inv = 169
# w       = 64
w=1
w_inv   = 190

# NTT / INTT operation
A = list(range(N))

# -----------------------------------
# A_ntt = IterativeForwardNTT(A,q,w,R)
print("######## START NTT ########")
A_ntt = [0] * len(A)

for idx in range(N):
    A_ntt[idx] = A[idx]
    
v = int(math.log(N, 2))

for i in range(0, v):
    for j in range(0, (2 ** i)):
        for k in range(0, (2 ** (v - i - 1))):
            s = j * (2 ** (v - i)) + k
            t = s + (2 ** (v - i - 1))

            w_temp = (w ** ((2 ** i) * k)) % q

            as_temp = A_ntt[s]
            at_temp = A_ntt[t]

            A_ntt[s] = (as_temp + at_temp) % q
            A_ntt[t] = ((as_temp - at_temp) * w_temp) % q
    print("stage: ", i)
    print(A_ntt)

# -----------------------------------
# Bit-Reverse integer
def intReverse(a,n):
    b = ('{:0'+str(n)+'b}').format(a)
    return int(b[::-1],2)

# A_rev = indexReverse(A_ntt,int(log(N,2)))
A_rev = [0] * N
for i in range(N):
    rev_idx = intReverse(i, int(math.log(N,2)))
    A_rev[rev_idx] = A_ntt[i]
    
# -----------------------------------
# A_rec = IterativeInverseNTT(A_rev,q,w_inv,R)
A_rec = [0] * len(A_rev)

for idx in range(N):
    A_rec[idx] = A_rev[idx]

v = int(math.log(N, 2))

for i in range(0, v):
    for j in range(0, (2 ** i)):
        for k in range(0, (2 ** (v - i - 1))):
            s = j * (2 ** (v - i)) + k
            t = s + (2 ** (v - i - 1))

            w_temp = (w_inv ** ((2 ** i) * k)) % q

            as_temp = A_rec[s]
            at_temp = A_rec[t]

            A_rec[s] = (as_temp + at_temp) % q
            A_rec[t] = ((as_temp - at_temp) * w_temp) % q

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
    
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m
    
N_inv = modinv(N, q)
for i in range(N):
    A_rec[i] = (A_rec[i] * N_inv) % q
    
# -----------------------------------
# A_res = indexReverse(A_rec,int(log(N,2)))
A_res = [0] * N
for i in range(N):
    res_idx = intReverse(i, int(math.log(N,2)))
    A_res[res_idx] = A_rec[i]

# -----------------------------------
# Sanity Check
if sum([abs(x-y) for x,y in zip(A,A_res)]) == 0:
    print("Sanity Check: NTT operation is correct.")
else:
    print("Sanity Check: Check your math with NTT/INTT operation.")
    
print("A: ", A)
print("A_ntt: ", A_ntt)
print("A_rev: ", A_rev)
print("A_rec: ", A_rec)
print("A_res: ", A_res)