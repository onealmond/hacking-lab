libhello.so : fakelib.o
	cc fakelib.o -shared -o libhello.so
	mkdir -p .helloWorld
	cp libhello.so .helloWorld
	
fakelib.o : 
		cp /home/lib/Helloworld.h .
		cc  -c -I/usr/lib/jvm/java-8-openjdk-amd64/include -fpic fakelib.c
