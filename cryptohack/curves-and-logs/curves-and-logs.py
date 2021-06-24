import math
import hashlib
from Crypto.Util import number

O = 'Origin'

def inv_mod(x, p):
    return pow(x, p-2, p) 

# Calculate S = P + Q
def ecc_points_add(P, Q, a, p):

    if P == O:
        return Q
    if Q == O:
        return P

    if P[0] == Q[0] and P[1] == -Q[1]:
        return O

    if P != Q:
        lam = (Q[1]-P[1])*inv_mod(Q[0]-P[0], p)
    else:
        lam = (3*pow(P[0],2)+a)*inv_mod(2*P[1], p)

    x3 = pow(lam, 2) - P[0] - Q[0]
    x3 %= p
    y3 = lam*(P[0]-x3)-P[1]
    return (int(x3), int(y3%p))

# Calculate Q = nP
def scalar_mul(P, n, a, p):
    R = O
    Q = P
    
    while n > 0:
        if n % 2 == 1:
            R = ecc_points_add(R, Q, a, p)
        Q = ecc_points_add(Q, Q, a, p)
        n = math.floor(n/2)
    return R

"""
A  QA = nA*G
B  QB = nB*G
A  S = nA*QB
B  S = nB*QA
"""
# E: Y2 = X3 + 497 X + 1768, p: 9739, G: (1804,5368)
a = 497
b = 1768
p = 9739

# QA = (815, 3190), with your secret integer nB = 1829.
nB = 1829
QA = (815, 3190)
S = scalar_mul(QA, nB, a, p)
print(S)
sha1 = hashlib.sha1()
sha1.update(str(S[0]).encode())
print(sha1.hexdigest())
