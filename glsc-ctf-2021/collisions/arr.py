#!/usr/bin/env python3

def bytes_to_array(dat, sz):
    dat = dat.split()
    arr = []
    for i in range(0, len(dat), sz):
        arr.append(int(''.join(reversed(dat[i:i+sz])), 16))
    return arr


expected = "ba 19 2e 98 d2 af 0e ab 1c 77 8f f6 bb d5 42 fd c3 e4 af 98 03 82 7a 1b 1a cc 31 5b c0 46 bc f2 14 e5 7e 9e 4a 36 7b 18 45 92 88 91 59 09 78 75 c4 74 5c e3 fe 71 d2 45 ad 15 7a cd e9 f0 a8 ae"

crc32_tab = "00 00 00 00 96 30 07 77 2c 61 0e ee ba 51 09 99 19 c4 6d 07 8f f4 6a 70 35 a5 63 e9 a3 95 64 9e 32 88 db 0e a4 b8 dc 79 1e e9 d5 e0 88 d9 d2 97 2b 4c b6 09 bd 7c b1 7e 07 2d b8 e7 91 1d bf 90 64 10 b7 1d f2 20 b0 6a 48 71 b9 f3 de 41 be 84 7d d4 da 1a eb e4 dd 6d 51 b5 d4 f4 c7 85 d3 83 56 98 6c 13 c0 a8 6b 64 7a f9 62 fd ec c9 65 8a 4f 5c 01 14 d9 6c 06 63 63 3d 0f fa f5 0d 08 8d c8 20 6e 3b 5e 10 69 4c e4 41 60 d5 72 71 67 a2 d1 e4 03 3c 47 d4 04 4b fd 85 0d d2 6b b5 0a a5 fa a8 b5 35 6c 98 b2 42 d6 c9 bb db 40 f9 bc ac e3 6c d8 32 75 5c df 45 cf 0d d6 dc 59 3d d1 ab ac 30 d9 26 3a 00 de 51 80 51 d7 c8 16 61 d0 bf b5 f4 b4 21 23 c4 b3 56 99 95 ba cf 0f a5 bd b8 9e b8 02 28 08 88 05 5f b2 d9 0c c6 24 e9 0b b1 87 7c 6f 2f 11 4c 68 58 ab 1d 61 c1 3d 2d 66 b6 90 41 dc 76 06 71 db 01 bc 20 d2 98 2a 10 d5 ef 89 85 b1 71 1f b5 b6 06 a5 e4 bf 9f 33 d4 b8 e8 a2 c9 07 78 34 f9 00 0f 8e a8 09 96 18 98 0e e1 bb 0d 6a 7f 2d 3d 6d 08 97 6c 64 91 01 5c 63 e6 f4 51 6b 6b 62 61 6c 1c d8 30 65 85 4e 00 62 f2 ed 95 06 6c 7b a5 01 1b c1 f4 08 82 57 c4 0f f5 c6 d9 b0 65 50 e9 b7 12 ea b8 be 8b 7c 88 b9 fc df 1d dd 62 49 2d da 15 f3 7c d3 8c 65 4c d4 fb 58 61 b2 4d ce 51 b5 3a 74 00 bc a3 e2 30 bb d4 41 a5 df 4a d7 95 d8 3d 6d c4 d1 a4 fb f4 d6 d3 6a e9 69 43 fc d9 6e 34 46 88 67 ad d0 b8 60 da 73 2d 04 44 e5 1d 03 33 5f 4c 0a aa c9 7c 0d dd 3c 71 05 50 aa 41 02 27 10 10 0b be 86 20 0c c9 25 b5 68 57 b3 85 6f 20 09 d4 66 b9 9f e4 61 ce 0e f9 de 5e 98 c9 d9 29 22 98 d0 b0 b4 a8 d7 c7 17 3d b3 59 81 0d b4 2e 3b 5c bd b7 ad 6c ba c0 20 83 b8 ed b6 b3 bf 9a 0c e2 b6 03 9a d2 b1 74 39 47 d5 ea af 77 d2 9d 15 26 db 04 83 16 dc 73 12 0b 63 e3 84 3b 64 94 3e 6a 6d 0d a8 5a 6a 7a 0b cf 0e e4 9d ff 09 93 27 ae 00 0a b1 9e 07 7d 44 93 0f f0 d2 a3 08 87 68 f2 01 1e fe c2 06 69 5d 57 62 f7 cb 67 65 80 71 36 6c 19 e7 06 6b 6e 76 1b d4 fe e0 2b d3 89 5a 7a da 10 cc 4a dd 67 6f df b9 f9 f9 ef be 8e 43 be b7 17 d5 8e b0 60 e8 a3 d6 d6 7e 93 d1 a1 c4 c2 d8 38 52 f2 df 4f f1 67 bb d1 67 57 bc a6 dd 06 b5 3f 4b 36 b2 48 da 2b 0d d8 4c 1b 0a af f6 4a 03 36 60 7a 04 41 c3 ef 60 df 55 df 67 a8 ef 8e 6e 31 79 be 69 46 8c b3 61 cb 1a 83 66 bc a0 d2 6f 25 36 e2 68 52 95 77 0c cc 03 47 0b bb b9 16 02 22 2f 26 05 55 be 3b ba c5 28 0b bd b2 92 5a b4 2b 04 6a b3 5c a7 ff d7 c2 31 cf d0 b5 8b 9e d9 2c 1d ae de 5b b0 c2 64 9b 26 f2 63 ec 9c a3 6a 75 0a 93 6d 02 a9 06 09 9c 3f 36 0e eb 85 67 07 72 13 57 00 05 82 4a bf 95 14 7a b8 e2 ae 2b b1 7b 38 1b b6 0c 9b 8e d2 92 0d be d5 e5 b7 ef dc 7c 21 df db 0b d4 d2 d3 86 42 e2 d4 f1 f8 b3 dd 68 6e 83 da 1f cd 16 be 81 5b 26 b9 f6 e1 77 b0 6f 77 47 b7 18 e6 5a 08 88 70 6a 0f ff ca 3b 06 66 5c 0b 01 11 ff 9e 65 8f 69 ae 62 f8 d3 ff 6b 61 45 cf 6c 16 78 e2 0a a0 ee d2 0d d7 54 83 04 4e c2 b3 03 39 61 26 67 a7 f7 16 60 d0 4d 47 69 49 db 77 6e 3e 4a 6a d1 ae dc 5a d6 d9 66 0b df 40 f0 3b d8 37 53 ae bc a9 c5 9e bb de 7f cf b2 47 e9 ff b5 30 1c f2 bd bd 8a c2 ba ca 30 93 b3 53 a6 a3 b4 24 05 36 d0 ba 93 06 d7 cd 29 57 de 54 bf 67 d9 23 2e 7a 66 b3 b8 4a 61 c4 02 1b 68 5d 94 2b 6f 2a 37 be 0b b4 a1 8e 0c c3 1b df 05 5a 8d ef 02 2d"


expected = bytes_to_array(expected, 1)
print(expected, len(expected))

crc32_tab = bytes_to_array(crc32_tab, 4)
print(crc32_tab, len(crc32_tab))
