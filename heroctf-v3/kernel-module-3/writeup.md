
This was the third round of kernel module challenges. This time, *"cat /dev/safe"* indicates there are three locked locks.

```bash
/ $ cat /dev/safe
Safe state :
 - Lock1 : Locked
 - Lock2 : Locked
 - Lock3 : Locked
pLNLKetvAnbu
            KeMиetvAnb u@K0pPKuKrL@@/ $
```

Download and decompile *"safe_mod.ko"*, same steps can be found in writeup for [last round](../kernel-module-2/writeup.md). There two event handlers *device_file_ioctl* and *device_file_read*. take a look into *device_file_ioctl*. *ioctl*, input and output control, is system call to pass control commands and arguments to device driver. *device_file_ioctl* unlocks lock1 with command *0x40087877* and argument *0x45*. Lock3 needs lock1 and lock2 to be unlocked first, passing argument *0x2f* to unlock lock2, lock3 can be unlocked with argument *0x14*.

```c
undefined8 device_file_ioctl(undefined8 param_1,undefined8 param_2,ulong param_3)
{
  long lVar1;
  long in_GS_OFFSET;
  
  printk(&DAT_001004b0,param_2,0x40087877,param_3 & 0xffffffff);
  printk(&DAT_001005f7,(ulong)((int)param_2 == 0x40087877));
  if ((int)param_2 == 0x40087877) {
    printk(&DAT_00100607);
    if ((lock1 != '\0') && (param_3 == 0x45)) {
      lock1 = '\0';
      printk(&DAT_00100624);
    }
    if (lock1 == '\0') {
      if (lock2 == '\0') {
        if ((lock3 != '\0') && (param_3 == 0x14)) {
          lock3 = '\0';
          printk(&DAT_001004e0);
          if (*(long *)(&current_task + in_GS_OFFSET) == 0) {
            printk(&DAT_00100510);
          }
          else {
            printk(&DAT_00100540,(ulong)*(uint *)(*(long *)(&current_task + in_GS_OFFSET) + 0x4e8));
            lVar1 = prepare_creds();
            if (lVar1 == 0) {
              printk(&DAT_00100570);
            }
            else {
              *(undefined4 *)(lVar1 + 0x14) = 0;
              *(undefined4 *)(lVar1 + 4) = 0;
              *(undefined4 *)(lVar1 + 0x18) = 0;
              *(undefined4 *)(lVar1 + 8) = 0;
              commit_creds(lVar1);
            }
          }
        }
      }
      else {
        if (param_3 == 0x2f) {
          lock2 = '\0';
          printk(&DAT_0010063e);
        }
      }
    }
  }
  else {
    printk(&DAT_00100658);
  }
  printk(&DAT_0010066d);
  return 0;
}
```

It needed to read *flag.txt* in code as root privileges were given to the unlock process only in this challenge. Coded this up as following.

```c
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
```

Enter shared directory */tmp/tmp.3jwI1hvC0l* on host and build it, in case of dependency issue we need to build it with ``-static`` flag to link dependency staticly.

```bash
gcc -static -o ioctl ioctl.c
```

Enter VM and run fresh built unlocker.

```bash
/ $ /mnt/share/ioctl
ioctl...Hey King (or Queen) !\n I hope you enjoyed these little challenges (this really served as an introduction).\n
If you liked these and want to learn more, check out the LinKern challenges on root-me ! :)\n Anyway, well played, because it's really not that easy..
Here's your flag : Hero{y0u_4re_Da_cHrD3V_M4sT3R}
```

### Reference

[IOCTL Man Page](https://man7.org/linux/man-pages/man2/ioctl.2.html)
