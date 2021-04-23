
Check out the user profile section, user email is hidden. Inspect the source, in ``custom.js``, there is a function called ``retriveEmail``, it send a ``GET`` request to api with parameter ``act=getemail``, could it get us email of the user?

```js
function retrieveEmail(e){var t=new XMLHttpRequest;t.open("GET","api/action.php?act=getemail",!0),t.setRequestHeader("X-SAFEPROTECTION","enNlYW5vb2Zjb3Vyc2U="),t.onreadystatechange=function(){this.readyState===XMLHttpRequest.DONE&&this.status},t.send()}
```

Try to request the api with ``curl`` and header for protection.

```bash
curl "http://35.227.24.107/9259a99869/api/action.php?act=getemail" -h "X-SAFEPROTECTION:enNlYW5vb2Zjb3Vyc2U="
```

Wow! The flag is in response.
