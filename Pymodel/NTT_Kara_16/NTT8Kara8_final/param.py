import math
import sympy

# ------------------------------------------------
# Generate parameters
N       = 0
K       = 0
q       = 0
psi     = 0
psi_inv = 0
phi     = 0
phi_inv = 0
N_inv   = 0
inv_2   = 0

# Basic parameters
N = 65536
K = 32
q = 998244353
assert (N % 2) == 0, "N must be a power of 2"
assert math.log(q,2) <= K, "q must not be larger than 2^K"
assert q % (2*N) == 1, "q must be 1 mod 2N"

# Weight parameters
g = sympy.primitive_root(q)
phi = pow(g, (q-1)//N, q)
psi = pow(g, (q-1)//(2*N), q)
assert pow(psi, 2, q) == phi, "psi^2 must be phi"
assert pow(phi, N, q) == 1, "phi^N must be 1"
assert pow(psi, N, q) == q-1, "psi^N must be -1"
assert pow(psi, 2*N, q) == 1, "psi^2N must be 1"

# Inv parameters
phi_inv = sympy.mod_inverse(phi, q)
psi_inv = sympy.mod_inverse(psi, q)
assert (phi * phi_inv) % q == 1, "phi * phi_inv must be 1"
assert (psi * psi_inv) % q == 1, "psi * psi_inv must be 1"
N_inv = sympy.mod_inverse(N, q)
inv_2 = sympy.mod_inverse(2, q)
assert (N * N_inv) % q == 1, "N * N_inv must be 1"
assert (2 * inv_2) % q == 1, "2 * inv_2 must be 1"

# ------------------------------------------------
# Print parameters
print("-----------------------")
print("N      : {}".format(N))
print("K      : {}".format(K))
print("q      : {}".format(q))
print("phi    : {}".format(phi))
print("phi_inv: {}".format(phi_inv))
print("psi    : {}".format(psi))
print("psi_inv: {}".format(psi_inv))
print("N_inv  : {}".format(N_inv))
print("inv_2  : {}".format(inv_2))
print("-----------------------")