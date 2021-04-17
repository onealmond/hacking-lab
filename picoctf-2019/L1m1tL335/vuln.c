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

void replaceIntegerInArrayAtIndex(unsigned int *array, int index, int value) {
   array[index] = value;
}

int main(int argc, char *argv[])
{
   int index;
   int value;
   int array[666];
   puts("Input the integer value you want to put in the array\n");
   scanf("%d",&value);
   fgetc(stdin);
   puts("Input the index in which you want to put the value\n");
   scanf("%d",&index);
   replaceIntegerInArrayAtIndex(array,index,value);
   exit(0);
}

