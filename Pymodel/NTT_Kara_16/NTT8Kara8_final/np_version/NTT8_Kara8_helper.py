import numpy as np

def NTT8(arrayIn, q, phi):
    N = len(arrayIn)
    arrayOut = arrayIn.copy()
    
    for k in range(8):
        for j in range((1<<k)):
            for i in range((N>>(k+1))):
                phi_temp = pow(phi, (1<<k)*i, q)
                add_temp = arrayOut[i+j*(N>>k)] + arrayOut[i+j*(N>>k)+(N>>(k+1))]
                sub_temp = (arrayOut[i+j*(N>>k)] - arrayOut[i+j*(N>>k)+(N>>(k+1))]) * phi_temp
                            
                arrayOut[i+j*(N>>k)]            = (add_temp % q)
                arrayOut[i+j*(N>>k)+(N>>(k+1))] = (sub_temp % q)
    
    return arrayOut

def Inv_NTT8(arrayIn, q, phi_inv, inv_2):
    N = len(arrayIn)
    arrayOut = arrayIn.copy()
    
    for k in range(8):
        for j in range(128>>k):
            for i in range(256<<k):
                phi_temp = pow(phi_inv, (128>>k)*i, q)
                mul_temp = arrayOut[i+j*(512<<k)+(256<<k)] * phi_temp % q
                add_temp = arrayOut[i+j*(512<<k)] + mul_temp
                sub_temp = arrayOut[i+j*(512<<k)] - mul_temp
                
                arrayOut[i+j*(512<<k)]            = add_temp % q
                arrayOut[i+j*(512<<k)+(256<<k)]   = sub_temp % q
        for i in range(N):
            arrayOut[i] = (arrayOut[i] * inv_2) % q
    
    return arrayOut

# def INTT8(arrayIn, q, phi_inv, inv_2):
#     N = len(arrayIn)
#     arrayOut = [0] * N
#     a0 = [0] * N
#     a1 = [0] * N
#     a2 = [0] * N
#     a3 = [0] * N
#     a4 = [0] * N
#     a5 = [0] * N
#     a6 = [0] * N
#     a7 = [0] * N
    
#     # Stage 0
#     ### group 0: {0,256},      {1,257},      ..., {255,511}
#     ### group 1: {512,768},    {513,769},    ..., {767,1023}
#     ### ...
#     ### group 127: {57344,57600}, {57345,57601}, ..., {57600,57855}
#     print("INTT-STAGE-0")
#     for j in range(128):
#         for i in range(256):
#             a0[i+j*512]     = (arrayIn[i+j*512] + (arrayIn[i+j*512+256] * (phi_inv**(128*i) % q))) % q
#             a0[i+j*512+256] = (arrayIn[i+j*512] - (arrayIn[i+j*512+256] * (phi_inv**(128*i) % q))) % q
#     for i in range(N):
#         a0[i] = (a0[i] * inv_2) % q
    
#     # Stage 1
#     ### group 0: {0,512},      {1,513},      ..., {511,1023}
#     ### group 1: {1024,1536},  {1025,1537},  ..., {1535,2047}
#     ### ...
#     ### group 63: {57344,57856}, {57345,57857}, ..., {57855,58367}
#     print("INTT-STAGE-1")
#     for j in range(64):
#         for i in range(512):
#             a1[i+j*1024]     = (a0[i+j*1024] + (a0[i+j*1024+512] * (phi_inv**(64*i) % q)) % q)
#             a1[i+j*1024+512] = (a0[i+j*1024] - (a0[i+j*1024+512] * (phi_inv**(64*i) % q)) % q)
#     for i in range(N):
#         a1[i] = (a1[i] * inv_2) % q
    
#     # Stage 2
#     ### group 0: {0,1024},      {1,1025},      ..., {1023,2047}
#     ### group 1: {2048,3072},   {2049,3073},   ..., {3071,4095}
#     ### ...
#     ### group 31: {57344,58368}, {57345,58369}, ..., {58367,59391}
#     print("INTT-STAGE-2")
#     for j in range(32):
#         for i in range(1024):
#             a2[i+j*2048]      = (a1[i+j*2048] + (a1[i+j*2048+1024] * (phi_inv**(32*i) % q)) % q)
#             a2[i+j*2048+1024] = (a1[i+j*2048] - (a1[i+j*2048+1024] * (phi_inv**(32*i) % q)) % q)
#     for i in range(N):
#         a2[i] = (a2[i] * inv_2) % q
    
