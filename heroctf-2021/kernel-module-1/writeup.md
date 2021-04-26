
The *cat* command on server is malfunctioning, *which* command said *cat* command is using */bin/cat*. To correct it, we remove */bin/cat*, the whole vm is built upon *busybox*, so soft link */bin/busybox* to */bin/cat*.

```bash
rm -f /bin/cat
ln -s /bin/busybox /bin/cat
```

*cat /dev/safe* to get the flag.

```bash
cat /dev/safe
Hero{s0_yOu_C4n_r34d_Fr0m_cHrD3v}
```
