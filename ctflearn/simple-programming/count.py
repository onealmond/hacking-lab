#!/usr/bin/env python3
from collections import Counter

total = 0

with open('data.dat') as fd:
    while True:
        line = fd.readline()
        if not line:
            break
        
        counter = Counter()
        for i in line:
            counter[i] += 1

        one = counter['1']
        zero = counter['0']

        if one % 2 == 0 or  zero % 3 == 0:
                total += 1

print(total)


