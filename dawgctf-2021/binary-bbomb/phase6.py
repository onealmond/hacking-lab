#!/usr/bin/env python3
expected = [0] * 24
expected[0] = ord('@')
expected[1] = 0x77
expected[2] = 0x23
expected[3] = 0x91
expected[4] = 0xb0
expected[5] = 0x72
expected[6] = 0x82
expected[7] = 0x77
expected[8] = 99
expected[9] = 0x31
expected[10] = 0xa2
expected[11] = 0x72
expected[12] = 0x21
expected[13] = 0xf2
expected[14] = 0x67
expected[15] = 0x82
expected[16] = 0x91
expected[17] = 0x77
expected[18] = 0x26
expected[19] = 0x91
expected[20] = 0
expected[21] = 0x33
expected[22] = 0x82
expected[23] = 0xc4

ans = [0] * len(expected)
for i in range(len(expected)):
    a = expected[i] ^ 100
    a = ((a << 4)&0xf0) | ((a >> 4)&0xf)
    ans[i] = a

print(''.join(map(chr, ans)))
