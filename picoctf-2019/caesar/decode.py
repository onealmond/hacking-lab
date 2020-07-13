# [Caesar cipher](https://privacycanada.net/classical-encryption/caesar-cipher/)

enc = 'zolppfkdqeboryfzlktjxksyyl'

for l in range(26):
    r = ''
    for c in enc:
        ci = ord(c) - ord('a')
        r += chr((ci + l)%26 + ord('a'))
    print(r)
