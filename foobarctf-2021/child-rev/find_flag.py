#!/usr/bin/env python3
dat = "78 2f 01 00 00 00 00 00 30 2f 01 00 00 00 00 00 72 2f 01 00 00 00 00 00 5f 2f 01 00 00 00 00 00 61 2f 01 00 00 00 00 00 6e 2f 01 00 00 00 00 00 64 2f 01 00 00 00 00 00 5f 2f 01 00 00 00 00 00 6c 2f 01 00 00 00 00 00 30 2f 01 00 00 00 00 00 67 2f 01 00 00 00 00 00 31 2f 01 00 00 00 00 00 63 2f 01 00 00 00 00 00 40 2f 01 00 00 00 00 00 6c 2f 01 00 00 00 00 00 5f 2f 01 00 00 00 00 00 73 2f 01 00 00 00 00 00 68 2f 01 00 00 00 00 00 31 2f 01 00 00 00 00 00 66 2f 01 00 00 00 00 00 74 2f 01 00 00 00 00 00 5f 2f 01 00 00 00 00 00 65 2f 01 00 00 00 00 00 40 2f 01 00 00 00 00 00 73 2f 01 00 00 00 00 00 79 2f 01 00 00 00 00 00 5f 2f 01 00 00 00 00 00 72 2f 01 00 00 00 00 00 31 2f 01 00 00 00 00 00 67 2f 01 00 00 00 00 00 68 2f 01 00 00 00 00 00 38 2f 01 00 00 00 00 00 3f 2f 01 00 00 00 00 00 3f 2f 01 00 00 00 00 00"
dat = dat.split()
arr = []

for i in range(0, len(dat), 8):
  arr.append(int(''.join(reversed(dat[i:i+8])), 16))

key = 0x00012f00
flag = [0]*0x22

for i in range(len(flag)):
    flag[i] = arr[i] ^ key

print(''.join(map(chr, flag)))