#!/usr/bin/env python3
import pwn

host = "class-meets.hsc.tf" 
port = 1337

def calc(ms, ds, me, de, i1, v1, i2, v2):
    begin = ms * 30 + ds
    end = me * 30 + de
    sched1 = 'i'*i1+'v'*v1
    sched2 = 'i'*i2+'v'*v2

    ret = 0
    s1 = 0
    s2 = 0

    for day in range(0, end+1): 
        if day % 7 in (5, 6):
            continue
        if day >= begin and sched1[s1] == sched2[s2]:
            ret += 1
        s1 = (s1+1) % len(sched1)
        s2 = (s2+1) % len(sched2)

    return ret

def remote():
    pr = pwn.connect(host, port)
    try:
        pr.readline()
        pr.readline()
        pr.readline()

        while True:
            line = pr.readline().decode().strip()
            if not line.startswith('M'):
                print(line)
                break
            ms, ds = line.split()
            me, de = pr.readline().decode().strip().split()
            i1, v1 = pr.readline().decode().strip().split()
            i2, v2 = pr.readline().decode().strip().split()

            ms = int(ms[1:])
            ds = int(ds[1:])
            me = int(me[1:])
            de = int(de[1:])
            i1 = int(i1[1:])
            v1 = int(v1[1:])
            i2 = int(i2[1:])
            v2 = int(v2[1:])

            print(f'ms={ms} ds={ds}')
            print(f'me={me} de={de}')
            print(f'i1={i1} v1={v1}')
            print(f'i2={i2} v2={v2}')

            ans = calc(ms,ds,me,de,i1,v1,i2,v2)
            print(f'ans={ans}')
            pr.sendline(str(ans))
            print(pr.readline())
            print(pr.readline())
            print(pr.readline())
        print(pr.readall(2))
    except Exception as ex:
        print(ex)
    finally:
        pr.close()


#print(calc(0,3,0,16,2,4,4,1))
#print(calc(1,5,2,28,5,2,8,3))
#print(calc(5,6,8,3,3,3,4,6))
remote()
# flag{truly_4_m45t3r_4t_c00rd1n4t1n9_5ch3dul35}
