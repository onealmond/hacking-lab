
mystery = open('../c0rrupt/mystery','rb').read()

def add_png_hdr1():
    hdr1=list(map(lambda x: int(x,16), ['0x'+c for c in
      '89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52'.split(' ')]))
    hdr2=list(map(lambda x: int(x,16),['0x'+c for c in '00 00 06 a1 00 00 02 60 08 02 00 00 00 85 ad 5e'.split(' ')]))

    buf = list(mystery)
    buf[:16] = hdr1
    buf[70] = 0
    buf[87:91] = [ord('I'),ord('D'),ord('A'),ord('T')]
    # distance between the 1st IDAT and the 2nd one
    #
    # $ binwalk -R IDAT c0rrupt/img.png
    #
    # DECIMAL       HEXADECIMAL     DESCRIPTION
    # --------------------------------------------------------------------------------
    # 87            0x57            IDAT
    # 65544         0x10008         IDAT
    # ...
    # dist = 65544 - 87 - 4 = 0xffa5
    #
    # 00000050: 5224 f0aa aaff a549 4441 5478 5eec bd3f  R$.....IDATx^..?
    #  we have 0xaaaaffa5
    # change aaaa to 0000
    buf[83:85] = [0, 0]
    
    with open('c0rrupt-img.png','wb') as fd:
        #fd.write(bytes(hdr1)+mystery)
        fd.write(bytes(buf))

add_png_hdr1()
