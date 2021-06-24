# Reference: https://hgarrereyn.gitbooks.io/th3g3ntl3man-ctf-writeups/content/2017/picoCTF_2017/problems/cryptography/ECC2/ECC2.html
# Pohlig-Hellman attack to find n so that P = nG
import hashlib
from Crypto.Cipher import AES
from source_ba064d03b53a5fd7321dd0007b72906b import Point, gen_shared_secret

def decrypt_flag(shared_secret: int, iv: str, encrypted: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]

    iv = bytes.fromhex(iv)
    encrypted = bytes.fromhex(encrypted)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(encrypted)
    return plaintext

p = 310717010502520989590157367261876774703
a = 2
b = 3
g_x = 179210853392303317793440285562762725654
g_y = 105268671499942631758568591033409611165

F = FiniteField(p)
E = EllipticCurve(F, [a, b])

# P = nG
P = E.point((280810182131414898730378982766101210916, 291506490768054478159835604632710368904))
G = E.point((g_x, g_y))

print('factor E.order():', factor(E.order()))

factors, exps = zip(*factor(E.order()))
primes = [factors[i]^exps[i] for i in range(len(factors))]
print(primes)
dlogs = []

for fac in primes:
  t = int(G.order() / fac)
  dlog = discrete_log(t*P, t*G, operation="+")
  dlogs += [dlog]
  print("factor:", fac, "dlog:", dlog)

print(dlogs)
n = crt(dlogs, primes)
print(n * G == P)
print(n)

"""
factor E.order(): 2^2 * 3^7 * 139 * 165229 * 31850531 * 270778799 * 179317983307
[4, 2187, 139, 165229, 31850531, 270778799, 179317983307]
factor: 4 dlog: 47836431801801373761601790722388100620
factor: 2187 dlog: 1871
factor: 139 dlog: 73
factor: 165229 dlog: 2080
factor: 31850531 dlog: 704661
factor: 270778799 dlog: 105138385
factor: 179317983307 dlog: 109957133994
[47836431801801373761601790722388100620, 1871, 73, 2080, 704661, 105138385, 109957133994]
True
47836431801801373761601790722388100620
"""

# decrypt flag
iv = '07e2628b590095a5e332d397b8a59aa7'
encrypted_flag = '8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af'

b_x = 272640099140026426377756188075937988094
b_y = 51062462309521034358726608268084433317
B = Point(b_x, b_y)

"""
S = n * B
enc = e(S, iv, plain)

S = n * A
A = double_and_add(G, n)
"""
# generate shared secret with previously found ``n``
s = gen_shared_secret(B, n)
print(s)
print(decrypt_flag(s, iv, encrypted_flag))
