#!/usr/bin/env python3
import base64

data = open('cipher.txt', 'rb').read()

while True:
    try:
        data = base64.b64decode(data)
    except Exception as e:
        print(data)
        print(e)
        break
