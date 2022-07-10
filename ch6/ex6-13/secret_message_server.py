from scapy.all import *
msg = ""


def filter_message(packet):
    return UDP in packet and packet[IP].src == "127.0.0.1"


def print_char(packet):
    char = packet[UDP].dport
    msg += chr(char)


while True:
    packet = sniff(count=1, lfilter=filter_message, prn=print_char)
    if filter_message(packet) and packet[UDP].dport == 12345:
        break
