
The service takes user input as plain text, appends the flag to it to make a padded string for ``AES_ECB``` to encrypt.

```python
def encrypt(plaintext):
    plaintext = bytes.fromhex(plaintext)

    padded = pad(plaintext + FLAG.encode(), 16)
    cipher = AES.new(KEY, AES.MODE_ECB)

    try:
        encrypted = cipher.encrypt(padded)
    except ValueError as e:
        return {"error": str(e)}

    return {"ciphertext": encrypted.hex()}
```

According to the way ECB mode works, if the input is *"111111111111111"*, as the flag startswith *"crypto{"* *plain text + FLAG* becomes *"111111111111111crypto{...}"*. The first 16 bytes of cipher text of *"111111111111111ccrypto{...}"* and the first 16 bytes of cipher text of *"111111111111111crypto{...}"* should be the same.

```python
print('  ', end='')
print_blk(encrypt(bytes.hex(b'1'*15)), 32)

for i in range(ord('a'),ord('z')):
    print(chr(i), '', end='')
    print_blk(encrypt(bytes.hex(b'1'*15+int.to_bytes(i, 1, 'little'))), 32)
```

```bash
  220a332f2bf0be3f1c3973707be93dba  5245173a0a15bd37034d6761ed2a7fba  6397a55a1e310cbc60120becb2d9453f  <= cipher text of "111111111111111crypto{...}"
a 33a2d339a8fab0ae628424d69a015106  d0312d0b8a979846ca0bb572e29eff03  dd362b0c5b430f4c2aaec01ee288ce24  
b dd498d35ca964fd218ce3e7bc3cca1cc  d0312d0b8a979846ca0bb572e29eff03  dd362b0c5b430f4c2aaec01ee288ce24  
c 220a332f2bf0be3f1c3973707be93dba  d0312d0b8a979846ca0bb572e29eff03  dd362b0c5b430f4c2aaec01ee288ce24  <= cipher text of "111111111111111ccrypto{...}"
d 91a7b888c4f4f3be960ab9a7f3460776  d0312d0b8a979846ca0bb572e29eff03  dd362b0c5b430f4c2aaec01ee288ce24
...
```

By adding verified characters one by one shall be able to get the flag. As the length of flag is unknown, compare the second block, ``cipher[32:64]`` by guessing. Also needed to add time to sleep to avoid request rate exceeded error from server.

```python
def bruteforce():
    flag = ''
    total = 32 - 1
    alphabet = '_'+'@'+'}'+string.digits+string.ascii_lowercase+string.ascii_uppercase

    while True:
        payload = '1' * (total-len(flag))
        expected = encrypt(payload.encode().hex())
        print('E', '', end='')
        print_blk(expected, 32)
        
        for c in alphabet: 
            res = encrypt(bytes.hex((payload + flag + c).encode()))
            print(c, '', end='')
            print_blk(res, 32)
            if res[32:64] == expected[32:64]:
                flag += c
                print(flag)
                break
            time.sleep(1)

        if flag.endswith('}'): break

    print(flag)
```

Waited for a while the flag came out to be ``crypto{p3n6u1n5_h473_3cb}``.

The full code is [here](https://github.com/onealmond/hacking-lab/blob/master/cryptohack/ecb-oracle/ecb-oracle.py).
