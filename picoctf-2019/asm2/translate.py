def asm2(a, b):
  while a <= 0x47a6:
    b += 1
    a += 0xa9
  return b

print(hex(asm2(0x9,0x1e)))
