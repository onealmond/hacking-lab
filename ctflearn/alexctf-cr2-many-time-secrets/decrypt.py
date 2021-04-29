import string

msg = []

with open('msg', 'r') as fd:
    buf = fd.readlines()
    print('len of one line', len(buf[0].strip()))
    msg = ''.join([l.strip() for l in buf])

msg = [int(msg[i:i+2], 16) for i in range(0, len(msg), 2)]
prefix = "ALEXCTF{"

plain = [chr(msg[i] ^ ord(prefix[i])) for i in range(len(prefix))]
print(''.join(plain))

# Guess the plain starts with "Dear Friend"
plain = ''.join(plain) + "end"
print(plain)

prefix = ''.join(map(chr, [msg[i] ^ ord(plain[i]) for i in range(len(plain))]))
print(prefix)

# Guess flag starts with "ALEXFLAG{HERE_"
prefix += "E_"
plain = ''.join(map(chr, [msg[i] ^ ord(prefix[i]) for i in range(len(prefix))]))
print(plain)

# Found some meaningful words in partially decoded message
plain = ''.join(map(chr, [msg[i] ^ ord(prefix[i%len(prefix)]) for i in range(len(msg))]))
print(plain)

i = plain.find('nderstood')
plain = plain[:i-1] + 'u' + plain[i:]
i = plain.find('sed', i)
plain = plain[:i-1] + 'u' + plain[i:]
i = plain.find('time ', i)
plain = plain[:i+5] + 'padding' + plain[i+5+7:]
i = plain.find("kcz", i)
plain = plain[:i] + 'key' + plain[i+3:]
i = plain.find("gree", i)
plain = plain[:i-1] + 'a' + plain[i:]
i = plain.find("ncryption", i)
plain = plain[:i-1] + 'e' + plain[i:]
i = plain.find("schcne", i)
plain = plain[:i] + 'scheme' + plain[i+6:]
print(plain)

prefix = ''.join(map(chr, [msg[i] ^ ord(plain[i]) for i in range(len(plain))]))
print("== with modified plain text")
print(prefix)

# Now we know the flag starts with "ALEXCTF{HERE_GOES_"
# and the plain text becomes "Dear Friend, This "
prefix = "ALEXCTF{HERE_GOES_"
plain = ''.join(map(chr, [msg[i] ^ ord(prefix[i%len(prefix)]) for i in range(len(msg))]))
print("== with prefix:", prefix)
print(plain)

# Got more words by guessing "THE_FLAG", but still not completely right
prefix = prefix + "THE_FLAG"
plain = ''.join(map(chr, [msg[i] ^ ord(prefix[i%len(prefix)]) for i in range(len(msg))]))
print("== with prefix:", prefix)
print(plain)

i = plain.find("-@8O")
plain = plain[:i] + " I u" + plain[i+4:]
i = plain.find("encry", i)
plain = plain[:i+5] + "ption" + plain[i+5+5:]
i = plain.find("-d}Nhod", i)
plain = plain[:i] + " method" + plain[i+7:]
i = plain.find("cracfl", i)
plain = plain[:i+4] + "ked " + plain[i+4+4:]
i = plain.find("kepy", i)
plain = plain[:i+3] + "t secure" + plain[i+3+8:]
i = plain.find("yb|8[", i)
plain = plain[:i] + "you a" + plain[i+5:]
i = plain.find("thdz8_n", i)
plain = plain[:i] + "this e" + plain[i+6:]
plain = plain[:-1] + "s"
print(plain)

prefix = ''.join(map(chr, [msg[i] ^ ord(plain[i]) for i in range(len(plain))]))
print("== with modified plain text")
print(prefix)

# now we know the flag is "ALEXCTF{HERE_GOES_THE_KEY}", test again
prefix = "ALEXCTF{HERE_GOES_THE_KEY}"
plain = ''.join(map(chr, [msg[i] ^ ord(prefix[i%len(prefix)]) for i in range(len(msg))]))
print("== with prefix:", prefix)
print(plain)
