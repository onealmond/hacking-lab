#!/usr/bin/env python3

data = open('abondoned_street_challenge2.jpg', 'rb').read()

i = 0
xi = 0
yi = 0
while i < len(data):
    i = data.find(b'\xff\xc0', i)
    if i == -1: break
    yi = i+5
    xi = i+7
    break

print('x', xi, data[xi:xi+2], 'y', yi, data[yi:yi+2])
data = data[:yi] + b'\x04\x60' + data[yi+2:]
with open('fix.jpg', 'wb') as fd:
    fd.write(data)
