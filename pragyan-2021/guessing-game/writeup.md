The program asks us to input 10 numbers, then it do calculation with these 10 numbers, check the result with bytes stored in ``match``. Decompile the program with ``r2``, we are able to take a look into how the calculation works. 


```asm
      ...
      0x56383f24c108      488d3df90e00.  lea rdi, str.Enter_10_numbers_to_check_your_luck ; 0x56383f24d008 ; "Enter 10 numbers to check your luck"
      0x56383f24c10f      488d2d160f00.  lea rbp, [0x56383f24d02c] ; " %u"
      0x56383f24c116      e815ffffff     call sym.imp.puts
      0x56383f24c11b      488b3dc62f00.  mov rdi, qword [reloc.stdout] ; [0x56383f24f0e8:8]=0
      0x56383f24c122      e849ffffff     call sym.imp.fflush
      0x56383f24c127      660f1f840000.  nop word [rax + rax]
  ┌─> 0x56383f24c130      4889de         mov rsi, rbx
  ╎   0x56383f24c133      4889ef         mov rdi, rbp
  ╎   0x56383f24c136      31c0           xor eax, eax
  ╎   0x56383f24c138      4883c304       add rbx, 4
  ╎   0x56383f24c13c      e83fffffff     call sym.imp.__isoc99_scanf
  ╎   0x56383f24c141      4939dc         cmp r12, rbx
  └─< 0x56383f24c144      75ea           jne 0x56383f24c130
      0x56383f24c146      660fefc0       pxor xmm0, xmm0
      0x56383f24c14a      488d6c2430     lea rbp, [rsp + 0x30]
      0x56383f24c14f      4c8d642458     lea r12, [rsp + 0x58]
      0x56383f24c154      48c744245000.  mov qword [rsp + 0x50], 0
      0x56383f24c15d      0f29442430     movaps xmmword [rsp + 0x30], xmm0
      0x56383f24c162      0f29442440     movaps xmmword [rsp + 0x40], xmm0
      0x56383f24c167      660f1f840000.  nop word [rax + rax]
  ┌─> 0x56383f24c170      bb05000000     mov ebx, 5
 ┌──> 0x56383f24c175      e816ffffff     call sym.imp.rand
 ╎╎   0x56383f24c17a      314500         xor dword [rbp], eax
 ╎╎   0x56383f24c17d      83eb01         sub ebx, 1
 └──< 0x56383f24c180      75f3           jne 0x56383f24c175
  ╎   0x56383f24c182      4883c504       add rbp, 4
  ╎   0x56383f24c186      4c39e5         cmp rbp, r12
  └─< 0x56383f24c189      75e5           jne 0x56383f24c170
      0x56383f24c18b      f30f7e542450   movq xmm2, qword [rsp + 0x50]
      0x56383f24c191      f30f7e5c2420   movq xmm3, qword [rsp + 0x20]
      0x56383f24c197      660f6f442430   movdqa xmm0, xmmword [rsp + 0x30]
      0x56383f24c19d      660fef0424     pxor xmm0, xmmword [rsp]
      0x56383f24c1a2      660fefd3       pxor xmm2, xmm3
      0x56383f24c1a6      660fef05122f.  pxor xmm0, xmmword [obj.arr]
      0x56383f24c1ae      f30f7e1d2a2f.  movq xmm3, qword [0x56383f24f0e0] ; [0x56383f24f0e0:8]=0
      0x56383f24c1b6      660f6f4c2410   movdqa xmm1, xmmword [rsp + 0x10]
      0x56383f24c1bc      660fef4c2440   pxor xmm1, xmmword [rsp + 0x40]
      0x56383f24c1c2      660fef0d062f.  pxor xmm1, xmmword [0x56383f24f0d0]
      0x56383f24c1ca      660fefd3       pxor xmm2, xmm3
      0x56383f24c1ce      660f7ec0       movd eax, xmm0
      0x56383f24c1d2      3905a82e0000   cmp dword [obj.match], eax ; [0x56383f24f080:4]=0x3653a908
      ...
```

Translate it to psudocode, it gets clearer.

