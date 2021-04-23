Inspect the source code of malvertising homepage, there is a link to /ads/ad.html, which is the ad page.
Inspect the ad page found a metris.js.

To decode the key strings, 
- disable the click event listener in browser
- add alert(<encoded key string>) to a button tag

prettify the js code and decode some of the key strings, the logic is getting clear.

```js
l();
var s="constructor";
var t=document['getElementById']("adimg");
t['onload']=function(){
  try{
    var u=steg['decode'](t);
  }catch(v){
  }
  if(Number(/android/i['test'](navigator['userAgent']))){
    s[s][s](u)();
  }
};
```

There is a decode logic to run, which requires userAgent to be 'android'.

change the user agent in browser. go to 'Network conditions' in 'more tools', change the user agent to 'android'.
After refresh the ad page, we have another js file in sources.

```bash
  /ads/src/uHsdvEHFDwljZFhPyKxp.js
```

Brute force to find the key.

```js
for (let i = 'A'.charCodeAt(0); i <= 'Z'.charCodeAt(0); i++) {
  for (let j = 'A'.charCodeAt(0); j <= 'Z'.charCodeAt(0); j++) {
    lan = String.fromCharCode(i) + String.fromCharCode(j);
    for (let k = 0; k < 512; k++) {
      // LINUX00000EN0001011MOZILLA003
      // LINUX00000{lan}{ref/redirectCount/cookieNabled/onLine}MOZILLA003
      ref = k.toString(2);
      key = 'LINUX10000' + lan + ref + 'MOZILLA003'; 
      res = T.d0(a, key);
      var invalid = false;
      for (let err = 0; err < res.length; err++) {
        if (res[err].charCodeAt(0) > 126) {
          invalid = true;
          break;
        }
      }

      if (invalid) continue;
      console.log(key, res);
    }
  }
}
```

With the correct key we got another path

```bash
  src/npoTHyBXnpZWgLorNrYc.js
```

After prettify npoTHyBXnpZWgLorNrYc.js we found a path in the script.

```js
_0x3ed5d1['setAttribute']('src','./src/WFmJWvYBQmZnedwpdQBU.js');
document['head']['appendChild'](_0x3ed5d1);
```

By wget the path, we found the flag in the source code.

```bash
wget https://malvertising.web.ctfcompetition.com/ads/src/WFmJWvYBQmZnedwpdQBU.js
```
