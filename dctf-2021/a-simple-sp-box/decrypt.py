#!/usr/bin/env python3
import pwn
import string
from math import ceil, log


host = "dctf1-chall-sp-box.westeurope.azurecontainer.io"
port = 8888


def find_shuffled():
    ALPHABET = string.ascii_letters + string.digits + "_!@#$%.'\"+:;<=}{"
    shuffled = []

    pr = pwn.connect(host, port)
    ret = ''
    try:
        pr.readline()
        flag = pr.readline().strip().decode()

        for a in ALPHABET:
            pr.sendlineafter('>', a*len(flag))
            pr.readline()
            enc = pr.readline().strip().decode()
            print(a, enc)
            shuffled.append(enc[0])

        for a in flag:
           i = shuffled.index(a)
           ret += ALPHABET[i]
    finally:
        pr.close()
    return ret

def decode(message):
    message = list(message)
    rounds = int(2 * ceil(log(len(message), 2))) 

    for round in range(rounds):
        if round < (rounds-1):
            odd = message[:len(message)//2]
            even = message[len(message)//2:]
            i = 0
            j = 0
            k = 0
            while i < len(odd) and j < len(even):
                if k % 2 == 1:
                    message[k] = odd[i]
                    i += 1
                else:
                    message[k] = even[j]
                    j += 1
                k += 1

            if i < len(odd):
                message[k] = odd[i]
            if j < len(even):
                message[k] = even[j]

    return ''.join(message)

enc = find_shuffled()
# 3u__Stdds_bc0h_c_f0y_3tti0xcy_hfnu}l0s3{_n
print(decode(enc))
