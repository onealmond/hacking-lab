The flag has been encoded into string *IOWJLQMAGH* except prefix *flag{* and suffix '}', the mapping is as following.

```python
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
encoded = ""
for character in flag[5:-1]:
    encoded+=letters[(letters.index(character)+18)%26] #encode each character
```

So if we could find out the reverse mapping, we could decode the flag.

```python
r_letters = [letters[(i+18)%26] for i in range(26)]
for c in cipher:
    a = r_letters.index(c)
    print(letters[a], end='')
```

By decoding the string got the flag *flag{QWERTYUIOP}*.
