#!/usr/bin/env python3

def func3_1(param_1):
    cVar1 = 0
      
    if ((ord('@') < param_1) and (param_1 < ord('['))):
        param_1 = param_1 - 0xd
        if (param_1 < ord('A')):
          cVar1 = ord('\x1a')
        else:
          cVar1 = ord('\0')
        
        param_1 = cVar1 + param_1
    
    if ((ord('`') < param_1) and (param_1 < ord('{'))):
        param_1 = param_1 - 0xd
        if (param_1 < ord('a')):
          cVar1 = ord('\x1a')
        else:
          cVar1 = ord('\0')

        param_1 = cVar1 + param_1
    return param_1

def func3_2(param_1):
  cVar1 = 0
  
  if ((ord(' ') < param_1) and (param_1 != ord('\x7f'))):
    param_1 = param_1 - 0x2f
    if (param_1 < ord('!')):
      cVar1 = ord('^')
    else:
      cVar1 = ord('\0')
    param_1 = cVar1 + param_1
 
  return param_1


s = "\"_9~Jb0!=A`G!06qfc8'_20uf6`2%7"
ans = []
for i in range(len(s)):
    for c in range(255):
        x = func3_1(c)
        x = func3_2(x)
        if x == ord(s[i]):
            ans.append(c)
            break
            
print(''.join(map(chr, ans)))
