#!/usr/bin/env python3
from PIL import Image
from Crypto.Util import number

img = Image.open('lsblue.png')
img = img.convert('RGB')
w, h = img.size
pixels = img.load()

bits = ''

for j in range(h):
    for i in range(w):
        r,g,b = pixels[i,j]
        bits += bin(b)[-1]

flag = b''
for i in range(0, len(bits), 8):
    flag += chr(int(bits[i:i+8],2)).encode()
print(flag)