#     # Stage 3
#     ### group 0: {0,2048},      {1,2049},      ..., {2047,4095}
#     ### group 1: {4096,6144},   {4097,6145},   ..., {6143,8191}
#     ### ...
#     ### group 15: {57344,59392}, {57345,59393}, ..., {59391,61439}
#     print("INTT-STAGE-3")
#     for j in range(16):
#         for i in range(2048):
#             a3[i+j*4096]      = (a2[i+j*4096] + (a2[i+j*4096+2048] * (phi_inv**(16*i) % q)) % q)
#             a3[i+j*4096+2048] = (a2[i+j*4096] - (a2[i+j*4096+2048] * (phi_inv**(16*i) % q)) % q)
#     for i in range(N):  
#         a3[i] = (a3[i] * inv_2) % q
    
#     # Stage 4
#     ### group 0: {0,4096},      {1,4097},      ..., {4095,8191}
#     ### group 1: {8192,12288},  {8193,12289},  ..., {12287,16383}
#     ### ...
#     ### group 7: {57344,61440}, {57345,61441}, ..., {61439,65535}
#     print("INTT-STAGE-4")
#     for j in range(8):
#         for i in range(4096):
#             a4[i+j*8192]      = (a3[i+j*8192] + (a3[i+j*8192+4096] * (phi_inv**(8*i) % q)) % q)
#             a4[i+j*8192+4096] = (a3[i+j*8192] - (a3[i+j*8192+4096] * (phi_inv**(8*i) % q)) % q)
#     for i in range(N):
#         a4[i] = (a4[i] * inv_2) % q
    
#     # Stage 5
#     ### group 0: {0,8192},      {1,8193},      ..., {8191,16383}
#     ### group 1: {16384,24576}, {16385,24577}, ..., {24575,32767}
#     ### group 2: {32768,40960}, {32769,40961}, ..., {40959,49151}
#     ### group 3: {49152,57344}, {49153,57345}, ..., {57343,65535}
#     print("INTT-STAGE-5")
#     for j in range(4):
#         for i in range(8192):
#             a5[i+j*16384]      = (a4[i+j*16384] + (a4[i+j*16384+8192] * (phi_inv**(4*i) % q)) % q)
#             a5[i+j*16384+8192] = (a4[i+j*16384] - (a4[i+j*16384+8192] * (phi_inv**(4*i) % q)) % q)
#     for i in range(N):
#         a5[i] = (a5[i] * inv_2) % q
    
#     # Stage 6
#     ### group 0: {0,16384},     {1,16385},     ..., {16383,32767}
#     ### group 1: {32768,49152}, {32769,49153}, ..., {49151,65535}
#     print("INTT-STAGE-6")
#     for j in range(2):
#         for i in range(16384):
#             a6[i+j*32768]       = (a5[i+j*32768] + (a5[i+j*32768+16384] * (phi_inv**(2*i) % q)) % q)
#             a6[i+j*32768+16384] = (a5[i+j*32768] - (a5[i+j*32768+16384] * (phi_inv**(2*i) % q)) % q)
#     for i in range(N):
#         a6[i] = (a6[i] * inv_2) % q
        
#     # Stage 7
#     ### group 0: {0,32768}, {1,32769}, ..., {32767,65535}
#     print("INTT-STAGE-7")
#     for i in range(32768):
#         a7[i]       = (a6[i] + (a6[i+32768] * (phi_inv**i % q)) % q)
#         a7[i+32768] = (a6[i] - (a6[i+32768] * (phi_inv**i % q)) % q)
#     for i in range(N):
#         a7[i] = (a7[i] * inv_2) % q
        
#     for idx in range(N):
#         arrayOut[idx] = a7[idx]
    
#     return arrayOut

