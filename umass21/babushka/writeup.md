

In script ``babushka.py``, there are 250 functions with random generated names, half of them are not called. To seperate them we generate a list of all the random generated names in file ``func_names``, scan again to find thoses actually contribute to the final result, we only pay attention to those function listed in file ``valid_funcs``.

```bash
for f in `cat func_names`;do c=$(grep $f babushka.py |wc -l);if [ $c -gt 1 ];then echo $f:$c;fi;done > valid_funcs
```


``check_key`` takes input string as key and pads it to reach length of ``128``, return a list of boolean value, ``combiner`` takes the list as parameter, return true if particular positions in the list is ``True``.


Run ``combiner`` only with key ``UMASS``, we get a list of 23 ``False`` from ``check_key``.

```python
    key = input("Oi, babushka, what's the key? ")
    combiner = types.FunctionType(types.CodeType(*pickle.loads(b'\x80\x04\x95\xcc\x00\x00\x00\x00\x00\x00\x00]\x94(K\x01K\x00K\x00K\x04K\x03KCC@d\x01}\x01|\x00D\x00]\x0c}\x02|\x01o\x12|\x02}\x01q\x08d\x02}\x03|\x00D\x00]\x0c}\x02|\x03|\x02O\x00}\x03q\x1e|\x01s4|\x03r8d\x02p>|\x00d\x03\x19\x00S\x00\x94(N\x88\x89K\x00t\x94)(\x8c\nOUVCHXMRZO\x94\x8c\nGDOZHYKENT\x94\x8c\nTZCLOUEGVM\x94\x8c\nMMBJDKSFLR\x94t\x94\x8c\x0e<OwOwhatsthis>\x94\x8c\x0cany_combiner\x94J\xa2\xee\x81\x02C\x0e\x00\x01\x04\x01\x08\x01\n\x01\x04\x01\x08\x01\n\x01\x94))e.')), globals())

    res = check_key(key)
    print(res)
```

Create a list of 23 ``True``, change one position to ``False`` every time. As long as ``res[0]`` is ``True``, the result is ``Yes!``.

```python
    res = [True] * 23
    for i in range(len(res)):
        res[i] = False
        if combiner(res):
            print("Yes!")
        else:
            print("No!")
        res[i] = True
```

```bash
python3 babushka.py <<< UMASS
Oi, babushka, what's the key? No!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
Yes!
```

Insert debug code ``print(inspect.stack()[0].function, b)`` into each function before return, we are able to observe how return of each function affect the final result. Play around with different conditions, it seems if the ``14th`` place of list returned by ``DSIIPABGWUFNMMMZAGWI`` function is ``True``, the result is ``Yes!``.

```python
BHXFVDRTGGNFTXBCOMOJ [False, False, False, False]
BFUQBRFEKUSFTVYAIUBC [False, False, False, False, False, False, False, False]                                                                                       LXNQKJIZEUZPFAQFDWIY [False, False, False, False, False, False, False, False, False, False, False, False]
DSIIPABGWUFNMMMZAGWI [False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False]
GXMDJYHXMQHQTWTTLDEF [False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False]
AVMDIBYGKPJHLWZSFMZK [False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False]                                                                                                                                            
QHNSNERTVUQZQIOVLXHU [True, False, False, False]
...
check_key: [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True]
Yes!
```

The 14th value is controlled by bytecode in function ``DSIIPABGWUFNMMMZAGWI``. Disassemble bytecode (``code0``) in function ``DSIIPABGWUFNMMMZAGWI`` with Python module ``dis``, we get another piece of bytecode(``code1``), disassemble ``code1`` we get bytecodes (``code2``) without any further call to randomly named function. Every return appends a ``True`` or ``False`` to the list, so return of ``code1`` might give us what we what.

```python
import types,pickle,dis
code = types.CodeType(*pickle.loads(b'\x80\x04\x95\x11\x13\x00\x00\x00\x00\x00\x00]\x94(K\x01K\x00K...\x01\x14\x01\x16\x018\x01\x06\x01\x1a\x01\x0c\x01\x94))e.'))
dis.disco(code)
```

Now take a look into the dissambled ``code1``, to make it return ``True`` we need to make the key meet all the requirements here.

