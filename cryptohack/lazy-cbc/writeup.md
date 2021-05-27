

Took a look into the code, the key was used for both key and IV for AES-CBC encryption and decryption, *get_flag* needed the key to get the flag. Function *receive* decrypts given cipher text, if failed, the decrypted message returned.


```python
@chal.route('/lazy_cbc/encrypt/<plaintext>/')
def encrypt(plaintext):
    plaintext = bytes.fromhex(plaintext)
    if len(plaintext) % 16 != 0:
        return {"error": "Data length must be multiple of 16"}

    cipher = AES.new(KEY, AES.MODE_CBC, KEY)
    encrypted = cipher.encrypt(plaintext)

    return {"ciphertext": encrypted.hex()}


@chal.route('/lazy_cbc/get_flag/<key>/')
def get_flag(key):
    key = bytes.fromhex(key)

    if key == KEY:
        return {"plaintext": FLAG.encode().hex()}
    else:
        return {"error": "invalid key"}


@chal.route('/lazy_cbc/receive/<ciphertext>/')
def receive(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)
    if len(ciphertext) % 16 != 0:
        return {"error": "Data length must be multiple of 16"}

    cipher = AES.new(KEY, AES.MODE_CBC, KEY)
    decrypted = cipher.decrypt(ciphertext)

    try:
        decrypted.decode() # ensure plaintext is valid ascii
    except UnicodeDecodeError:
        return {"error": "Invalid plaintext: " + decrypted.hex()}

    return {"success": "Your message has been received"}
```

Time to do some math. According to AES-CBC decription process, we have the following equations. *pn* for the nth block of plain text, *cn* for the nth block of cipher text, *d()* is the decryption function.

```python
key = iv = d(c0) ^ p0

p0 = d(c0) ^ iv
p1 = d(c1) ^ c0 
p2 = d(c2) ^ c1
```

If *c1 = 0* and *c2 = c0*, the equations above become

```python
p0 = d(c0) ^ iv
p1 = d(0) ^ c0
p2 = d(c0) ^ 0
```

If xor *p0* and *p2*, since key is used as IV, we have the following transformation to get the key.

```python
p0 ^ p2 = d(c0) ^ iv ^ d(c0)
        = iv = key
```

Made up plain text that takes 3 blocks.

```python
plain = (b'a'*(16*3)).hex()
```

Encrypted it we have cipher text

```python
cipher = '1c5ded2c669062d2cd3a11766371be1a38f0a5d3c96961eac8586bb4549dfc41c49a8a3d4c17740bf224d19d129fa9a8'
```

Altered the cipher text so that the second block is filled with zeroes and the third block equal to the first one.

```python
fake_cipher = cipher[:32] + '0'*32 + cipher[:32]
```

Attempted to decrypt the fake cipher text just made up, the serve gave this error with decrypted message.

```python
{"error":"Invalid plaintext: 6161616161616161616161616161616155cb30af3a7c7a40f8ce7e766c8037579bf317d1684a16e1e95691b163dc178a"}
```

Xor'd the first block and the third block of the fake plain text to get IV, as well as the key, which is *fa9276b0092b77808837f0d002bd76eb*.

```python
fake_plain = '6161616161616161616161616161616155cb30af3a7c7a40f8ce7e766c8037579bf317d1684a16e1e95691b163dc178a'
fake_plain = bytes.fromhex(fake_plain)
iv = [0]*16
for i in range(len(iv)):
   iv[i] = fake_plain[i] ^ fake_plain[32+i] 
```

Requested ``get_flag`` with the key, the flag returned in hex. Decoded it to be ``crypto{50m3_p30pl3_d0n7_7h1nk_IV_15_1mp0r74n7_?}``.

```
flag = '63727970746f7b35306d335f703330706c335f64306e375f3768316e6b5f49565f31355f316d70307237346e375f3f7d'
print(bytes.fromhex(flag))
```