def Kara8(arrayIn, q):
    N = len(arrayIn)
    x = np.zeros(6561, dtype=np.int64)
    y = np.zeros(6561, dtype=np.int64)
    arrayOut = np.zeros(6561, dtype=np.int64)
    
    # Stage 0
    ### group num  = 1
    ### group size = 256
    # print("KARA8-STAGE-0")
    for j in range(1):
        for i in range(128):
            x[j*384+i]     = arrayIn[j*256+i]
            x[j*384+i+128] = (arrayIn[j*256+i] + arrayIn[j*256+i+128]) % q
            x[j*384+i+256] = arrayIn[j*256+i+128]
    
    # Stage 1
    ### group num  = 3
    ### group size = 128
    # print("KARA8-STAGE-1")
    for j in range(3):
        for i in range(64):
            y[j*192+i]     = x[j*128+i]
            y[j*192+i+64]  = (x[j*128+i] + x[j*128+i+64]) % q
            y[j*192+i+128] = x[j*128+i+64]
    
    # Stage 2
    ### group num  = 9
    ### group size = 64
    # print("KARA8-STAGE-2")
    for j in range(9):
        for i in range(32):
            x[j*96+i]      = y[j*64+i]
            x[j*96+i+32]   = (y[j*64+i] + y[j*64+i+32]) % q
            x[j*96+i+64]   = y[j*64+i+32]
    
    # Stage 3
    ### group num  = 27
    ### group size = 32
    # print("KARA8-STAGE-3")
    for j in range(27):
        for i in range(16):
            y[j*48+i]      = x[j*32+i]
            y[j*48+i+16]   = (x[j*32+i] + x[j*32+i+16]) % q
            y[j*48+i+32]   = x[j*32+i+16]
    
    # Stage 4
    ### group num  = 81
    ### group size = 16
    # print("KARA8-STAGE-4")
    for j in range(81):
        for i in range(8):
            x[j*24+i]      = y[j*16+i]
            x[j*24+i+8]    = (y[j*16+i] + y[j*16+i+8]) % q
            x[j*24+i+16]   = y[j*16+i+8]
    
    # Stage 5
    ### group num  = 243
    ### group size = 8
    # print("KARA8-STAGE-5")
    for j in range(243):
        for i in range(4):
            y[j*12+i]      = x[j*8+i]
            y[j*12+i+4]    = (x[j*8+i] + x[j*8+i+4]) % q
            y[j*12+i+8]    = x[j*8+i+4]
    
    # Stage 6
    ### group num  = 729
    ### group size = 4
    # print("KARA8-STAGE-6")
    for j in range(729):
        for i in range(2):
            x[j*6+i]       = y[j*4+i]
            x[j*6+i+2]     = (y[j*4+i] + y[j*4+i+2]) % q
            x[j*6+i+4]     = y[j*4+i+2]
    
    # Stage 7
    ### group num  = 2187
    ### group size = 2
    # print("KARA8-STAGE-7")
    for j in range(2187):
        for i in range(1):
            arrayOut[j*3+i]       = x[j*2+i]
            arrayOut[j*3+i+1]     = (x[j*2+i] + x[j*2+i+1]) % q
            arrayOut[j*3+i+2]     = x[j*2+i+1]
    
    return arrayOut

