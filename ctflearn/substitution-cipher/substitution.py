#!/usr/bin/env/python3

mapper = {}

def build_mapper(cipher, plain):
    for i in range(len(cipher)):
        mapper[cipher[i]] = plain[i]

build_mapper('RTETDZTK', 'december')
build_mapper('FGXTDZTK', "november")
build_mapper('L', 's')
build_mapper('Y', 'f')
build_mapper('M', 't')
build_mapper('I', 'h')
build_mapper('O', 'i')
build_mapper('W', 'u')
build_mapper('H', 'p')
build_mapper('B', 'y')
build_mapper('S', 'l')
build_mapper('A', 'a')
build_mapper('U', 'g')
build_mapper('V', 'x')
build_mapper('Q', 'k')
build_mapper('C', 'w')

msg = open('substitution.txt').read()

if True:
    buf = []
    for i in range(len(msg)):
        if msg[i].isdigit() or msg[i] == ' ':
            buf.append(msg[i])
            continue

        if mapper.get(msg[i], None):
            buf.append(mapper[msg[i]])
        else:
            buf.append(msg[i])

    if buf and ord(buf[0]) >= ord('A'):
        print('[', ''.join(buf), ']')
