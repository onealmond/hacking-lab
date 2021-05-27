

Ran ``exiftool -v6 Jakarta.jpg``, it shown the following bytes at the end of output.

```bash
Unknown trailer (5650 bytes at offset 0xc41e1):
c41e1: c4 4e a5 c0 71 10 e1 44 17 ca a3 a3 ee be 20 58 [.N..q..D...... X]
c41f1: 69 77 57 bc 6b 8a 85 ca cb 70 98 07 45 6d 2c 43 [iwW.k....p..Em,C]
c4201: 49 21 26 aa d5 cd 49 6a 08 e5 58 65 c4 2d 3a 5b [I!&...Ij..Xe.-:[]
c4211: 69 33 99 46 3e 76 a3 df 9f 26 20 bc 23 53 cd 22 [i3.F>v...& .#S."]
c4221: bc 1b ba 71 5e b2 a3 05 f2 fc e2 9e fd a8 4b 44 [...q^.........KD]
c4231: b0 f7 48 ed f8 7f 39 de 7c 51 db 77 98 69 2e 9b [..H...9.|Q.w.i..]
c4241: d5 aa d0 d4 ad d7 28 5e 26 6d e1 fd 4a f0 39 ce [......(^&m..J.9.]
c4251: a0 91 17 0a 08 ef a0 3f 0b dd 16 b0 2e d3 17 dd [.......?........]
...
```

Dump those bytes to *jakarta_data.py* and analyzed, found several EOF markers, *'\xff\xd9'*. Got 4 parts after splitted them by *'\xff\xd9'*.

```python
from jakarta_data import *

parts = []
data = bytes(data)
parts = data.split(b'\xff\xd9')[:-1]

for i in range(len(parts)):
    print(i, parts[i][:16], '...', parts[i][-16:], len(parts[i]))
```

```bash
0 b'\xc4N\xa5\xc0q\x10\xe1D\x17\xca\xa3\xa3\xee\xbe X' ... b'U\xba\xeb5\xac\x8d\xa3\x95\xdfw\t\t\x0b\x1e\xd0a' 3243
1 b'jnqpsu!pt\njnqpsu' ... b'qsjoubcmf`btdjj\n' 1510
2 b'$"0vts0cjo0qzuip' ... b')#Bmm!Epof"#*\n\n\n' 377
3 b'\\\xe3\x99s\xfb\xc3\x9bN\xba\xadT\xb8\xff\x06\xa3s' ... b'\x18\x18,\xffu\xa3\xd4\xc2\xece\xc0\xa0\x974d\xad' 512
```

The first part had length 3243, generated a 4096 bits RSA key at [CryptoTools](https://cryptotools.net/rsagen), the key has the same length, so part 0 was likely to be the encrypted RSA key.

*exiftool* also gave 1437 bytes of data at the second comment, analyzed it at [this site](https://www.boxentriq.com/code-breaking/text-analysis), ROT25 gave a meaningful string *"thischalle"*, decrypted it with ROT25, the plain text was a description about this challenge. Ran ROT25 on part 1, it gave some bytes look like python script, ROT -1 on each punctuation and digits, decrypted text was python script with three functions, *ReadBinaryFile*, *WriteBinaryFile* and *xorFilesAtOffset*.

Those bytes used to xor RSA key were still unknown. As a RSA key starts with *'-----BEGIN RSA PRIVATE KEY-----'*, xor the prefix and part 0 to get xor'd bytes, search these bytes in the jpg file, the match should be the bytes used to xor RSA key.

```python
jpg = open('Jakarta.jpg', 'rb').read()
rsa_prefix = b'-----BEGIN RSA PRIVATE KEY-----'
xord_offset = 0
for r in range(0, len(parts[0]), len(rsa_prefix)):
    xor_bytes = []
    for i in range(len(rsa_prefix)):
        xor_bytes.append(rsa_prefix[i]^parts[0][r+i])

    a = jpg.find(bytes(xor_bytes))
    if a != -1:
        print('found', a, r)
        xord_offset = a
        break
```

With this method, found the bytes at offset *12862*. Xor bytes start at *12862* and part 0, I managed to find the RSA key.

```python
with open('jakarta_rsa.key', 'wb') as fd:
    for i in range(len(parts[0])):
        fd.write(int.to_bytes(parts[0][i] ^ jpg[xord_offset+i], 1, 'little'))
```

So where is the flag? Part 2 and 3 were not used, one has 377 bytes, the other has 512 bytes, tried out part 3 first. Dumped part 3 to file *jakarta_flag* and uploaded it as input to [CyberChef](https://gchq.github.io/CyberChef/) *RSA Decrypt* option, choose *RSAES-PKCS1-V1_5* for encryption scheme, used previously found *jakarta_key* to decrypt it, output was the flag.

```python
with open('jakarta_flag', 'wb') as fd:
    fd.write(parts[3])
```
