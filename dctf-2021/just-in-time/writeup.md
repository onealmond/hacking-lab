
There were some miss leading information here, if follow the decompiled code from *ghidra* can easily go on the wrong way, renamed some of the symbols accordingly. *file_data* was the key, it was used in the last two *copy_xor* call.

```c
undefined8 main(undefined8 param_1,undefined8 *param_2)
{
  char *__src;
  undefined8 local_58;
  undefined8 local_50;
  undefined8 local_48;
  undefined8 local_40;
  undefined4 local_38;
  undefined2 local_34;
  undefined local_32;
  char *local_30;
  char *local_28;
  char *file_data;
  
  file_data = (char *)malloc(8);
  __src = (char *)read_file(*param_2);
  strncpy(file_data,__src,8);
  local_58 = 0x486765792038261b;
  local_50 = 0x754b623167242872;
  local_48 = 0x747d4e603566227b;
  local_40 = 0x252f764e31333323;
  local_38 = 0x46313160;
  local_34 = 0x3123;
  local_32 = 0;
  local_28 = (char *)malloc(0x27);
  strncpy(local_28,(char *)&local_58,0x27);
  decrypt(local_28);
  puts("Decryption finished.");
  local_30 = (char *)malloc(0x27);
  __src = (char *)copy_xor(&local_58,file_data,file_data);
  strncpy(local_30,__src,0x27);
  local_30 = (char *)copy_xor(local_30,file_data,file_data);
  decrypt2(local_30);
  free(local_28);
  free(local_30);
  free(file_data);
  return 0;
}
```

Tried to set breakpoints after the two functions, in ``radare2`` disassembled code the function was located at ``0x55d6817f91c5``.

```asm
0x55d6817f95b3      488b55e8       mov rdx, qword [rbp - 0x18]
0x55d6817f95b7      488d45b0       lea rax, [rbp - 0x50]
0x55d6817f95bb      4889d6         mov rsi, rdx
0x55d6817f95be      4889c7         mov rdi, rax
0x55d6817f95c1      e8fffbffff     call 0x55d6817f91c5
0x55d6817f95c6      4889c1         mov rcx, rax
0x55d6817f95c9      488b45d8       mov rax, qword [rbp - 0x28]
0x55d6817f95cd      4889da         mov rdx, rbx
0x55d6817f95d0      4889ce         mov rsi, rcx
0x55d6817f95d3      4889c7         mov rdi, rax
0x55d6817f95d6      e875faffff     call sym.imp.strncpy
0x55d6817f95db      488b55e8       mov rdx, qword [rbp - 0x18]
0x55d6817f95df      488b45d8       mov rax, qword [rbp - 0x28]
0x55d6817f95e3      4889d6         mov rsi, rdx
0x55d6817f95e6      4889c7         mov rdi, rax
0x55d6817f95e9      e8d7fbffff     call 0x55d6817f91c5
0x55d6817f95ee      488945d8       mov qword [rbp - 0x28], rax
```

By checking out the result found out the flag was *dctf{df77dbe0c407dd4a188e12013ccb009f}*.

```bash
[0x7f68e5645110]> db 0x55d6817f95ee
[0x7f68e5645110]> dc
Decryption finished.
hit breakpoint at: 0x55d6817f95c6
[0x55d6817f95c6]> dr rax
0x55d682c59930
[0x55d6817f95c6]> x @rax
- offset -       0 1  2 3  4 5  6 7  8 9  A B  C D  E F  0123456789ABCDEF
0x55d682c59930  6463 7466 7b64 6637 3764 6265 3063 3430  dctf{df77dbe0c40
0x55d682c59940  3764 6434 6131 3838 6531 3230 3133 6363  7dd4a188e12013cc
0x55d682c59950  6230 3039 667d 0000 b106 0200 0000 0000  b009f}..........
0x55d682c59960  0000 0000 0000 0000 0000 0000 0000 0000  ................
0x55d682c59970  0066 6f70 656e 0073 7472 6e63 7079 0070  .fopen.strncpy.p
0x55d682c59980  7574 7300 7075 7463 6861 7200 7072 696e  uts.putchar.prin
0x55d682c59990  7466 0073 7472 6c65 6e00 6663 6c6f 7365  tf.strlen.fclose
0x55d682c599a0  006d 616c 6c6f 6300 6672 6561 6400 5f5f  .malloc.fread.__
0x55d682c599b0  6378 615f 6669 6e61 6c69 7a65 005f 5f6c  cxa_finalize.__l
0x55d682c599c0  6962 635f 7374 6172 745f 6d61 696e 0066  ibc_start_main.f
0x55d682c599d0  7265 6500 6c69 6263 2e73 6f2e 3600 474c  ree.libc.so.6.GL
0x55d682c599e0  4942 435f 322e 322e 3500 5f49 544d 5f64  IBC_2.2.5._ITM_d
0x55d682c599f0  6572 6567 6973 7465 7254 4d43 6c6f 6e65  eregisterTMClone
0x55d682c59a00  5461 626c 6500 5f5f 676d 6f6e 5f73 7461  Table.__gmon_sta
0x55d682c59a10  7274 5f5f 005f 4954 4d5f 7265 6769 7374  rt__._ITM_regist
0x55d682c59a20  6572 544d 436c 6f6e 6554 6162 6c65 0000  erTMCloneTable..
```
