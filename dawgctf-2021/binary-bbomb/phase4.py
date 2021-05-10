#!/usr/bin/env python3

local_48 = [1, 0x7b, 0x3b18, 0x1c640d]
iVar3 = list(map(lambda v: v*0x37, local_48))
print(iVar3)

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
     
print(find_fibonacci_index(iVar3))
