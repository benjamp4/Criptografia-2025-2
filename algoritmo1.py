# Entrada del usuario
texto = input("Ingresa el texto: ")
desplazamiento = int(input("Ingresa el desplazamiento: "))

resultado = ""

for c in texto: # recorriendo el string
    ascii_val = ord(c)              # ord sirve para obtener el valor numerico ascii de un caracter
    nuevo_val = (ascii_val + desplazamiento) % 256  # módulo 256 para no salir del rango ASCII
    resultado += chr(nuevo_val)     # convertir de nuevo a caracter

print("Texto cifrado:", resultado)
