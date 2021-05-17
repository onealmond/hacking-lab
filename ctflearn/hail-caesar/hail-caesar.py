#!/usr/bin/env python3
import base64
import string

comm1 = """/<V5;)j}j6\<Y)8><\9Fbu,Hy4ONC}pxP"4st12wn`?@O$6BgQo7i#gtD|s>3lf="""
comm2 = """2m{y!"%w2'z{&o2UfX~ws%!._s+{ (&@Vwu{ (&@_w%{v{(&0 """

def bruteforce_caesar(comm):
    for l in range(-255, 255):
        if l == 0: continue
        s = ''
        for c in comm:
            a = (ord(c)+l-32)%(127-32)+32

            if a > 0 and a < 127 and chr(a) in string.printable:
                s += chr(a)
                continue
            s = ''
            break
        if len(s) >= len(comm)/2:
            print(l, s)

bruteforce_caesar(comm1)
print('-'*80)
bruteforce_caesar(comm2)
