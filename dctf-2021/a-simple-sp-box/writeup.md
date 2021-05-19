
The service encrypted plain text by multiple rounds, which is determined by length of plain text, if length of plain text was odd, it appended a *'_'* to the end, then go for ``int(2 * ceil(log(len(message), 2)))`` rounds of encryption. For each round, it substituted message according to a shuffled alphabet, rearrange the message by moving all the odd positions to the head and move all the even positions to the tail.


```python
random = SystemRandom()
ALPHABET = ascii_letters + digits + "_!@#$%.'\"+:;<=}{"
shuffled = list(ALPHABET)

random.shuffle(shuffled) 
S_box = {k : v for k, v in zip(ALPHABET, shuffled)} 

def encrypt(message):
    if len(message) % 2:
        message += "_"

    message = list(message)
    rounds = int(2 * ceil(log(len(message), 2))) 

    for round in range(rounds):
        message = [S_box[c] for c in message]
        if round < (rounds-1):
            message =  [message[i] for i in range(len(message)) if i%2 == 1] + [message[i] for i in range(len(message)) if i%2 == 0]
    return ''.join(message)
```

What were known here 
- length(cipher) = length(plain) or length(plain)+1
- relative positions of each characters in message in round n and message in round n+1

What were unknown here
- alphabet mapping
- exact length of plain text

As the substitution went on in each round, like *a->b,b->c,c->d...x->y*, eventually, there was a mapping from *a* to *y*. If we could find out what mapped to what, we were able to decrypt it. The service allowed to guess 10000 times, for each time, it printed a cipher text of input if incorrect, went throught all characters in alphabet, we shall get the shuffled alphabet used by server.

```python
for _ in range(150):
    guess = input("> ").strip()
    assert 0 < len(guess) <= 10000

    if guess == flag:
        print("Well done. The flag is:")
        print(flag)
        break

    else:
        print("That doesn't look right, it encrypts to this:")
        print(encrypt(guess))
```

```bash
$ nc dctf1-chall-sp-box.westeurope.azurecontainer.io 8888
Here's the flag, please decrypt it for me:
+B22aXqqO2nxMY2x2LMy2+XXpM<xy2YLbBd0MO+j2b
> aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
That doesn't look right, it encrypts to this:
111111111111111111111111111111111111111111
> 
```

If input *'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'*, it would be encrypted to *'111111111111111111111111111111111111111111'*, so for each character in alphabet take one character from cipher text to made up shuffled alphabet.


```python
def find_shuffled():
    ALPHABET = string.ascii_letters + string.digits + "_!@#$%.'\"+:;<=}{"
    shuffled = []

    pr = pwn.connect(host, port)
    ret = ''
    try:
        pr.readline()
        line = pr.readline().strip().decode()

        for a in ALPHABET:
            pr.sendlineafter('>', a*len(line))
            pr.readline()
            enc = pr.readline().strip().decode()
            print(a, enc)
            shuffled.append(enc[0])

        for a in line:
           i = shuffled.index(a)
           ret += ALPHABET[i]
    finally:
        pr.close()
    return ret
```

By replacing alphabet, got a string *3u__Stdds_bc0h_c_f0y_3tti0xcy_hfnu}l0s3{_n*, looked like a disordered flag. The second step reorder it by moving the odds and evens back to where ther were.

```python
def decode(message):
    message = list(message)
    rounds = int(2 * ceil(log(len(message), 2))) 

    for round in range(rounds):
        if round < (rounds-1):
            odd = message[:len(message)//2]
            even = message[len(message)//2:]
            i = 0
            j = 0
            k = 0
            while i < len(odd) and j < len(even):
                if k % 2 == 1:
                    message[k] = odd[i]
                    i += 1
                else:
                    message[k] = even[j]
                    j += 1
                k += 1

            if i < len(odd):
                message[k] = odd[i]
            if j < len(even):
                message[k] = even[j]

    return ''.join(message)
```

```bash
[x] Opening connection to dctf1-chall-sp-box.westeurope.azurecontainer.io on port 8888
[x] Opening connection to dctf1-chall-sp-box.westeurope.azurecontainer.io on port 8888: Trying 20.76.178.163
[+] Opening connection to dctf1-chall-sp-box.westeurope.azurecontainer.io on port 8888: Done
a 888888888888888888888888888888888888888888
b ::::::::::::::::::::::::::::::::::::::::::
c MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
d bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
e BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
f ffffffffffffffffffffffffffffffffffffffffff
g cccccccccccccccccccccccccccccccccccccccccc
h qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq
i EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
j !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
k ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ
l ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
m yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
n oooooooooooooooooooooooooooooooooooooooooo
o ##########################################
p FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
q uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu
r @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
s 777777777777777777777777777777777777777777
t $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
u llllllllllllllllllllllllllllllllllllllllll
v }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
w zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
x 555555555555555555555555555555555555555555
y LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL
z hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
A 222222222222222222222222222222222222222222
B ..........................................
C 111111111111111111111111111111111111111111
D ++++++++++++++++++++++++++++++++++++++++++
E GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
F IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
G XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
H HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
I KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
J WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
K nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
L dddddddddddddddddddddddddddddddddddddddddd
M 444444444444444444444444444444444444444444
N gggggggggggggggggggggggggggggggggggggggggg
O 666666666666666666666666666666666666666666
P TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
Q YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
R __________________________________________
S NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN
T xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
U iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
V eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
W RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
X CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
Y ''''''''''''''''''''''''''''''''''''''''''
Z wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
0 JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ
1 SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
2 DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
3 pppppppppppppppppppppppppppppppppppppppppp
4 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
5 OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
6 tttttttttttttttttttttttttttttttttttttttttt
7 PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
8 mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
9 UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU
_ 333333333333333333333333333333333333333333
! AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
@ ==========================================
# rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
$ kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
% VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
. 999999999999999999999999999999999999999999
' aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
" 000000000000000000000000000000000000000000
+ QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ
: jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
; ssssssssssssssssssssssssssssssssssssssssss
< <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
= vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
} """"""""""""""""""""""""""""""""""""""""""
{ {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{
[*] Closed connection to dctf1-chall-sp-box.westeurope.azurecontainer.io port 8888
dctf{S0_y0u_f0und_th3_cycl3s_in_th3_s_b0x}
```
