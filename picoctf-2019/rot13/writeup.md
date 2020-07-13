ROT13 on the given string exclude the '{', '}' and '_', to simplify the process, we treat all the letter as lowercase.

```
s = 'cvpbPGS{abg_gbb_onq_bs_n_ceboyrz}'
''.join(list(map(lambda c: chr(ord('a')+(ord(c.lower())-ord('a')+13)%26) if c not in ('{','}','_') else c,s)))
```

uppercase 'ctf' in converted string to get the flag.
