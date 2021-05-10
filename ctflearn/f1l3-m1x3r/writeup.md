
Checked out file type with *file*, it seems unable to recognize it.

```bash
$ file fl4g.jpeg 
fl4g.jpeg: data
```

Read the data in *xxd*, noticed that first several bytes looks weird for a jpeg file.

```bash
$ xxd fl4g.jpeg |head
00000000: e0ff d8ff 464a 1000 0100 4649 6000 0101  ....FJ....FI`...
00000010: 0000 6000 4300 dbff 0202 0300 0302 0203  ..`.C...........
00000020: 0403 0303 0504 0303 0405 0508 070a 0504  ................
00000030: 0c08 0607 0b0c 0c0a 0d0b 0b0a 0d10 120e  ................
00000040: 0b0e 110e 1016 100b 1514 1311 0f0c 1515  ................
00000050: 1416 1817 1514 1218 00db ff14 0403 0143  ...............C
00000060: 0504 0504 0905 0509 0d0b 0d14 1414 1414  ................
00000070: 1414 1414 1414 1414 1414 1414 1414 1414  ................
00000080: 1414 1414 1414 1414 1414 1414 1414 1414  ................
00000090: 1414 1414 1414 1414 1414 1414 c0ff 1414  ................
```

A jpeg file is supposed to starts with *FF D8 FF E0 00 10 4A 46 49 46 00 01*, according to [list of file signatures](https://wikimili.com/en/List_of_file_signatures). It seems reversed every 4 bytes. Could this happened to the rest also?

To check it out, dump it every 4 bytes reversed.

```python
buf = open('fl4g.jpeg', 'rb').read()

fix = b''
with open('fl4g-fix.jpeg', 'wb') as fd:
    for i in range(0, len(buf), 4):
        fd.write(bytes(list(reversed(buf[i:i+4]))))
```

Checked fixed file out with *file*, it looks back on track.

```bash
$ file fl4g-fix.jpeg 
fl4g-fix.jpeg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 96x96, segment length 16, baseline, precision 8, 262x102, components 3
```

Viewed it in *ristretto* and found the flag.
