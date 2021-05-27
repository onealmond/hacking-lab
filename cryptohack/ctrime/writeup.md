

The function *encrypt* append the flag to user input, uses *zlib* to compress the concatenated string. Since *zlib* eleminates duplicate string, it leaks the actual length of plain text. If adding one character to plain text doesn't increase the length of encrypted cipher text, it's likely to be a correct guess. Check throught alphabet for each position to find out the flag.


```python
def encrypt(plaintext):
    plaintext = bytes.fromhex(plaintext)

    iv = int.from_bytes(os.urandom(16), 'big')
    cipher = AES.new(KEY, AES.MODE_CTR, counter=Counter.new(128, initial_value=iv))
    encrypted = cipher.encrypt(zlib.compress(plaintext + FLAG.encode()))

    return {"ciphertext": encrypted.hex()}
```

The flag starts with *"crypto{"*, encrypted it the server output a cipher text of length 68, by adding a character is unlikely to exists in the flag the cipher text length became 70. 

```python
>>> b'crypto{'.hex()
'63727970746f7b'
>>> len('cdb32bf7901f3e434d6f53a7049b9171a85a11a5dd5272a7d723c508d8219fc9d1ec')
68
>>> b'crypto{>'.hex()
'63727970746f7b3e'
>>> len('921b4d1e22174bc99878f251e5c6a8a3c83d373abf8ad91dc9c48d53e2913ddab3729b')
70
```

With the following script I can get *"crypto{CRIM"*, but it didn't figure out the next character, well, it's not hard to make a guess, by adding *E* behind *M* the script kept going until the end and output the flag *crypto{CRIME_571ll_p4y5}*.

```python
alphabet = '}'+'!'+'_'+'@'+'?'+string.ascii_uppercase+string.digits+string.ascii_lowercase

def bruteforce():
    
    flag = b'crypto{'
    cipher = encrypt(flag.hex())
    mi = len(cipher)

    while True:
        for c in alphabet:
            cipher = encrypt((flag+c.encode()).hex())
            print(c, len(cipher))
            if mi == len(cipher):
                flag += c.encode()
                mi = len(cipher)
                print(mi, flag)
                break
            if c == alphabet[-1]:
                mi += 2
                break
            time.sleep(1)

        if flag.endswith(b'}'): 
            print(flag)
            break
```

The full code is [here](https://github.com/onealmond/hacking-lab/blob/master/cryptohack/ctrime/ctrime.py).
