# main.py
from algoritmoCesar import caesar_cipher
from pingv4 import send_stealth_ping

# Entrada del usuario
texto = input("Ingrese el texto a cifrar: ")
corrimiento = int(input("Ingrese el corrimiento: "))

# Cifrado César
texto_cifrado = caesar_cipher(texto, corrimiento)
print("Texto cifrado:", texto_cifrado)

# Enviar automáticamente por ICMP
send_stealth_ping(texto_cifrado)
