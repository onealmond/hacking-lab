

Try to ping-pong some subpaths, ``/robots.txt`` shows something interesting.

```bash
user-agent: kilroy
/hidden892734569.html
```

Request ``/hidden892734569.html`` gives us a clue about style file. Send request to check it out.

```bash
http --follow -v https://ctf-web2.ncsa.tech/style.css
```

After several redirections, we finally receive some useful message.

```bash
HTTP/1.1 302 Found
content-length: 36
content-type: text/plain; charset=utf-8
date: Mon, 19 Apr 2021 08:47:55 GMT
interesting: TXIuIFJvYm90byBzZXo6IFRyeSBnb2luZyB0byAvY3NzL3N0eWxlNzU2NDg3NS5jc3M=
keep-alive: timeout=5
location: /css/style.css
vary: Accept
x-powered-by: Express

Found. Redirecting to /css/style.css

```

Decode the base64-encoded message we get yet another css path.

```bash
$ base64 -d <<< TXIuIFJvYm90byBzZXo6IFRyeSBnb2luZyB0byAvY3NzL3N0eWxlNzU2NDg3NS5jc3M=
Mr. Roboto sez: Try going to /css/style7564875.css
```

Request ``/css/style7564875.css`` resulting a rejection. 

```bash
$ http --follow -v https://ctf-web2.ncsa.tech/css/style7564875.css
...
Mr. Roboto sez: You are almost there.  Maybe a different User-Agent: would help. Your User-Agent: HTTPie/1.0.3
```

Request again with agent shown in ``robots.txt``.

```bash
http --follow -v https://ctf-web2.ncsa.tech/css/style7564875.css User-Agent:kilroy
```

Finally the flag shown up.
