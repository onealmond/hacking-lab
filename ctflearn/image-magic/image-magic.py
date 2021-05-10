#!/usr/bin/env python3

from PIL import Image

img = Image.open('out+copy.jpg', 'r')
img = img.convert('RGB')
pixels = img.load()

w, _  = img.size
actual_h = w // 304

img_fixed = Image.new(img.mode, (304, actual_h))
fixed = img_fixed.load()

fy = 0

for x in range(0, actual_h):
    row = []
    fx = 0
    for i in range(x, w, actual_h):
        fixed[fx,fy] = pixels[i,0]
        fx += 1
    fy += 1

img_fixed.show()
