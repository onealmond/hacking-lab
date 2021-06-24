#!/usr/bin/env python3
import gmpy
from Cryptodome.Util import number
from itertools import combinations


def load_output():
    ret = {'n':[], 'c':[]}
    with open("output_0ef6d6343784e59e2f44f61d2d29896f.txt", 'rb') as fd:
        while True:
            line = fd.readline()
            if not line: break
            line = line.strip().decode()
            if not line: continue
            
            k, v = line.split('=')
            k = k.strip()
            if k == 'e':
                continue
            ret[k].append(int(v))

    return ret

def decrypt(grps, e):
    for grp in combinations(zip(grps['n'], grps['c']), e):
        N = 1
        for x in grp: N *= x[0]

        M = 0
        for x in grp:
            M += x[1]*number.inverse(N//x[0], x[0])*(N//x[0])
        M %= N

        m, exact = gmpy.root(M, e)
        if exact:
            print(number.long_to_bytes(m))


# Reference
# [Hastad’s Broadcast Attack](https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-2/)
grps = load_output()
decrypt(grps, 3)
