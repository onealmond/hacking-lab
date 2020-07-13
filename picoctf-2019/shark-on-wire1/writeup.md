Download and open the pcap file with wireshark.

Check the UDP stream data, packages from 10.0.0.2 looks suspicious.

Using python scap module to load the pcap file.

Concat the raw data from 10.0.0.2 to 10.0.0.13, got a string in flag format, but it saids 
```
  picoCTF{N0t_a_fLag}
```
Concat the raw data from 10.0.0.2 to 10.0.0.12, got a valid flag
