#!/usr/bin/env python3
import requests

def print_blk(hex_blks, sz):
   for i in range(0, len(hex_blks), sz):
       print(hex_blks[i:i+sz], ' ', end='')
   print()

def encrypt(key, plain):
    url = "http://aes.cryptohack.org/triple_des/encrypt/"
    rsp = requests.get(url + key + '/' + plain + '/').json()
    if rsp.get("error", None):
        raise ValueError(rsp["error"])
    return rsp["ciphertext"]

def encrypt_flag(key):
    url = "http://aes.cryptohack.org/triple_des/encrypt_flag/"
    rsp = requests.get(url + key + '/').json()
    if rsp.get("error", None):
        raise ValueError(rsp["error"])
    return rsp["ciphertext"]

key = b'\x00'*8 + b'\xff'*8
flag = encrypt_flag(key.hex())
flag_sz = 34
cipher = encrypt(key.hex(), flag)
print_blk(cipher, 16)
print(bytes.fromhex(cipher))
