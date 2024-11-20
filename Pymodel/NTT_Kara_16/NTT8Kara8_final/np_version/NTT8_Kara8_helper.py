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