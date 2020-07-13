List all the numbers

```
flag = [16, 9, 3, 15, 3, 20, 6, 20, 8, 5, 14, 21, 13, 2, 5, 18, 19, 13, 1, 19, 15, 14]
```

The numbers look like index, the first 7 could be "picoCTF", could it be alphbet order?

```
chr(ord('a')+16) => q
chr(ord('a')+9) => j
```

but 
```
p = chr(ord('a')+15)
i = chr(ord('a')+8)
```

We need to minus one for each of them.
```
chr(ord('a')+16-1) => p
chr(ord('a')+9-1) => i
chr(ord('a')+3-1) => c
chr(ord('a')+15-1) => o
chr(ord('a')+3-1) => c
chr(ord('a')+20-1) => t
chr(ord('a')+6-1) => f
```

But we don't know should it be uppercase or lowercase. for uppercase flag we only need to change 'a' to 'A' and try out both flags.
It sais the uppercase one is correct.
