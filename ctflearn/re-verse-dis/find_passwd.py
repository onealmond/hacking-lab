#!/usr/bin/env python3

def bytes_to_array(dat, sz):
    dat = dat.split()
    arr = []
    for i in range(0, len(dat), sz):
        arr.append(int(''.join(reversed(dat[i:i+sz])), 16))
    return arr

key = "IdontKnowWhatsGoingOn"
s = "08 00 00 00 06 00 00 00 2c 00 00 00 3a 00 00 00 32 00 00 00 30 00 00 00 1c 00 00 00 5c 00 00 00 01 00 00 00 32 00 00 00 1a 00 00 00 12 00 00 00 45 00 00 00 1d 00 00 00 20 00 00 00 30 00 00 00 0d 00 00 00 1b 00 00 00 03 00 00 00 7c 00 00 00 13 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
s = bytes_to_array(s, 4)
pw = []

for i in range(len(key)):
    pw.append(ord(key[i]) ^ s[i])
print(''.join(map(chr, pw)))
    
