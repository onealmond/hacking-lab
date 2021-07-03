#!/usr/bin/env python3
flag = 'flag{xxxxx}'
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cipher = 'IOWJLQMAGH'

r_letters = [letters[(i+18)%26] for i in range(26)]
for c in cipher:
    a = r_letters.index(c)
    print(letters[a], end='')
