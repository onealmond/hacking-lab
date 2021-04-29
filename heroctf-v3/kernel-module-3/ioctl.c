#include <sys/ioctl.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

int main() {
  printf("ioctl...");
  fflush(stdout);
  int fd = open("/dev/safe", O_RDWR);
  if (fd < 0) {
    printf("failed to open device\n");
    fflush(stdout);
    close(fd);
    return 0;
  }

  // unlock lock1
  int res = ioctl(fd, 0x40087877, 0x45);
  if (res != 0) {
    printf("ioctl failed, %d", res);
    fflush(stdout);
    goto quit;
  }
  // unlock lock2
  res = ioctl(fd, 0x40087877, 0x2f);
  if (res != 0) {
    printf("ioctl failed, %d", res);
    fflush(stdout);
    goto quit;
  }

  // unlock lock3
  res = ioctl(fd, 0x40087877, 0x14);
  if (res != 0) {
    printf("ioctl failed, %d", res);
    fflush(stdout);
    goto quit;
  }
  system("cat flag.txt");

quit:
  close(fd);
  return 0;
}
