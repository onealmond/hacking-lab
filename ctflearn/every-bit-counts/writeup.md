
Decompile the program with ``ghidra`` we got a super long ``if-else`` block in *main* function. It takes *0x34* bytes of input, if every position of input meet the requirements, we found the flag. 

A simple way to figure out the correct input is to mimic the check process. We only look into those ``!= 0`` part of check, translate it to ``|=`` for corresponding positions. There are 233 of non-zero check by ``greap``.

```c
  unsigned char param[0x34] = {0};
  param[0x24] |= 0x10;
  param[0x2f] |= 0x20;
  param[0x20] |= 0x20;
  param[0x2b] |= 4;
  param[8] |= 1;
  param[0x2e] |= 4;
  param[0x30] |= 0x10;
  ...
```

In case of missing bytes, we place palceholders for those unset.

```c
  for (int i = 0; i < sizeof(param); ++i) {
    if (param[i] == 0)
      printf("+");
    else
      printf("%c", param[i]);
  }
```


In this way we got an incomplete output.

```bash
+WFlearn{w0w_you_f0und_My_fl@g_y0u_Ar3_so_much_n1c3}
```

But the missing part is easy to guess, change the first 3 chars to *"CTF"*, here comes the flag.

```
./every_bit_counts CTFlearn{w0w_you_f0und_My_fl@g_y0u_Ar3_so_much_n1c3}
Wow you found my flag!
```

Here is an interesting solution from CTFLearn community.

```python
#/usr/bin/env python3

import sys
import time

pwd = bytearray('.' * 52, 'utf8')

with open('every_bit_counts', 'rb') as f:
    f.seek(0x486)
    while True:
        code = f.read(11)
        if code != b'\x48\x8b\x45\xf0\x48\x83\xc0\x08\x48\x8b\x08':  # MOV+ADD+MOV
            break

        code = f.read(3)  # ADD (optional) + MOVSX
        if code == b'\x48\x83\xc1':
            offset = int.from_bytes(f.read(1), 'big')
            code = f.read(3)
        else:
            offset = 0

        code = f.read(3)  # AND (3 or 6 bytes)
        mask = code[2]
        if mask == 0x80:
            f.read(3)

        code = f.read(9)  # CMP + JN/JNZ
        if code[4] == 0x85:  # JNZ
            pwd[offset] &= ~mask
        else:
            pwd[offset] |= mask

        print(pwd.decode('utf8'), end='\r')
        time.sleep(0.02)
        sys.stdout.flush()
print()
```
