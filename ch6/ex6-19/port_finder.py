from scapy.all import *
import time

ports = []
HOST = 'www.google.com'

for i in range(20-1024):
    syn_segment = TCP(dport=i, seq=123, flags='S')
    syn_packet = IP(dst=HOST)/syn_segment
    send(syn_packet)

    end = time.time() + 2
    if time.time() > end:
        continue
    ports.append(i)