#!/usr/bin/env python3

def the_simpsons():
    encoded = "152 162 152 145 162 167 150 172 153 162 145 170 141 162"
    cipher = list(map(lambda x: int(x, 8), encoded.split()))
    key = "110 157 167 040 155 165 143 150 040 144 151 144 040 115 141 147 147 151 145 040 157 162 151 147 151 156 141 154 154 171 040 143 157 163 164 077 040 050 104 151 166 151 144 145 144 040 142 171 040 070 054 040 164 157 040 164 150 145 040 156 145 141 162 145 163 164 040 151 156 164 145 147 145 162 054 040 141 156 144 040 164 150 145 156 040 160 154 165 163 040 146 157 165 162 051"
    key = list(map(lambda x: chr(int(x, 8)), key.split()))
    print(''.join(key))

    key = round(847.63/8)+4
    key = chr(key)
    key = key + key + chr(ord(key)-4)
    print("CTFlearn{", end='')
    for i in range(len(cipher)):
        a = chr(ord('a')+(cipher[i]-ord(key[i % len(key)])+26) % 26)
        print(a, end='')
    print("}")

the_simpsons()
