#!/usr/bin/env python

s = "q{vpln'bH_varHuebcrqxetrHOXEj"
output = []

for c in range(256):
    output.append([])
    for i in range(len(s)):
        a = ord(s[i]) ^ c
        if (a >= ord('a') and a <= ord('z')) or\
           (a >= ord('A') and a <= ord('Z')) or\
           (a >= ord('0') and a <= ord('9')) or\
           a == ord('_') or a == ord('{') or a == ord('}') or a == ord('@'):
           output[-1].append(chr(a))
    if output[-1] and output[-1][-1] == '}':
        print(chr(c), ''.join(output[-1]))
