We can get the flag using ``print-flag`` command. Before the ``print_flag`` function actualy print the flag, it needs to validate access information.


```
  unsigned long ac1 = ((unsigned long *)u->access_code)[0];
  unsigned long ac2 = ((unsigned long *)u->access_code)[1];
  if (ac1 != 0x4343415f544f4f52 || ac2 != 0x45444f435f535345) {
    fprintf(stdout, "Incorrect Access Code: \"");
    for (int i = 0; i < ACCESS_CODE_LEN; i++) {
      putchar(u->access_code[i]);
    }
    fprintf(stdout, "\"\n");
    return;
  }

```

```
>>> pwn.p64(0x4343415f544f4f52)
b'ROOT_ACC'
>>> pwn.p64(0x45444f435f535345)
b'ESS_CODE'
```

Which means the ``access_code`` needs to be ``ROOT_ACCESS_CODE``.

So how do we set the correct code to ``access_code``?

Take a look at ``login``, it's using ``malloc`` to allocate memory for user struct and username, as ``malloc`` simply allocate chunks of memory without initialization, information previously written there will still exists.


In ``logout``, the user struct is being freed first, and then, the username. The deallocated pointers are stored like a stack, when it needs to allocate again, as in ``login``, the old pointer to username is being used to create user struct.

```
| username    | 
| user struct |
| ----------- |

```

Now, we need to store the ``user`` struct in username, so that the ``access_code`` can be the expected one.

```
>>> len('A'*8+'ROOT_ACCESS_CODE'+'A'*8)
32
```

Login with username ``'A'*8+'ROOT_ACCESS_CODE'+'A'*8``, logout, and then, login again with a shorter name to get flag with command ``print_flag``.
