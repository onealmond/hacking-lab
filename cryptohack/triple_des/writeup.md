
The service allowed to specify key and plain text for encryption. A weak key can cause double encrytion, if use a weak key to encrypt the flag, encrypt again the encrypted flag with the same key, the encrypted flag got decrypted.

```python
IV = os.urandom(8)
FLAG = ?


@chal.route('/triple_des/encrypt/<key>/<plaintext>/')
def encrypt(key, plaintext):
    try:
        key = bytes.fromhex(key)
        plaintext = bytes.fromhex(plaintext)
        plaintext = xor(plaintext, IV)

        cipher = DES3.new(key, DES3.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext)
        ciphertext = xor(ciphertext, IV)

        return {"ciphertext": ciphertext.hex()}

    except ValueError as e:
        return {"error": str(e)}


@chal.route('/triple_des/encrypt_flag/<key>/')
def encrypt_flag(key):
    return encrypt(key, pad(FLAG.encode(), 8).hex())
```

Tested several weak keys, found out *"b'\x00'*8 + b'\xff'*8"* works.

```python
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
```

```bash
63727970746f7b6e  30745f346c6c5f6b  3379735f3472335f  673030645f6b3379  737d060606060606  
b'crypto{n0t_4ll_k3ys_4r3_g00d_k3ys}\x06\x06\x06\x06\x06\x06'
```
