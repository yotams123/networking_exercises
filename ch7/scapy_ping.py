from scapy.all import *

HOST = 'www.google.com'

icmp_packet = ICMP()
full_packet = IP(dst=HOST)/ICMP()

response_packet = sr1(full_packet)
response_packet.show()