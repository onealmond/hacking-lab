#!/usr/bin/env python
from PIL import Image

img = Image.open('color_img.png', 'r')
img = img.convert('RGB')

pixels = img.load()
w, h = img.size

for y in range(h):
    s = []
    for x in range(w):
        if pixels[x,y] == pixels[x-1,y]:continue
        r, g, b = pixels[x, y]
        print(''.join(map(chr, [r,g,b])), end='')
    print()
    break
