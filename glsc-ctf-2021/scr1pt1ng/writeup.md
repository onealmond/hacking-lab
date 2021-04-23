
Decompile ``scr1pt1ng`` with ``ghidra``, we can see that the program use predefined array ``ENCODED_FLAG`` for calculation, function ``func_3367`` is the begining of a series of ``func_xxxx`` calls,

```c
int main(void) {
  long lVar1;
  undefined8 in_RSI;
  undefined8 *puVar2;
  uint8_t decoded_flag [59];
  
  lVar1 = 7;
  puVar2 = (undefined8 *)decoded_flag;
  while (lVar1 != 0) {
    lVar1 = lVar1 + -1;
    *puVar2 = 0;
    puVar2 = puVar2 + 1;
  }
  *(undefined2 *)puVar2 = 0;
  *(undefined *)((long)puVar2 + 2) = 0;
  func_3367(puVar2,in_RSI,(long)puVar2 + 3);
  decoded_flag._0_8_ = ENCODED_FLAG._0_8_;
  decoded_flag._8_8_ = ENCODED_FLAG._8_8_;
  decoded_flag._16_8_ = ENCODED_FLAG._16_8_;
  decoded_flag._24_8_ = ENCODED_FLAG._24_8_;
  decoded_flag._32_8_ = ENCODED_FLAG._32_8_;
  decoded_flag._40_8_ = ENCODED_FLAG._40_8_;
  decoded_flag._48_8_ = ENCODED_FLAG._48_8_;
  decoded_flag[56] = ENCODED_FLAG[56];
  decoded_flag[57] = '\n';
  printf(decoded_flag);
  return 0;
}

```

There are tons of similer functions, what they do is generate two random numbers from ``rand``, if the two numbers equal to each other, go through the operation, ``ROTR``, ``ROTL``, ``MINUS``, ``PLUS`` OR ``XOR``, at the end it calls another similer function.

```c
void func_3367(void)
{
  int iVar1;
  int iVar2;
  uint8_t idx;
  
  iVar1 = rand();
  iVar2 = rand();
  if (iVar1 == iVar2) {
    ENCODED_FLAG[51] = ROTR((uint)ENCODED_FLAG[51],0xd1);
  }
  func_3769();
  return;
}
```

If we simply run the program, we got unprocessed ``ENCODED_FLAG``, a meaning less string, cause no operation is performed, we need to make the two results from ``rand()`` equal. We could create a fake library and preload when we run the program, the library provide a fake ``rand`` function to return same number every time, so we shall be able to meet the requirement of two equal random numbers.

```bash
#!/bin/bash
cat > fake-so.c << EOF
int rand(void) {return 1;}
EOF

gcc -shared -fpic fake-so.c -o fake-so.so
LD_PRELOAD=./fake-so.so ./scr1pt1ng
```

The ``exploit.sh`` generate a source file contains only fake ``rand`` function, compile with ``gcc`` to get the ``.so`` file, ``LD_PRELOAD`` allows us to do exactly what we want. Now ``scr1pt1ng`` can output the decoded flag.

```bash
GLSC{Le4rn1ng_h0w_t0_scr1pt_y0ur_t00ls_I5_very_p0werful!}
```
