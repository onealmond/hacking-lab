Sign up with username=gg, password=gg and then sign in with the previous credential.
Try to visit existen posts we figured the url of post seems iterable by changing parameter `id`

Try to access

```html
  http://34.74.105.127/af82d5a390/index.php?page=view.php&id=2
```
It leads us to a private post that contains a flag.

Created a post with tag ``<script>`` in title and body, then we found a flag in result message.

Inspect home page, we found two input tags with ``'hidden'`` attributes, one with attribute ``user_id=<number>``, change the ``user_id`` to ``1``, after create a post we get a flag at the top of post timeline.

Try to login as ``'user'`` with password ``'password'``, there is a flag at home page after login

Checking value of key ``'id'`` in application cookies, figured the session id value is md5 hex digest of user id. change it to ``hashlib.md5('1'.encode()).hexdigest()`` to login as admin. There is a flag at home page.

Delete a post via url to get one flag, the value of id is md5 hex digest of post id.
