
The given file ``dis.txt`` is output of Python module ``dis``, simply walkthrough the operations we can recover the Python code.

```python
def func():
    fp = open('flag.txt').read()
    cipher = ''

    for i in range(len(fp)):
        temp = func2(ord(fp[i]), 170)
        cipher = cipher + chr(func2(temp, i))

    print(cipher)
    f = open('encrypted_flag.txt', 'w')
    f.write(cipher)
```

The output is also given, we can reverse the operations to find out the flag.

```python
output = 'éÿîÅËÎÞÃÙóÙÕÎÈÊúèÞÎÜÌÌÕÓÕìùÂéçÆÐþÿñÖËîÿôÿ'
decoded = []
for i in range(len(output)):
    a = ord(output[i])^i
    a = a^170
    decoded.append(a)

print(decoded)
print(''.join(map(chr, decoded)))
```
