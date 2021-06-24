            ;-- section..text:
            ;-- segment.LOAD1:
            ;-- .text:
            ;-- weird_function_please_ignore:
            ;-- map._home_ctf_lab_ex_hacking_lab_circlecitycon_2021_weird_rop_weird_rop_f17e9f493733a383aac548dbf1320c33.r_x:
            0x00401000      5e             pop rsi                     ; [02] -r-x section size 361 named .text
            0x00401001      c3             ret
            0x00401002      48c7c0000000.  mov rax, 0
            0x00401009      c3             ret
            0x0040100a      48c7c0010000.  mov rax, 1
            0x00401011      c3             ret
            0x00401012      48c7c7010000.  mov rdi, 1
            0x00401019      c3             ret
            0x0040101a      4883f756       xor rdi, 0x56               ; 86
            0x0040101e      c3             ret
            0x0040101f      4883f725       xor rdi, 0x25               ; 37
            0x00401023      c3             ret
            0x00401024      4881f72e0300.  xor rdi, 0x32e              ; 814
            0x0040102b      c3             ret
            0x0040102c      4881f7880100.  xor rdi, 0x188              ; 392
            0x00401033      c3             ret
            0x00401034      4881f7e50100.  xor rdi, 0x1e5              ; 485
            0x0040103b      c3             ret
            0x0040103c      4881f7550300.  xor rdi, 0x355              ; 853
            0x00401043      c3             ret
            0x00401044      4881f70c0300.  xor rdi, 0x30c              ; 780
            0x0040104b      c3             ret
            0x0040104c      4881f79b0100.  xor rdi, 0x19b              ; 411
            0x00401053      c3             ret
            0x00401054      4881f7370200.  xor rdi, 0x237              ; 567
            0x0040105b      c3             ret
            0x0040105c      4881f7140300.  xor rdi, 0x314              ; 788
            0x00401063      c3             ret
            0x00401064      4881f7c10000.  xor rdi, 0xc1               ; 193
            0x0040106b      c3             ret
            0x0040106c      4881f7b30200.  xor rdi, 0x2b3              ; 691
            0x00401073      c3             ret
            0x00401074      4881f7810200.  xor rdi, 0x281              ; 641
            0x0040107b      c3             ret
            0x0040107c      4883f753       xor rdi, 0x53               ; 83
            0x00401080      c3             ret
            0x00401081      4881f7740200.  xor rdi, 0x274              ; 628
            0x00401088      c3             ret
            0x00401089      4883f71d       xor rdi, 0x1d               ; 29
            0x0040108d      c3             ret
            0x0040108e      4881f7a90100.  xor rdi, 0x1a9              ; 425
            0x00401095      c3             ret
            0x00401096      4883f76f       xor rdi, 0x6f               ; 111
            0x0040109a      c3             ret
            0x0040109b      4881f7cd0300.  xor rdi, 0x3cd              ; 973
            0x004010a2      c3             ret
            0x004010a3      4881f78e0200.  xor rdi, 0x28e              ; 654
            0x004010aa      c3             ret
            0x004010ab      4881f76b0100.  xor rdi, 0x16b              ; 363
            0x004010b2      c3             ret
            0x004010b3      4881f7f40100.  xor rdi, 0x1f4              ; 500
            0x004010ba      c3             ret
            0x004010bb      4881f7ab0300.  xor rdi, 0x3ab              ; 939
            0x004010c2      c3             ret
            0x004010c3      4881f7980100.  xor rdi, 0x198              ; 408
            0x004010ca      c3             ret
            0x004010cb      4881f7a30100.  xor rdi, 0x1a3              ; 419
            0x004010d2      c3             ret
            0x004010d3      4881f79a0200.  xor rdi, 0x29a              ; 666
            0x004010da      c3             ret
            0x004010db      0f05           syscall
            0x004010dd      c3             ret
            0x004010de      5a             pop rdx
            0x004010df      c3             ret
            ;-- vuln:
            0x004010e0      55             push rbp
            0x004010e1      4889e5         mov rbp, rsp
            0x004010e4      4883ec10       sub rsp, 0x10
            0x004010e8      48c7c0020000.  mov rax, 2
            0x004010ef      488d3c250020.  lea rdi, map._home_ctf_lab_ex_hacking_lab_circlecitycon_2021_weird_rop_weird_rop_f17e9f493733a383aac548dbf1320c33.rw_
            0x004010f7      48c7c6020000.  mov rsi, 2
            0x004010fe      48c7c2000000.  mov rdx, 0
            0x00401105      0f05           syscall
            0x00401107      4883c030       add rax, 0x30               ; 48
            0x0040110b      880424         mov byte [rsp], al
            0x0040110e      c64424010a     mov byte [rsp + 1], 0xa
            0x00401113      48c7c0010000.  mov rax, 1
            0x0040111a      48c7c7010000.  mov rdi, 1
            0x00401121      4889e6         mov rsi, rsp
            0x00401124      48c7c2020000.  mov rdx, 2
            0x0040112b      0f05           syscall
            0x0040112d      48c7c0000000.  mov rax, 0
            0x00401134      48c7c7000000.  mov rdi, 0
            0x0040113b      4889e6         mov rsi, rsp
            0x0040113e      48c7c2c80000.  mov rdx, 0xc8               ; 200
            0x00401145      0f05           syscall
            0x00401147      48c7c7000000.  mov rdi, 0
            0x0040114e      4883c410       add rsp, 0x10
            0x00401152      5d             pop rbp
            0x00401153      c3             ret
            ;-- entry0:
            ;-- _start:
            ;-- rip:
            0x00401154      e887ffffff     call loc.vuln
            0x00401159      48c7c03c0000.  mov rax, 0x3c               ; '<' ; 60
            0x00401160      48c7c7000000.  mov rdi, 0
            0x00401167      0f05           syscall
            0x00401169      0000           add byte [rax], al
            0x0040116b      0000           add byte [rax], al
