
Key information

- every column of pixels was put side by side
- width of the image was 304 

Check out with *exiftool*, the image size is *27968x1*, *27968/304 == 92.0*, so the actual height is 92.

```bash
$ exiftool out+copy.jpg
ExifTool Version Number         : 12.16
File Name                       : out+copy.jpg
Directory                       : .
File Size                       : 42 KiB
File Modification Date/Time     : 2021:05:07 11:13:49+08:00
File Access Date/Time           : 2021:05:07 11:52:09+08:00
File Inode Change Date/Time     : 2021:05:07 11:51:32+08:00
File Permissions                : rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : None
X Resolution                    : 1
Y Resolution                    : 1
Image Width                     : 27968
Image Height                    : 1
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 27968x1
Megapixels                      : 0.028
```

The correct order of pixels in messed up image looks like

```python
pixel[0,0],pixel[0,1],pixel[0,2]...pixel[0,303],pixel[1,0],pixel[1,1],pixel[1,2]...pixel[1,303]...pixel[91,303]
```

So to correct this, read pixel at every 92 steps in row , join them together to be one new row, repeated until reached the all the pixels. The flag is in image preview.

```python
img = Image.open('out+copy.jpg', 'r')
img = img.convert('RGB')
pixels = img.load()

w, _  = img.size
actual_h = w // 304

img_fixed = Image.new(img.mode, (304, actual_h))
fixed = img_fixed.load()

fy = 0

for x in range(0, actual_h):
    row = []
    fx = 0
    for i in range(x, w, actual_h):
        fixed[fx,fy] = pixels[i,0]
        fx += 1
    fy += 1

img_fixed.show()
```
