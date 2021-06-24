
Play around with the *sneks.pyc*, it seems the code read a string from comman line argument and encode each character to number. Tried out string *'flag{'*

```bash
python3 sneks.pyc flag{
9273726921930789991758 166410277506205636620946 836211434898484229672 15005205362068960832084 226983740520068639569752018 
```

The output was the same as the first 5 numbers in output. So if we try out the possible characters for each position in flag, if the output matches the prefix in *output.txt*, it's the right character, iterate throught all numbers in *output.txt* shall recover the flag.

```python
def bruteforce():
    output = open('output.txt', 'rb').read()
    flag = 'flag{'
    for i in range(5, len(output.split())):
        for a in range(33, 127):
            p = Popen(['python3', target, flag+chr(a)], stdout=PIPE)
            res = p.stdout.read()
            if res == output[:len(res)]:
                flag += chr(a)
                print(flag)
                break
    print(flag)
```

```bash
flag{s
flag{s3
flag{s3q
flag{s3qu
flag{s3qu3
flag{s3qu3n
flag{s3qu3nc
flag{s3qu3nc3
flag{s3qu3nc35
flag{s3qu3nc35_
flag{s3qu3nc35_4
flag{s3qu3nc35_4n
flag{s3qu3nc35_4nd
flag{s3qu3nc35_4nd_
flag{s3qu3nc35_4nd_5
flag{s3qu3nc35_4nd_5u
flag{s3qu3nc35_4nd_5um
flag{s3qu3nc35_4nd_5um5
flag{s3qu3nc35_4nd_5um5}
flag{s3qu3nc35_4nd_5um5}
```
