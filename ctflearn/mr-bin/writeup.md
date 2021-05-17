
*binwalk* extracted two files from image.jpg, *bin*, which was empty and D0F0.zip.

Decompressed *D0F0.zip* with *7z*, it asked for password. Revisited *image.jpg* and found password *mr_b1n*.

```bash
$ vim image.jpg
...pass:<89>mr_b1n...
```

After decompression, *bin* file contained 360001 bytes. According to hint from image.jpg, *bin* is a 600x600 ascii picture.

```bash
$ strings image.jpg |head
JFIF
NjAweDYwMF9waWN0dXJl
QA%C
(%-B
 B)X
k&v+
!`BB
%d @)
KBABXX0
L^W*Pd
$ base64 -d <<< NjAweDYwMF9waWN0dXJl
600x600_picture
```

The line was too long to read even reshaped it to matrix of 600x600. Trimed additional 0s from top, bottom, left and right, read it vertically the flag was *CTFlearn{y0u_n4i13d_it}*
