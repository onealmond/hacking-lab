

### The 1st Part of Kernel

```asm
     │ │    0x0040117e      498b00         mov rax, qword [r8]
     │ │    0x00401181      4831c3         xor rbx, rax
     │ │    0x00401184      48b8569ad581.  movabs rax, 0x4b227ff781d59a56
     │ │    0x0040118e      4839d8         cmp rax, rbx
     │ │    0x00401191      0f856b030000   jne loc._BadFlag
```

In *rax* is the first 8 bytes of kernel, the the expected result of xoring *rax* and *rbx* is *0x4b227ff781d59a56*. So 

```python
 kernel[:8] = 0x4b227ff781d59a56 ^ rbx
```

Value in *rbx* is calculated in *_Step1*, it seems like a input-irralevant value. A simple way to get the value would be run in debugger, break at specific point and read the value. 

```asm
     │ │    0x0040112d      4831db         xor rbx, rbx
     │ │    0x00401130      b8c5000000     mov eax, 0xc5               ; 197
     │ │    0x00401135      e8a6060000     call loc._GetTData
     │ │    0x0040113a      4889c3         mov rbx, rax
     │ │    0x0040113d      b8ab000000     mov eax, 0xab               ; 171
     │ │    0x00401142      e899060000     call loc._GetTData
     │ │    0x00401147      4801c3         add rbx, rax
     │ │    0x0040114a      b8ab030000     mov eax, 0x3ab              ; 939
     │ │    0x0040114f      e88c060000     call loc._GetTData
     │ │    0x00401154      4801c3         add rbx, rax
     │ │    0x00401157      b877020000     mov eax, 0x277              ; 631
     │ │    0x0040115c      e87f060000     call loc._GetTData
     │ │    0x00401161      4801c3         add rbx, rax
     │ │    0x00401164      b801010000     mov eax, 0x101              ; 257
     │ │    0x00401169      e872060000     call loc._GetTData
     │ │    0x0040116e      4801c3         add rbx, rax
     │ │    0x00401171      b887000000     mov eax, 0x87               ; 135
     │ │    0x00401176      e865060000     call loc._GetTData
     │ │    0x0040117b      4801c3         add rbx, rax
```

*rbx* read is *0x2a460d92f5a1f504*, so here is the first part, *Rotterda*.

```python
s = hex(0x2a460d92f5a1f504^0x4b227ff781d59a56)[2:]
param = ''.join(reversed(''.join(map(chr, [int(s[i:i+2],16) for i in range(0,len(s),2)]))))
print('part1:', param)
kernel.append(param)
```

### The 2nd Part of Kernel

```asm
     │ │    0x004011d6      b9ffffffff     mov ecx, 0xffffffff         ; -1
     │ │    0x004011db      4821c8         and rax, rcx
     │ │    0x004011de      4831db         xor rbx, rbx
     │ │    0x004011e1      418b5809       mov ebx, dword [r8 + 9]
     │ │    0x004011e5      4801d8         add rax, rbx
     │ │    0x004011e8      48b946ff6457.  movabs rcx, 0x15764ff46
     │ │    0x004011f2      4839c8         cmp rax, rcx
     │ │    0x004011f5      0f8507030000   jne loc._BadFlag
```

In *_Step3* the second part is checked, it should satisfy condition

```python
(rax&0xffffffff) + part = 0x15764ff46
```

Same way to get value in *rax*, so the second part is *P0rt*.

```python
v = data[343]
s = hex(0x15764ff46 - (v&0xffffffff))[2:]
param = ''.join(reversed(''.join(map(chr, [int(s[i:i+2],16) for i in range(0,len(s),2)]))))
print('part2:', param)
kernel.append(param)
```

### The 3rd Part of Kernel

The third part located in *_Step4a*, it needs to satisfy condition

```python
part - rbx == 0x17d4a53553
```

```asm
     │ │    0x004012d7      498b400e       mov rax, qword [r8 + 0xe]
     │ │    0x004012db      4889c1         mov rcx, rax
     │ │    0x004012de      48b8ffffffff.  movabs rax, 0xffffffffff    ; 1099511627775
     │ │    0x004012e8      4821c1         and rcx, rax
     │ │    0x004012eb      4821c3         and rbx, rax
     │ │    0x004012ee      4839d9         cmp rcx, rbx
     │ │    0x004012f1      0f820b020000   jb loc._BadFlag
     │ │    0x004012f7      4829d9         sub rcx, rbx
     │ │    0x004012fa      48b85335a5d4.  movabs rax, 0x17d4a53553
     │ │    0x00401304      4839c1         cmp rcx, rax
     │ │    0x00401307      0f85f5010000   jne loc._BadFlag
```

