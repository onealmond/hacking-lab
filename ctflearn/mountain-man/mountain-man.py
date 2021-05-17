#!/usr/bin/env python3
import string

data = open('MountainMan.jpg', 'rb').read()

i = 0
begin = 0
end = 0
while True:
    i = data.find(b'\xff\xd9', i) 
    if i == -1: break
    print(i, data[i-4:i+4])
    if begin == 0:
        begin = i + 2
    elif end == 0:
        end = i
    i = i + 2

gap = data[begin:end]
print(begin, end, len(gap))
for i in range(256):
    s = ''
    for a in gap:
        c = a ^ i
        if c > 0 and c < 255 and chr(c) in string.printable:
            s += chr(c)
            continue
        s = ''
        break
    if s: print(i, s)

