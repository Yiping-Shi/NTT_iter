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

n_inv = modinv(2, 12289)
print(n_inv)

a = [6103, 9211]
b = [6103, 9211]
phi = 6553
q = 12289

a1 = [0] * 2
a1[0] = (a[0] + a[1]) % q
a1[1] = (a[0] - a[1]) % q
b1 = [0] * 2
b1[0] = (b[0] + b[1]) % q
b1[1] = (b[0] - b[1]) % q
print(a1)
print(b1)

c = [0] * 2
c[0] = a1[0] * b1[0] % q
c[1] = a1[1] * b1[1] % q
print(c)

c1 = [0] * 2
c1[0] = (c[0] + c[1]) % q
c1[1] = (c[0] - c[1]) % q
print(c1)



A = [6103, 9211]
B = [6103, 9211]
print("A: ", A)
print("B: ", B)

psi_inv = 2545
A[1] = A[1] * psi_inv % q
B[1] = B[1] * psi_inv % q
print("A: ", A)
print("B: ", B)

C = [0] * 3
for i in range(2):
    for j in range(2):
        C[i+j] += (A[i] * B[j]) % q

print("C: ", C)
C[0] = (C[0] - C[2]) % q
print("C: ", C)