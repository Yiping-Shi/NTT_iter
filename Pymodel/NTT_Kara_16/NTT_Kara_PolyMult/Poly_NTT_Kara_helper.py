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
        # print("arrayOut: ", arrayOut)
    
    return arrayOut


def ntt_ct_std2rev_stage_1(arrayIn, N, phi, q):
    k_values = [0,0,0,4, 0,4,2,6, 0,4,2,6, 1,5,3,7]
    p = [pow(phi, k, q) for k in k_values]
    p[0] = 0
    
    arrayOut = [0] * N
    for i in range(N):
        arrayOut[i] = arrayIn[i]
    
    t = 1 << 0
    d = N >> 1
    for s in range(d):
        x = arrayOut[s+d]
        arrayOut[s+d] = (arrayOut[s] - x) % q
        arrayOut[s] = (arrayOut[s] + x) % q
    
    return arrayOut

def ntt_ct_std2rev_stage_2(arrayIn, N, phi, q):
    k_values = [0,0,0,4, 0,4,2,6, 0,4,2,6, 1,5,3,7]
    p = [pow(phi, k, q) for k in k_values]
    p[0] = 0
    
    arrayOut = [0] * N
    for i in range(N):
        arrayOut[i] = arrayIn[i]
    
    t = 1 << 1
    d = N >> 2
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
    
    return arrayOut

def ntt_ct_std2rev_stage_3(arrayIn, N, phi, q):
    k_values = [0,0,0,4, 0,4,2,6, 0,4,2,6, 1,5,3,7]
    p = [pow(phi, k, q) for k in k_values]
    p[0] = 0
    
    arrayOut = [0] * N
    for i in range(N):
        arrayOut[i] = arrayIn[i]
    
    t = 1 << 2
    d = N >> 3
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
    
    return arrayOut

def ntt_ct_std2rev_stage_4(arrayIn, N, phi, q):
    k_values = [0,0,0,4, 0,4,2,6, 0,4,2,6, 1,5,3,7]
    p = [pow(phi, k, q) for k in k_values]
    p[0] = 0
    
    arrayOut = [0] * N
    for i in range(N):
        arrayOut[i] = arrayIn[i]
    
    t = 1 << 3
    d = N >> 4
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
    
    return arrayOut