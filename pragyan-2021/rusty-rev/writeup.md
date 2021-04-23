
Connect to the server with ``nc``, we were given an encrypted flag.

```c
JcOCLQgPJEjwNAZHgVFzAoMVHOiCRVAVKkvFidUvzmUSSnqJzO
```

The program used to encrypt the flag is also given. To run it we need to create a fake flag file locally. Decompile the program doesn't provide much helpful information, except tons of rust system function calls, and it loads plain text flag from file ``flag.txt``, call an encrypt function to do the dirty work, then output the encrypted flag. Try out different strings, it seems there is some character level mapping between plain text and encrypted one. So maybe we could brute-force to find out the plain text flag.

The encrypt flag has length of 50 bytes, possible characters for creating the flag include uppercase and lowercase letters, digits and punctuations, let's try underline and dash first. So we generate the flag file, launch the program to output the encrypt flag, compare the output with the given flag character by character, add it to result list if match.

```python
enc_flag = 'JcOCLQgPJEjwNAZHgVFzAoMVHOiCRVAVKkvFidUvzmUSSnqJzO'
flag = []
pat = re.compile('Flag: (\w+)\n')
candidates = string.ascii_lowercase+string.ascii_uppercase+string.digits+'_'+'-'

for k in range(len(enc_flag)):
    for c in candidates:
        with open('flag.txt', 'w') as fd:
            fd.write(''.join(flag)+c)
        p = Popen(['./revme'], stdout=PIPE)
        enc = pat.search(p.stdout.read().decode()).group()[6:].strip()
        if enc[k] == enc_flag[k]:
            flag.append(c)
            break

print(''.join(flag))
```

Finally join all the characters we get the plain text flag.
