#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define FLAGSIZE 128

void win() {
  char buf[FLAGSIZE];
  FILE *f = fopen("flag.txt","r");
  fgets(buf,FLAGSIZE,f);
  fprintf(stdout,"%s\n",buf);
  fflush(stdout);
}

int main(int argc, char *argv[])
{
   char *fullname, *name, *lastname;
   fullname = malloc(666);
   name = malloc(66);
   lastname = malloc(66);
   printf("Oops! a new developer copy pasted and printed an address as a decimal...\n");
   printf("%d\n",fullname);
   printf("Input fullname\n");
   gets(fullname);
   printf("Input lastname\n");
   gets(lastname);
   free(fullname);
   puts("That is all...\n");
   free(name);
   free(lastname);
   exit(0);
}