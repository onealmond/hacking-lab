
We were asked to find out where does it jump to from *0x80484e2*. The destination is stored in register *eax*.

```asm
 80484df:       8b 45 f0                mov    -0x10(%ebp),%eax
 80484e2:       ff d0                   call   *%eax <--- What address does this jump to??
```

Look back a few lines, there was a ``fgets`` call to get user input and the value is stored in *eax*. When user input is *jump*, ``fgets`` reads only 4 bytes, the last byte is set to *"\x00"* for end of string, therefore, in register *eax* the value is *006d756a* for string *"
jum\x00"*.

```asm
 80484b4:       50                      push   %eax
 80484b5:       6a 04                   push   $0x4
 80484b7:       8d 45 f0                lea    -0x10(%ebp),%eax
 80484ba:       50                      push   %eax
 80484bb:       e8 80 fe ff ff          call   8048340 <fgets@plt>
```

The coming loop increaments value in *eax* by 5 for 8 times, so when it quit the loop, *eax* became *0x006d756a+40*, which is the flag *0x6d7592* without leading zeros.

```asm
 80484cc:       8b 45 f0                mov    -0x10(%ebp),%eax
 80484cf:       83 c0 05                add    $0x5,%eax
 80484d2:       89 45 f0                mov    %eax,-0x10(%ebp)
 80484d5:       83 45 f4 01             addl   $0x1,-0xc(%ebp)
 80484d9:       83 7d f4 07             cmpl   $0x7,-0xc(%ebp)
 80484dd:       7e ed                   jle    80484cc <jump+0x3d>
```
