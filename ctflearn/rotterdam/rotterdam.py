#!/usr/bin/env python3
prefix = 'CTFlearn{'
kernel = []

s = hex(0x2a460d92f5a1f504^0x4b227ff781d59a56)[2:]
param = ''.join(reversed(''.join(map(chr, [int(s[i:i+2],16) for i in range(0,len(s),2)]))))
print('part1:', param)
kernel.append(param)

s = hex(0x15764ff46 - (0x4f7fb8ade2f2cef6&0xffffffff))[2:]
param = ''.join(reversed(''.join(map(chr, [int(s[i:i+2],16) for i in range(0,len(s),2)]))))
print('part2:', param)
kernel.append(param)

s = hex(0x4d998c32ff+0x17d4a53553)[2:]
param = ''.join(reversed(''.join(map(chr, [int(s[i:i+2],16) for i in range(0,len(s),2)]))))
print('part3:', param)
kernel.append(param)

s = hex(0x6a8754493837f7d400a77b9be//0xdeb4fa4d998c32ff)[2:]
param = ''.join(reversed(''.join(map(chr, [int(s[i:i+2],16) for i in range(0,len(s),2)]))))
param = 'B' + param
print('part4:', param)
kernel.append(param)

# we need to find a divident makes 
# - 0x1f6ff5218c40de9c//input == 0x4f5352
# - 0x1f6ff5218c40de9c%input == 0x55930dbbe
# input = (0x1f6ff5218c40de9c-0x55930dbbe)/0x4f5352
s = "6574743157"
param = ''.join(reversed(''.join(map(chr, [int(s[i:i+2],16) for i in range(0,len(s),2)]))))
print('part5:', param)
kernel.append(param)

print('_'.join(kernel))
