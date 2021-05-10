
Print every pixel in hex with *PIL*.

```python
img = Image.open('color_img.png', 'r')
img = img.convert('RGB')

pixels = img.load()
w, h = img.size

for y in range(h):
    s = []
    for x in range(w):
        r, g, b = pixels[x, y]
        print(' #{:02x}{:02x}{:02x}'.format(r,g,b), end='')
    print()
```

It's not hard to figure that every row is the same according to image preview, so took a look into one row. Then I realized that these were some letters in ASCII, well, repeatedly.

```bash
#666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #666c61 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #677b63 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #306c30 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #725f63 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #306433 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00 #647d00
```

Instead of printing color code, printed them as characters.

```python
        print(''.join(map(chr, [r,g,b])), end='')
```

Now it looks better.

```bash
flaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflaflag{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{cg{c0l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l00l0r_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_cr_c0d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d30d3d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}d}
```

By skipping duplicate pixels, it shown the flag.

```python
for y in range(h):
    s = []
    for x in range(w):
        if pixels[x,y] == pixels[x-1,y]:continue
        r, g, b = pixels[x, y]
        print(''.join(map(chr, [r,g,b])), end='')
    print()
    break
```
