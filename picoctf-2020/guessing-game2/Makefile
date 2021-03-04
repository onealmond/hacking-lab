all:
	#gcc -m32 -no-pie -Wl,-z,relro,-z,now -o vuln vuln.c
	gcc -m64 -no-pie -Wl,-z,relro,-z,now -o vuln64 vuln.c

clean:
	rm vuln
