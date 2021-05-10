
The chanlenge is seperated into total 9 phases. It allows to skip phases to get to the phase about to solve. Answers to all phases needed to be wrapped with *"DawgCTF{}"* to be the flag.

## Phase1

Phase 1 is the easist one, checkout the code in *ulong phase1(undefined8 param_1)*, it requires reversed input to match *"Gn1r7s_3h7_Gn15Rev3R"*, so the answer is *"R3veR51nG_7h3_s7r1nG"*.

```c
  ...
  i = 0;
  sVar1 = strlen(__s);
  while( true ) {
    sVar2 = strlen("Gn1r7s_3h7_Gn15Rev3R");
    if (sVar2 <= (ulong)(long)i) break;
    sVar2 = strlen(__s);
    if (sVar2 <= (ulong)(long)i) break;
    if ("Gn1r7s_3h7_Gn15Rev3R"[i] != __s[(long)((int)sVar1 - i) + -1]) {
      local_34 = 0;
    }
    i = i + 1;
  }
  sVar1 = strlen("Gn1r7s_3h7_Gn15Rev3R");
  if ((long)i != sVar1) {
    local_34 = 0;
  }
  ...
```

## Phase2

Here is phase 2, result of xoring input and 5 should be *"Dk52m6WZw@s6w0dIZh@2m5a"*.

```c
  local_30 = 1;
  __s = (char *)calloc(0x29,1);
  getInput(2,param_1,&DAT_00102831,__s);
  local_2c = 0;
  while( true ) {
    sVar1 = strlen("Dk52m6WZw@s6w0dIZh@2m5a");
    if (sVar1 <= (ulong)(long)local_2c) break;
    sVar1 = strlen(__s);
    if (sVar1 <= (ulong)(long)local_2c) break;
    if ("Dk52m6WZw@s6w0dIZh@2m5a"[local_2c] != (byte)(__s[local_2c] ^ 5U)) {
      local_30 = 0;
    }
    local_2c = local_2c + 1;
  }
  sVar1 = strlen("Dk52m6WZw@s6w0dIZh@2m5a");
  if ((long)local_2c != sVar1) {
    local_30 = 0;
  }
```

So the answer was

```python
>>> s="Dk52m6WZw@s6w0dIZh@2m5a"
>>> ''.join(map(lambda x: chr(ord(x)^5), s))
'An07h3R_rEv3r5aL_mE7h0d'
```


## Phase3

Phase 3 check 

```c
char * func3_1(char *param_1)
{
  char cVar1;
  
  if (('@' < *param_1) && (*param_1 < '[')) {
    *param_1 = *param_1 + -0xd;
    if (*param_1 < 'A') {
      cVar1 = '\x1a';
    }
    else {
      cVar1 = '\0';
    }
    *param_1 = cVar1 + *param_1;
  }
  if (('`' < *param_1) && (*param_1 < '{')) {
    *param_1 = *param_1 + -0xd;
    if (*param_1 < 'a') {
      cVar1 = '\x1a';
    }
    else {
      cVar1 = '\0';
    }
    *param_1 = cVar1 + *param_1;
  }
  return param_1;
}

char * func3_2(char *param_1)
{
  char cVar1;
  
  if ((' ' < *param_1) && (*param_1 != '\x7f')) {
    *param_1 = *param_1 + -0x2f;
    if (*param_1 < '!') {
      cVar1 = '^';
    }
    else {
      cVar1 = '\0';
    }
    *param_1 = cVar1 + *param_1;
  }
  return param_1;
}
```

```c
ulong phase3(undefined8 param_1) {
  ...
  __s1 = (char *)calloc(0x29,1);
  getInput(3,param_1,&DAT_00102831,__s1);
  i = __s1;
  while (*i != '\0') {
    pcVar2 = (char *)func3_1(i);
    *i = *pcVar2;
    pcVar2 = (char *)func3_2(i);
    *i = *pcVar2;
    i = i + 1;
  }
  iVar1 = strcmp(__s1,"\"_9~Jb0!=A`G!06qfc8\'_20uf6`2%7");
  ...
}
```

The expected string is ``"\"_9~Jb0!=A`G!06qfc8'_20uf6`2%7"``, as there were branches in *func3_1* and *func3_2*, brute force seems simpler way to solve it.

```python
s = "\"_9~Jb0!=A`G!06qfc8'_20uf6`2%7"
ans = []
for i in range(len(s)):
    for c in range(255):
        x = func3_1(c)
        x = func3_2(x)
        if x == ord(s[i]):
            ans.append(c)
            break
            
