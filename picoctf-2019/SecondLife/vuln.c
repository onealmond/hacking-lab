#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#define FLAG_BUFFER 200
#define LINE_BUFFER_SIZE 20

void win() {
  char buf[FLAG_BUFFER];
  FILE *f = fopen("flag.txt","r");
  fgets(buf,FLAG_BUFFER,f);
  fprintf(stdout,"%s\n",buf);
  fflush(stdout);
}

int main(int argc, char *argv[])
{
   //This is rather an artificial pieace of code taken from Secure Coding in c by Robert C. Seacord 
   char *first, *second, *third, *fourth;
   char *fifth, *sixth, *seventh;
   first=malloc(256);
   printf("Oops! a new developer copy pasted and printed an address as a decimal...\n");
   printf("%d\n",first);
   fgets(first, LINE_BUFFER_SIZE, stdin);
   second=malloc(256);
   third=malloc(256);
   fourth=malloc(256);
   free(first);
   free(third);
   fifth=malloc(128);
   free(first);
   sixth=malloc(256);
   puts("You should enter the got and the shellcode address in some specific manner... an overflow will not be very useful...");
   gets(sixth);
   seventh=malloc(256);
   exit(0);
}

