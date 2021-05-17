
Check the jpg file out in *strings*, it shown 4 lines of encoded string, look like bas64.

```bash
$ strings The-Keymaker.jpg |head
JFIF
CTFlearn{TheKeymakerIsK00l}
b3BlbnNzbCBlbmMgLWQgLWFlcy0yNTYtY2JjIC1pdiBTT0YwIC1LIFNPUyAtaW4gZmxhZy5lbmMg
LW91dCBmbGFnIC1iYXNlNjQKCml2IGRvZXMgbm90IGluY2x1ZGUgdGhlIG1hcmtlciBvciBsZW5n
dGggb2YgU09GMAoKa2V5IGRvZXMgbm90IGluY2x1ZGUgdGhlIFMwUyBtYXJrZXIKCg==
CmmtaSHhAsK9pLMepyFDl37UTXQT0CMltZk7+4Kaa1svo5vqb6JuczUqQGFJYiycY
 , #&')*)
-0-(0%()(
((((((((((((((((((((((((((((((((((((((((((((((((((
RR=,Q
```

Decoded the 4 lines of string with base64, got a hint and a cipher text, guessed it was the encrypted flag.

```bash
hint b'openssl enc -d -aes-256-cbc -iv SOF0 -K SOS -in flag.enc -out flag -base64\n\niv does not include the marker or length of SOF0\n\nkey does not include the S0S marker\n\n'
cipher b"\x9akZHx@\xb0\xafi,\xc7\xa9\xc8P\xe5\xdf\xb5\x13]\x04\xf4\x08\xc9mfN\xfe\xe0\xa6\x9a\xd6\xcb\xe8\xe6\xfa\x9b\xe8\x9b\x9c\xcdJ\x90\x18RX\x8b'\x18"
```

The cipher text should be decrypted with AES-256-CBC, so key length is 32 bytes and IV length is 16 bytes. The hint also indicated IV starts at SOF0 marker without marker or length, key starts at SOS marker without marker. According to the JPEG spec, find SOF0 by marker *'ffc0'*, whilst key by marker *'ffda'*.

```python
def find_iv():
    begin = data.find(b'\xFF\xC0')
    iv_len = 16
    # skip marker and length
    end = begin + 4 + iv_len
    SOF0 = data[begin+4:end]
    return SOF0

def find_key():
    begin = data.find(b'\xFF\xDA')
    key_len = 32
    # skip marker
    end = begin + 2 + key_len
    SOS = data[begin+2:end]
    return SOS
```

Once key and IV are found, decrypt with AES-CBC.

```python
key = find_key()
iv = find_iv()

aes = AES.new(key, mode=AES.MODE_CBC, IV=iv)
dec = aes.decrypt(cipher)
print('flag', dec)
```

Found flag in output.

```bash
key 000c03010002110311003f00f9766bfc44beda8f3f5c031b92cb0e92d6bdc952 32
iv 0800be00c803011100021101031101ff 16
flag b'CTFlearn{Ne0.TheMatrix}        \n\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
```

*openssl* also worked.

```bash
$ openssl enc -d -aes-256-cbc -iv 0800be00c803011100021101031101ff -K 000c03010002110311003f00f9766bfc44beda8f3f5c031b92cb0e92d6bdc952 -base64 <<< "mmtaSHhAsK9pLMepyFDl37UTXQT0CMltZk7+4Kaa1svo5vqb6JuczUqQGFJYiycY" 
CTFlearn{Ne0.TheMatrix} 
```
