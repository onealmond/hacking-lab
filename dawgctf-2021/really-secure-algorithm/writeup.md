
Given *n*, *c*, and *e* are big. Thrown *n* into [factordb.com](http://factordb.com/), it gave the same *q* and *p*, which means ``n=pow(p,2)``. As *p* and *q* are the same, ``phi=(p-1)*(q-1)=pow(p-1,2)``

```python
from Cryptodome.Util import number

n = <very big>
c = <very big>
e = <very big>

p = <result from factordb.com>

phi = pow(p-1,2)
d = number.inverse(e, phi)
ans = pow(c, d, p)
print(number.long_to_bytes(ans))
```

Decrypted message is the flag.

```python
b'DawgCTF{sm@ll_d_b1g_dr3am5}'
```
