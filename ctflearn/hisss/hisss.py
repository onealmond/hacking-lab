#!/usr/bin/env python3
from PIL import Image
import numpy as np

png1 = Image.open('1.png')
png2 = Image.open('2.png')

png1 = np.array(png1)
png2 = np.array(png2)

result = np.bitwise_xor(png1, png2).astype(np.uint8)
Image.fromarray(result).show()
#CTF{I_L0V3_PYTH0N}
