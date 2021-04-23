#/usr/bin/env python3

import sys
import time

pwd = bytearray('.' * 52, 'utf8')

with open('every_bit_counts', 'rb') as f:
    f.seek(0x486)
    while True:
        code = f.read(11)
        if code != b'\x48\x8b\x45\xf0\x48\x83\xc0\x08\x48\x8b\x08':  # MOV+ADD+MOV
            break

        code = f.read(3)  # ADD (optional) + MOVSX
        if code == b'\x48\x83\xc1':
            offset = int.from_bytes(f.read(1), 'big')
            code = f.read(3)
        else:
            offset = 0

        code = f.read(3)  # AND (3 or 6 bytes)
        mask = code[2]
        if mask == 0x80:
            f.read(3)

        code = f.read(9)  # CMP + JN/JNZ
        if code[4] == 0x85:  # JNZ
            pwd[offset] &= ~mask
        else:
            pwd[offset] |= mask

        print(pwd.decode('utf8'), end='\r')
        time.sleep(0.02)
        sys.stdout.flush()
print()
