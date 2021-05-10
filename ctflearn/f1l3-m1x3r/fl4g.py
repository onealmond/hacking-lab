#!/usr/bin/env python3

buf = open('fl4g.jpeg', 'rb').read()

fix = b''
with open('fl4g-fix.jpeg', 'wb') as fd:
    for i in range(0, len(buf), 4):
        fd.write(bytes(list(reversed(buf[i:i+4]))))

