
The flag was in an encrypted PNG file with AES-ECB, as *StepUpCounter* was initialized with *step_up=False*, IV wasn't updated during encryption. Considering the plain text is a PNG file, the header is known, the key size is 16, so use the first 16 bytes of cipher text to xor the first 16 bytes of PNG header to leak the key. Once got the key, xor it with each block of the cipher text to recover the PNG file.


```python
class StepUpCounter(object):
    def __init__(self, value=os.urandom(16), step_up=False):
        self.value = value.hex()
        self.step = 1
        self.stup = step_up

    def increment(self):
        if self.stup:
            self.newIV = hex(int(self.value, 16) + self.step)
        else:
            self.newIV = hex(int(self.value, 16) - self.stup)
        self.value = self.newIV[2:len(self.newIV)]
        return bytes.fromhex(self.value.zfill(32))

    def __repr__(self):
        self.increment()
        return self.value

def encrypt():
    cipher = AES.new(KEY, AES.MODE_ECB)
    ctr = StepUpCounter()

    out = []
    with open("challenge_files/bean_flag.png", 'rb') as f:
        block = f.read(16)
        while block:
            keystream = cipher.encrypt(ctr.increment())
            xored = [a^b for a, b in zip(block, keystream)]
            out.append(bytes(xored).hex())
            block = f.read(16)

    return {"encrypted": ''.join(out)}
```

The following script implemented the solution, in recovered PNG file, the flag was *"crypto{hex_bytes_beans}"*.


```python
def encrypt():
    url = "http://aes.cryptohack.org/bean_counter/encrypt/"
    rsp = requests.get(url)
    return rsp.json()['encrypted']

png_hdr = bytes([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52])
encrypted = bytes.fromhex(encrypt())

keystream = []
for i in range(len(png_hdr)):
    keystream.append(png_hdr[i] ^ encrypted[i])

print(keystream)

png = [0]*len(encrypted)
for i in range(len(encrypted)):
    png[i] = encrypted[i] ^ keystream[i%len(keystream)]

with open('bean_counter.png', 'wb') as fd:
    fd.write(bytes(png))
```

The full code is [here](https://github.com/onealmond/hacking-lab/blob/master/cryptohack/bean-counter/bean-counter.py).
