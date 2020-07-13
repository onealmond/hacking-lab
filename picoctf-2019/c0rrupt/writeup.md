Command `file` doesn't know what `mystery` is, saids `data`, analysing with `xxd` found an ending flag `IEND`, looks like this is a corrupted png file.

Try to correct the header first. we have img.png with PNG header.

```
pngcheck c0rrupt/img.png
```

`pngcheck` saids 'CRC error in chunk pHYs', now we need to fix pHYs chunk.

```
$ pngcheck -v c0rrupt/img.png

  chunk pHYs at offset 0x00042, length 9: 2852132389x5669 pixels/meter
```

Found problem with width x height.


With pngcheck we still have chunk length problem
  invalid chunk length (too large)


The following line doesn't look right, 0xabDET is not a valid type.

```
00000050: 5224 f0aa aaff a5ab 4445 5478 5eec bd3f  R$......DETx^..?
```

Change it to IDAT
```
00000050: 5224 f0aa aaff a549 4441 5478 5eec bd3f  R$.....IDATx^..?
```

```
binwalk -R IDAT c0rrupt/img.png

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
87            0x57            IDAT
65544         0x10008         IDAT
131080        0x20008         IDAT
196616        0x30008         IDAT
202951        0x318C7         IDAT
```

Since we have 0xaaaaffa5 already, only need to change 0xaaaa to 0000. Try to check again with pngcheck we got no more error. Open the fixed image img.png found one flag.
