#!/usr/bin/env python3

def print_blk(hex_blks, sz):
   for i in range(0, len(hex_blks), sz):
       print(hex_blks[i:i+sz], ' ', end='')
   print()

plain = (b'a'*(16*3)).hex()
# ENCRYPT(PLAINTEXT)
cipher = '1c5ded2c669062d2cd3a11766371be1a38f0a5d3c96961eac8586bb4549dfc41c49a8a3d4c17740bf224d19d129fa9a8'
print_blk(cipher, 32)

# alter cipher text
fake_cipher = cipher[:32] + '0'*32 + cipher[:32]
print_blk(fake_cipher, 32)
print(fake_cipher)

# RECEIVE(CIPHERTEXT)
fake_plain = '6161616161616161616161616161616155cb30af3a7c7a40f8ce7e766c8037579bf317d1684a16e1e95691b163dc178a'
print_blk(fake_plain, 32)
fake_plain = bytes.fromhex(fake_plain)
iv = [0]*16
for i in range(len(iv)):
   iv[i] = fake_plain[i] ^ fake_plain[32+i] 
print(bytes(iv).hex())

# GET_FLAG(KEY)
flag = '63727970746f7b35306d335f703330706c335f64306e375f3768316e6b5f49565f31355f316d70307237346e375f3f7d'
print(bytes.fromhex(flag))
