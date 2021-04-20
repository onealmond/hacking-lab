#!/usr/bin/env python3

ran = [36, 184, 75, 50, 106, 222, 33, 64, 75, 253, 75, 85, 118, 114, 201, 92, 121, 55, 219, 18, 48, 67, 22, 5, 184, 96, 219, 113, 158, 97, 171, 102, 131, 244, 199, 55, 173, 40, 184, 46]
arr = [ord(c) for c in list(("DeltaForce" * 4))]
match = [8, 169, 83, 54, 120, 162, 97, 29, 81, 247, 122, 68, 111, 40, 202, 127, 57, 33, 233, 0, 64, 81, 67, 38, 190, 126, 215, 82, 253, 4, 239, 3, 49, 11, 209, 71, 226, 13, 147, 78]
buf = [0]*40
xmm0 = ran[0:16]
xmm1 = buf[16:32]
xmm2 = ran[32:40]
xmm3 = ran[0:16]

def reverse():
    xmm0 = [0] * 40

    for i in range(40):
        xmm0[i] = match[i] ^ arr[i]
    for i in range(40):
        buf[i] = xmm0[i] ^ ran[i]

    for i in range(4):
        xmm1[i] = match[16+i] ^ arr[16+i]

    for i in range(4):
        xmm1[i] ^= ran[16+i]

    buf[16:20] = xmm1[:4]

reverse()
print(' '.join([str(int.from_bytes(bytes(buf[i:i+4]),'little')) for i in range(0, len(buf), 4)]))
