
There were four entries in *obj.funcs*, select option 3 to enter the hidden one. 

```asm
0x00401d38      8b052aa60c00   mov eax, dword [obj.modded] ; [0x4cc368:4]=20
0x00401d3e b    83f814         cmp eax, 0x14               ; rax
```

In option 3, it requires *obj.modded* to be *0x14* to go on. *obj.modded* is increamented by one every time enter option 1, so selected option 1 for 20 times then option 3, it printed the flag.

```bash
flag{b4bys73p5upt3hm0un741n}
```
