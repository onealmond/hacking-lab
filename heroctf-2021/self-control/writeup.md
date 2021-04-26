
We are required to fix a corrupted elf file by patch two bytes at particular position. Chec it with ``readelf`` first.

```bash
$ readelf -h READFLAG 
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Shared object file)
  Machine:                           Intel IA-64
  Version:                           0x1
  Entry point address:               0x10a1
  Start of program headers:          64 (bytes into file)
  Start of section headers:          15040 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         11
  Size of section headers:           64 (bytes)
  Number of section headers:         30
  Section header string table index: 29
```

Machine looks unusal and ``objdump`` complains *architecture UNKNOWN*. To continue analyse it with local analyse tools we need to change it to *AMD x86-64 architecture*, which is *62* for the *e_machine* field of ELF header *Elf64_Ehdr*.

```bash
$ objdump -D READFLAG 

READFLAG:     file format elf64-little

objdump: can't disassemble for architecture UNKNOWN!
```

For 64bits machine, *e_machine* is located at the 19th position and it takes two bytes.

```c
#define EI_NIDENT 16

typedef struct {
        unsigned char   e_ident[EI_NIDENT];
        Elf64_Half      e_type;
        Elf64_Half      e_machine;
        Elf64_Word      e_version;
        Elf64_Addr      e_entry;
        Elf64_Off       e_phoff;
        Elf64_Off       e_shoff;
        Elf64_Word      e_flags;
        Elf64_Half      e_ehsize;
        Elf64_Half      e_phentsize;
        Elf64_Half      e_phnum;
        Elf64_Half      e_shentsize;
        Elf64_Half      e_shnum;
        Elf64_Half      e_shstrndx;
} Elf64_Ehdr;
```

Source: [ELF Header](https://refspecs.linuxfoundation.org/elf/gabi4+/ch4.eheader.html)

```c
/* 64-bit ELF base types. */
typedef __u64	Elf64_Addr;
typedef __u16	Elf64_Half;
typedef __s16	Elf64_SHalf;
typedef __u64	Elf64_Off;
typedef __s32	Elf64_Sword;
typedef __u32	Elf64_Word;
typedef __u64	Elf64_Xword;
typedef __s64	Elf64_Sxword;
```

Source: [elf.h](https://github.com/torvalds/linux/blob/master/include/uapi/linux/elf.h)


```bash
$ xxd READFLAG |head 
00000000: 7f45 4c46 0201 0100 0000 0000 0000 0000  .ELF............
00000010: 0300 3200 0100 0000 a110 0000 0000 0000  ..2.............
00000020: 4000 0000 0000 0000 c03a 0000 0000 0000  @........:......
00000030: 0000 0000 4000 3800 0b00 4000 1e00 1d00  ....@.8...@.....
00000040: 0600 0000 0400 0000 4000 0000 0000 0000  ........@.......
00000050: 4000 0000 0000 0000 4000 0000 0000 0000  @.......@.......
00000060: 6802 0000 0000 0000 6802 0000 0000 0000  h.......h.......
00000070: 0800 0000 0000 0000 0300 0000 0400 0000  ................
00000080: a802 0000 0000 0000 a802 0000 0000 0000  ................
00000090: a802 0000 0000 0000 1c00 0000 0000 0000  ................
```

As the difference is one byte, we just change *0x32* to *0x3e*, at last we save it to *fix*.

```python
readflag = open("READFLAG", "rb").read()
readflag = readflag[:18] + b'\x3e' + readflag[19:]


with open("fix", "wb") as fd:
    fd.write(readflag)
```

Run *fix* in ``gdb``, segfault raise at ``_start``, let's take a look at the entry address.

```bash
   0x55555555509b                  add    BYTE PTR [rax], al
   0x55555555509d                  add    BYTE PTR [rax], al
   0x55555555509f                  add    BYTE PTR [rcx], dh
 → 0x5555555550a1 <_start+1>       in     eax, dx
   0x5555555550a2 <_start+2>       mov    r9, rdx
   0x5555555550a5 <_start+5>       pop    rsi
   0x5555555550a6 <_start+6>       mov    rdx, rsp
   0x5555555550a9 <_start+9>       and    rsp, 0xfffffffffffffff0
   0x5555555550ad <_start+13>      push   rax
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "fix", stopped 0x5555555550a1 in _start (), reason: SIGSEGV
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x5555555550a1 → _start()
```

The header said the entry point address is at *0x10a1*. 

```bash
$ readelf -h READFLAG 
ELF Header:
  Magic:   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF64
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              DYN (Shared object file)
  Machine:                           Advanced Micro Devices X86-64
  Version:                           0x1
  Entry point address:               0x10a1
  Start of program headers:          64 (bytes into file)
  Start of section headers:          15040 (bytes into file)
  Flags:                             0x0
  Size of this header:               64 (bytes)
  Size of program headers:           56 (bytes)
  Number of program headers:         11
  Size of section headers:           64 (bytes)
  Number of section headers:         30
  Section header string table index: 29
```

But *_start* actually located at *0x10a0*.

```bash
$ readelf -s fix|grep _start
     4: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __libc_start_main@GLIBC_2.2.5 (2)
     5: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND __gmon_start__
    41: 0000000000003de8     0 NOTYPE  LOCAL  DEFAULT   19 __init_array_start
    48: 0000000000004048     0 NOTYPE  WEAK   DEFAULT   24 data_start
    53: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __libc_start_main@@GLIBC_
    54: 0000000000004048     0 NOTYPE  GLOBAL DEFAULT   24 __data_start
    55: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND __gmon_start__
    60: 00000000000010a0    43 FUNC    GLOBAL DEFAULT   14 _start
    61: 0000000000004058     0 NOTYPE  GLOBAL DEFAULT   25 __bss_start
```

According to the *Elf64_Ehdr* struct, the entry point address is stored in field *e_entry*, at the 25th position of header and it takes 8 bytes. But the difference is just one byte, so we just need to overwrite *0xa1* with *0xa0*

```python
readflag = open("READFLAG", "rb").read()
readflag = readflag[:18] + b'\x3e' + readflag[19:]
readflag = readflag[:24] + b'\xa0' + readflag[25:]


with open("fix", "wb") as fd:
    fd.write(readflag)
```

Now we run it again, no error and no output either, these might be the two bytes we need to change, patch it to the server, it response with the flag.

