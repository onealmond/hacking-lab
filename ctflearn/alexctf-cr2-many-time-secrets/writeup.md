
As the key is partially known, the prefix *"ALEXCTF{"*, we shall be able to get part of the plain text by xor it with the cipher text. 

```python
plain = [chr(msg[i] ^ ord(prefix[i])) for i in range(len(prefix))]
print(''.join(plain))
```

The decoded text is *"Dear Fri"*, guessed the plain text starts with *"Dear Friend"*. Decrypt key with it we got *"ALEXFLAG{HER"*.

```python
prefix = ''.join(map(chr, [msg[i] ^ ord(plain[i]) for i in range(len(plain))]))
```

Guessed the following characters are "E_", so the decrypted key became *"ALEXFLAG{HERE_"*. So the plain text starts with *"Dear Friend, "*. Tried to decrypt the whole plain text with it, we found some meaningful words in partially decoded plain text.

```python
plain = ''.join(map(chr, [msg[i] ^ ord(prefix[i%len(prefix)]) for i in range(len(msg))]))
print(plain)
```

```bash
Dear Friend, Rkix<tgSr.^<Wnderstood my kjs}kkv`s<Wsed One time vbd+ynmLn~cuMn scheme, I hcbro<tf_c.~his the only eh`rrltgQy.zyVhod that is mgwhnqazWto{p[ proven to be&mo<c|_terxever if the kcz bo e[gz7oGcure, Let Me mmo|<ihnab<Cgree with me rl ~oe.Jgd<Gncryption schcne+}ly_n}9
```

Tried to fix some understanable words and decode the key with it.

```python
i = plain.find('nderstood')
plain = plain[:i-1] + 'u' + plain[i:]
i = plain.find('sed', i)
plain = plain[:i-1] + 'u' + plain[i:]
i = plain.find('time ', i)
plain = plain[:i+5] + 'padding' + plain[i+5+7:]
i = plain.find("kcz", i)
plain = plain[:i] + 'key' + plain[i+3:]
i = plain.find("gree", i)
plain = plain[:i-1] + 'a' + plain[i:]
i = plain.find("ncryption", i)
plain = plain[:i-1] + 'e' + plain[i:]
i = plain.find("schcne", i)
plain = plain[:i] + 'scheme' + plain[i+6:]
print(plain)

prefix = ''.join(map(chr, [msg[i] ^ ord(plain[i]) for i in range(len(plain))]))
print(prefix)
```

In the output, we can find the next word of key *"GOES"*, so now the decrypted key became *"ALEXCTF{HERE_GOES"*.

```bash
Dear Friend, Rkix<tgSr.^<understood my kjs}kkv`s<used One time paddingLn~cuMn scheme, I hcbro<tf_c.~his the only eh`rrltgQy.zyVhod that is mgwhnqazWto{p[ proven to be&mo<c|_terxever if the key bo e[gz7oGcure, Let Me mmo|<ihnab<agree with me rl ~oe.Jgd<encryption scheme+}ly_n}9
ALEXCTF{HERE_ALEXCTF{HERE}ALEXCTF{HERE_ALEXCTF{HERE}ALEXCTF{HERE_GOESTL{HERE_ALEXCTF{HERE_ALEXCTF{HERE_ALEXCTF{HERE_ALEXCTF{HERE_ALEXCTF{HERE_ALEXCTF{HERE_ALEXCTF{HERE_ALEXCTF{HERE_ALEXCTF{HERE_GOEXCTF{HERE_ALEXCTF{HERE_ALEXCTF{HERE}ALEXCTF{HERE_ALEXCTF{HERE}ALEXCTF{HERE_GOEXCTF{HER
```

We are looking for flag, so could it be *"HERE_GOES_THE_FLAG"*? The decoded text is different, still not done yet, but we can see some more meaningful words.

```bash
Dear Friend, This time-@8Onderstood my mistake acm8Osed One time pad encry}}qUn scheme, I heard that-`lis the only encryption-d}Nhod that is mathematicletC proven to be not cracfl|ever if the key is kepy)k_cure, Let Me know if yb|8[gree with me to use thdz8_ncryption scheme alway~'
```

Tried to fix some of them and decode the key.

```python
i = plain.find("-@8O")
plain = plain[:i] + " I u" + plain[i+4:]
i = plain.find("encry", i)
plain = plain[:i+5] + "ption" + plain[i+5+5:]
i = plain.find("-d}Nhod", i)
plain = plain[:i] + " method" + plain[i+7:]
i = plain.find("cracfl", i)
plain = plain[:i+4] + "ked " + plain[i+4+4:]
i = plain.find("kepy", i)
plain = plain[:i+3] + "t secure" + plain[i+3+8:]
i = plain.find("yb|8[", i)
plain = plain[:i] + "you a" + plain[i+5:]
i = plain.find("thdz8_n", i)
plain = plain[:i] + "this e" + plain[i+6:]
plain = plain[:-1] + "s"
print(plain)

prefix = ''.join(map(chr, [msg[i] ^ ord(plain[i]) for i in range(len(plain))]))
print(prefix)
```

Now we could identitfy the flag *"ALEXCTF{HERE_GOES_THE_KEY}"*.

```bash
ALEXCTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOES_THE_FLAGALEXCTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOES_THE_FLAGALEXCTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOES_THE_FLAGALEXCTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOES_THE_F
```

Verified the key by decrypt the whold cipher text with it.

```python
prefix = "ALEXCTF{HERE_GOES_THE_KEY}"
plain = ''.join(map(chr, [msg[i] ^ ord(prefix[i%len(prefix)]) for i in range(len(msg))]))
print(plain)
```

Here is the plain text and the above is the right key, also the flag.

```bash
Dear Friend, This time I understood my mistake and used One time pad encryption scheme, I heard that it is the only encryption method that is mathematically proven to be not cracked ever if the key is kept secure, Let Me know if you agree with me to use this encryption scheme always.
```
