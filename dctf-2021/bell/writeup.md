

According to decompiled code, needed to input number for each round to match output of *triangle* function. The total rounds to take was randomly generated.

```c
undefined8 process(uint param_1)
{
  long lVar1;
  bool isValid;
  long lVar2;
  long in_FS_OFFSET;
  uint i;
  long input;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  isValid = true;
  i = 1;
  while ((int)i <= (int)param_1) {
    lVar2 = triangle((ulong)param_1,(ulong)i,(ulong)i);
    __isoc99_scanf();
    if (lVar2 != input) {
      isValid = false;
    }
    i = i + 1;
  }
  if (isValid) {
    system("cat flag.txt");
  }
  else {
    puts("Better luck next time.");
  }
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}

long triangle(uint param_1,int param_2)
{
  long lVar1;
  long lVar2;
  
  if ((int)param_1 < param_2) {
    lVar1 = 0;
  }
  else {
    if ((param_1 == 1) && (param_2 == 1)) {
      lVar1 = 1;
    }
    else {
      if (param_2 == 1) {
        lVar1 = triangle((ulong)(param_1 - 1),(ulong)(param_1 - 1),(ulong)(param_1 - 1));
      }
      else {
        lVar2 = triangle((ulong)param_1,(ulong)(param_2 - 1U),(ulong)(param_2 - 1U));
        lVar1 = triangle((ulong)(param_1 - 1),(ulong)(param_2 - 1U),(ulong)(param_2 - 1U));
        lVar1 = lVar1 + lVar2;
      }
    }
  }
  return lVar1;
}

undefined8 main(void)
{
  int rnd;
  uint uVar1;
  time_t tVar2;
  
  tVar2 = time((time_t *)0x0);
  srand((uint)tVar2);
  rnd = rand();
  uVar1 = rnd % 5 + 8;
  printf("%d\n",(ulong)uVar1);
  process((ulong)uVar1);
  return 0;
}
```

Here is the implement of *triangle* in Python.

```python
def triangle(param_1, param_2):
    a = 0
    b = 0

    if param_1 < param_2:
        a = 0
    else:
        if param_1 == 1 and param_2 == 1:
            a = 1
        else:
            if param_2 == 1:
                a = triangle(param_1-1, param_1-1)
            else:
                b = triangle(param_1, param_2-1)
                a = triangle(param_1-1, param_2-1)
                a = a + b
    return a
```

Calculated with *triangle* for each round and sent to server, after particular number of rounds, it replied with the flag.

```python
num = int(pr.readline().decode())
print(num)
for i in range(1, num+1):
    tri = triangle(num, i)
    print(tri)
    pr.sendline(str(tri))
print(pr.readall(2))
```

```bash
$ python3 exploit.py 
[+] Opening connection to dctf-chall-bell.westeurope.azurecontainer.io on port 5311: Done
10
21147
25287
30304
36401
43833
52922
64077
77821
94828
115975
[+] Receiving all data: Done (35B)
[*] Closed connection to dctf-chall-bell.westeurope.azurecontainer.io port 5311
b'dctf{f1rst_step_t0wards_b3ll_l4bs}\n'
```

Full source code is [here](https://github.com/onealmond/hacking-lab/blob/master/dctf-2021/bell/exploit.py).
