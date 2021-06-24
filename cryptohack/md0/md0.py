from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import pwn
import json

"""
p0 = key

c0 = e(p0, 0) ^ 0
c1 = e(p1, c0) ^ c0
c2 = e(p2, c1) ^ c1

c1 = e(p1, c0) ^ c0
c1' = e(p1', c0) ^ c0
"""

host = "socket.cryptohack.org"
port = 13388

def exploit():
    pr = pwn.connect(host, port)
    try:
        pr.readline()
        pr.sendline('{"option":"sign","message":""}')
        """
        c0 = e(key)
        c1 = e(padding)
        """
        c1 = bytes.fromhex(json.loads(pr.readline().strip().decode())["signature"])
        data = b'admin=True' + b'\x06'*6
        fake = pwn.xor(AES.new(data, AES.MODE_ECB).encrypt(c1), c1).hex()
        """
        p0 = key
        p1 = padding_16
        p2 = admin=True + padding_6
        """
        data = (b'\x10'*16+b'admin=True').hex()
        pr.sendline(f'{{"option":"get_flag","signature":"{fake}","message":"{data}"}}')
        print(pr.readline())
    finally:
        pr.close()

exploit()
