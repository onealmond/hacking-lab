

It looked complicated, just ran the *interpreter bin* it gave the this output seem to be the flag.

```bash
I
n
t
e
r
p
r
e
t
e
r
_
w
r
i
t
t
e
n
_
i
n
_
C
_
i
s
_
a
_
g
r
e
a
t
_
i
d
e
a
```

Concatenated all the characters to get the flag.

```python
>>> data = open('output', 'rb').read()
>>> b''.join(data.split())
b'Interpreter_written_in_C_is_a_great_idea'
```