*rbx* got from *r2* is *0x4d998c32ff*, so the part is *Rh1ne*.

```python
s = hex(0x4d998c32ff+0x17d4a53553)[2:]
param = ''.join(reversed(''.join(map(chr, [int(s[i:i+2],16) for i in range(0,len(s),2)]))))
print('part3:', param)
kernel.append(param)
```

### The 4th Part of Kernel


```asm
     │ │    0x00401395      498b4014       mov rax, qword [r8 + 0x14]
     │ │    0x00401399      4889c1         mov rcx, rax
     │ │    0x0040139c      48b8ffffffff.  movabs rax, 0xffffffffff    ; 1099511627775
     │ │    0x004013a6      4821c1         and rcx, rax
     │ │    0x004013a9      4889c8         mov rax, rcx
     │ │    0x004013ac      4831d2         xor rdx, rdx
     │ │    0x004013af      48f7e3         mul rbx
     │ │    0x004013b2      4989c2         mov r10, rax
     │ │    0x004013b5      4989d3         mov r11, rdx
     │ │    0x004013b8      48b8beb9770a.  movabs rax, 0x37f7d400a77b9be
     │ │    0x004013c2      4c39d0         cmp rax, r10
     │ │    0x004013c5      0f8537010000   jne loc._BadFlag
     │ │    0x004013cb      48b838495487.  movabs rax, 0x6a87544938
     │ │    0x004013d5      4c39d8         cmp rax, r11
     │ │    0x004013d8      0f8524010000   jne loc._BadFlag
```

The 4th part is supposed to equal to ``0x6a8754493837f7d400a / rbx``. *rbx* is *0xdeb4fa4d998c32ff*, it makes the result a float-point number.


```python
s = hex(0x6a8754493837f7d400a77b9be//0xdeb4fa4d998c32ff)[2:]
param = ''.join(reversed(''.join(map(chr, [int(s[i:i+2],16) for i in range(0,len(s),2)]))))
```

Tried out different values at for the first character of word *?l1tz*.
- *4l1tz* leads to r11 = *0x6a8754492b*
- *6l1tz* leads to r11 = *0x6a8754492d*

So if we want the result ends with *0x38*, we need to make the first characterc ``chr(ord('6')+(0x38-(0x2d))) = 'A'``, but *Alitz* leads to r11 = *0x6a87544937*, whilst *B* is working. So the 4th part is *Bl1tz*.
param = 'B' + param
print('part4:', param)
kernel.append(param)
```

### The 5th Part of Kernel

```asm
     │ │    0x00401480      4889d8         mov rax, rbx
     │ │    0x00401483      48f7f1         div rcx
     │ │    0x00401486      4989c2         mov r10, rax
     │ │    0x00401489      4989d3         mov r11, rdx
     │ │    0x0040148c      48b89da04000.  movabs rax, loc.congrats    ; 0x40a09d ; "Congrats!! You found the flag!!\n"
     │ │    0x00401496      b852534f00     mov eax, 0x4f5352           ; 'RSO'
     │ │    0x0040149b      4c39d0         cmp rax, r10
     │ │    0x0040149e      7562           jne loc._BadFlag
     │ │    0x004014a0      48b89da04000.  movabs rax, loc.congrats    ; 0x40a09d ; "Congrats!! You found the flag!!\n"
     │ │    0x004014aa      48b8bedb3059.  movabs rax, 0x55930dbbe
     │ │    0x004014b4      4c39d8         cmp rax, r11
     │ │    0x004014b7      7549           jne loc._BadFlag
```

We need to find a divident makes

```python
rbx // part == 0x4f5352
rbx % part == 0x55930dbbe
```

Value in *rbx* is *0x1f6ff5218c40de9c*, so we have the last part *W1tte*.

```python
s = hex((0x1f6ff5218c40de9c-0x55930dbbe)//0x4f5352)[2:]
param = ''.join(reversed(''.join(map(chr, [int(s[i:i+2],16) for i in range(0,len(s),2)]))))
print('part5:', param)
kernel.append(param)
```

### The Splitter

The splitter check comes after each part, it needs to be *"_"*.

```asm
     │ │    0x00401211      418a0408       mov al, byte [r8 + rcx]
     │ │    0x00401215      4883f85f       cmp rax, 0x5f               ; 95
```

So, join all the parts we have the kernel

```bash
part1: Rotterda
part2: P0rt
part3: Rh1ne
part4: Bl1tz
part5: W1tte
Rotterda_P0rt_Rh1ne_Bl1tz_W1tte
```
