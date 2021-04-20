import string, re
from subprocess import Popen, PIPE

enc_flag = 'JcOCLQgPJEjwNAZHgVFzAoMVHOiCRVAVKkvFidUvzmUSSnqJzO'
flag = []
pat = re.compile('Flag: (\w+)\n')
candidates = string.ascii_lowercase+string.ascii_uppercase+string.digits+'_'+'-'

for k in range(len(enc_flag)):
    for c in candidates:
        with open('flag.txt', 'w') as fd:
            fd.write(''.join(flag)+c)
        p = Popen(['./revme'], stdout=PIPE)
        enc = pat.search(p.stdout.read().decode()).group()[6:].strip()
        if enc[k] == enc_flag[k]:
            flag.append(c)
            break

print(''.join(flag))
