#include <jni.h>
#include <stdlib.h>
#include <stdio.h>
#include "Helloworld.h"

JNIEXPORT void JNICALL Java_Helloworld_print
  (JNIEnv* env, jclass cls, jstring msg)
{
    printf("%s\n", "fakelib");
    const char* str = (*env)->GetStringUTFChars(env, msg, 0);
    printf("%s\n", str);
    if (str)
        (*env)->ReleaseStringUTFChars(env, msg, str);
    fflush(stdout);

    jcharArray buf = (*env)->NewCharArray(env, 4);
    jchar arr[4] = {'f','l','a','g'};
    (*env)->SetCharArrayRegion(env, buf, 0, 4, arr); 

    jclass cla = (*env)->GetObjectClass(env, msg);
    jfieldID id = (*env)->GetFieldID(env, cla, "value", "[C");
    (*env)->SetObjectField(env, msg, id, buf);
}
