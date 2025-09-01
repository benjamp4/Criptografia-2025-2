#!/usr/bin/env python3
from scapy.all import rdpcap, ICMP
import sys

GREEN = "\033[32m"
RESET = "\033[0m"
# === Descifrado César ===
def caesar_decipher(texto, corrimiento):
    out = []
    for ch in texto:
        if 'a' <= ch <= 'z':
            out.append(chr((ord(ch) - 97 - corrimiento) % 26 + 97))
        elif 'A' <= ch <= 'Z':
            out.append(chr((ord(ch) - 65 - corrimiento) % 26 + 65))
        else:
            out.append(ch)
    return ''.join(out)
# === Heurística para puntuar textos plausibles ===
def score_text(texto):
    frecuentes = "aeiosnrlct" 
    return sum(texto.lower().count(c) for c in frecuentes)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} archivo.pcapng")
        sys.exit(1)

    filename = sys.argv[1]
    pkts = rdpcap(filename)
    # Extraer mensaje cifrado de los ICMP
    chars = []
    for pkt in pkts:
        if ICMP in pkt and pkt[ICMP].type == 8:  # echo-request
            raw = bytes(pkt[ICMP].payload)
            if raw:
                ch = raw[:1].decode(errors="ignore")
                if ch:
                    chars.append(ch)

    mensaje_cifrado = ''.join(chars)
    # Probar todos los corrimientos y calcular puntajes
    opciones = []
    for corr in range(26):
        texto = caesar_decipher(mensaje_cifrado, corr)
        puntaje = score_text(texto)
        opciones.append((texto, puntaje, corr))

    # Determinar el mejor corrimiento (más alto puntaje)
    mejor_corr = max(opciones, key=lambda x: x[1])[2]
    # Mostrar corrimiento 1,2,3... con el correcto en verde
    print("\nResultados del descifrado:\n")
    for texto, puntaje, corr in opciones:
        if corr == mejor_corr:
            print(GREEN + f"[Corrimiento {corr:2}] {texto}" + RESET)
        else:
            print(f"[Corrimiento {corr:2}] {texto}")
