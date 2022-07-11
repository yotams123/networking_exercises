from scapy.all import *


def dns_filter(packet):
    return DNS in packet and packet[DNS].opcode == 0 and packet[DNSQR].qtype==1


def s(packet):
    packet_udp = UDP(dport=packet[UDP].sport, sport=packet[UDP].dport)
    packet_ip = IP(dst=packet[IP].src, src=packet[IP].dst)
    packet_dns = None
    with open('db.txt', 'r') as db:
        for line in db:
            site = line.split()[0]
            if site in str(packet[DNSQR].qname):
                addr = line.split()[1]
                print("found")
                packet_dns = DNS(id=packet[DNS].id, qd=packet[DNS].qd, aa=1, qr=1,
                                    an=DNSRR(rrname=packet[DNS].qd.qname, ttl=100, rdata=addr))
                print(addr)
    if not packet_dns:
        dns_query = DNS(rd=1, qd=DNSQR(qname=packet[DNSQR].qname))
        response = sr1(IP(dst="198.41.0.4")/UDP(dport=53)/dns_query, verbose=0)
        packet_dns = response[DNS]
        packet_dns.show()
    packet_to_send = packet_ip/packet_udp/packet_dns
    send(packet_to_send)
    return


while True:
    my_packets = sniff(count=1, lfilter=dns_filter, prn=s)