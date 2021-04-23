
Play the game, it allows user to go four directions, look around, take and use items, add items to inventory. The case is considered solved when stamp on the the swissblonkel scenario case, so it needs these two items in inventory and use solved stamp, then case solved and quite automatically.

```bash
a> inventory
You have a room-temperature coffee. Ew.
You have a month-old chinese food. Ew.
You have a the swissblonkel scenario. Hey, this is the case I'm supposed to solve!
You have a solved stamp. This might come in handy...
a> use solved stamp
Case solved!
```

Disassamble the program with ``ghidra``, this snipe of code looks interesting.

```c
    ... 
                  res = strcmp(action,"jhiezetfmvirlnjfbobk");
                  if (res == 0) {
                    JHIEZETFMVIRLNJFBOBK = 1;
                  }
    ...
    if (JHIEZETFMVIRLNJFBOBK != 0) {
      i = 0;
      while (i < 0x23) {
        putchar((int)(char)(LHEIBZNXEKQSAPHHUWTQ[i] ^ COJASZQHPZXKLAPHRHOK[i]));
        i = i + 1;
      }
      putchar(10);
    }
```

So if action matchs ``jhiezetfmvirlnjfbobk``, it'll print ``xor`` result of ``LHEIBZNXEKQSAPHHUWTQ`` and ``COJASZQHPZXKLAPHRHOK``, likely to be the flag.

Play again, make sure we got both stamp and the case we need to solve, before we use the stamp, perform action ``jhiezetfmvirlnjfbobk`` to toggle the flag, then use ``solved stamp``, the game exits with flag printed.

```bash
a> take the swissblonkel scenario
Got the the swissblonkel scenario!
a> go west
You are in Agency Lobby. It's late, the receptionist is out. 
To the north is Chief's Office.
To the east is Dangeresque's Office.
To the west is Alleyway.

a> go north
You are in Chief's Office. Geez, maybe I should leave. He looks pissed. 
To the south is Agency Lobby.
There are a few things here:
- solved stamp

a> take solved stamp       
Got the solved stamp!
a> jhiezetfmvirlnjfbobk                                                                                                                                                 
a> use solved stamp         
Case solved!
{Flag} !!
```
