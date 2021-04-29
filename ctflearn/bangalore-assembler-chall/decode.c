#include <stdio.h>

unsigned long vals1[30] = {0x00014c4c5e, 0x005130720c, 0x003e87df91, 0x00340ccb70, 0x00676fa321, \
            0x002aa1a2a0, 0x005165565c, 0x0005526445, 0x006a480682, 0x0033dfa545, \
            0x004c88ea19, 0x0073255b4e, 0x0074c67bfe, 0x0052f90324, 0x006f44e5df, \
            0x001435d143, 0x0066d75377, 0x0035b86969, 0x000448dc19, 0x000c13eaf7, \
            0x0015fedd23, 0x00422b655c, 0x0061ef012d, 0x000fd42ba5, 0x002ca8f2c9, \
            0x00054b8249, 0x006dc2f69d, 0x0076ba54d5, 0x0068e371c0, 0x001551247c
}; 
unsigned long vals2[30] = {0x0002f21618, 0x00577d3f68, 0x000c838fda, 0x0068e5cdc4, 0x006314b34d, \
            0x007a193245, 0x0009525af6, 0x0031a96ada, 0x0056957557, 0x0001610dfe, \
            0x002e59bcbf, 0x002051fae0, 0x0068b5e038, 0x0031f0fadb, 0x004160e7a4, \
            0x006e7ff823, 0x006130cd85, 0x0063a55548, 0x007a88b47f, 0x000938111f, \
            0x006b16ee35, 0x0078cb6446, 0x0016cab7a1, 0x001e9a7cd6, 0x0027f24b7f, \
            0x004a9f28e9, 0x00029c5bf9, 0x000ee5248e, 0x007e91a8b2, 0x006add9c6a
}; 
unsigned long vals3[30] = {0x0053d9c12d, 0x007e4f6f47, 0x0056084aad, 0x0053ce10aa, 0x00349ef85d, \
            0x007a19aaaa, 0x001e102afb, 0x005f71a2af, 0x005a6edb6c, 0x0021ca6074, \
            0x000de96e1d, 0x006def4121, 0x00626b818b, 0x0071f7f9f7, 0x0064c5dc07, \
            0x005c41e208, 0x003934170c, 0x0043ffab5b, 0x006aa9e600, 0x0070f44639, \
            0x0072f4fbbb, 0x0034b15564, 0x0055f40b0a, 0x00146e2173, 0x004c244136, \
            0x003d5f0e6a, 0x005b745413, 0x0074b3a37f, 0x0048669939, 0x0048659c9f
}; 
unsigned long vals4[30] = {0x0051095f4d, 0x000bd6fed3, 0x0021d06bec, 0x0068a2be66, 0x0065b4db28, \
            0x00523e80b2, 0x00151e2877, 0x007b25fbce, 0x001c3f1002, 0x005f3de306, \
            0x005190a5b8, 0x00141e6c1e, 0x0046f23ce0, 0x0002fd6107, 0x0005340b05, \
            0x0032e8d951, 0x0031aae0ef, 0x00721b2012, 0x0027b2da28, 0x0053c349bb, \
            0x002580f1e2, 0x001a0fb431, 0x00147d67e6, 0x0024ee0a0e, 0x003dd7b640, \
            0x0034f01b4d, 0x003d60a616, 0x007f05ad3c, 0x000b8b10dd, 0x007064f0ad
};
unsigned long flag [30] = {0x00a8f10265, 0x00e2b9dd5a, 0x003ed39108, 0x0137df46b0, 0x0163cf89f4, \
            0x0130e2005e, 0x0059c5c456, 0x00e4b06978, 0x00b6f2b73e, 0x0073c8b677, \
            0x00c89c6ede, 0x0112b6833f, 0x01060a173a, 0x00f81b68de, 0x00d9941c55, \
            0x0111dd04a2, 0x0122e71875, 0x014cbd3551, 0x003c2b50ed, 0x00b98307b9, \
            0x0119622208, 0x00a8575118, 0x0041cb19f0, 0x005eee93e0, 0x0056973551, \
            0x00a7a5c099, 0x00688bacfc, 0x017032876f, 0x00ba9e9447, 0x0138b04da1
};

unsigned long step1(int i) {
  unsigned long a = vals4[i];
  unsigned long b = flag[i];
  return b - a;
}

unsigned long step2(int i, unsigned long c) {
  unsigned long a = vals3[i];
  return a ^ c;
}

unsigned long step3(int i, unsigned long c) {
  unsigned long a = vals2[i];
  return c - a;
}

unsigned long step4(int i, unsigned long c) {
  unsigned long a = vals1[i];
  return c ^ a;
}

int main() {
  unsigned long res;
  unsigned long flag[30] = {0};

  for (int i = 0; i < 30; i++) {
    res = step1(i);
    res = step2(i, res);
    res = step3(i, res);
    res = step4(i, res);
    flag[i] = res % 256;
    printf("%c", flag[i]);
  }
}
