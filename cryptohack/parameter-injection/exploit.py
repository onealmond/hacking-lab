import pwn
import json
import hashlib
from Crypto.Cipher import AES

host = "socket.cryptohack.org"
port = 13371

"""
https://cryptopals.com/sets/5/challenges/34

Normal traffic:

A->B
Send "p", "g", "A"
B->A
Send "B"
A->B
Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
B->A
Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv

Injected traffic:

A->M
Send "p", "g", "A"
M->B
Send "p", "g", "p"
B->M
Send "B"
M->A
Send "p"
A->M
Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
M->B
Relay that to B
B->M
Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
M->A
Relay that to A

Result

A: A = pow(g, a, p)
B: B = pow(g, p, p)
A: k = pow(p, a, p)
B: k = pow(p, b, p)

So k = 0
"""

def exploit():
    pr = pwn.connect(host, port)
    try:
        pr.readuntil(": ")
        line = json.loads(pr.readline().strip().decode())
        #p = int(line['p'][2:].strip('f'), 16)
        p = int(line['p'], 16)
        g = int(line['g'], 16)
        A = int(line['A'], 16)

        payload = json.dumps({"p":hex(p),"g":hex(g),"A":hex(p)})
        print(payload, len(payload))
        pr.sendlineafter(": ", payload)

        pr.readuntil(": ")
        line = json.loads(pr.readline().strip().decode())
        B = int(line['B'], 16)

        payload = json.dumps({"B":hex(p)})
        print(payload, len(payload))
        pr.sendlineafter(": ", payload)

        pr.readuntil(": ")
        line = json.loads(pr.readline().strip().decode())
        print(line)

        iv = bytes.fromhex(line['iv'])
        encrypted_flag = bytes.fromhex(line['encrypted_flag'])
        sha1 = hashlib.sha1()
        secret = 0
        sha1.update(str(secret).encode())
        key = sha1.digest()[:16]
        aes = AES.new(key, AES.MODE_CBC, iv)
        print(aes.decrypt(encrypted_flag))
    finally:
        pr.close()

exploit()
