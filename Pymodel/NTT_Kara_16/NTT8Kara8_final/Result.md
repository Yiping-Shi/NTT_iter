[shiyiping@panda NTT8Kara8_final]$ python Poly_NTT8_Kara8.py

## Parameter Definition

| N         =  65536     |
| :--------------------- |
| K         =  32        |
| q         =  998244353 |
| phi       =  629671588 |
| phi_inv   =  283043518 |
| psi       =  24514907  |
| psi_inv   =  3707709   |
| N_inv     =  998229121 |
| inv_2     =  499122177 |

---
## 0. Initialization
('A[0:16]: ', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
('B[0:16]: ', [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

## 1. Negacyclic convolution (Preprocess)
***('Nega_conv Time: ', 3369.5423288345337)***

## 2. NTT (8 stages)
***('NTT Time: ', 5925.766027927399)***

## 3. Karatsuba (8 stages)
***('Karatsuba Time: ', 2.1045401096343994)***

## 4. Element-wise Multiplication
***('Element-wise Multiplication Time: ', 0.5550050735473633)***

## 5. Inv-Karatsuba (8 stages)
***('Inv_Karatsuba Time: ', 4.856817007064819)***

## 6. Inv-NTT (8 stages)
***('INTT Time: ', 5587.164417028427)***

## 7. Negacyclic convolution (Postprocess)
('C[0:16]: ', [995506068L, 844609430L, 693778330L, 543012770L, 392312752L, 241678278L, 91109350L, 938850323L, 788412493L, 638040215L, 487733491L, 337492323L, 187316713L, 37206663L, 885406528L, 735427604L])

***('Inv_Nega_conv Time: ', 1402.7926428318024)***

## Verification
('Base[0:16]: ', [995506068, 844609430, 693778330, 543012770, 392312752, 241678278, 91109350, 938850323, 788412493, 638040215, 487733491, 337492323, 187316713, 37206663, 885406528, 735427604])

C == Base --> Verification PASS! 😊 😊 😊 😊 😊

## Total Time consumption
('Execution Time: ', 17318.86577105522)
