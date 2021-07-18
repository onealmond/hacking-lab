#!/usr/bin/env python3
from Cryptodome.Util import number

n = 228430203128652625114739053365339856393
e = 65537
c = 126721104148692049427127809839057445790

# from factordb.com
p = 12546190522253739887
q = 18207136478875858439

d = number.inverse(e, (p-1)*(q-1))
print(number.long_to_bytes(pow(c, d, n)))
# flag{68ab82df34}
