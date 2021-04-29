#!/usr/bin/env python3
# The Luhn algorithm https://www.geeksforgeeks.org/luhn-algorithm/

s = "543210******1234"

def luhn(s):
    ret = 0
    for i in range(len(s)-2, -1, -2):
        a = int(s[i]) * 2
        if a > 9:
            a = a//10 + a%10
        ret += a

    ret += sum([int(s[i]) for i in range(len(s)-1, -1, -2)])
    return ret

for i in range(0, 999999):
    t = s[:6] + str(i).rjust(6, '0') + s[-4:]
    if luhn(t) % 10 == 0 and \
        int(t) % 123457 == 0:
            print(t)
