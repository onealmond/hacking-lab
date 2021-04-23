

The program asks us to provide input to recover password. User input go through the following calculation, we need to find out the input that makes the result match array ``EXPECTED``.

```c
ulong update_crc_32(uint param_1,byte param_2)
{
  return (ulong)(param_1 >> 8 ^ *(uint *)(crc_tab32 + (ulong)(byte)(param_2 ^ (byte)param_1) * 4));
}
```

```c
  printf("Please provide input to recover your password: ");
  i = 0;
  while ((i < 0x40 && (iVar1 = getchar(), iVar1 != -1))) {
    input[i] = (uint8_t)iVar1;
    crc32_cur8 = update_crc_32((ulong)crc32_cur8,(ulong)input[i],(ulong)input[i]);
    masked_uint8_t = ~(byte)crc32_cur8;
    if (masked_uint8_t == EXPECTED[i]) {
      correct[i] = true;
    }
    crc32_cur16 = update_crc_32((ulong)crc32_cur16,(ulong)masked_uint8_t);
    from_blob[i] = BLOB[(int)(uint)(ushort)~(ushort)crc32_cur16];
    decrypted[i] = input[i] ^ from_blob[i];
    i = i + 1;
  }
  printf("\nRecovered password: %s\n",decrypted);
```

The idea is we minic the process, brute-force to find out the ``0x40`` characters.

```c
unsigned int update_crc32(unsigned int param1, unsigned char param2) {
    return (unsigned int)((param1 >> 8) ^ crc32_tab[(unsigned char)(param2^(unsigned char)param1)]);
}

int main() {

  unsigned int cur8 = 0xffffffff;

  for (int i = 0; i < 0x40; ++i) {
    bool found = false;
    for (unsigned int j = 0; j < 256; ++j) {
      unsigned int res = update_crc32(cur8, j);
      if ((unsigned char)(~res) == expected[i]) {
          cur8 = res;
          printf("%c", j);
          break;
      }
    }
  }
  return 0;
}
```

Dumnp the output to ``c0ll1s10ns`` we can finally get the flag.

```bash
$ g++ recover.cpp && ./a.out |./c0ll1s10ns 
Please provide input to recover your password: 
Recovered password: GLSC{hop3_th3r3_w3R3n't_t00_m4ny_c0ll1s10ns_Those_can_be_a_Pa1n}
```
