from scapy.all import *

# ip_packet = IP(dst="www.google.com")/Raw("CYYYYYBBBBBBEEEERRRR")
# ip_packet.show()
# send(ip_packet)


def facebook_filter(packet):
    return IP in packet and (packet[IP].dst == '157.240.196.35' or packet[IP].src == "157.240.196.35")


my_packets = sniff(count=10, lfilter=facebook_filter)
my_packets.summary()