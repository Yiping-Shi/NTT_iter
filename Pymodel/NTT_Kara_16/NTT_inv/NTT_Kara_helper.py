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

# NTT pre-stage
def NTT3_Kara1_pre_stage(arrayIn, q, phi):
    
    N = len(arrayIn)
    arrayOut = [0] * int(N*3/2)
    a0 = [0] * N
    a1 = [0] * N
    a2 = [0] * N
    a3 = [0] * int(N*3/2)
    
    v = int(math.log(N, 2))
    
    # Stage 0
    ### group 0: {0,8}, {1,9}, ..., {7,15}
    a0[0]  = (arrayIn[0] + arrayIn[8])  % q
    a0[1]  = (arrayIn[1] + arrayIn[9])  % q
    a0[2]  = (arrayIn[2] + arrayIn[10]) % q
    a0[3]  = (arrayIn[3] + arrayIn[11]) % q
    a0[4]  = (arrayIn[4] + arrayIn[12]) % q
    a0[5]  = (arrayIn[5] + arrayIn[13]) % q
    a0[6]  = (arrayIn[6] + arrayIn[14]) % q
    a0[7]  = (arrayIn[7] + arrayIn[15]) % q
    a0[8]  = (arrayIn[0] - arrayIn[8])  * (phi**0 % q) % q
    a0[9]  = (arrayIn[1] - arrayIn[9])  * (phi**1 % q) % q
    a0[10] = (arrayIn[2] - arrayIn[10]) * (phi**2 % q) % q
    a0[11] = (arrayIn[3] - arrayIn[11]) * (phi**3 % q) % q
    a0[12] = (arrayIn[4] - arrayIn[12]) * (phi**4 % q) % q
    a0[13] = (arrayIn[5] - arrayIn[13]) * (phi**5 % q) % q
    a0[14] = (arrayIn[6] - arrayIn[14]) * (phi**6 % q) % q
    a0[15] = (arrayIn[7] - arrayIn[15]) * (phi**7 % q) % q
    
    # Stage 1
    ### group 0: {0,4},  {1,5},  {2,6},   {3,7}
    ### group 1: {8,12}, {9,13}, {10,14}, {11,15}
    a1[0]  = (a0[0] + a0[4]) % q
    a1[1]  = (a0[1] + a0[5]) % q
    a1[2]  = (a0[2] + a0[6]) % q
    a1[3]  = (a0[3] + a0[7]) % q
    a1[4]  = (a0[0] - a0[4]) * (phi**0 % q) % q
    a1[5]  = (a0[1] - a0[5]) * (phi**2 % q) % q
    a1[6]  = (a0[2] - a0[6]) * (phi**4 % q) % q
    a1[7]  = (a0[3] - a0[7]) * (phi**6 % q) % q
    a1[8]  = (a0[8]  + a0[12]) % q
    a1[9]  = (a0[9]  + a0[13]) % q
    a1[10] = (a0[10] + a0[14]) % q
    a1[11] = (a0[11] + a0[15]) % q
    a1[12] = (a0[8]  - a0[12]) * (phi**0 % q) % q
    a1[13] = (a0[9]  - a0[13]) * (phi**2 % q) % q
    a1[14] = (a0[10] - a0[14]) * (phi**4 % q) % q
    a1[15] = (a0[11] - a0[15]) * (phi**6 % q) % q
    
    # Stage 2
    ### group 0: {0,2},   {1,3}
    ### group 1: {4,6},   {5,7}
    ### group 2: {8,10},  {9,11}
    ### group 3: {12,14}, {13,15}
    a2[0]  = (a1[0]  + a1[2]) % q
    a2[1]  = (a1[1]  + a1[3]) % q
    a2[2]  = (a1[0]  - a1[2]) * (phi**0 % q) % q
    a2[3]  = (a1[1]  - a1[3]) * (phi**4 % q) % q
    a2[4]  = (a1[4]  + a1[6]) % q
    a2[5]  = (a1[5]  + a1[7]) % q
    a2[6]  = (a1[4]  - a1[6]) * (phi**0 % q) % q
    a2[7]  = (a1[5]  - a1[7]) * (phi**4 % q) % q
    a2[8]  = (a1[8]  + a1[10]) % q
    a2[9]  = (a1[9]  + a1[11]) % q
    a2[10] = (a1[8]  - a1[10]) * (phi**0 % q) % q
    a2[11] = (a1[9]  - a1[11]) * (phi**4 % q) % q
    a2[12] = (a1[12] + a1[14]) % q
    a2[13] = (a1[13] + a1[15]) % q
    a2[14] = (a1[12] - a1[14]) * (phi**0 % q) % q
    a2[15] = (a1[13] - a1[15]) * (phi**4 % q) % q
    
    # Stage 3
    ### group 0: {0,1}
    ### group 1: {2,3}
    ### ...
    ### group 7: {14,15}
    a3[0]  = a2[0]
    a3[1]  = (a2[0] + a2[1]) % q
    a3[2]  = a2[1]
    a3[3]  = a2[2]
    a3[4]  = (a2[2] + a2[3]) % q
    a3[5]  = a2[3]
    a3[6]  = a2[4]
    a3[7]  = (a2[4] + a2[5]) % q
    a3[8]  = a2[5]
    a3[9]  = a2[6]
    a3[10] = (a2[6] + a2[7]) % q
    a3[11] = a2[7]
    a3[12] = a2[8]
    a3[13] = (a2[8] + a2[9]) % q
    a3[14] = a2[9]
    a3[15] = a2[10]
    a3[16] = (a2[10] + a2[11]) % q
    a3[17] = a2[11]
    a3[18] = a2[12]
    a3[19] = (a2[12] + a2[13]) % q
    a3[20] = a2[13]
    a3[21] = a2[14]
    a3[22] = (a2[14] + a2[15]) % q
    a3[23] = a2[15]
    
    for idx in range(int(N*3/2)):
        arrayOut[idx] = a3[idx]
    
    print("stage 0: ", a0)
    print("stage 1: ", a1)
    print("stage 2: ", a2)
    print("stage 3: ", a3)
    
    return arrayOut

