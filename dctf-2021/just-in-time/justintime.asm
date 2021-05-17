            ;-- main:
            0x55d6817f94c5      55             push rbp
            0x55d6817f94c6      4889e5         mov rbp, rsp
            0x55d6817f94c9      53             push rbx
            0x55d6817f94ca      4883ec58       sub rsp, 0x58
            0x55d6817f94ce      897dac         mov dword [rbp - 0x54], edi
            0x55d6817f94d1      488975a0       mov qword [rbp - 0x60], rsi
            0x55d6817f94d5      bf08000000     mov edi, 8
            0x55d6817f94da      e8d1fbffff     call sym.imp.malloc
            0x55d6817f94df      488945e8       mov qword [rbp - 0x18], rax
            0x55d6817f94e3      488b45a0       mov rax, qword [rbp - 0x60]
            0x55d6817f94e7      488b00         mov rax, qword [rax]
            0x55d6817f94ea      4889c7         mov rdi, rax
            0x55d6817f94ed      e878fdffff     call 0x55d6817f926a
            0x55d6817f94f2      4889c1         mov rcx, rax
            0x55d6817f94f5      488b45e8       mov rax, qword [rbp - 0x18]
            0x55d6817f94f9      ba08000000     mov edx, 8
            0x55d6817f94fe      4889ce         mov rsi, rcx
            0x55d6817f9501      4889c7         mov rdi, rax
            0x55d6817f9504      e847fbffff     call sym.imp.strncpy
            0x55d6817f9509      48b81b263820.  movabs rax, 0x486765792038261b
            0x55d6817f9513      48ba72282467.  movabs rdx, 0x754b623167242872 ; 'r($g1bKu'
            0x55d6817f951d      488945b0       mov qword [rbp - 0x50], rax
            0x55d6817f9521      488955b8       mov qword [rbp - 0x48], rdx
            0x55d6817f9525      48b87b226635.  movabs rax, 0x747d4e603566227b ; '{"f5`N}t'
            0x55d6817f952f      48ba23333331.  movabs rdx, 0x252f764e31333323 ; '#331Nv/%'
            0x55d6817f9539      488945c0       mov qword [rbp - 0x40], rax
            0x55d6817f953d      488955c8       mov qword [rbp - 0x38], rdx
            0x55d6817f9541      c745d0603131.  mov dword [rbp - 0x30], 0x46313160 ; '`11F'
            0x55d6817f9548      66c745d42331   mov word [rbp - 0x2c], 0x3123 ; '#1'
            0x55d6817f954e      c645d600       mov byte [rbp - 0x2a], 0
            0x55d6817f9552      b827000000     mov eax, 0x27           ; ''' ; 39
            0x55d6817f9557      4898           cdqe
            0x55d6817f9559      4889c7         mov rdi, rax
            0x55d6817f955c      e84ffbffff     call sym.imp.malloc
            0x55d6817f9561      488945e0       mov qword [rbp - 0x20], rax
            0x55d6817f9565      b827000000     mov eax, 0x27           ; ''' ; 39
            0x55d6817f956a      4863d0         movsxd rdx, eax
            0x55d6817f956d      488d4db0       lea rcx, [rbp - 0x50]
            0x55d6817f9571      488b45e0       mov rax, qword [rbp - 0x20]
            0x55d6817f9575      4889ce         mov rsi, rcx
            0x55d6817f9578      4889c7         mov rdi, rax
            0x55d6817f957b      e8d0faffff     call sym.imp.strncpy
            0x55d6817f9580      488b45e0       mov rax, qword [rbp - 0x20]
            0x55d6817f9584      4889c7         mov rdi, rax
            0x55d6817f9587      e8e6fdffff     call 0x55d6817f9372
            0x55d6817f958c      488d3d7d0a00.  lea rdi, str.Decryption_finished. ; 0x55d6817fa010 ; "Decryption finished."
            0x55d6817f9593      e8c8faffff     call sym.imp.puts
            0x55d6817f9598      b827000000     mov eax, 0x27           ; ''' ; 39
            0x55d6817f959d      4898           cdqe
            0x55d6817f959f      4889c7         mov rdi, rax
            0x55d6817f95a2      e809fbffff     call sym.imp.malloc
            0x55d6817f95a7      488945d8       mov qword [rbp - 0x28], rax
            0x55d6817f95ab      b827000000     mov eax, 0x27           ; ''' ; 39
            0x55d6817f95b0      4863d8         movsxd rbx, eax
            0x55d6817f95b3      488b55e8       mov rdx, qword [rbp - 0x18]
            0x55d6817f95b7      488d45b0       lea rax, [rbp - 0x50]
            0x55d6817f95bb      4889d6         mov rsi, rdx
            0x55d6817f95be      4889c7         mov rdi, rax
            0x55d6817f95c1      e8fffbffff     call 0x55d6817f91c5
            0x55d6817f95c6      4889c1         mov rcx, rax
            0x55d6817f95c9      488b45d8       mov rax, qword [rbp - 0x28]
            0x55d6817f95cd      4889da         mov rdx, rbx
            0x55d6817f95d0      4889ce         mov rsi, rcx
            0x55d6817f95d3      4889c7         mov rdi, rax
            0x55d6817f95d6      e875faffff     call sym.imp.strncpy
            0x55d6817f95db      488b55e8       mov rdx, qword [rbp - 0x18]
            0x55d6817f95df      488b45d8       mov rax, qword [rbp - 0x28]
            0x55d6817f95e3      4889d6         mov rsi, rdx
            0x55d6817f95e6      4889c7         mov rdi, rax
            0x55d6817f95e9      e8d7fbffff     call 0x55d6817f91c5
            0x55d6817f95ee      488945d8       mov qword [rbp - 0x28], rax
            0x55d6817f95f2      488b45d8       mov rax, qword [rbp - 0x28]
            0x55d6817f95f6      4889c7         mov rdi, rax
            0x55d6817f95f9      e862feffff     call 0x55d6817f9460
            0x55d6817f95fe      488b45e0       mov rax, qword [rbp - 0x20]
            0x55d6817f9602      4889c7         mov rdi, rax
            0x55d6817f9605      e826faffff     call sym.imp.free
            0x55d6817f960a      488b45d8       mov rax, qword [rbp - 0x28]
            0x55d6817f960e      4889c7         mov rdi, rax
            0x55d6817f9611      e81afaffff     call sym.imp.free
            0x55d6817f9616      488b45e8       mov rax, qword [rbp - 0x18]
            0x55d6817f961a      4889c7         mov rdi, rax
            0x55d6817f961d      e80efaffff     call sym.imp.free
            0x55d6817f9622      b800000000     mov eax, 0
            0x55d6817f9627      488b5df8       mov rbx, qword [rbp - 8]
            0x55d6817f962b      c9             leave
            0x55d6817f962c      c3             ret
            0x55d6817f962d      0f1f00         nop dword [rax]
            0x55d6817f9630      4157           push r15
            0x55d6817f9632      4c8d3daf2700.  lea r15, segment.GNU_RELRO ; 0x55d6817fbde8
            0x55d6817f9639      4156           push r14
            0x55d6817f963b      4989d6         mov r14, rdx
            0x55d6817f963e      4155           push r13
            0x55d6817f9640      4989f5         mov r13, rsi
            0x55d6817f9643      4154           push r12
            0x55d6817f9645      4189fc         mov r12d, edi
            0x55d6817f9648      55             push rbp
            0x55d6817f9649      488d2da02700.  lea rbp, section..fini_array ; 0x55d6817fbdf0
            0x55d6817f9650      53             push rbx
            0x55d6817f9651      4c29fd         sub rbp, r15
            0x55d6817f9654      4883ec08       sub rsp, 8
            0x55d6817f9658      e8a3f9ffff     call map._home_zex_lab_ex_hacking_lab_dctf_2021_just_in_time_justintime.r_x
            0x55d6817f965d      48c1fd03       sar rbp, 3
            0x55d6817f9661      741b           je 0x55d6817f967e
            0x55d6817f9663      31db           xor ebx, ebx
            0x55d6817f9665      0f1f00         nop dword [rax]
            0x55d6817f9668      4c89f2         mov rdx, r14
            0x55d6817f966b      4c89ee         mov rsi, r13
            0x55d6817f966e      4489e7         mov edi, r12d
            0x55d6817f9671      41ff14df       call qword [r15 + rbx*8]
            0x55d6817f9675      4883c301       add rbx, 1
            0x55d6817f9679      4839dd         cmp rbp, rbx
            0x55d6817f967c      75ea           jne 0x55d6817f9668
            0x55d6817f967e      4883c408       add rsp, 8
            0x55d6817f9682      5b             pop rbx
            0x55d6817f9683      5d             pop rbp
            0x55d6817f9684      415c           pop r12
            0x55d6817f9686      415d           pop r13
            0x55d6817f9688      415e           pop r14
            0x55d6817f968a      415f           pop r15
