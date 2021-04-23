The challenge gives a url named ``/header.php``, we got blocked whiling access the page

```html
Sorry, it seems as if your user agent is not correct, in order to access this website. The one you supplied is: chrome 
<!-- Sup3rS3cr3tAg3nt  -->
```

Changed the user agent to ``Sup3rS3cr3tAg3nt`` and visit again, we got a new hint

```html
Sorry, it seems as if you did not just come from the site, "awesomesauce.com".                  
<!-- Sup3rS3cr3tAg3nt  -->
```

Now we change the referrer to ``awesomesauce.com`` and try again

```bash
curl -v -H 'User-Agent: Sup3rS3cr3tAg3nt' --referrer awesomesauce.com http://165.227.106.113/header.php
```

The flag is in the response.