def Inv_Kara8(arrayIn, q):
    N = len(arrayIn)
    x = np.zeros(6561, dtype=np.int64)
    y = np.zeros(6561, dtype=np.int64)
    arrayOut = np.zeros(256, dtype=np.int64)
    
    # Stage 0
    ### group num  = 2187
    ### group size = 3
    # print("INV-KARA8-STAGE-0")
    for i in range(2187):
        for k in range(1):
            x[i*3+k]    = arrayIn[i*3+k]
            x[i*3+1+k]  = (arrayIn[i*3+1+k] - arrayIn[i*3+k] - arrayIn[i*3+2+k]) % q
            x[i*3+2+k]  = arrayIn[i*3+2+k]
    y = [0] * 6561
    for i in range(2187):
        for j in range(3):
            for k in range(1):
                y[i*3+j+k] = (y[i*3+j+k] + x[i*3+j+k]) % q
    
    # Stage 1
    ### group num  = 729
    ### group size = 9
    # print("INV-KARA8-STAGE-1")
    for i in range(729):
        for k in range(3):
            x[i*9+k]    = y[i*9+k]
            x[i*9+3+k]  = (y[i*9+3+k] - y[i*9+k] - y[i*9+6+k]) % q
            x[i*9+6+k]  = y[i*9+6+k]
    y = [0] * 6561
    for i in range(729):
        for j in range(3):
            for k in range(3):
                y[i*7+j*2+k] = (y[i*7+j*2+k] + x[i*9+j*3+k]) % q
    
    # Stage 2
    ### group num  = 243
    ### group size = 21
    # print("INV-KARA8-STAGE-2")
    for i in range(243):
        for k in range(7):
            x[i*21+k]    = y[i*21+k]
            x[i*21+7+k]  = (y[i*21+7+k] - y[i*21+k] - y[i*21+14+k]) % q
            x[i*21+14+k] = y[i*21+14+k]
    y = [0] * 6561
    for i in range(243):
        for j in range(3):
            for k in range(7):
                y[i*15+j*4+k] = (y[i*15+j*4+k] + x[i*21+j*7+k]) % q
    
    # Stage 3
    ### group num  = 81
    ### group size = 45
    # print("INV-KARA8-STAGE-3")
    for i in range(81):
        for k in range(15):
            x[i*45+k]    = y[i*45+k]
            x[i*45+15+k] = (y[i*45+15+k] - y[i*45+k] - y[i*45+30+k]) % q
            x[i*45+30+k] = y[i*45+30+k]
    y = [0] * 6561
    for i in range(81):
        for j in range(3):
            for k in range(15):
                y[i*31+j*8+k] = (y[i*31+j*8+k] + x[i*45+j*15+k]) % q
    
    # Stage 4
    ### group num  = 27
    ### group size = 93
    # print("INV-KARA8-STAGE-4")
    for i in range(27):
        for k in range(31):
            x[i*93+k]    = y[i*93+k]
            x[i*93+31+k] = (y[i*93+31+k] - y[i*93+k] - y[i*93+62+k]) % q
            x[i*93+62+k] = y[i*93+62+k]
    y = [0] * 6561
    for i in range(27):
        for j in range(3):
            for k in range(31):
                y[i*63+j*16+k] = (y[i*63+j*16+k] + x[i*93+j*31+k]) % q
    
    # Stage 5
    ### group num  = 9
    ### group size = 189
    # print("INV-KARA8-STAGE-5")
    for i in range(9):
        for k in range(63):
            x[i*189+k]    = y[i*189+k]
            x[i*189+63+k] = (y[i*189+63+k] - y[i*189+k] - y[i*189+126+k]) % q
            x[i*189+126+k] = y[i*189+126+k]
    y = [0] * 6561
    for i in range(9):
        for j in range(3):
            for k in range(63):
                y[i*127+j*32+k] = (y[i*127+j*32+k] + x[i*189+j*63+k]) % q
                
    # Stage 6
    ### group num  = 3
    ### group size = 381
    # print("INV-KARA8-STAGE-6")
    for i in range(3):
        for k in range(127):
            x[i*381+k]    = y[i*381+k]
            x[i*381+127+k] = (y[i*381+127+k] - y[i*381+k] - y[i*381+254+k]) % q
            x[i*381+254+k] = y[i*381+254+k]
    y = [0] * 6561
    for i in range(3):
        for j in range(3):
            for k in range(127):
                y[i*255+j*64+k] = (y[i*255+j*64+k] + x[i*381+j*127+k]) % q
    
    # Stage 7
    ### group num  = 1
    ### group size = 765
    # print("INV-KARA8-STAGE-7")
    for i in range(1):
        for k in range(255):
            x[i*765+k]    = y[i*765+k]
            x[i*765+255+k] = (y[i*765+255+k] - y[i*765+k] - y[i*765+510+k]) % q
            x[i*765+510+k] = y[i*765+510+k]
    temp = [0] * 511
    for i in range(1):
        for j in range(3):
            for k in range(255):
                temp[i*511+j*128+k] = (temp[i*511+j*128+k] + x[i*765+j*255+k]) % q
    
    # concat 511 to 256
    for i in range(256):
        arrayOut[i] = temp[i]
    for i in range(255):
        arrayOut[i] = (arrayOut[i] + temp[i+256]) % q
    
    return arrayOut