
Seeded-random number generator in Python give same sequence everytime. Using this feature, the random number sequence used to calculate cipher text was known.   

```python
>>> import random
>>> random.seed(100)
>>> random.randint(1,100)
19
>>> random.randint(1,100)
59
>>> random.randint(1,100)
59
>>> random.randint(1,100)
99
>>> random.randint(1,100)
23
>>> random.seed(100)
>>> random.randint(1,100)
19
>>> random.randint(1,100)
59
>>> random.randint(1,100)
59
>>> random.randint(1,100)
99
>>> random.randint(1,100)
23
```

Assume ``r = pow(g, random.randrange(2, p-1), p)``, iterate through all possible characters to find plaintext that makes ``m * r % plaintext == cipher``.

```python
for c in ciphers:
    r = pow(g, random.randrange(2, p-1), p)
    for a in range(33, 127):
        if a * r % p == c:
            flag += chr(a)
            break

print(flag)
```

In the end the script bring up the flag *CCC{f13ld5_4nd_1nv3rs3s}*.
