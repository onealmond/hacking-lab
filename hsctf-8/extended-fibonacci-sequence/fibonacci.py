#!/usr/bin/env python3
import pwn

host = "extended-fibonacci-sequence.hsc.tf"
port = 1337

def calc(n):
    mem = [0]*1000
    mem[1] = 1
    s = str(mem[1])
    ret = int(s[-11:])
    for i in range(2, n+1):
        mem[i%len(mem)] = mem[(i-1) % len(mem)] + mem[(i-2) % len(mem)]
        s += str(mem[i%len(mem)])
        ret += int(s[-11:])
    return int(str(ret)[-11:])

def remote():
    pr = pwn.connect(host, port)
    try:
        pr.readline()
        while True:
            n = pr.readline().decode().strip()
            print(n, end=' ')
            ans = calc(int(n))
            print(ans)
            pr.sendlineafter(': ', str(ans))
    except Exception as ex:
        pass
    finally:
        pr.close()

#print(calc(1000))
remote()
# flag{nacco_ordinary_fib}
