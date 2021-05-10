
Tried to input some invalid expressions for it to calculate, it shown error messages start with *"Unexpected"*. Decode *WeirdCalculator.apk* in *apktool* and grep the error message.

```bash
$ grep Unexpected smali/de/vidar/weirdcalculator/ -R
smali/de/vidar/weirdcalculator/Parser$AnonymousClass1InternalParser.smali:    const-string v4, "Unexpected: "
smali/de/vidar/weirdcalculator/Parser$AnonymousClass1InternalParser.smali:    const-string v6, "Unexpected: "
```

Take a look in to the smali file, in method *parseExpression* there was an array *array_0*, it seems the output is calculated by xor the array with *0x539*.

```java
.method parseExpression()D
    ...
    .line 56
    const/16 v4, 0x29

    new-array v0, v4, [I

    fill-array-data v0, :array_0

    .line 57
    .local v0, "flarry":[I
    array-length v5, v0

    const/4 v4, 0x0

    :goto_1
    if-ge v4, v5, :cond_3

    aget v1, v0, v4

    .line 58
    .local v1, "i":I
    const-string v6, "OUTPUT"

    xor-int/lit16 v7, v1, 0x539

    invoke-static {v7}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

    move-result-object v7

    invoke-static {v6, v7}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I

    .line 57
    add-int/lit8 v4, v4, 0x1

    goto :goto_1

    .line 61
    .end local v0    # "flarry":[I
    .end local v1    # "i":I
    :cond_3
    return-wide v2

    .line 56
    nop

    :array_0
    .array-data 4
        0x57f
        0x575
        0x578
        0x57e
        0x542
        0x578
        0x569
        0x572
        0x566
        0x50d
        0x557
        0x558
        0x555
        0x540
        0x54a
        0x508
        0x54a
        0x566
        0x508
        0x54a
        0x566
        0x54b
        0x50d
        0x54d
        0x551
        0x50a
        0x54b
        0x566
        0x50a
        0x558
        0x54a
        0x540
        0x566
        0x508
        0x54a
        0x557
        0x54d
        0x566
        0x508
        0x54d
        0x544
    .end array-data
.end method
```

Tried to do it in Python, it printed the flag *FLAG{APK_4nalys1s_1s_r4th3r_3asy_1snt_1t}*

```python
array_0 = [
        0x57f,
        0x575,
        0x578,
        0x57e,
        0x542,
        0x578,
        0x569,
        0x572,
        0x566,
        0x50d,
        0x557,
        0x558,
        0x555,
        0x540,
        0x54a,
        0x508,
        0x54a,
        0x566,
        0x508,
        0x54a,
        0x566,
        0x54b,
        0x50d,
        0x54d,
        0x551,
        0x50a,
        0x54b,
        0x566,
        0x50a,
        0x558,
        0x54a,
        0x540,
        0x566,
        0x508,
        0x54a,
        0x557,
        0x54d,
        0x566,
        0x508,
        0x54d,
        0x544,
        ]

for a in array_0:
    print(chr(a^0x539), end='')
```
