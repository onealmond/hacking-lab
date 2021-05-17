
The cipher text looked like encoded with base64, by decoding it, got another base64 encoded text. Recursively decode the text until it failed.

```python
data = open('cipher.txt', 'rb').read()

while True:
    try:
        data = base64.b64decode(data)
    except Exception as e:
        print(data)
        print(e)
        break
```

The flag shown up.

```bash
$ python3 decode.py 
b'dctf{Th1s_l00ks_4_lot_sm4ll3r_th4n_1t_d1d}'
Invalid base64-encoded string: number of data characters (33) cannot be 1 more than a multiple of 4
```
