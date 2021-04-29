
Logged in to the server and launched vm by running *run*, *cat flag.txt* gave nothing. Checked out *dmesg*, it seems module *safe_mod.ko* registered a device with major number 248.

```bash
/ $ dmesg
...
[    2.128520] safe: Registering device
[    2.128934] safe: device registered with major number 248
...
```

Read from */dev/safe*, looks like we need a password.

```bash
/ $ cat /dev/safe
The safe is locked. Enter the password first.                                                                                                                       pLNL0JHJKetvAnbu
                KJeMJetvAnb u@JJK0 JPKuKrL@@/ $
```

```bash
scp -P 4822 kern2@ai.heroctf.fr/tmp/tmp.OJ9tU6gDg4/test safe_mod.ko
```

Copied ``safe_mod.ko`` to ``/mnt/share/test``, so it can be access from host, download it to local with ``scp``. Decompiled it in ``ghidra``, the two functions ``device_file_write`` and ``device_file_read`` to handle write and read events respectively. As we are going to write password to the device, take a look in to the ``device_file_write`` function.

```c
void device_file_write.cold(void)
{
  char cVar1;
  char cVar2;
  long cred;
  size_t len;
  char *cur;
  char *unaff_R12;
  int i;
  long in_GS_OFFSET;

  i = 0;
  cred = _copy_from_user();
  if (cred == 0) {
    while( true ) {
      len = strlen(unaff_R12);
      if (len <= (ulong)(long)i) break;
      cur = unaff_R12 + (long)i;
      cVar1 = *cur;
      if ((cVar1 == '\n') || (cVar1 == '\0')) break;
      if ((byte)(cVar1 + 0xbfU) < 0x1a) {
        cVar2 = cVar1 + -0xd;
        if ((char)(cVar1 + '\r') < '[') {
          cVar2 = cVar1 + '\r';
        }
        *cur = cVar2;
      }
      else {
        cVar2 = -0xd;
        if ((int)cVar1 + 0xd < 0x7b) {
          cVar2 = '\r';
        }
        *cur = cVar1 + cVar2;
      }
      i = i + 1;
    }
    cur = strstr(unaff_R12,"OpenSesame");
    if (cur != (char *)0x0) {
      if (*(long *)(&current_task + in_GS_OFFSET) == 0) {
        printk(&DAT_00100348);
      }
      else {
        printk(&DAT_00100378,(ulong)*(uint *)(*(long *)(&current_task + in_GS_OFFSET) + 0x4e8));
        cred = prepare_creds();
        if (cred == 0) {
          printk(&DAT_001003a8);
        }
        else {
          *(undefined4 *)(cred + 0x14) = 0;
          *(undefined4 *)(cred + 4) = 0;
          *(undefined4 *)(cred + 0x18) = 0;
          *(undefined4 *)(cred + 8) = 0;
          commit_creds(cred);
        }
      }
    }
    kfree();
  }
  return;
}
```

The function checks the input if everything goes well it gives root privileges to particular process via *commit_creds*. So we need to input something to make the processed string contains *"OpenSesame"*. Made *"OpenSesame"* the expected string and brute-force through all the printable characters to find the input that meets the requirement.

```python
expected = "OpenSesame"
buf = ['?']*len(expected)

for i in range(len(buf)):
    for c in string.printable:
        buf[i] = c

        if ord(buf[i]) + 0xbf < 0x1a:
            a = ord(buf[i]) - 0xd
            if ord(buf[i]) + ord('\r') < ord('['):
                a = ord(buf[i]) + ord('\r')
            buf[i] = chr(a)
        else:
            a = -0xd
            if ord(buf[i]) + 0xd < 0x7b:
                a = ord('\r')
            buf[i] = chr(ord(buf[i]) + a)

        if buf[i] == expected[i]:
            buf[i] = c
            print(buf, end='\r')
            break
        buf[i] = '?'

print()
print(''.join(buf))
```

Ran the decode script to found out the correct input is *"BcraFrfnzr"*.

```bash
/ $ echo BcraFrfnzr >/dev/safe
```

Wrote it to */dev/safe*, checked again ``dmesg``, root privileges has been given.

```bash
/ # dmesg | tail
...
[ 4348.341676] safe: user message allocated to 0x00000000a716d495
[ 4348.341725] safe: Writing 11 bytes at 0x00000000a716d495
[ 4348.341832] safe: Giving root privileges to PID 82...
```

*cat flag.txt* again, it output the flag.

```bash
/ # cat flag.txt
Hero{y0u_c4n_4ls0_Wr1t3_?!!}
```

### Reference

[modify Process Credentials In Linux Kernel](https://blog.cubieserver.de/2018/modify-process-credentials-in-linux-kernel)
