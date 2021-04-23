
It's a program built for 64-bit ARM architecture.

```bash
$ file chains
chains: ELF 64-bit LSB shared object, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, for GNU/Linux 3.7.0, stripped
$ checksec --file chains
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      FILE
Partial RELRO   No canary found   NX enabled    PIE enabled     No RPATH   No RUNPATH   chains
```

Decompile it with ``ghidra``, according to function ``FUN_00100838`` and ``FUN_001007cc``, we know that the program needs to calculate times return from ``FUN_001007cc`` for numbers from 1 to 900000000, if the times match value at even position(``target``) in array ``DAT_00111040``, then value at odd position(``count``) is reduced by 1. So if we group the array by ``target``, it's about to find the ``count``th value in corresponding ``target`` group.

```c
ulonglong FUN_001007cc(uint param_1)
{
  uint cur;
  uint ret;
  
  ret = 0;
  cur = param_1;
  while (cur != 1) {
    if ((cur & 1) == 0) {
      cur = cur >> 1;
    }
    else {
      cur = cur * 3 + 1;
    }
    ret = ret + 1;
  }
  return (ulonglong)ret;
}

undefined8 FUN_00100838(void)
{
  int target;
  int res;
  uint cur;
  uint N;
  int count;
  
  cur = 0;
  do {
    if (0x29f7 < cur) {
      putchar(10);
      return 0;
    }
    target = *(int *)(&DAT_00111040 + (ulonglong)cur * 4);
    count = *(int *)(&DAT_00111040 + (ulonglong)(cur + 1) * 4);
    N = 1;
    while (N < 900000000) {
      res = FUN_001007cc((ulonglong)N);
      if (target == res) {
        count = count + -1;
      }
      if (count == 0) {
        putchar(N + 0xca5b17ff);
        fflush(stdout);
        break;
      }
      N = N + 1;
    }
    cur = cur + 2;
  } while( true );
}
```

## Find out the array

``DAT_00111040`` is an integer array, dump the whole block of data and process it with ``python``.

```python
dat = dat.split(' ')
targets = []

for i in range(0, len(dat), 4):
  targets.append(int(''.join(reversed(dat[i:i+4])), 16))

print(targets)
print('targets size:', len(targets))

distinct_targets = dict()
counter = Counter()
for i in range(0, len(targets), 2):
    counter[targets[i]] += 1

print(counter)
print('counter size:', len(counter))
print(distinct_targets)
```

We get an array with 2686 elements, but only 19 distinct targets.

```python
[136, 4253818, 136, 4253813, 271, 1779864, 136, 4253816, 136, 4253816, 211, 3144285, 136,...,352, 495094, 136, 4253825, 181, 4130208, 136, 4253767]
targets size: 2686
Counter({211: 628, 136: 500, 160: 81, 181: 52, 352: 22, 266: 11, 105: 10, 271: 7, 199: 7, 273: 7, 247: 5, 113: 3, 341: 3, 110: 2, 303: 1, 318: 1, 116: 1, 202: 1, 185: 1})
counter size: 19
```

## Calculate times

As we only interest in results from ``FUN_001007cc`` that exist in distinct targets, we could precalculate them for reference. The max target is ``352``, then we stop calculate when it exceeds the value to save time. Redirect the result to file for later lookup. It took about 20min to generate the whole map.

```c++
unordered_map<unsigned int, vector<unsigned int>> target_group = {
 {211,vector<unsigned int>()},
 {136,vector<unsigned int>()},
 {160,vector<unsigned int>()},
 {181,vector<unsigned int>()},
 {352,vector<unsigned int>()},
 {266,vector<unsigned int>()},
 {105,vector<unsigned int>()},
 {271,vector<unsigned int>()},
 {199,vector<unsigned int>()},
 {273,vector<unsigned int>()},
 {247,vector<unsigned int>()},
 {113,vector<unsigned int>()},
 {341,vector<unsigned int>()},
 {110,vector<unsigned int>()},
 {303,vector<unsigned int>()},
 {318,vector<unsigned int>()},
 {116,vector<unsigned int>()},
 {202,vector<unsigned int>()},
 {185,vector<unsigned int>()}
};

unsigned int FUN_001007cc(unsigned int num) {
  unsigned int cur;
  unsigned int ret;
  
  ret = 0;
  cur = num;

  while (cur != 1 && ret < 353) {
    if ((cur & 1) == 0) {
      cur = cur >> 1;
    } else {
      cur = cur * 3 + 1;
    }
    ret++;
  }
  return (unsigned long)ret;
}

int precalculate() {
  unsigned int res, N;

  for (N = 1; N < 900000000; ++N) {
    res = FUN_001007cc(N);
    if (target_group.find(res) != target_group.end()){
      target_group[res].push_back(N);
    }
  }

  for (auto& t : target_group) {
    printf("%u:", t.first);
    for (auto& n : t.second) {
      printf("%u,", n);
    }
    printf("\n");
  }
  
  return 0;
}
```

## Lookup the targets

Now we iterate through the array to find matches, convert number at ``arr[cur+1]-1`` in ``target_group[arr[cur]]`` to ``char``, concatenate all the chars we get a long description about Collatz conjecture and the flag is at the end of it. It took about 28sec to generate the result.

```python
target_group = {}

with open('target_group') as fd:
    while True:
        l = fd.readline()
        if l == None or l == '':
            break
        t = l.split(":")
        target_group[int(t[0])] = list(map(int, t[1].split(',')[:-1]))

flag = ''

for cur in range(0, len(arr), 2):
    if target_group[arr[cur]] is not None:
        if arr[cur+1] <= len(target_group[arr[cur]]):
            N = target_group[arr[cur]][arr[cur+1]-1]
            print(N, (N+0xca5b17ff)%256, chr((N+0xca5b17ff)%256))
            flag += chr((N+0xca5b17ff)%256)
print('flag:', flag)
```




