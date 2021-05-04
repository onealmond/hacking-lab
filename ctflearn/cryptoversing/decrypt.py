#!/usr/bin/env python3
from Cryptodome.Util import number

expected = 0x685f624f7d4563444f522b47297568286a6c2c764c
expected = number.long_to_bytes(expected)

def decrypt():
    buf = [0]*len(expected)
    arr = [0]*6
    arr[0] = 0x10
    arr[1] = 0x18
    arr[2] = len(buf) >> 1
    arr[3] = len(buf)
    arr[4] = 0
    arr[5] = len(buf) >> 1
    for i in range(2):
        cur = arr[i + 4]
        while cur < arr[i + 2]:
          buf[cur] = expected[cur] ^ arr[i]
          cur = cur + 1;

    return ''.join(map(chr, buf))

print(decrypt())
