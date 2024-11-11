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

def intt_ct_rev2std_stage_1(arrayIn, N, phi_inv, q):
    k_values = [0,0,0,4, 0,2,4,6, 0,1,2,3, 4,5,6,7]
    p = [pow(phi_inv, k, q) for k in k_values]
    p[0] = 0
    
    arrayOut = [0] * N
    for i in range(N):
        arrayOut[i] = arrayIn[i]
    
    t = 1 << 0
    # First loop: j = 0, w_t^j = 1
    for s in range(0, N, t*2):
        x = arrayOut[s + t]
        arrayOut[s + t] = (arrayOut[s] - x) % q
        arrayOut[s] = (arrayOut[s] + x) % q
        
    # General case: j > 0
    for j in range(1, t):
        w = p[t + j]  # w_t^j
        for s in range(j, N, t*2):
            x = arrayOut[s + t] * w
            arrayOut[s + t] = (arrayOut[s] - x) % q
            arrayOut[s] = (arrayOut[s] + x) % q
    
    return arrayOut

def intt_ct_rev2std_stage_2(arrayIn, N, phi_inv, q):
    k_values = [0,0,0,4, 0,2,4,6, 0,1,2,3, 4,5,6,7]
    p = [pow(phi_inv, k, q) for k in k_values]
    p[0] = 0
    
    arrayOut = [0] * N
    for i in range(N):
        arrayOut[i] = arrayIn[i]
    
    t = 1 << 1
    # First loop: j = 0, w_t^j = 1
    for s in range(0, N, t*2):
        x = arrayOut[s + t]
        arrayOut[s + t] = (arrayOut[s] - x) % q
        arrayOut[s] = (arrayOut[s] + x) % q
        
    # General case: j > 0
    for j in range(1, t):
        w = p[t + j]  # w_t^j
        for s in range(j, N, t*2):
            x = arrayOut[s + t] * w
            arrayOut[s + t] = (arrayOut[s] - x) % q
            arrayOut[s] = (arrayOut[s] + x) % q
    
    return arrayOut

def intt_ct_rev2std_stage_3(arrayIn, N, phi_inv, q):
    k_values = [0,0,0,4, 0,2,4,6, 0,1,2,3, 4,5,6,7]
    p = [pow(phi_inv, k, q) for k in k_values]
    p[0] = 0
    
    arrayOut = [0] * N
    for i in range(N):
        arrayOut[i] = arrayIn[i]
    
    t = 1 << 2
    # First loop: j = 0, w_t^j = 1
    for s in range(0, N, t*2):
        x = arrayOut[s + t]
        arrayOut[s + t] = (arrayOut[s] - x) % q
        arrayOut[s] = (arrayOut[s] + x) % q
        
    # General case: j > 0
    for j in range(1, t):
        w = p[t + j]  # w_t^j
        for s in range(j, N, t*2):
            x = arrayOut[s + t] * w
            arrayOut[s + t] = (arrayOut[s] - x) % q
            arrayOut[s] = (arrayOut[s] + x) % q
    
    return arrayOut

def intt_ct_rev2std_stage_4(arrayIn, N, phi_inv, q):
    k_values = [0,0,0,4, 0,2,4,6, 0,1,2,3, 4,5,6,7]
    p = [pow(phi_inv, k, q) for k in k_values]
    p[0] = 0
    
    arrayOut = [0] * N
    for i in range(N):
        arrayOut[i] = arrayIn[i]
    
    t = 1 << 3
    # First loop: j = 0, w_t^j = 1
    for s in range(0, N, t*2):
        x = arrayOut[s + t]
        arrayOut[s + t] = (arrayOut[s] - x) % q
        arrayOut[s] = (arrayOut[s] + x) % q
        
    # General case: j > 0
    for j in range(1, t):
        w = p[t + j]  # w_t^j
        for s in range(j, N, t*2):
            x = arrayOut[s + t] * w
            arrayOut[s + t] = (arrayOut[s] - x) % q
            arrayOut[s] = (arrayOut[s] + x) % q
    
    return arrayOut

def karatsuba_preprocess(arrayIn, N, q):
    N_half = int(N/2)
    N23 = int(N*3/2)
    arrayOut = [0] * (N23)
    
    for i in range(N_half):
        arrayOut[i*3] = arrayIn[i*2]
        arrayOut[i*3+1] = (arrayIn[i*2] + arrayIn[i*2+1]) % q
        arrayOut[i*3+2] = arrayIn[i*2+1]
    
    return arrayOut

def karatsuba_postprocess(arrayIn, N, q):
    N_half = int(N/2)
    N23 = int(N*3/2)
    temp = [0] * N23
    arrayOut = [0] * N
    
    for i in range(N_half):
        temp[i*3] = arrayIn[i*3]
        temp[i*3+1] = (arrayIn[i*3+1] - arrayIn[i*3] - arrayIn[i*3+2]) % q
        temp[i*3+2] = arrayIn[i*3+2]

    for i in range(N_half):
        arrayOut[i*2] = (temp[i*3] - temp[i*3+2]) % q
        arrayOut[i*2+1] = temp[i*3+1]
    
    return arrayOut