#!/usr/bin/env python3
import pwn

host = "not-really-math.hsc.tf"
port = 1337

def calc(s):
    parts = s.split('m')
    res = 1
    for p in parts:
        if 'a' in p:
            res *= sum(map(int, p.split('a')))
        else:
            res *= int(p)
        res %= pow(2,32)-1 
    return res

def remote():
    pr = pwn.connect(host, port)
    try:
        pr.readline()
        while True:
            s = pr.readline().decode().strip()
            print(s, end=' ')
            ans = calc(s)
            print(ans)
            pr.sendlineafter(': ', str(ans))
    except Exception as ex:
        pass
    finally:
        pr.close()

#print(calc('2m3a19m2a38m1'))
#print(calc('3a2a3m3a3'))
#print(calc('3m3a3a1a2'))
#print(calc('5m5a5m5m2m3m5m5a3m2m1a4a4m3a3'))
#print(calc('51m81m51a87m84a26a65a95a74a70'))
remote()
