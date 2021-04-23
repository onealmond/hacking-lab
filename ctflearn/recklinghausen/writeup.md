
Function ``CheckMsg`` xor the input string with ``msg5`` array, the result is supposed to be equal to ``msg[i+2]``.

```c
undefined8 CheckMsg(char *param_1)

{
  size_t sVar1;
  long i;
  
  sVar1 = strlen(param_1);
  if ((ulong)(uint)msg5[0] != sVar1) {
    return 0;
  }
  if (msg5[0] != 0) {
    i = 0;
    do {
      if (msg5[i + 2] != (byte)(param_1[i] ^ msg5[1])) {
        return 0;
      }
      i = i + 1;
    } while ((int)i < (int)(uint)msg5[0]);
  }
  return 1;
}
```

So we could xor ``msg5[i]`` and ``msg5[i+2]`` to find out value at corresponding position of input string.

```python
def uncheck():
    buf = [0]*msg5[0]

    if msg5[0] != 0:
        for i in range(msg5[0]):
            buf[i] = msg5[i+2] ^ msg5[1]
    return buf
```

The ``msg5`` array could be obtained from ``ghidra``.

```python
def bytes_to_array(dat, sz):
    dat = dat.split()
    arr = []
    for i in range(0, len(dat), sz):
        arr.append(int(''.join(reversed(dat[i:i+sz])), 16))
    return arr

msg5 = "21 7e 3d 2a 38 12 1b 1f 0c 10 05 2c 0b 16 0c 18 1b 0d 0a 0d 0e 17 1b 12 1b 21 38 1b 0d 0a 17 08 1f 12 03"
msg5 = bytes_to_array(msg5, 1)
```

```bash
./Recklinghausen `python3 exploit.py`
Welcome to the Recklinghausen Reversing Challenge!
Compile Options: ${CMAKE_CXX_FLAGS} -O0 -fno-stack-protector -mno-sse
CONGRATULATIONS!! You found the flag!! : CTFlearn{Ruhrfestspiele_Festival}
All Done!
```
