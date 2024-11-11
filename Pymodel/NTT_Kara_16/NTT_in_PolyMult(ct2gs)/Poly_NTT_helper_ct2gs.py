import math

def nega_conv_mul_array(arrayIn, N, psi, q):
    """
    Negacyclic convolution multiplication of arrayIn with psi_array
    Perform in-place product: arrayIn[i] = arrayIn[i] * psi_array[i] % q

    :param arrayIn: list of int32 elements
    :param N: length of list arrayIn
    :param psi: base value for power calculation
    :param q: modulus
    """
    arrayOut  = [0] * N
    psi_array = [pow(psi,i,q) for i in range(N)]
    
    for i in range(N):
        arrayOut[i] = (arrayIn[i] * psi_array[i]) % q
        
    return arrayOut


def ntt_ct_std2rev(arrayIn, N, phi, q):
    """
    - input: arrayIn[0 ... n-1] in standard order
    - phi: base value for power calculation to generate p array
      p array elements are calculated as p[k] = pow(phi, k, q), where
      k = [-, 0, 0, 4, 0, 4, 2, 6, 0, 4, 2, 6, 1, 5, 3, 7]
    
    - output: NTT(arrayIn) in bit-reverse order

    :param arrayIn: list of int32 elements (input array)
    :param N: length of input array arrayIn
    :param phi: base value for power calculation
    :param q: modulus
    """
    k_values = [0,0,0,4, 0,4,2,6, 0,4,2,6, 1,5,3,7]
    p = [pow(phi, k, q) for k in k_values]
    p[0] = 0
    
    arrayOut = [0] * N
    for i in range(N):
        arrayOut[i] = arrayIn[i]
    
    d = N
    t = 1
    while t < N:
        d >>= 1
        # First loop: j=0, bitrev(j)=0
        for s in range(d):
            x = arrayOut[s+d]
            arrayOut[s+d] = (arrayOut[s] - x) % q
            arrayOut[s] = (arrayOut[s] + x) % q
        u = 0
        for j in range(1,t):
            w = p[t+j]  # w_t^bitrev(j)
            u += 2*d    # u = 2*d*j
            for s in range(u,u+d):
                x = arrayOut[s+d] * w
                arrayOut[s+d] = (arrayOut[s] - x) % q
                arrayOut[s] = (arrayOut[s] + x) % q
        t <<= 1
        print("stage: ", math.log2(t))
        print("arrayOut: ", arrayOut)
    
    return arrayOut
       
        
def mul_array_elementwise(A_ntt, B_ntt, N, q):
    """
    Element-wise multiplication of two arrays A_ntt and B_ntt, modulo q.
    
    :param A_ntt: list of int32 elements (first input array)
    :param B_ntt: list of int32 elements (second input array)
    :param N: length of input arrays A_ntt and B_ntt
    :param q: modulus
    
    :return: list of int32 elements (resulting array C_ntt)
    """
    C_ntt = [0] * N
    C_ntt = [(A_ntt[i] * B_ntt[i]) % q for i in range(N)]
    return C_ntt


def intt_gs_rev2std(arrayIn, N, phi_inv, q):
    """
    - input: arrayIn[0 ... n-1] in bit-reverse order
    - phi-inv: base value for power calculation to generate p array
      p array elements are calculated as p[k] = pow(phi_inv, k, q), where
      k = [-, 0, 0, 4, 0, 4, 2, 6, 0, 4, 2, 6, 1, 5, 3, 7]
    
    - output: INTT(arrayIn) in standard order

    :param arrayIn: list of int32 elements (input array)
    :param N: length of input array arrayIn
    :param phi-inv: base value for power calculation
    :param q: modulus
    """
    k_values = [0,0,0,4, 0,4,2,6, 0,4,2,6, 1,5,3,7]
    p = [pow(phi_inv, k, q) for k in k_values]
    p[0] = 0
    
    arrayOut = [0] * N
    for i in range(N):
        arrayOut[i] = arrayIn[i]
    
    d = 1
    t = N
    while d < N:
        t >>= 1
        # First loop: j=0, bitrev(j)=0
        for s in range(d):
            x = arrayOut[s+d]
            arrayOut[s+d] = (arrayOut[s] - x) % q
            arrayOut[s] = (arrayOut[s] + x) % q
        u = 0
        for j in range(1,t):
            w = p[t+j]
            u += 2*d
            for s in range(u,u+d):
                x = arrayOut[s+d]
                arrayOut[s+d] = ((arrayOut[s] - x) * w) % q
                arrayOut[s] = (arrayOut[s] + x) % q
        d <<= 1
        print("stage: ", math.log2(d))
        print("arrayOut: ", arrayOut)
    
    # v = int(math.log(N, 2))
    # for i in range(0, v):
    #     for j in range(0, (2 ** i)):
    #         for k in range(0, (2 ** (v - i - 1))):
    #             s = j * (2 ** (v - i)) + k
    #             t = s + (2 ** (v - i - 1))
                
    #             w = (phi_inv ** ((2 ** i) * k)) % q
                
    #             as_temp = arrayOut[s]
    #             at_temp = arrayOut[t]
                
    #             arrayOut[s] = (as_temp + at_temp) % q
    #             arrayOut[t] = ((as_temp - at_temp) * w) % q
    #     print("stage: ", i)
    #     print("arrayOut: ", arrayOut)
        
    return arrayOut

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