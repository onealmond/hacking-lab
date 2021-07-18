According to the source code, given ``p`` is higher bits of ``p``, given ``q`` is lower bits of ``q``.

```python
from Crypto.Util.number import *
import binascii
flag = open('flag.txt','rb').read()
p = getPrime(1024)
q = getPrime(1024)
n = p*q
e = 2**16+1
pt = int(binascii.hexlify(flag).decode(),16)
print(p>>512)
print(q%(2**512))
print(n, e)
print(pow(pt,e,n))
```

Say ``p_hi`` and ``p_lo`` are higher bits and lower bits of ``p``, whilst ``q_hi`` and ``q_lo`` are higher bits and lower bits of ``q``. ``p`` should be ``p_hi << 512 + p_lo``, since ``n = p*q`` and ``q_lo`` is ``q mod 2**512``, ``p_lo`` should be ``n * inverse(q, 2**512) % 2**512``. When we find ``p``, ``q`` can be calculated by ``n / p``.

``d`` can then be calculated by ``inverse(e, phi)`` and ``phi`` is multiplication of ``p-1`` and ``q-1``.

```python
p = p * 2**512 + n * inverse(q, 2**512) % 2**512
q = n // p
d = inverse(e, (q-1)*(p-1))
plain = long_to_bytes(pow(cipher, d, n))
print(plain)
```
