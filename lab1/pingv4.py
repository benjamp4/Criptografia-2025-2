# pingv4.py
from scapy.all import IP, ICMP, send
import os

def send_stealth_ping(message, dst="8.8.8.8"):
    for ch in message:
        payload = bytes(ch, 'utf-8') + os.urandom(48 - 1)
        pkt = IP(dst=dst) / ICMP(type="echo-request") / payload
        send(pkt, verbose=0)
