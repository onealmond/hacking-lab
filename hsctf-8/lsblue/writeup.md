The flag has been hidden into the image pixels using LSB, for those not familier with this kind of problem check out the links at the end.

The solution is to read pixels of the image and get the least significant bit from each pixels, concatenate them to recover the hidden information in binary, convert the binary string to characters.

```python
for j in range(h):
    for i in range(w):
        r,g,b = pixels[i,j]
        bits += bin(b)[-1]

flag = b''
for i in range(0, len(bits), 8):
    flag += chr(int(bits[i:i+8],2)).encode()
print(flag)
```

The output is long, the flag is located at the begining of the output.

```bash
#python3 lsblue.py|head -c128
#b'flag{0rc45_4r3nt_6lu3_s1lly_4895131}\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x
```

# Reference
- [What Is Stegonagraphy](https://ctf101.org/forensics/what-is-stegonagraphy/)
- [Steganography Least Significant Bit](https://www.boiteaklou.fr/Steganography-Least-Significant-Bit.html)
