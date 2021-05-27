#!/usr/bin/env python3
import requests

def print_blk(hex_blks, sz):
   for i in range(0, len(hex_blks), sz):
       print(hex_blks[i:i+sz], ' ', end='')
   print()

def encrypt():
    url = "http://aes.cryptohack.org/stream_consciousness/encrypt"
    rsp = requests.get(url)
    return rsp.json()['ciphertext']

def xor_all(ciphers, test_key):
    for cipher in ciphers:
        cipher = bytes.fromhex(cipher)
        for i in range(len(test_key)):
            if i >= len(cipher): break
            a = test_key[i] ^ cipher[i]
            if not (a > 31 and a < 127):
                return False
            print(chr(a), end='')
        print()
        print('cipher', bytes.hex(cipher))
    return True

def guess_next(cipher, key, guess):
    cipher = bytes.fromhex(cipher)
    for i in range(len(key)):
        if i >= len(cipher): break
        a = key[i] ^ cipher[i]
        print(chr(a), end='')
    print()
    if i + 1 < len(cipher) and guess:
        key.append(ord(guess) ^ cipher[i+1])

def test_key(cipher, key):
    for i in range(len(key)):
        if i >= len(cipher): break
        b = key[i] ^ cipher[i]
        print(chr(b), end='')
    print()

def dump_ciphers():
    ciphers = set()
    count = len(ciphers)
    with open('ciphers-1.txt', 'wb') as fd:
        for i in range(20):
            c = encrypt()
            ciphers.add(c)
            if len(ciphers) > count:
                count = len(ciphers)
                fd.write(c.encode()+b'\n')

def load_ciphers():
    ciphers = set()
    with open('ciphers.txt', 'rb') as fd:
        while True:
            line = fd.readline().strip().decode()
            if not line: break
            ciphers.add(line)
    return ciphers

# Finding partial key and the encrypted flag by part of the flag
def find_key_and_flag():
    prefix = b'crypto{'
    key = []
    encrypted_flag = b''
    for c in ciphers:
        c = bytes.fromhex(c)
        k = []
        for i in range(len(prefix)):
            k.append(prefix[i] ^ c[i]) 
        if xor_all(ciphers, k):
            print('found', k, len(k))
            key[:] = k[:]
            encrypted_flag = c
            break

        if key: break
    return key, encrypted_flag

#dump_ciphers()
ciphers = load_ciphers()
key, encrypted_flag = find_key_and_flag()

# Guessing the rest of key using known cipher texts and encrypted flag.
guess_next("9b645ac3ca3d8417cbb439a43713f6ace0f4a8cf5bed4bcc53fa5ffef57feb55369186cc4badd48d37c547c2a4306eb67d", key, ' ')
test_key(encrypted_flag, key)
guess_next("8e7f08cfc93daf58daa67df62313e1e5f9faf7870bf5459558f118b7fa2bbf553cc387c05fe980ff72fe1ecebf3628e3", key, 'y')
test_key(encrypted_flag, key)
guess_next("8e7f08cfc93daf58daa67df62313e1e5f9faf7870bf5459558f118b7fa2bbf553cc387c05fe980ff72fe1ecebf3628e3", key, 's')
test_key(encrypted_flag, key)
guess_next("8e7f08cfc93daf58daa67df62313e1e5f9faf7870bf5459558f118b7fa2bbf553cc387c05fe980ff72fe1ecebf3628e3", key, ' ')
test_key(encrypted_flag, key)
guess_next("9b645ac3ca3d8417cbb439a43713f6ace0f4a8cf5bed4bcc53fa5ffef57feb55369186cc4badd48d37c547c2a4306eb67d", key, ' ')
guess_next(encrypted_flag.hex(), key, 'r')
guess_next(encrypted_flag.hex(), key, '3')
guess_next(encrypted_flag.hex(), key, '4')
guess_next(encrypted_flag.hex(), key, 'm')
guess_next(encrypted_flag.hex(), key, '_')
guess_next("8e7f08cfc93daf58daa67df62313e1e5f9faf7870bf5459558f118b7fa2bbf553cc387c05fe980ff72fe1ecebf3628e3", key, 'g')
guess_next("92780d8adc6fa242c7f53cea325de7ede7eda28713fc03805dbf1df2bb28f7583d919cc00ca2c5d864ac0ad8e53026b6395c", key, 'y')
guess_next("9b645ac3ca3d8417cbb439a43713f6ace0f4a8cf5bed4bcc53fa5ffef57feb55369186cc4badd48d37c547c2a4306eb67d", key, 'h')
guess_next(encrypted_flag.hex(), key, '5')
guess_next(encrypted_flag.hex(), key, '3')
guess_next(encrypted_flag.hex(), key, '_')
guess_next("8e7f08cfc93daf58daa67df62313e1e5f9faf7870bf5459558f118b7fa2bbf553cc387c05fe980ff72fe1ecebf3628e3", key, 'y')
guess_next("8d7f1bde8c7ced5bcca17deb305dfbe4fef3bcd45bed4c8d45bf0bfffe31bf4e36d499c048e5d4c337e10281b63169af3d0fc01ca0d5ae24f61fe41a5e1cbaa1be3ffbfd5194e56d96bafcc4be4de1c6f7494a53d7a5fa3f6cd17d6249389144ffe2c607fa24f4ea6475ec4ee6c7ae5a458a95e1adbe9430b33685e1fcc73054afc51216bfebfcaa67513ae99ace52e82b7b525a271932c17e0418a73658ec", key, 't')
guess_next(encrypted_flag.hex(), key, '_')
guess_next("92780d8adc6fa242c7f53cea325de7ede7eda28713fc03805dbf1df2bb28f7583d919cc00ca2c5d864ac0ad8e53026b6395c", key, 'b')
guess_next("92780d8adc6fa242c7f53cea325de7ede7eda28713fc03805dbf1df2bb28f7583d919cc00ca2c5d864ac0ad8e53026b6395c", key, 'e')
guess_next("8d7f1bde8c7ced59c2a629fd760ee2e9fbf1fbd313f057cc41fe16f9ef7ff75c379f", key, 't')
guess_next("8d7f1bde8c7ced59c2a629fd760ee2e9fbf1fbd313f057cc41fe16f9ef7ff75c379f", key, ' ')
guess_next("8e7f08cfc93daf58daa67df62313e1e5f9faf7870bf5459558f118b7fa2bbf553cc387c05fe980ff72fe1ecebf3628e3", key, ' ')
guess_next("933709c2cd71a117cfba2ee17618f9e9e5e4afcf12f743cc50f11bb7f530eb1d34d4808544accd8c75ed04caeb", key, ' ')
test_key(encrypted_flag, key)