def Kara1_INTT3_pre_stage(arrayIn, q, phi_inv, inv_2):
    N = int(len(arrayIn)*2/3)
    arrayOut = [0] * N
    a0_temp = [0] * int(N*3/2)
    a0 = [0] * N
    a1 = [0] * N
    a2 = [0] * N
    a3 = [0] * N
    
    v = int(math.log(N, 2))
    print("arrayIn: ", arrayIn)
    
    # stage 0
    ### group 0: {0,1}
    ### group 1: {2,3}
    ### ...
    ### group 7: {14,15}
    a0_temp[0] = arrayIn[0]
    a0_temp[1] = (arrayIn[1] - arrayIn[0] - arrayIn[2]) % q
    a0_temp[2] = arrayIn[2]
    a0_temp[3] = arrayIn[3]
    a0_temp[4] = (arrayIn[4] - arrayIn[3] - arrayIn[5]) % q
    a0_temp[5] = arrayIn[5]
    a0_temp[6] = arrayIn[6]
    a0_temp[7] = (arrayIn[7] - arrayIn[6] - arrayIn[8]) % q
    a0_temp[8] = arrayIn[8]
    a0_temp[9] = arrayIn[9]
    a0_temp[10] = (arrayIn[10] - arrayIn[9] - arrayIn[11]) % q
    a0_temp[11] = arrayIn[11]
    a0_temp[12] = arrayIn[12]
    a0_temp[13] = (arrayIn[13] - arrayIn[12] - arrayIn[14]) % q
    a0_temp[14] = arrayIn[14]
    a0_temp[15] = arrayIn[15]
    a0_temp[16] = (arrayIn[16] - arrayIn[15] - arrayIn[17]) % q
    a0_temp[17] = arrayIn[17]
    a0_temp[18] = arrayIn[18]
    a0_temp[19] = (arrayIn[19] - arrayIn[18] - arrayIn[20]) % q
    a0_temp[20] = arrayIn[20]
    a0_temp[21] = arrayIn[21]
    a0_temp[22] = (arrayIn[22] - arrayIn[21] - arrayIn[23]) % q
    a0_temp[23] = arrayIn[23]
    print("a0_temp: ", a0_temp)
    
    a0[0]  = (a0_temp[0] + a0_temp[2]) % q
    a0[1]  = a0_temp[1]
    a0[2]  = (a0_temp[3] + a0_temp[5]) % q
    a0[3]  = a0_temp[4]
    a0[4]  = (a0_temp[6] + a0_temp[8]) % q
    a0[5]  = a0_temp[7]
    a0[6]  = (a0_temp[9] + a0_temp[11]) % q
    a0[7]  = a0_temp[10]
    a0[8]  = (a0_temp[12] + a0_temp[14]) % q
    a0[9]  = a0_temp[13]
    a0[10] = (a0_temp[15] + a0_temp[17]) % q
    a0[11] = a0_temp[16]
    a0[12] = (a0_temp[18] + a0_temp[20]) % q
    a0[13] = a0_temp[19]
    a0[14] = (a0_temp[21] + a0_temp[23]) % q
    a0[15] = a0_temp[22]   
    
    print("a0: ", a0)
    
    # stage 1
    ### group 0: {0,2},   {1,3}
    ### group 1: {4,6},   {5,7}
    ### group 2: {8,10},  {9,11}
    ### group 3: {12,14}, {13,15}
    a1[0]  = (a0[0] + (a0[2] * (phi_inv**0 % q))) % q
    a1[1]  = (a0[1] + (a0[3] * (phi_inv**4 % q))) % q
    a1[2]  = (a0[0] - (a0[2] * (phi_inv**0 % q))) % q
    a1[3]  = (a0[1] - (a0[3] * (phi_inv**4 % q))) % q
    a1[4]  = (a0[4] + (a0[6] * (phi_inv**0 % q))) % q
    a1[5]  = (a0[5] + (a0[7] * (phi_inv**4 % q))) % q
    a1[6]  = (a0[4] - (a0[6] * (phi_inv**0 % q))) % q
    a1[7]  = (a0[5] - (a0[7] * (phi_inv**4 % q))) % q
    a1[8]  = (a0[8] + (a0[10] * (phi_inv**0 % q))) % q
    a1[9]  = (a0[9] + (a0[11] * (phi_inv**4 % q))) % q
    a1[10] = (a0[8] - (a0[10] * (phi_inv**0 % q))) % q
    a1[11] = (a0[9] - (a0[11] * (phi_inv**4 % q))) % q
    a1[12] = (a0[12] + (a0[14] * (phi_inv**0 % q))) % q
    a1[13] = (a0[13] + (a0[15] * (phi_inv**4 % q))) % q
    a1[14] = (a0[12] - (a0[14] * (phi_inv**0 % q))) % q
    a1[15] = (a0[13] - (a0[15] * (phi_inv**4 % q))) % q
    for i in range(N):
        a1[i] = (a1[i] * inv_2) % q
    print("a1: ", a1)
    
    # stage 2
    ### group 0: {0,4},  {1,5},  {2,6},   {3,7}
    ### group 1: {8,12}, {9,13}, {10,14}, {11,15}
    a2[0]  = (a1[0] + (a1[4] * (phi_inv**0 % q))) % q
    a2[1]  = (a1[1] + (a1[5] * (phi_inv**2 % q))) % q
    a2[2]  = (a1[2] + (a1[6] * (phi_inv**4 % q))) % q
    a2[3]  = (a1[3] + (a1[7] * (phi_inv**6 % q))) % q
    a2[4]  = (a1[0] - (a1[4] * (phi_inv**0 % q))) % q
    a2[5]  = (a1[1] - (a1[5] * (phi_inv**2 % q))) % q
    a2[6]  = (a1[2] - (a1[6] * (phi_inv**4 % q))) % q
    a2[7]  = (a1[3] - (a1[7] * (phi_inv**6 % q))) % q
    a2[8]  = (a1[8]  + (a1[12] * (phi_inv**0 % q))) % q
    a2[9]  = (a1[9]  + (a1[13] * (phi_inv**2 % q))) % q
    a2[10] = (a1[10] + (a1[14] * (phi_inv**4 % q))) % q
    a2[11] = (a1[11] + (a1[15] * (phi_inv**6 % q))) % q
    a2[12] = (a1[8]  - (a1[12] * (phi_inv**0 % q))) % q
    a2[13] = (a1[9]  - (a1[13] * (phi_inv**2 % q))) % q
    a2[14] = (a1[10] - (a1[14] * (phi_inv**4 % q))) % q
    a2[15] = (a1[11] - (a1[15] * (phi_inv**6 % q))) % q
    for i in range(N):
        a2[i] = (a2[i] * inv_2) % q
    print("a2: ", a2)
    
    # stage 3
    ### group 0: {0,8}, {1,9}, ..., {7,15}
    a3[0]  = (a2[0] + (a2[8]  * (phi_inv**0 % q))) % q
    a3[1]  = (a2[1] + (a2[9]  * (phi_inv**1 % q))) % q
    a3[2]  = (a2[2] + (a2[10] * (phi_inv**2 % q))) % q
    a3[3]  = (a2[3] + (a2[11] * (phi_inv**3 % q))) % q
    a3[4]  = (a2[4] + (a2[12] * (phi_inv**4 % q))) % q
    a3[5]  = (a2[5] + (a2[13] * (phi_inv**5 % q))) % q
    a3[6]  = (a2[6] + (a2[14] * (phi_inv**6 % q))) % q
    a3[7]  = (a2[7] + (a2[15] * (phi_inv**7 % q))) % q
    a3[8]  = (a2[0] - (a2[8]  * (phi_inv**0 % q))) % q
    a3[9]  = (a2[1] - (a2[9]  * (phi_inv**1 % q))) % q
    a3[10] = (a2[2] - (a2[10] * (phi_inv**2 % q))) % q
    a3[11] = (a2[3] - (a2[11] * (phi_inv**3 % q))) % q
    a3[12] = (a2[4] - (a2[12] * (phi_inv**4 % q))) % q
    a3[13] = (a2[5] - (a2[13] * (phi_inv**5 % q))) % q
    a3[14] = (a2[6] - (a2[14] * (phi_inv**6 % q))) % q
    a3[15] = (a2[7] - (a2[15] * (phi_inv**7 % q))) % q
    for i in range(N):
        a3[i] = (a3[i] * inv_2) % q
    print("a3: ", a3)
    
    for idx in range(N):
        arrayOut[idx] = a3[idx]
    
    return arrayOut