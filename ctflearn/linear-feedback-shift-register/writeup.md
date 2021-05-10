
# Linear-feedback Shift Register

As the flag would be wrapped in *"CTFlearn{}"*, so the first 9 characters in plain text are known. The each character in cipher text is result of *plain[i] ^ result[i-1]*, so *cipher[i]^plain[i]* gives *result[i-1]*

```python
for i in range(len(prefix)):
    print(bin(prefix[i] ^ cipher[i])[2:].rjust(8, '0'))
```

The algorithm xor every MSB positions in previous result except the first character in plain text, MSB positions are fixed for every characters in plain text. By analysing the binary format of positional result as follow, I figured out positions to get most significant bit are 6,5,3,2 and 0.

```python
    00000101   # C
    00000010   # T
    00000001   # F
    10000000   # l
    01000000   # e
    10100000   # a
    11010000   # r
    11101000   # n
    11110100   # {
```

The decode process would looks like this.

```python
def decode():
    msb_pos = [6,5,3,2,0]
    last = 0
    last = prefix[-1] ^ cipher[len(prefix)-1]

    output=''
    for i in range(len(prefix), len(cipher)):
        last = get_next(last, msb_pos)
        output += chr(cipher[i] ^ last)
        
    print(prefix+output.encode())
```

``get_next`` takes previous result and msb positions, calculate the msb with *msb*, return result of *(msb << 7)|last >> 1)*

```python
def get_next(last, pos):
    m = msb(last, pos)
    return (m << 7)|(last >> 1)
```

*msb* takes indies of previous result of *get_next* to calculate the next most significant bit, xor bits at corresponding indies and return the msb for the next character.

```python
def msb(num, pos):
    ret = (num & (1 << pos[0])) >> pos[0]

    for p in pos[1:]:
        ret ^= (num & (1 << p)) >> p
    return ret
```

Decoded *secretMessage.hex* to get the flag.

```python
cipher = open('secretMessage.hex', 'rb').read()
decode()
```
