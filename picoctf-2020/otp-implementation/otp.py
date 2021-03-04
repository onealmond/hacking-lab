from subprocess import Popen, PIPE, DEVNULL
import string, re


def must_guess():
    target = "lfmhjmnahapkechbanheabbfjladhbplbnfaijdajpnljecghmoafbljlaamhpaheonlmnpmaddhngbgbhobgnofjgeaomadbidl"
    sample = string.hexdigits[:-6]
    target_len = 100
    key = ['0'] * target_len

    for i in range(target_len):
        for x in sample:
            key[i] = x
            p = Popen(['ltrace', '-s', '1000', './otp', ''.join(key)], stderr=PIPE, stdout=DEVNULL)
            output = p.stderr.read().decode()
            res = re.search('strncmp\(\"(.+)\".+\)', output).group(1)[:100]
            if target[i] == res[i]:
                break

    print('key:', ''.join(key))
    flag = open('flag.txt').read()
    print('flag:', ''.join([chr(x^y) for x, y in zip(bytes.fromhex(''.join(key)), bytes.fromhex(flag))]))


must_guess()
