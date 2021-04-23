 
Disassemble the program with ``ghidra``, looks like the program take a string as parameter on startup and does some calculation with it, at the end, compares the result with string ``lfmhjmnahapkechbanheabbfjladhbplbnfaijdajpnljecghmoafbljlaamhpaheonlmnpmaddhngbgbhobgnofjgeaomadbidl``, if match the given string is the key, we need to ``xor`` the key with the string in ``flag.txt`` to get the flag.

```c
...
// calculate with the given string
while( true ) {
  iVar3 = valid_char((ulong)(uint)(int)param[i]);
  if (iVar3 == 0) break;
  if (i == 0) {
    cVar1 = jumble();
    bVar2 = (byte)(cVar1 >> 7) >> 4;
    buf[0] = (cVar1 + bVar2 & 0xf) - bVar2;
  }
  else {
    cVar1 = jumble();
    bVar2 = (byte)((int)cVar1 + (int)buf[i + -1] >> 0x37);
    buf[i] = ((char)((int)cVar1 + (int)buf[i + -1]) + (bVar2 >> 4) & 0xf) - (bVar2 >> 4);
  }
  i = i + 1;
}
j = 0;
while (j < i) {
  buf[j] = buf[j] + 'a';
  j = j + 1;
}
// check whether input is the key
if (i == 100) {
  iVar3 = strncmp(buf,
                  "lfmhjmnahapkechbanheabbfjladhbplbnfaijdajpnljecghmoafbljlaamhpaheonlmnpmaddhngbgbhobgnofjgeaomadbidl"
                  ,100);
  if (iVar3 == 0) {
    puts("You got the key, congrats! Now xor it with the flag!");
    uVar4 = 0;
    goto LAB_001009ea;
  }
}
...
```

From ``valid_char`` we know that the string should be composed with ``0123456789abcdef``. So we need to guess a 100 bytes string with ``0123456789abcdef``.

```c
undefined8 valid_char(char param_1)
{
  undefined8 valid;
  
  if ((param_1 < '0') || ('9' < param_1)) {
    if ((param_1 < 'a') || ('f' < param_1)) {
      valid = 0;
    }
    else {
      valid = 1;
    }
  }
  else {
    valid = 1;
  }
  return valid;
}
```

Each byte is calculated based on the one before it, except the first one. We could generate possible strings and check if the first *n* bytes matchs the first *n* bytes of the target string. Trace the system call of ``strncmp`` we could get the result string.

```bash
$ ltrace -s 1000 ./otp aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
strncpy(0x7ffe7018cfb0, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", 100) = 0x7ffe7018cfb0
strncmp("fkpejodinchmbglafkpejodinchmbglafkpejodinchmbglafkpejodinchmbglafkpejodinchmbglafkpejodinchmbglafkpe\376\177", "lfmhjmnahapkechbanheabbfjladhbplbnfaijdajpnljecghmoafbljlaamhpaheonlmnpmaddhngbgbhobgnofjgeaomadbidl", 100) = -6
puts("Invalid key!"Invalid key!
)                                                                                    = 13
+++ exited (status 1) +++
```

Now we need to parse the output of ``ltrace`` to get the result string, then we compare it with the target string.

```python
for i in range(target_len):
    for x in sample:
        key[i] = x
        p = Popen(['ltrace', '-s', '1000', './otp', ''.join(key)], stderr=PIPE, stdout=DEVNULL)
        output = p.stderr.read().decode()
        res = re.search('strncmp\(\"(.+)\".+\)', output).group(1)[:100]
        if target[i] == res[i]:
            break
```

Finally, ``xor`` the key with ``flag.txt`` to decode the flag.

```python
''.join([chr(x^y) for x, y in zip(bytes.fromhex(''.join(key)), bytes.fromhex(flag))])
```
