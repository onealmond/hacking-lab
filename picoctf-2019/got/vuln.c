#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define FLAG_BUFFER 128

void win() {
  char buf[FLAG_BUFFER];
  FILE *f = fopen("flag.txt","r");
  fgets(buf,FLAG_BUFFER,f);
  puts(buf);
  fflush(stdout);
}


int *pointer;

int main(int argc, char *argv[])
{
  
   puts("You can just overwrite an address, what can you do?\n");
   puts("Input address\n");
   scanf("%d",&pointer);
   puts("Input value?\n");
   scanf("%d",pointer);
   puts("The following line should print the flag\n");
   exit(0);
}