```python
def forward():

    for i in range(16):
      xmm0[i] ^= buf[i]

    for i in range(16):
      xmm2[i] ^= xmm3[i]

    for i in range(16):
      xmm0[i] ^= arr[i]

    xmm3 = arr[-8:]
    xmm1 = buf[16:32]

    for i in range(17):
      xmm1[i] ^= ran[16+i]

    for i in range(17):
      xmm1[i] ^= arr[16+i]
     
    for i in range(8):
      xmm2[i] ^= xmm3[i]
```

``buf`` stores the 10 numbers from input, ``arr`` above is transformation result from original one, the transformation duplicates the string ``DeltaForce`` three times, so it becomes a string of four ``DeltaForce``, here is the decompiled code snipe from ``ghidra``.

```c
  ...
  i = 10;
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  do {
    arr[i] = arr[(int)i + (int)((i & 0xffffffff) / 10) * -10];
    i = i + 1;
  } while (i != 0x28);
  ...
```

``ran`` is a list of random numbers generated from constant seeded ``rand``.

```c
  srand(0xffffff);
  ...
  do {
    j = 5;
    do {
      random = rand();
      *(uint *)p2 = *(uint *)p2 ^ random;
      j = j + -1;
    } while (j != 0);
    p2 = (long *)((long)p2 + 4);
  } while (p2 != &local_20);
  ...
```

Now we need to do reverse calculation to find out what number should we input. All calculation is byte level, so ``buf`` need to be an array of size 40.

```python
ran = [36, 184, 75, 50, 106, 222, 33, 64, 75, 253, 75, 85, 118, 114, 201, 92, 121, 55, 219, 18, 48, 67, 22, 5, 184, 96, 219, 113, 158, 97, 171, 102, 131, 244, 199, 55, 173, 40, 184, 46]
arr = [ord(c) for c in list(("DeltaForce" * 4))]
match = [8, 169, 83, 54, 120, 162, 97, 29, 81, 247, 122, 68, 111, 40, 202, 127, 57, 33, 233, 0, 64, 81, 67, 38, 190, 126, 215, 82, 253, 4, 239, 3, 49, 11, 209, 71, 226, 13, 147, 78]
buf = [0]*40
xmm1 = buf[16:32]
xmm2 = ran[32:40]
xmm3 = ran[0:16]
```

Use ``bytes_to_array`` function to conver byte string of ``match`` to integer array that can be used for calculation.

```python
def bytes_to_array(dat, sz):
    dat = dat.split()
    arr = []
    for i in range(0, len(dat), sz):
        arr.append(int(''.join(reversed(dat[i:i+sz])), 16))
    return arr

match = "08 a9 53 36 78 a2 61 1d 51 f7 7a 44 6f 28 ca 7f 39 21 e9 00 40 51 43 26 be 7e d7 52 fd 04 ef 03 31 0b d1 47 e2 0d 93 4e"
match = bytes_to_array(match, 1)
```

The random byte list can be generated from ``rand`` in glibc with seed ``0xffffff``, or copy from ``r2``.

```asm
- offset -       0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x7ffd22229560  24b8 4b32 6ade 2140 4bfd 4b55 7672 c95c  $.K2j.!@K.KUvr.\
0x7ffd22229570  7937 db12 3043 1605 b860 db71 9e61 ab66  y7..0C...`.q.a.f
0x7ffd22229580  83f4 c737 ad28 b82e 
```

According to ``forward`` operations above, here is the reverse operations.

```python
def reverse():
    xmm0 = [0] * 40

    for i in range(40):
        xmm0[i] = match[i] ^ arr[i]
    for i in range(40):
        buf[i] = xmm0[i] ^ ran[i]

    for i in range(4):
        xmm1[i] = match[16+i] ^ arr[16+i]

    for i in range(4):
        xmm1[i] ^= ran[16+i]

    buf[16:20] = xmm1[:4]

reverse()
print(' '.join([str(int.from_bytes(bytes(buf[i:i+4]),'little')) for i in range(0, len(buf), 4)]))
```

Concatenate the numbers with space as delimiter and send to the server, the flag is in response.