```asm
42069667           0 LOAD_CONST               1 (True)
                   2 STORE_FAST               1 (OVXPEYYWSK)

42069668           4 LOAD_FAST                1 (OVXPEYYWSK)
                   6 JUMP_IF_FALSE_OR_POP   198
                   8 LOAD_GLOBAL              0 (ord)
                  10 LOAD_FAST                0 (QFBKDVBLQX)
                  12 LOAD_CONST               2 (12)
                  14 BINARY_SUBSCR
                  16 CALL_FUNCTION            1
                  18 LOAD_CONST               3 (128)
                  20 BINARY_AND
                  22 LOAD_CONST               4 (7)
                  24 BINARY_RSHIFT
                  26 LOAD_CONST               5 (0)
                  28 COMPARE_OP               2 (==)
                  30 JUMP_IF_FALSE_OR_POP   198
                  32 LOAD_GLOBAL              0 (ord)
                  34 LOAD_FAST                0 (QFBKDVBLQX)
                  36 LOAD_CONST               2 (12)
                  38 BINARY_SUBSCR
                  40 CALL_FUNCTION            1
                  42 LOAD_CONST               6 (64)
                  44 BINARY_AND
                  46 LOAD_CONST               7 (6)
                  48 BINARY_RSHIFT
                  50 LOAD_CONST               8 (1)
                  52 COMPARE_OP               2 (==)
                  54 JUMP_IF_FALSE_OR_POP   198
                  56 LOAD_GLOBAL              0 (ord)
                  58 LOAD_FAST                0 (QFBKDVBLQX)
                  60 LOAD_CONST               2 (12)
                  62 BINARY_SUBSCR
                  64 CALL_FUNCTION            1
                  66 LOAD_CONST               9 (32)
                  68 BINARY_AND
                  70 LOAD_CONST              10 (5)
                  72 BINARY_RSHIFT
                  74 LOAD_CONST               8 (1)
                  76 COMPARE_OP               2 (==)
                  78 JUMP_IF_FALSE_OR_POP   198
                  80 LOAD_GLOBAL              0 (ord)
                  82 LOAD_FAST                0 (QFBKDVBLQX)
                  84 LOAD_CONST               2 (12)
                  86 BINARY_SUBSCR
                  88 CALL_FUNCTION            1
                  90 LOAD_CONST              11 (16)
                  92 BINARY_AND
                  94 LOAD_CONST              12 (4)
                  96 BINARY_RSHIFT
                  98 LOAD_CONST               5 (0)
                 100 COMPARE_OP               2 (==)
                 102 JUMP_IF_FALSE_OR_POP   198
                 104 LOAD_GLOBAL              0 (ord)
                 106 LOAD_FAST                0 (QFBKDVBLQX)
                 108 LOAD_CONST               2 (12)
                 110 BINARY_SUBSCR
                 112 CALL_FUNCTION            1
                 114 LOAD_CONST              13 (8)
                 116 BINARY_AND
                 118 LOAD_CONST              14 (3)
                 120 BINARY_RSHIFT
                 122 LOAD_CONST               8 (1)
                 124 COMPARE_OP               2 (==)
                 126 JUMP_IF_FALSE_OR_POP   198
                 128 LOAD_GLOBAL              0 (ord)
                 130 LOAD_FAST                0 (QFBKDVBLQX)
                 132 LOAD_CONST               2 (12)
                 134 BINARY_SUBSCR
                 136 CALL_FUNCTION            1
                 138 LOAD_CONST              12 (4)
                 140 BINARY_AND
                 142 LOAD_CONST              15 (2)
                 144 BINARY_RSHIFT
                 146 LOAD_CONST               5 (0)
                 148 COMPARE_OP               2 (==)
                 150 JUMP_IF_FALSE_OR_POP   198
                 152 LOAD_GLOBAL              0 (ord)
                 154 LOAD_FAST                0 (QFBKDVBLQX)
                 156 LOAD_CONST               2 (12)
                 158 BINARY_SUBSCR
                 160 CALL_FUNCTION            1
                 162 LOAD_CONST              15 (2)
                 164 BINARY_AND
                 166 LOAD_CONST               8 (1)
                 168 BINARY_RSHIFT
                 170 LOAD_CONST               5 (0)
                 172 COMPARE_OP               2 (==)
                 174 JUMP_IF_FALSE_OR_POP   198
                 176 LOAD_GLOBAL              0 (ord)
                 178 LOAD_FAST                0 (QFBKDVBLQX)
                 180 LOAD_CONST               2 (12)
                 182 BINARY_SUBSCR
                 184 CALL_FUNCTION            1
                 186 LOAD_CONST               8 (1)
                 188 BINARY_AND
                 190 LOAD_CONST               5 (0)
                 192 BINARY_RSHIFT
                 194 LOAD_CONST               8 (1)
                 196 COMPARE_OP               2 (==)
                 ...

                3976 LOAD_GLOBAL              0 (ord)
                3978 LOAD_FAST                0 (QFBKDVBLQX)
                3980 LOAD_CONST               7 (6)
                3982 BINARY_SUBSCR
                3984 CALL_FUNCTION            1
                3986 LOAD_CONST              19 (15)
                3988 BINARY_AND
                3990 LOAD_CONST              12 (4)
                3992 BINARY_XOR
                3994 LOAD_CONST               5 (0)
                3996 COMPARE_OP               2 (==)
             >> 3998 STORE_FAST               1 (OVXPEYYWSK)

42069715        4000 LOAD_FAST                1 (OVXPEYYWSK)
                4002 EXTENDED_ARG            15
                4004 JUMP_IF_FALSE_OR_POP  4020
                4006 LOAD_GLOBAL              0 (ord)
                4008 LOAD_FAST                0 (QFBKDVBLQX)
                4010 LOAD_CONST              61 (27)
                4012 BINARY_SUBSCR
                4014 CALL_FUNCTION            1
                4016 LOAD_CONST              51 (95)
                4018 COMPARE_OP               2 (==)
             >> 4020 STORE_FAST               1 (OVXPEYYWSK)

42069716        4022 LOAD_FAST                1 (OVXPEYYWSK)
                4024 BUILD_LIST               1
                4026 STORE_FAST               1 (OVXPEYYWSK)

42069717        4028 LOAD_GLOBAL              2 (types)
                4030 LOAD_METHOD              3 (FunctionType)
                4032 LOAD_GLOBAL              2 (types)
                4034 LOAD_ATTR                4 (CodeType)
                4036 LOAD_GLOBAL              5 (pickle)
                4038 LOAD_METHOD              6 (loads)
                4040 LOAD_CONST              62 (b'\x80\x04\x95\x11\x13\x00\x00...\x01\x0c\x01\x94))e.')
                4042 CALL_METHOD              1
                4044 CALL_FUNCTION_EX         0
                4046 LOAD_GLOBAL              7 (globals)
                4048 CALL_FUNCTION            0
                4050 CALL_METHOD              2
                4052 STORE_FAST               3 (RWNMTPXTXX)

42069718        4054 LOAD_FAST                3 (RWNMTPXTXX)
                4056 LOAD_FAST                0 (QFBKDVBLQX)
                4058 CALL_FUNCTION            1
                4060 LOAD_FAST                1 (OVXPEYYWSK)
                4062 BINARY_ADD
                4064 STORE_FAST               1 (OVXPEYYWSK)

42069719        4066 LOAD_FAST                1 (OVXPEYYWSK)
                4068 RETURN_VALUE
```

