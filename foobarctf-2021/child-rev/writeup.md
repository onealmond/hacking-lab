
Run ``strings`` on ``childrev``, it shows an interesting message.

```bash
...
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
...
```

UPX is an open source executable packer, unpack it with ``upx``, now we can get on the real job.

Decompile the program in ``ghidra``, it takes user input and the four characters as parameters of ``XOR`` function, if XOR return non-zero result, the input is correct.

```c
undefined8 main(void)
{
  undefined local_38 [40];
  int local_10;
  char local_c;
  char local_b;
  char local_a;
  char local_9;
  
  printf("ENTER THE FLAG : ");
  __isoc99_scanf(&DAT_0049e182,local_38);
  local_9 = 'G';
  local_a = 'L';
  local_b = 'U';
  local_c = 'G';
  local_10 = XOR(local_38,0x47,0x4c,0x55,0x47);
  if (local_10 == 0) {
    puts("USE GHIDRA CUTTER OR IDA , THEN IT WILL BE EASY\n");
  }
  else {
    printf("YAY U MADE IT \n%c%c%c%c{%s}\n",(ulong)(uint)(int)local_9,(ulong)(uint)(int)local_a,
           (ulong)(uint)(int)local_b,(ulong)(uint)(int)local_c,local_38);
  }
  return 0;
}
```

Take a look into ``XOR`` function, it calls ``gen_key``to generate a key from the last four parameters, then ``xor`` the key with the first parameter byte by byte, finally it check whether the result match array ``DAT_0049e060``.

```c
ulong XOR(long param_1,char param_2,char param_3,char param_4,char param_5)
{
  ulong key;
  long j;
  ulong *puVar1;
  ulong *puVar2;
  byte bVar3;
  ulong local_248 [34];
  ulong auStack312 [36];
  int k;
  uint ret;
  int i;
  
  bVar3 = 0;
  key = gen_key((ulong)(uint)(int)param_2,(ulong)(uint)(int)param_3,(ulong)(uint)(int)param_4,
                (ulong)(uint)(int)param_5);
  i = 0;
  while (i < 0x22) {
    auStack312[i] = (long)*(char *)(param_1 + i) ^ key;
    i = i + 1;
  }
  j = 0x22;
  puVar1 = &DAT_0049e060;
  puVar2 = local_248;
  while (j != 0) {
    j = j + -1;
    *puVar2 = *puVar1;
    puVar1 = puVar1 + (ulong)bVar3 * 0x1ffffffffffffffe + 1;
    puVar2 = puVar2 + (ulong)bVar3 * 0x1ffffffffffffffe + 1;
  }
  ret = 0;
  k = 0;
  do {
    if (0x21 < k) {
LAB_00401e3c:
      return (ulong)ret;
    }
    if (auStack312[k] != local_248[k]) {
      ret = 0;
      goto LAB_00401e3c;
    }
    ret = 1;
    k = k + 1;
  } while( true );
}

```

The key is generated from "G", "L", "U", "G", so it's constant, by debugging it with ``r2`` we can find out the key is ``0x00012f00``.

```asm
...
0x00401d70      0fbe8da8fdff.  movsx ecx, byte [rbp - 0x258]
0x00401d77      0fbe95acfdff.  movsx edx, byte [rbp - 0x254]
0x00401d7e      0fbeb5b0fdff.  movsx esi, byte [rbp - 0x250]
0x00401d85      0fbe85b4fdff.  movsx eax, byte [rbp - 0x24c]
0x00401d8c      89c7           mov edi, eax
0x00401d8e      e81affffff     call sym.gen_key
0x00401d93      488945e8       mov qword [rbp - 0x18], rax
...
```

```bash
[0x00401cad]> dc
hit breakpoint at: 0x401d97
[0x00401d97]> dr rax
0x00012f00
```

Dump ``DAT_0049e060`` block into ``dat``, convert it to int array.

```python
dat = dat.split()
arr = []

for i in range(0, len(dat), 8):
  arr.append(int(''.join(reversed(dat[i:i+8])), 16))
```

So we can ``xor`` the ``arr`` and ``key`` to find out correct input.

```python
key = 0x00012f00
flag = [0]*0x22

for i in range(len(flag)):
    flag[i] = arr[i] ^ key

print(''.join(map(chr, flag)))
```

Enter the correct flag string, we get the actual flag in the output.

```bash
$ python3 find_flag.py | ./childrev
ENTER THE FLAG : YAY U MADE IT
{flag}
```
