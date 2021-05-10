
This challenge is similar to *Really Secure Algorithm*, except in this challenge given *n* are *c* are big, *e* is *65537*. Still needed to factorize *n*. Thrown *n* into [factordb.com](http://factordb.com/), it gave the same *q* and *p*, which means ``n=pow(p,2)``. As *p* and *q* are the same, ``phi=(p-1)*(q-1)=pow(p-1,2)``

```python
from Cryptodome.Util import number

n = <very big>
c = <very big>
e = 65537

p = <result from factordb.com>

phi = pow(p-1,2)
d = number.inverse(e, phi)
ans = pow(c, d, p)
print(number.long_to_bytes(ans))
```

Decrypted message is the flag.

```python
b'DawgCTF{wh0_n33ds_Q_@nyw@y}'
```
