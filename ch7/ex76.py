from scapy.all import *
import argparse


def run(a):
    count = 0
    print("Sending 4 packets.....")
    try:
        p = IP(dst=a)/ICMP()
        plist = []
        for i in range(4):
            plist.append(p)
        count = len(sr(plist, timeout=3)[0])
    except socket.gaierror:
        print("Not a valid IP address")
    print(f"Recieved {count} responses")


parser = argparse.ArgumentParser()
parser.add_argument("addr", help="Address to ping")

addr = parser.parse_args().addr
run(addr)
