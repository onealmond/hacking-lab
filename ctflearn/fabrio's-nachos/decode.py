#!/usr/bin/env python3
import base64
from Cryptodome.Util import number


def find_fibonacci_index(values):
    ma = max(values)

    w = [0] * 100
    w[0] = 1
    w[1] = 1
    i = 2
    n = 0
    seq = [-1] * len(values)
    while n < ma:
        n = w[(i-1)%100] + w[(i-2)%100]
        w[i % 100] = n
        try:
            loc = -1
            while True:
                loc = values.index(n, loc+1, len(values)) 
                seq[loc] = i+1
        except ValueError:
            pass
        finally:
            i += 1

    return seq

buf = open('base.txt', 'rb').read()
values = base64.b64decode(buf).split()
values = list(map(int, values))
seq = find_fibonacci_index(values)
print(seq)
print(''.join(map(chr, seq)))
