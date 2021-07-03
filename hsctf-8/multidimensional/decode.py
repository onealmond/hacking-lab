#!/usr/bin/env python3

def time(arr):
    t = [[8, 65, -18, -21, -15, 55], 
        [8, 48, 57, 63, -13, 5], 
        [16, -5, -26, 54, -7, -2], 
        [48, 49, 65, 57, 2, 10], 
        [9, -2, -1, -9, -11, -10], 
        [56, 53, 18, 42, -28, 5]]
    for j in range(len(arr[0])):
        for i in range(len(arr)):
            arr[i][j] = (arr[i][j]-t[j][i])%256

def matrics(s):
    arr = []
    for i in range(0, len(s), 6):
        arr.append(list(map(ord, s[i:i+6])))
    return arr


def space(n, arr):
    while n > 0:
        arr[(35 - n) // 6][(35 - n) % 6] += (n // 6) + (n % 6)
        n -= 1

def plane(arr):
    n = len(arr)

    for i in range(n):
        for j in range(n):
            arr[i][j] -= i + n - j

    for i in range(n//2):
        for j in range(n//2):
            t = arr[i][j]
            arr[i][j] = arr[n - 1 - j][i]
            arr[n - 1 - j][i] = arr[n - 1 - i][n - 1 - j]
            arr[n - 1 - i][n - 1 - j] = arr[j][n - 1 - i]
            arr[j][n - 1 - i] = t

def line(arr):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if i % 2 == 0 and j % 2 == 0:
                    arr[i][j] += 2
            if i % 2 != 0 and j % 2 != 0:
                    arr[i][j] -= 2

def flatten(arr):
    s = []
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            s.append(chr(arr[j][i]))
    return s

expected = "hey_since_when_was_time_a_dimension?"
arr = matrics(expected)
time(arr)
space(35, arr)
plane(arr)
line(arr)
s = flatten(arr)
for i in range(0, len(s), 2):
    s[i], s[i+1] = s[i+1], s[i]
print(''.join(s))