Translate them block by block, here is the positional values of the key according to the opcodes.

```python
s = [0]*128
s[:5] = 'UMASS'
s[5] = 123
s[6] = 112|4
s[7] = 96|8
s[8] = 51
s[9] = 80|15
s[10] = ((1<<6)&64)|((1<<5)&32)|((1<<4)&16)|((1<<1)&2)|((1<<0)&1)
s[11] = ((1<<6)&64)|((1<<5)&32)|((1<<4)&16)
s[12] = ((1<<6)&64)|((1<<5)&32)|((1<<3)&8)|((1<<0)&1)
s[13] = ((1<<5)&32)|((1<<4)&16)|((1<<0)&1)
s[14] = 49
s[15] = ((1<<6)&64)|((1<<5)&32)|((1<<0)&1)
s[16] = ((1<<6)&64)|((1<<5)&32)|((1<<2)&4)|((1<<1)&2)|((1<<0)&1)
s[17] = ((1<<5)&32)|((1<<4)&16)|((1<<1)&2)|((1<<0)&1)
s[18] = 80|15
s[19] = 98
s[20] = 112|9
s[21] = 116
s[22] = 48|3
s[23] = ((1<<6)&64)|((1<<5)&32)|((1<<1)&2)|((1<<0)&1)
s[24] = 48
s[25] = 100
s[26] = 51
s[27] = 95
s[28] = ((1<<6)&64)|((1<<5)&32)|((1<<1)&2)|((1<<0)&1)
s[29] = 112|4
s[30] = 96|6
s[31] = 116
s[32] = 96|9
s[33] = 109
s[34] = 51
s[35] = 95
s[36] = 104
s[37] = 97
s[38] = ((1<<6)&64)|((1<<5)&32)|((1<<1)&2)|((1<<0)&1)
s[39] = 96|11
s[40] = ((1<<6)&64)|((1<<5)&32)|((1<<4)&16)|((1<<3)&8)|((1<<2)&4)|((1<<0)&1)
print(''.join(s[:5])+''.join(map(chr, s[5:])))
```

Run the script and feed the output to ``babushka`` we get a ``yes!``, which means this the flag.

```bash
$ python3 key.py|python3 babushka.py
Yes!
```
