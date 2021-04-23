
The program takes 26 bytes of input to encrypt and shuffle it to get another 26 bytes of output, the correct input would make the output match the array ``expected``.

```c
  printf("Enter flag [CTFlearn{ ... }]: ");
  __edflag = (int)register0x00000020 + -0x38;
  __isoc99_scanf(&DAT_00100b87);
  encrypt(local_38,__edflag);
  lVar1 = shuffle(extraout_RAX);
  i = 0;
  do {
    if (0x19 < i) {
      puts("Correct!");
LAB_00100abf:
      if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return 0;
    }
    if (expected[i] != *(char *)(lVar1 + i)) {
      puts("Incorrect");
      goto LAB_00100abf;
    }
    i = i + 1;
  } while( true );
```

As we already have the answer, can we reverse each step to find out the correct input?

```c
void * shuffle(char *param_1) {
  size_t sz;
  void *ret;
  int i;
  
  sz = strlen(param_1);
  ret = malloc(sz - 4);
  i = 0;
  while( true ) {
    sz = strlen(param_1);
    if (sz <= (ulong)(long)i) break;
    *(char *)((long)ret + (long)i) = param_1[(long)i + 1];
    i = i + 2;
  }
  i = 1;
  while( true ) {
    sz = strlen(param_1);
    if (sz <= (ulong)(long)i) break;
    *(char *)((long)ret + (long)i) = param_1[(long)i + -1];
    i = i + 2;
  }
  return ret;
}
```

First we unshuffle the expected array.

```python
def unshuffle(param):
    buf = [0] * len(param)

    for i in range(0, len(param)-1, 2):
        buf[i+1] = param[i]

    for i in range(1, len(param), 2):
        buf[i-1] = param[i]

    return buf
```

This is how it encrypts input. ``uVar2`` variable is not so clear, but check the next step, ``uVar2`` is used to access buffer starts at ``local_48``. 

```c
void encrypt(char *__block,int __edflag) {
  size_t __size;
  void *pvVar1;
  uint uVar2;
  long in_FS_OFFSET;
  int i;
  undefined4 local_48 [4];
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  __size = strlen(__block);
  pvVar1 = malloc(__size);
  local_48[0] = 1;
  local_48[1] = 3;
  local_48[2] = 3;
  local_48[3] = 7;
  local_38 = 0xde;
  local_34 = 0xad;
  local_30 = 0xbe;
  local_2c = 0xef;
  i = 0;
  while( true ) {
    __size = strlen(__block);
    if (__size <= (ulong)(long)i) break;
    uVar2 = (uint)(i >> 0x1f) >> 0x1d;
    *(byte *)((long)pvVar1 + (long)i) = __block[i] ^ (byte)local_48[(int)((i + uVar2 & 7) - uVar2)];
    i = i + 1;
  }
  if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

Check it out in ``r2``, the index goes in range *0-7*.

```asm
       ╎│   0x55c93e800883      c1ea1d         shr edx, 0x1d
       ╎│   0x55c93e800886      01d0           add eax, edx 
       ╎│   0x55c93e800888      83e007         and eax, 7
       ╎│   0x55c93e80088b      29d0           sub eax, edx 
       ╎│   0x55c93e80088d      4898           cdqe

```

```bash
Enter flag [CTFlearn{ ... }]: AAAAAAAAAAAAAAAAAAAAAAAAAA
hit breakpoint at: 0x55c93e80088d
[0x55c93e80088d]> dr rax
0x00000000                       
[0x55c93e80088d]> dc    
hit breakpoint at: 0x55c93e80088d
[0x55c93e80088d]> dr rax
0x00000001
[0x55c93e80088d]> dc
hit breakpoint at: 0x55c93e80088d
[0x55c93e80088d]> dr rax
0x00000002
[0x55c93e80088d]> dc
hit breakpoint at: 0x55c93e80088d
[0x55c93e80088d]> dr rax
0x00000003
[0x55c93e80088d]> dc
hit breakpoint at: 0x55c93e80088d
[0x55c93e80088d]> dr rax
0x00000004
[0x55c93e80088d]> dc
hit breakpoint at: 0x55c93e80088d
[0x55c93e80088d]> dr rax
0x00000005
[0x55c93e80088d]> dc
hit breakpoint at: 0x55c93e80088d
[0x55c93e80088d]> dr rax
0x00000006
[0x55c93e80088d]> dc
hit breakpoint at: 0x55c93e80088d
[0x55c93e80088d]> dr rax
0x00000007
[0x55c93e80088d]> dc
hit breakpoint at: 0x55c93e80088d
[0x55c93e80088d]> dr rax
0x00000000
```

Now we decrypt the unshuffle result to get the input.

```python
def decrypt(block):
    local_48 = [1,3,3,7, 0xde, 0xad, 0xbe, 0xef]
    buf = [0] * len(block)
    ind = 0

    for i in range(len(block)):
        buf[i] = block[i] ^ local_48[ind]
        ind = (ind+1)%len(local_48)
    return buf
```

Combine them all together to find out the flag.

```python
def backward():
    buf = unshuffle(expected)
    buf = decrypt(buf)
    print(''.join(map(chr, buf)))

backward()
```

```bash
$ py3 exploit.py | ./reverseme
Enter flag [CTFlearn{ ... }]: Correct!
$ py3 exploit.py 
CTFLearn{reversing_is_fun}
```
