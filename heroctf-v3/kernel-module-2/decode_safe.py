#!/usr/bin/env python
import string

expected = "OpenSesame"
buf = ['?']*len(expected)

for i in range(len(buf)):
    for c in string.printable:
        buf[i] = c

        if ord(buf[i]) + 0xbf < 0x1a:
            a = ord(buf[i]) - 0xd
            if ord(buf[i]) + ord('\r') < ord('['):
                a = ord(buf[i]) + ord('\r')
            buf[i] = chr(a)
        else:
            a = -0xd
            if ord(buf[i]) + 0xd < 0x7b:
                a = ord('\r')
            buf[i] = chr(ord(buf[i]) + a)

        if buf[i] == expected[i]:
            buf[i] = c
            print(buf, end='\r')
            break
        buf[i] = '?'

print()
print(''.join(buf))
