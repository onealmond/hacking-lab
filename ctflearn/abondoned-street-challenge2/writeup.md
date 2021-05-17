
Examined the jpg file with *exiftool*, it shown the image width is 2016, height is 900.

```bash
Image Width                     : 2016
Image Height                    : 900
```

Checked out file size, 1008578 bytes.

```bash
$ wc -c abondoned_street_challenge2.jpg 
1008578 abondoned_street_challenge2.jpg
```
Roughly calculated height and width.

```python
>>> 1008578/900
1120.6422222222222
```

Considered changing the width to *1120*. To alter the width need to locate start of frame marker, *ffc0*.

> Start of frame marker (FFC0)

> - the first two bytes, the length, after the marker indicate the number of bytes, including the two length bytes, that this header contains
> - P -- one byte: sample precision in bits (usually 8, for baseline JPEG)
> - Y -- two bytes
> - X -- two bytes
> - Nf -- one byte: the number of components in the image
>   - 3 for color baseline JPEG images
>   - 1 for grayscale baseline JPEG images
> - Nf times:
>   - Component ID -- one byte
>   - H and V sampling factors -- one byte: H is first four bits and V is second four bits
>   - Quantization table number-- one byte

Source [post](http://www.geocities.ws/crestwoodsdd/JPEG.htm)

When the marker is located at *i*, then positions needed to change are *i+5* and *i+6*, 1120 is *0x460* in hex.

```python
data = open('abondoned_street_challenge2.jpg', 'rb').read()

i = 0
xi = 0
yi = 0
while i < len(data):
    i = data.find(b'\xff\xc0', i)
    if i == -1: break
    yi = i+5
    xi = i+7
    break

print('x', xi, data[xi:xi+2], 'y', yi, data[yi:yi+2])
data = data[:yi] + b'\x04\x60' + data[yi+2:]
with open('fix.jpg', 'wb') as fd:
    fd.write(data)
```

Fixed image shown string *"urban_exploration"*, so flag was *CTFlearn{urban_exploration}*.
