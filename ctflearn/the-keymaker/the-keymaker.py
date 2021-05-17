#!/usr/bin/env python3
import base64
from Crypto.Cipher import AES

def find_iv():
    begin = data.find(b'\xFF\xC0')
    iv_len = 16
    # skip marker and length
    end = begin + 4 + iv_len
    SOF0 = data[begin+4:end]
    return SOF0

def find_key():
    begin = data.find(b'\xFF\xDA')
    key_len = 32
    # skip marker
    end = begin + 2 + key_len
    SOS = data[begin+2:end]
    return SOS

a = 'b3BlbnNzbCBlbmMgLWQgLWFlcy0yNTYtY2JjIC1pdiBTT0YwIC1LIFNPUyAtaW4gZmxhZy5lbmMg' 
b = 'LW91dCBmbGFnIC1iYXNlNjQKCml2IGRvZXMgbm90IGluY2x1ZGUgdGhlIG1hcmtlciBvciBsZW5n'
c = 'dGggb2YgU09GMAoKa2V5IGRvZXMgbm90IGluY2x1ZGUgdGhlIFMwUyBtYXJrZXIKCg=='
d = b'mmtaSHhAsK9pLMepyFDl37UTXQT0CMltZk7+4Kaa1svo5vqb6JuczUqQGFJYiycY.'

hint = base64.b64decode(a+b+c)
print('hint', hint)
cipher = base64.b64decode(d)
print('cipher', cipher)

data = open('The-Keymaker.jpg', 'rb').read()

key = find_key()
print('key', key.hex(), len(key))
iv = find_iv()
print('iv', iv.hex(), len(iv))

aes = AES.new(key, mode=AES.MODE_CBC, IV=iv)
dec = aes.decrypt(cipher)
print('flag', dec)
