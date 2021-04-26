
Decompile *JNI.apk* with *apktool*, go direct to *fr.heroctf.jni.MainActivity* class as indicated in *AndroidManifest.xml*.

```xml
...
<activity android:name="fr.heroctf.jni.MainActivity">
    <intent-filter>
        <action android:name="android.intent.action.MAIN"/>
        <category android:name="android.intent.category.LAUNCHER"/>
    </intent-filter>
</activity>
...
```

*fr.heroctf.jni.MainActivity* is defined in *smali/fr/heroctf/jni/MainActivity.smali*. *checkFlag* function quickly grabbed eyeballs. As it's a native function, we need to look for the lower-level implementation, which is in ``lib``.

```java
...
invoke-virtual {p0, v0}, Lfr/heroctf/jni/MainActivity;->checkFlag(Ljava/lang/String;)Z
...
# virtual methods
.method public native checkFlag(Ljava/lang/String;)Z
.end method
```

There are 4 *so* for 4 architectures respectively.

```bash
lib/
lib/x86
lib/x86/libnative-lib.so
lib/arm64-v8a
lib/arm64-v8a/libnative-lib.so
lib/armeabi-v7a
lib/armeabi-v7a/libnative-lib.so
lib/x86_64
lib/x86_64/libnative-lib.so
```

I decompiled the one for *x86_64*, *lib/x86_64/libnative-lib.so*.

```c
ulong Java_fr_heroctf_jni_MainActivity_checkFlag
                (_JNIEnv *param_1,undefined8 param_2,_jstring *param_3)
{
  char *input;
  size_t len;
  long in_FS_OFFSET;
  byte ret;
  uchar is_copy;
  long canary;
  
  canary = *(long *)(in_FS_OFFSET + 0x28);
  input = (char *)GetStringUTFChars(param_1,param_3,&is_copy);
  if ((((is_copy == '\x01') && (len = strlen(input), len == 3)) && (*input == '6')) &&
     ((input[1] == '6' && (input[2] == '6')))) {
    ret = 1;
  }
  else {
    ret = 0;
  }
  if (*(long *)(in_FS_OFFSET + 0x28) == canary) {
    return (ulong)ret;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

According to the way it check flag, it's easy to point out what the kernel is, by adding the flag prefix and suffix, the flag is ``Hero{666}``.

