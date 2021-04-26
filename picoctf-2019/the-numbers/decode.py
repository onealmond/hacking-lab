flag = [16, 9, 3, 15, 3, 20, 6, 20, 8, 5, 14, 21, 13, 2, 5, 18, 19, 13, 1, 19, 15, 14]
decoded = list(map(lambda c: chr(ord('A')+c-1), flag))
print('{}{{{}}}'.format(''.join(decoded[:7]), ''.join(decoded[7:])))
