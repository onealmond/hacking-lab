#!/usr/bin/env python3
output = open('output.txt').read()
output = output.strip().split()

flag = []
table = {"PING":"1","PONG":"0"}

for a in output:
    flag.append(table[a]) 

for i in range(0, len(flag), 8):
    print(chr(int(''.join(flag[i:i+8]), 2)), end="")

print()
