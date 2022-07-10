from scapy.all import *

syn_segment = TCP(dport=24601, seq=123, flags='S')
syn_packet = IP(dst='www.google.com')/syn_segment

syn_ack_packet = sr1(syn_packet)
syn_ack_packet.show()

ack_value = syn_ack_packet[TCP].seq + 1
ack_segment = TCP(dport=80, seq=124, ack=ack_value, flags='A')
ack_packet = IP(dst='www.google.com')/ack_segment
send(ack_packet)
