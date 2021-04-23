

The script ``eat.py`` with a lot hard-to-read names, takes a string contains 9 characters as input, ``EAt`` takes two strings to output a final one, which should match *E10a23t9090t9ae0140*.

```python
def Eating(eat):
    return str(int(eat)*3)

def EAt(eat, eats):
    print(eat, eats)
    eat1 = 0
    eat2 = 0
    eat_x = 0
    eAt = ""
    while eat1 < len(eat) and eat2 < len(eats):
        if eat_x%eat_b == eat_d//eat_c:
            eAt += eats[eat2]
            eat2 += 1
        else:
            eAt += eat[eat1]
            eat1 += 1
        eat_x += 1
    return eAt

def aten(eat):
    return eat[::-1]

def eaT(eat):
    return str(int(eat[:3])*3) + eat[::-1]

def aTE(eat):
    return eat

def Ate(eat):
    return "Eat" + '9' + eat[:3]
```

We know that the expected ouput of ``EAt``, we could reverse calculate to find out the two input strings. The first string, let's say ``s1``, is composed with ``str(int(eat[:3])*3)`` and ``eat[::-1]``, the first part is number contains three digits, result of multiply 3 could be the 3-digit number or 4-digit number, the second part is reverse of input string, so we could setup two cases, *---_________* and *----_________*, placeholder *-* for digits and *_* for letters. The second string``s2`` is ``"Eat" + '9' + eat[:3]``, so the placeholder for ``s2`` is *Eat9_________*.

```python
eateat = EAt(eaT(eat), Ate(eat[::-1]))
if eateat == "E10a23t9090t9ae0140":
    flag = "eaten_" + eat
    print("absolutely EATEN!!! CTFlearn{",flag,"}")
```

As we have two cases, we would generate two possible strings, we could dump them to the ``eat.py`` script to see which one is correct. Or we can see there are some connection between ``s1`` and ``s2``, they are both using ``eat[::-1]``, so there are part of one should match part of the other. 

```python
ans = "E10a23t9090t9ae0140"

def exploit(s1):
    e1 = 0
    e2 = 0
    e3 = 0
    s2 = "Eat9___"

    while e1 < len(s1) and e2 < len(s2):
        if e3 % 3 == 2//4:
            s2 = s2[:e2] + ans[e3] + s2[e2+1:]
            e2 += 1
        else:
            s1 = s1[:e1] + ans[e3] + s1[e1+1:]
            e1 += 1
        e3 += 1 

    return s1, s2

s1, s2 = exploit("----_________")
if s1[4:7] == s2[-3:]:
    print("Case1:", str(int(s1[:4])//3) + s1[4:len(s1)-4+1][::-1])

s1, s2 = exploit("---_________")
if s1[3:6] == s2[-3:]:
    print("Case2:", str(int(s1[:3])//3) + s1[3:len(s1)-3+1][::-1])
```

By adding the part check, there is only one output.

```bash
Case1: 341eat009
```

Input the result from case1 to ``eat.py`` the flag is printed.

```bash
python3 eat.py <<< 341eat009
what's the answer
1023900tae143 Eat9900
absolutely EATEN!!! CTFlearn{ eaten_341eat009 }
```