print(''.join(map(chr, ans)))
```

The output is *D0uBl3_Cyc1iC_rO74tI0n_S7r1nGs*.

## Phase4

Phase 4 ran *func4* on each input, *func4* was a function to get the nth fibonacchi numbers. So phase 4 was about to find indics of particular fibonacchi numbers. 

```c
long func4(int param_1)
{
  long lVar1;
  long lVar2;
  
  if (param_1 < 1) {
    lVar1 = 0;
  }
  else {
    if (param_1 == 1) {
      lVar1 = 1;
    }
    else {
      lVar2 = func4((ulong)(param_1 - 1));
      lVar1 = func4((ulong)(param_1 - 2));
      lVar1 = lVar1 + lVar2;
    }
  }
  return lVar1;
}

ulong phase4(undefined8 param_1)
{
  ...
  local_5c = 1;
  local_48[0] = 1;
  local_48[1] = 0x7b;
  local_48[2] = 0x3b18;
  local_48[3] = 0x1c640d;
  iVar2 = func4(10);
  uVar4 = 0x10157f;
  __ptr = calloc(4,4);
  getInput(4,param_1,"%d%d%d%d",__ptr,(long)__ptr + 4,(long)__ptr + 8,(long)__ptr + 0xc,uVar4);
  i = 0;
  while (i < 4) {
    lVar1 = local_48[i];
    lVar3 = func4((ulong)*(uint *)((long)__ptr + (long)i * 4));
    if (lVar1 * iVar2 - lVar3 != 0) {
      local_5c = 0;
    }
    i = i + 1;
  }
  ...
}
```

Implement function *find_fibonacci_index* to return indics of given numbers.

```python
def find_fibonacci_index(values):
    ma = max(values)
    w = [0] * 100
    w[0] = 1
    w[1] = 1
    i = 2
    n = 0
    seq = [-1] * len(values)
    while n < ma:
        n = w[(i-1)%100] + w[(i-2)%100]
        w[i % 100] = n
        try:
            loc = -1
            while True:
                loc = values.index(n, loc+1, len(values)) 
                seq[loc] = i+1
        except ValueError:
            pass
        finally:
            i += 1
    return seq
```

According to function *phase4*, the fibonacchi numbers to look for indices are values in list *iVar3*, kept the name in python code.

```python
local_48 = [1, 0x7b, 0x3b18, 0x1c640d]
iVar3 = list(map(lambda v: v*0x37, local_48))
```

Finally, the output was *[10, 20, 30, 40]*, find out corresponding lines in password list *rockyou.txt*.

```bash
$ head -10 rockyou.txt |tail -1
abc123
$ head -20 rockyou.txt |tail -1
qwerty
$ head -30 rockyou.txt |tail -1
anthony
$ head -40 rockyou.txt |tail -1
123123
```

Joined them with *"_"*, the answer was *"abc123_qwerty_anthony_123123"*.

## Phase6

Phase 6 swap the 4 higher bits and the 4 lower bits of each byte in input, then xor the result with *100*, the expected output is in *local_38*.

```c
  ret = 1;
  local_38[0] = '@';
  local_38[1] = 0x77;
  local_38[2] = 0x23;
  local_38[3] = 0x91;
  local_34 = 0xb0;
  local_33 = 0x72;
  local_32 = 0x82;
  local_31 = 0x77;
  local_30 = 99;
  local_2f = 0x31;
  local_2e = 0xa2;
  local_2d = 0x72;
  local_2c = 0x21;
  local_2b = 0xf2;
  local_2a = 0x67;
  local_29 = 0x82;
  local_28 = 0x91;
  local_27 = 0x77;
  local_26 = 0x26;
  local_25 = 0x91;
  local_24 = 0;
  local_23 = 0x33;
  local_22 = 0x82;
  local_21 = 0xc4;
  __s = (char *)calloc(0x29,1);
  getInput(6,param_1,&DAT_00102831);
  i = 0;
  while( true ) {
    sVar1 = strlen(local_38);
    if (sVar1 <= (ulong)(long)i) break;
    sVar1 = strlen(__s);
    if (sVar1 <= (ulong)(long)i) break;
    __s[i] = (byte)((int)__s[i] << 4) | (byte)__s[i] >> 4;
    __s[i] = __s[i] ^ 100;
    if (__s[i] != local_38[i]) {
      ret = 0;
    }
    i = i + 1;
  }
  sVar1 = strlen(local_38);
  if ((long)i != sVar1) {
    ret = 0;
  }
```

So the answer is ``bits_swap(local_38^100)``, implemented in Python as follow.

```python
ans = [0] * len(expected)
for i in range(len(expected)):
    a = expected[i] ^ 100
    a = ((a << 4)&0xf0) | ((a >> 4)&0xf)
    ans[i] = a

print(''.join(map(chr, ans)))
```

The answer was *"B1t_Man1pUlaTi0n_1$_Fun"*.

