#!/usr/bin/env python3
from subprocess import Popen, PIPE

target = 'sneks.pyc'

def bruteforce():
    output = open('output.txt', 'rb').read()
    flag = 'flag{'
    for i in range(5, len(output.split())):
        for a in range(33, 127):
            p = Popen(['python3', target, flag+chr(a)], stdout=PIPE)
            res = p.stdout.read()
            if res == output[:len(res)]:
                flag += chr(a)
                print(flag)
                break
    print(flag)

bruteforce()
