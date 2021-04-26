#!/usr/bin/env python


def init_key():
    key = [[]]
    i = ord('A')
    j = 0

    while i < ord('Z')+1:
        if len(key[-1]) == 5:
            key.append([])

        key[-1].append(chr(i))
        print(chr(i), end=' ')
        j += 1
        if j % 5 == 0:
            print()
        i+=1
        if i == ord('K'): 
            i+=1
    return key

def decode(key, enc):
    parts = enc.split(',')
    flag = ['?']*len(parts)

    for i in range(len(parts)):
        flag[i] = parts[i]
        if not parts[i][0].isdigit():
            continue
        r = 0
        c = 0
        for a in parts[i]:
            if a.isdigit():
                if r == 0:
                    r = int(a)
                else:
                    c = int(a)
        f = key[int(r)-1][int(c)-1]
        flag[i] = f

    return flag

enc = "1-3,4-4,2-1,{,4-4,2-3,4-5,3-2,1-2,4-3,_,4-5,3-5,}"
key = init_key()
flag = decode(key, enc)
print(''.join(flag))
