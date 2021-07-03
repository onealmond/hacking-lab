Used an [online java compiler](https://www.onlinegdb.com/online_java_compiler) to bruteforce the seed with the following *main* function.

```java
public static void main(String[] args) {
        for (int s = 1; s < 1000; s++) {
          Random rand = new Random(s);
          char[] flag = new char[33];
          int[] c = {13, 35, 15, -18, 88, 68, -72, -51, 73, -10, 63, 
                          1, 35, -47, 6, -18, 10, 20, -31, 100, -48, 33, -12, 
                          13, -24, 11, 20, -16, -10, -76, -63, -18, 118};
          for (int i = 0; i < flag.length; i++) {
                  int r = rand.nextInt(128);
                  int n = r + c[i];
                  flag[i] = (char)n;
          }
          if (flag[0] == 'f' && flag[1] == 'l' && flag[32] == '}')
            display(flag);
        }
}
```


After a while the flog shown up *flag{s33d3d_r4nd0m1z3rs_4r3_c00l}*.
