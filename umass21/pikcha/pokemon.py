import requests
import json
import base64

remote = "http://104.197.195.221:8084"

def parse():
    sess = base64.decodebytes(rsp.cookies['session'].split('.')[0].encode()+b'==')
    ans = json.loads(sess)['answer']
    guess = ' '.join(map(str, json.loads(sess)['answer']))
    return guess

rsp = requests.get(remote)
guess = parse()

for i in range(1, 501):
    rsp = requests.post(remote,
            data={'guess': guess},
            headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            },
            cookies=rsp.cookies)
    print(rsp.text)
    guess = parse()
