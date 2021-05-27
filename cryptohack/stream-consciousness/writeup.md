
For every request, the server output cipher text of randomly picked plain text, one of them could be the flag if request enough times.

```python
KEY = ?
TEXT = ['???', '???', ..., FLAG]


@chal.route('/stream_consciousness/encrypt/')
def encrypt():
    random_line = random.choice(TEXT)

    cipher = AES.new(KEY, AES.MODE_CTR, counter=Counter.new(128))
    encrypted = cipher.encrypt(random_line.encode())

    return {"ciphertext": encrypted.hex()}
```

After 20 requests, I was able to get 16 distinct cipher texts.

```python
ciphers = set()
count = len(ciphers)
for i in range(20):
    c = encrypt()
    ciphers.add(c)
    if len(ciphers) > count:
        count = len(ciphers)
        print(c)
```

```python
9e7816c6d53dba5ecfb97df03e14e1e7b7e9b3c60fb96dcb5cbf13f2fa29f653349195855fa0c3c379e847c9b02d2ba332199618a2dde125ed5ef1544e54aabdba2de0ee5ddacd2f97aaa390f65fe2d1b2475610daadbf766b9f7a634b768f50f9efc047
9b645ac3ca3d8417cbb439a43713f6ace0f4a8cf5bed4bcc53fa5ffef57feb55369186cc4badd48d37c547c2a4306eb67d
98620e8ae53dba5ecfb97df73e12f8acfff4b689
8e7f08cfc93daf58daa67df62313e1e5f9faf7870bf5459558f118b7fa2bbf553cc387c05fe980ff72fe1ecebf3628e3
b96503dad872b65c90ac68b3244ebbe1c8efe8d24eaa7bdd04c019a3ac6bf340
956208958c4aa54e83ba28f669
8e7f1f8ad878bf45cab731e17609e7e5f9fafbce08b9508450eb5fe3f33abf4d32c280854fa4ce8b63ac05c4e52a26b0325dd90cb899a328a556f1071a4ea0a0ab38a1
8d7f1bde8c7ced5bcca17deb305dfbe4fef3bcd45bed4c8d45bf0bfffe31bf4e36d499c048e5d4c337e10281b63169af3d0fc01ca0d5ae24f61fe41a5e1cbaa1be3ffbfd5194e56d96bafcc4be4de1c6f7494a53d7a5fa3f6cd17d6249389144ffe2c607fa24f4ea6475ec4ee6c7ae5a458a95e1adbe9430b33685e1fcc73054afc51216bfebfcaa67513ae99ace52e82b7b525a271932c17e0418a73658ec
8a7208c2cd6dbe17cbb07dec370eafe1feeea8c21fb9508454bf0be5fa36f11d32df908545b680ce76ef0c81a72769ac330a98599bd8af25a552ea065f1ca7bab222e3f5598eed6094fe
9330178ad973a556d3a524a87634afe8f2eebed50dfc048545b35fe3f33abf5b32c498d10bb680c17ee2028de53c3cb67c349114ecccaf39e44ff50d1a5da3a3ff3fe7f91889e5629ff3f08cb340e783ba4e01
933709c2cd71a11b839c7ae83a5de3e3e4f8fbc20dfc569545f716f9fc7ff65b73d9918548aac5df79ab1381a63124a77c1fd71aa797
96780ccf803dbd45ccb73ce63a04b0acc3f5bede5bfd4b8216eb5ffcf530e81d3bde838548b7c5cd65f547c8b17e20b1705dde16bb99a924e856e91d5b48a6a1b865a1b2188eec6ada9ea681b859f283b6454b10dba0f67361cd6b6500
8d7f1bde8c7ced59c2a629fd760ee2e9fbf1fbd313f057cc41fe16f9ef7ff75c379f
92780d8adc6fa242c7f53cea325de7ede7eda28713fc03805dbf1df2bb28f7583d919cc00ca2c5d864ac0ad8e53026b6395c
933709c2cd71a117cfba2ee17618f9e9e5e4afcf12f743cc50f11bb7f530eb1d34d4808544accd8c75ed04caeb
9e651fd9df30a056c8bc33e3761ce1e8b7d0b2cb17f04a8943e6
```

