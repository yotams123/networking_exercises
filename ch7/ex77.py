from scapy.all import *
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("addr", help="Address to ping")

HOST = parser.parse_args().addr

response = None
end_time = None
start_time = None
packet = None

try:
    start_time = time.time()
    packet = IP(dst=HOST, ttl=1)/ICMP()
    response = sr1(packet, verbose=0, timeout=3)
    end_time = time.time()
except socket.gaierror:
    print("Invalid host")
    quit(69)

t = 1
prev = None

while response[IP].src != prev:
    print(f"{t}\t{response[IP].src}\t\t{end_time - start_time} secs")
    prev = response[IP].src

    t += 1
    packet[IP].ttl = t

    start_time = time.time()
    response = sr1(packet, verbose=0)
    end_time = time.time()
