from scapy.all import *

domain = input("Enter domain: ")
packet = IP(dst='8.8.8.8')/UDP(sport=12345, dport=53)/DNS(qdcount=1)/DNSQR(qname=domain)

response = sr1(packet)

try:
    print(response[DNSRR][1].rdata)
except IndexError:
    print(response[DNSRR].rdata)
