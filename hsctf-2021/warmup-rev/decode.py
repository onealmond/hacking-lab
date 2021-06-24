def hot(s):
    adj = [-72, 7, -58, 2, -33, 1, -102, 65, 13, -64, 
				21, 14, -45, -11, -48, -7, -1, 3, 47, -65, 3, -18, 
				-73, 40, -27, -73, -13, 0, 0, -68, 10, 45, 13]
    ret = list(s)
    for i in range(len(adj)):
        ret[i] -= adj[i]
    return ret

def warm(t):
    """
    1111l2222l3333
    a = 1111l
    t1 = 2222l3333
    b = 2222l
    c = 3333
    c + b + a = 33332222l1111l
    a + t1 = 1111l33332222l
    """
    i = t.index(ord('l'), 0, len(t)-1)
    a = t[i+1:]
    t1 = t[:i+1]

    for i in range(1, len(t1)):
        s = a + t1[i:] + t1[:i]
        yield s

def cold(t):
    return t[-17:] + t[:-17]

def cool(t):
    ret = list(t)

    for i in range(len(t)):
        if i % 2 == 0:
            ret[i] = (ret[i]-int(3 * (i/2))) % 256
    return ''.join(map(chr, ret)).encode()

match = b'4n_3nd0th3rm1c_rxn_4b50rb5_3n3rgy'
# match = b'|g\xc2\x991\xc2\x8fc\xc2\x963[s]_^n\xc2\x8fyyk0u_GyJ}~l3nwh:l'
"""
???????l?????????l???????
a = ??????l
b = ???????????l
c = ??????
"""
for m in warm(hot(match)):
    f = cold(cool(m)) 

    if f.endswith(b'}'):
        print('flag', f)
        break

# flag{1ncr34s3_1n_3nth4lpy_0f_5y5}
