#!/usr/bin/env python3
import math

O = 'Origin'

def inv_mod(x, p):
    return pow(x, p-2, p) 

def ecc_points_add(P, Q, a, p):

    if P == O:
        return Q
    if Q == O:
        return P

    if P[0] == Q[0] and P[1] == -Q[1]:
        return O

    if P != Q:
        #lam = (Q[1]-P[1])/(Q[0]-P[0])
        lam = (Q[1]-P[1])*inv_mod(Q[0]-P[0], p)
    else:
        #lam = (3*pow(P[0],2)+a)/(2*P[1])
        lam = (3*pow(P[0],2)+a)*inv_mod(2*P[1], p)

    x3 = pow(lam, 2) - P[0] - Q[0]
    x3 %= p
    y3 = lam*(P[0]-x3)-P[1]
    return (int(x3), int(y3%p))


if __name__ == '__main__':
    P = (493, 5564)
    Q = (1539, 4742)
    R = (4403, 5202)

    # E: Y2 = X3 + 497 X + 1768, p: 9739
    a = 497
    b = 1768
    p = 9739

    # test
    X = (5274, 2841)
    Y = (8669, 740)
    S = ecc_points_add(X, X, a, p)
    print(S, S == (7284, 2107))
    S = ecc_points_add(X, Y, a, p)
    print(S, S == (1024, 4440))

    # S(x,y) = P + P + Q + R
    S = ecc_points_add(P, P, a, p)
    print('P+P', S)
    S = ecc_points_add(S, Q, a, p)
    print('S+Q', S)
    S = ecc_points_add(S, R, a, p)
    print('S+R', S)
    print(S == (4215, 2162))
