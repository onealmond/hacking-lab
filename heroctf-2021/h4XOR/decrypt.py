#!/usr/bin/env python3
from pwn import xor
from random import randint
from os import urandom


output_img = open("flag.png", "wb")
input_img = open("flag.png.enc", "rb").read()

header = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00"
key = [0]*9
for i in range(9):
    key[i] = int(input_img[i]) ^ int(header[i])
output_img.write(xor(input_img, key))
