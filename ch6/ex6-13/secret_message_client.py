from scapy.all import *

msg = input("Enter message: ")

for i in msg:
    port = ord(i)
    packet = IP(dst='127.0.0.1')/UDP(sport=12345, dport=port)
    packet.show()
    send(packet)

packet = IP(dst='127.0.0.1')/UDP(sport=12345, dport=12345)