
From ``xor.py`` we know it generate a random key and xor it with the image to generate a encrypted one.

```python
#!/usr/bin/env python3
from os import urandom
from random import randint
from pwn import xor

input_img = open("flag.png", "rb").read()
output_img = open("flag.png.enc", "wb")

key = urandom(8) + bytes([randint(0, 9)])
output_img.write(xor(input_img, key))
```

Since the origin image is *png* format, the header is widely known. If we xor the header with the first 9 bytes of encrypted image, we are able to get the key.

```python
key = header ^ flag.png.enc[:9]
```

```python
output_img = open("flag.png", "wb")
input_img = open("flag.png.enc", "rb").read()

header = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00"
key = [0]*9
for i in range(9):
    key[i] = int(input_img[i]) ^ int(header[i])
output_img.write(xor(input_img, key))
```

```bash
$ file flag.png
flag.png: PNG image data, 300 x 300, 8-bit/color RGBA, non-interlaced
```

Open the decrypted image *flag.png* with ``ristretto``, the flag is at the bottom left, ``Hero{123_xor_321}``.
