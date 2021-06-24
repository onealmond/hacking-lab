#!/usr/bin/env python3
import pwn

host = "extended-fibonacci-sequence-2.hsc.tf"
port = 1337

def calc(n):
    mem = [0]*1000
    mem[0] = 4
    mem[1] = 5

    ret = mem[0]*(n+1) + mem[1]*(n)

    for i in range(2, n+1):
        mem[i%len(mem)] = mem[(i-1) % len(mem)] + mem[(i-2) % len(mem)]
        ret += mem[i%len(mem)]*(n-i+1)
        if len(str(ret)) > 10:
            ret = int(str(ret)[-10:])
    return ret

def remote():
    pr = pwn.connect(host, port)
    try:
        while True:
            pr.readline()
            pr.readline()
            pr.readline()
            n = pr.readline().decode().strip()
            print(n, end=' ')
            if not n.isnumeric():
                break
            ans = calc(int(n))
            print(ans)
            pr.sendline(str(ans))
    except Exception as ex:
        print(ex)
    finally:
        pr.close()

#print(calc(30))
remote()
# flag{i_n33d_a_fl4g._s0m3b0dy_pl3ase_giv3_m3_4_fl4g.}
