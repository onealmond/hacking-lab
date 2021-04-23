
The program takes input from command line, which is supposed to be the flag we are looking for.

From the check bellow we know the first 9 bytes are *CTFlearn{*, no surprise.

```c
    __s = *(byte **)(argv + 8);
    i = 9;
    pbVar8 = __s;
    pbVar10 = (byte *)"CTFlearn{";
    do {
      if (i == 0) break;
      i = i + -1;
      bVar12 = *pbVar8 < *pbVar10;
      bVar13 = *pbVar8 == *pbVar10;
      pbVar8 = pbVar8 + (ulong)bVar14 * -2 + 1;
      pbVar10 = pbVar10 + (ulong)bVar14 * -2 + 1;
    } while (bVar13);
```

Notice that before the final ``strcmp``, there is a test for value in register *r13*, it needs to be *0x1c*, looks like this is the length of the string should be, we need to pass that too.

```asm
    12e7:       49 01 c5                add    %rax,%r13
    12ea:       49 83 fd 1c             cmp    $0x1c,%r13
    12ee:       75 7f                   jne    136f <main+0x22f>
    12f0:       48 89 ee                mov    %rbp,%rsi
    12f3:       4c 89 f7                mov    %r14,%rdi
    12f6:       e8 15 fe ff ff          callq  1110 <strcmp@plt>
```

Run it in ``gdb`` with test string ``CTFlearn{aaaaaaaaaaaaaaaaaa}``, set a breakpoint at the test before ``strcmp``.

```bash
$rax   : 0x00005555555580fd  →  0x000000000000007d ("}"?)
$rbx   : 0xe3
$rcx   : 0x7d
$rdx   : 0x2
$rsp   : 0x00007fffffffda90  →  0x00007fff00000079 ("y"?)
$rbp   : 0x00005555555580e0  →  "CTFlearn{Prince_Princess_Devi}"
$rsi   : 0x7d
$rdi   : 0x00005555555580fd  →  0x000000000000007d ("}"?)
$rip   : 0x00005555555552e7  →  <main+423> add r13, rax
$r8    : 0x2000
$r9    : 0x00005555555581df  →  0x0055555556aeb000
$r10   : 0x6e
$r11   : 0x246
$r12   : 0x000055555556aeb0  →  0x00005555555560c1  →  0x6c6c4100676e694b ("King"?)
$r13   : 0xffffaaaaaaaa7f21
$r14   : 0x00007fffffffdfa1  →  "CTFlearn{aaaaaaaaaaaaaaaaaa}"
$r15   : 0xc
```

The value in register *r13* is *0x1e*, no pass. But we have a string shown up at register *rbp*, *CTFlearn{Prince_Princess_Devi}*.

```bash
gef➤  registers $r13
$r13   : 0x1e 
```

If we use ``CTFlearn{Prince_Princess_Devi}``, we are not going to pass the length check, the value in register *r13* becomes *0x21*. We need to try some different strings. Take a look into the following block of code, ``bVar2`` and ``bVar3`` are values at position *0x11* and *0x16*, the later checks indidate they should both be  *0x5f*, underscore.

```c
...
bVar2 = __s[0x11];
bVar3 = __s[0x16];
...
lVar6 = __stpcpy_chk(j + 0x1040e8,
                     *(undefined8 *)(i + (ulong)((uint)(bVar2 == 0x5f) + 2) * 8),
                     (undefined8 *)((long)puVar9 - (j + 0x1040e8)));
lVar6 = __memcpy_chk(lVar6,&DAT_0010200e,2,(undefined8 *)((long)puVar9 - lVar6));
lVar6 = __stpcpy_chk(lVar6 + 1,*(undefined8 *)(i + ((ulong)(bVar3 == 0x5f) * 5 + 3) * 8),
                     0x1041df - lVar6);
...
```

With placeholders the input looks likc "CTFlearn{++++++++_++++_++++}".

```c
People'sSquareandPark.KandawgyiNaturePark.Devi.ShwedagonPagoda.BagoRiver.Thaketa.Maha.AlexanderFraser.Burma.Myanmar.Yangon.Princess.Prince.Queen.Kin
```

As the word are picked from program, we rearrange the words and add ``King`` and ``Bago`` to make it up. Input ``CTFlearn{Princess_King_Bago}`` brings us through the length check, another string shown up at address in register *rbp*.

```bash
$rax   : 0x00005555555580fb  →  0x000000000000007d ("}"?)
$rbx   : 0xe5
$rcx   : 0x7d
$rdx   : 0x2
$rsp   : 0x00007fffffffda90  →  0x00007fff00000079 ("y"?)
$rbp   : 0x00005555555580e0  →  "CTFlearn{Princess_Maha_Devi}"
$rsi   : 0x7d
$rdi   : 0x00005555555580fb  →  0x000000000000007d ("}"?)
$rip   : 0x00005555555552e7  →  <main+423> add r13, rax
$r8    : 0x2000
$r9    : 0x00005555555581df  →  0x0055555556aeb000
$r10   : 0x6e
$r11   : 0x246
$r12   : 0x000055555556aeb0  →  0x00005555555560c1  →  0x6c6c4100676e694b ("King"?)
$r13   : 0xffffaaaaaaaa7f21
$r14   : 0x00007fffffffdfa1  →  "CTFlearn{Princess_King_Bago}"
$r15   : 0xc
```

Continue to ``strcmp``, this string looks like what we are looking for and we picked the wrong words before. 

```c
strcmp@plt (
   $rdi = 0x00007fffffffdfa1 → "CTFlearn{Princess_King_Bago}",
   $rsi = 0x00005555555580e0 → "CTFlearn{Princess_Maha_Devi}",
   $rdx = 0x0000000000000002,
   $rcx = 0x000000000000007d
)
```

Run again with it, yeah, this is our flag.

```bash
CONGRATULATIONS, you found the flag:  CTFlearn{Princess_Maha_Devi}
```
