
The service asked to decrypt the secret it sent, it would give the flag if the secret can be successfully decrypted. The key for encrypt was made from *time()*, the secret was a 16 bytes token in hex, encrypted with des3-cfb, iv is fixed, b"00000000". It allowed to guess for 3 times with timeout. To decrypt it using *Crypto.Cipher.DES3*, needed to find the same key server was used, so it's matter of time to create the key. 

```python
key = str(int(time())).zfill(16).encode("utf-8")
secret = token_hex(16)
cipher = DES3.new(key, DES3.MODE_CFB, b"00000000")
encrypted = cipher.encrypt(secret.encode("utf-8"))
```

First of all, tried to get the encrypted secret within the first timeout, that was easy with code to read the two numbers then sent the result of ``a*b``.

```python
a = randint(1000000000000000, 9999999999999999)
b = randint(1000000000000000, 9999999999999999)

print("Show me you are worthy and solve for x! You have one second.")
print("{} * {} = ".format(a, b))

answ, _ = timedInput("> ", timeOut = 1, forcedTimeout = True)

try:
    assert(a*b == int(answ))
except:
    print("You are not worthy!")
    exit(1)
```

Found out a good moment to create the key after several attempts. With one last try, server replied with the flag.

```
pr.readline()
line = pr.readline().strip().decode().split()
des3 = DES3.new(str(int(time())).zfill(16).encode("utf-8"),DES3.MODE_CFB, b"00000000")
a, b = int(line[0]), int(line[2])
print(a, b)
pr.sendlineafter('>', str(a*b))
pr.readline()
enc = bytes.fromhex(pr.readline().strip().decode())
dec = des3.decrypt(enc)
pr.sendlineafter('>', dec)
print(dec, len(dec))
print(pr.readline())
print(pr.readall(2))
```

```bash
$ python3 exploit.py 
[+] Opening connection to dctf-chall-just-take-your-time.westeurope.azurecontainer.io on port 9999: Done
3813597240164301 1847525826721293
b'ed715a18e9e8d3faffcf71cba9584777' 32
b' Congratulations! Here is your flag.\n'
[+] Receiving all data: Done (29B)
[*] Closed connection to dctf-chall-just-take-your-time.westeurope.azurecontainer.io port 9999
b'dctf{1t_0n1y_t0Ok_2_d4y5...}\n'
```

Full exploit goes [here](https://github.com/onealmond/hacking-lab/blob/master/dctf-2021/just-take-your-time/exploit.py).
