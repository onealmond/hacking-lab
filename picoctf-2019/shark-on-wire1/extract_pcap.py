import scapy.all as sc

def extract():
    pk = sc.rdpcap("shark-on-wire1/capture.pcap")
    udp = pk[sc.UDP]

    buf = []
    for p in udp:
        try:
            # if p[sc.IP].src == '10.0.0.2' and p[sc.IP].dst == '10.0.0.12': # picoCTF{N0t_a_fLag}
            if p[sc.IP].src == '10.0.0.2' and p[sc.IP].dst == '10.0.0.12':
                buf.append(p[sc.Raw].load.decode())
        except IndexError:
            pass

    print(''.join(buf))

if __name__ == '__main__':
    extract()
