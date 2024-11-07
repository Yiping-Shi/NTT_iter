import math

# Modular inverse (https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python)
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

# Bit-Reverse integer
def intReverse(a,n):
    b = ('{:0'+str(n)+'b}').format(a)
    return int(b[::-1],2)

# Bit-Reversed index
def indexReverse(a,r):
    n = len(a)
    b = [0]*n
    for i in range(n):
        rev_idx = intReverse(i,r)
        b[rev_idx] = a[i]
    return b

# forward ntt (takes input in normal order, produces output in bit-reversed order)
def IterativeForwardNTT(arrayIn, P, W):

    arrayOut = [0] * len(arrayIn)
    N = len(arrayIn)

    for idx in range(N):
        arrayOut[idx] = arrayIn[idx]

    v = int(math.log(N, 2))

    for i in range(0, v):
        for j in range(0, (2 ** i)):
            for k in range(0, (2 ** (v - i - 1))):
                s = j * (2 ** (v - i)) + k
                t = s + (2 ** (v - i - 1))

                w = (W ** ((2 ** i) * k)) % P

                as_temp = arrayOut[s]
                at_temp = arrayOut[t]

                arrayOut[s] = (as_temp + at_temp) % P
                arrayOut[t] = ((as_temp - at_temp) * w) % P

    return arrayOut

# inverse ntt (takes input in normal order, produces output in bit-reversed order)
def IterativeInverseNTT(arrayIn, P, W):

    arrayOut = [0] * len(arrayIn)
    N = len(arrayIn)

    for idx in range(N):
        arrayOut[idx] = arrayIn[idx]

    v = int(math.log(N, 2))

    for i in range(0, v):
        for j in range(0, (2 ** i)):
            for k in range(0, (2 ** (v - i - 1))):
                s = j * (2 ** (v - i)) + k
                t = s + (2 ** (v - i - 1))

                w = (W ** ((2 ** i) * k)) % P

                as_temp = arrayOut[s]
                at_temp = arrayOut[t]

                arrayOut[s] = (as_temp + at_temp) % P
                arrayOut[t] = ((as_temp - at_temp) * w) % P

    N_inv = modinv(N, P)
    for i in range(N):
        arrayOut[i] = (arrayOut[i] * N_inv) % P

    return arrayOut
