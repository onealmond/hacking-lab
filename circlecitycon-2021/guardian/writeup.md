Ran the program locally it quite with segfault error, guessed it might need something like *flag.txt* to run. Create a fake flag file and run again, it worked! It asked to input a password, input something random like *'aaa'* it said incorrect and quite.   

```bash
HOOOOOOOOOO Goes there? Do you have the password?
> aaa

Hoo hoo hoo!
That is incorrect, my guardian.
```

Try again with content in the fake flag file, something interesting happend.

```bash
HOOOOOOOOOO Goes there? Do you have the password?
> this-is-fake-flag
✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  
✅  ✅  ✅  ✅  ✅  ✅  ✅  ✅  
✅  
We will do our best.....you have fought well.
```

It checks user input byte by byte, if a byte is correct it prints a check mark. Bruteforce seems like a solution. To make one guess, we need to check the number of check marks, the flag starts with *"CCC{"*, we can start from here. 

```python   
def guess(remote, flag):
    if remote:
        pr = pwn.connect(host, port)
    else:
        pr = pwn.process(target)

    try:
        pr.sendlineafter('\n> ', flag)
        ret = 0
        while True:
            line = pr.readline().strip()
            if line.startswith(b'Ho') or line.startswith(b'We'):
                break
            ret += len(line.split())
        return ret
    finally:
        pr.close()

def exploit(remote=False):

    flag = "CCC{"

    while True:
        for a in range(126, 32, -1):
            correct = guess(remote, flag+chr(a))
            if correct == len(flag)+1:
                flag += chr(a)
                print(flag)
                break

        if flag.endswith('}'):
            break

    print(flag)
```

It took quite a while to finish guessing and print the flag.

```bash
CCC{let_m3_thr0ugh!_let_me_p4ss!_d0_y0u_th1nk_y0u_c4n_h3lp_h3r?}
```
