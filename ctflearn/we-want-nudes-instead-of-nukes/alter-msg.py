#!/usr/bin/env python3
block_size = 16
iv = '391e95a15847cfd95ecee8f7fe7efd66'
cipher = '8473dcb86bc12c6b6087619c00b6657e'
plain = 'FIRE_NUKES_MELA!'
fake_plain = 'SEND_NUDES_MELA!'

iv = bytes.fromhex(iv)
cipher = bytes.fromhex(cipher)
fake_iv = []

for i in range(block_size):
    fake_iv.append(iv[i] ^ ord(plain[i]) ^ ord(fake_plain[i]))

fake_iv = bytes(fake_iv)
print('iv', fake_iv.hex(), len(fake_iv))
print('flag{{{},{}}}'.format(fake_iv.hex(), cipher.hex()))
