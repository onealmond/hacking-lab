At the end of the given image there is the following piece of code.

```bash
$ strings 840828909.jpg |tail -5
Ahh! Realistically the Simpsons would use octal instead of decimal!
encoded = 152 162 152 145 162 167 150 172 153 162 145 170 141 162
key = chr(SolutionToDis(110 157 167 040 155 165 143 150 040 144 151 144 040 115 141 147 147 151 145 040 157 162 151 147 151 156 141 154 154 171 040 143 157 163 164 077 040 050 104 151 166 151 144 145 144 040 142 171 040 070 054 040 164 157 040 164 150 145 040 156 145 141 162 145 163 164 040 151 156 164 145 147 145 162 054 040 141 156 144 040 164 150 145 156 040 160 154 165 163 040 146 157 165 162 051))
key = key + key + chr(ord(key)-4)
print(DecodeDat(key=key,text=encoded))
```

According to the hints of finger number, the encoded text and key are octal. Decoded the key it says

```bash
How much did Maggie originally cost? (Divided by 8, to the nearest integer, and then plus four)
```

Searched around, I found this [post](https://screenrant.com/simpsons-opening-credits-maggie-cash-register-money-change-reason/).

> "In the original opening sequence, Maggie is rung up at a price of $847.63. This number wasn’t a random one, and was actually the monthly cost of raising a child back in 1989 – a subtle and clever detail."


The original cost is *847.63*, so according to the code snippet the key is *nnj*.

```python
key = round(847.63/8)+4
key = chr(key)
key = key + key + chr(ord(key)-4)
```

Decrypted cipher text with *Vigenère Cipher* got the kernel of flag, wrapping it with *CTFlearn{}* is the flag *CTFlearn{wearenumberone}*.

```python
cipher = list(map(lambda x: int(x, 8), encoded.split()))
for i in range(len(cipher)):
    a = chr(ord('a')+(cipher[i]-ord(key[i % len(key)])+26) % 26)
    print(a, end='')
```