Since the all the plain texts share one key, the key shall work on all of cipher texts. The prefix of the flag is *"crypto{"*, with that, the key could be partially recovered.

```python
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
```

With the script part of the key is recovered to be ``[218, 23, 122, 170, 172, 29, 205]`` and found out the encrypted flag. What's more, from the debug information from *xor_all* function, some readable texts were shown.

```bash
What a   
cipher 8d7f1bde8c7ced59c2a629fd760ee2e9fbf1fbd313f057cc41fe16f9ef7ff75c379f
Three b   
cipher 8e7f08cfc93daf58daa67df62313e1e5f9faf7870bf5459558f118b7fa2bbf553cc387c05fe980ff72fe1ecebf3628e3
I shall    
cipher 933709c2cd71a117cfba2ee17618f9e9e5e4afcf12f743cc50f11bb7f530eb1d34d4808544accd8c75ed04caeb
Dolly w      
cipher 9e7816c6d53dba5ecfb97df03e14e1e7b7e9b3c60fb96dcb5cbf13f2fa29f653349195855fa0c3c379e847c9b02d2ba332199618a2dde125ed5ef1544e54aabdba2de0ee5ddacd2f97aaa390f65fe2d1b
2475610daadbf766b9f7a634b768f50f9efc047
How pro         
cipher 92780d8adc6fa242c7f53cea325de7ede7eda28713fc03805dbf1df2bb28f7583d919cc00ca2c5d864ac0ad8e53026b6395c
But I w           
cipher 98620e8ae53dba5ecfb97df73e12f8acfff4b689
As if I             
cipher 9b645ac3ca3d8417cbb439a43713f6ace0f4a8cf5bed4bcc53fa5ffef57feb55369186cc4badd48d37c547c2a4306eb67d
Love, p               
cipher 96780ccf803dbd45ccb73ce63a04b0acc3f5bede5bfd4b8216eb5ffcf530e81d3bde838548b7c5cd65f547c8b17e20b1705dde16bb99a924e856e91d5b48a6a1b865a1b2188eec6ada9ea681b859f283b
6454b10dba0f67361cd6b6500
Perhaps                  
cipher 8a7208c2cd6dbe17cbb07dec370eafe1feeea8c21fb9508454bf0be5fa36f11d32df908545b680ce76ef0c81a72769ac330a98599bd8af25a552ea065f1ca7bab222e3f5598eed6094fe
I'm unh                    
cipher 9330178ad973a556d3a524a87634afe8f2eebed50dfc048545b35fe3f33abf5b32c498d10bb680c17ee2028de53c3cb67c349114ecccaf39e44ff50d1a5da3a3ff3fe7f91889e5629ff3f08cb340e783b
a4e01                        
Our? Wh                       
cipher 956208958c4aa54e83ba28f669
crypto{                         
cipher b96503dad872b65c90ac68b3244ebbe1c8efe8d24eaa7bdd04c019a3ac6bf340                                                                                             What a                             
cipher 8d7f1bde8c7ced5bcca17deb305dfbe4fef3bcd45bed4c8d45bf0bfffe31bf4e36d499c048e5d4c337e10281b63169af3d0fc01ca0d5ae24f61fe41a5e1cbaa1be3ffbfd5194e56d96bafcc4be4de1c6f
7494a53d7a5fa3f6cd17d6249389144ffe2c607fa24f4ea6475ec4ee6c7ae5a458a95e1adbe9430b33685e1fcc73054afc51216bfebfcaa67513ae99ace52e82b7b525a271932c17e0418a73658ec
```

What left to do was some manual work, the two functions below were quite handy.

```python
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
```

After quite a while guess and test, the flag was recovered, *crypto{k3y57r34m_r3u53_15_f474l}*.

```python
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
```

Full source code can be found [here](https://github.com/onealmond/hacking-lab/blob/master/cryptohack/stream-consciousness/stream-consciousness.py).
