# reference https://luniverse.io/cryptography-101-rsa-algorithm/?lang=ko
import Cryptodome.Util.number as number

e = 3
c = 219878849218803628752496734037301843801487889344508611639028
n = 245841236512478852752909734912575581815967630033049838269083

# factorize n @ http://factordb.com/index.php?query=245841236512478852752909734912575581815967630033049838269083
p = 416064700201658306196320137931
q = 590872612825179551336102196593

# calculate phi(n) and d
phi = (q-1)*(p-1)
d = number.inverse(e, phi)

# plaintext: M = Cᵈ (mod n)
print(number.long_to_bytes(pow(c, d, n)))
