def cifrar_vigenere(texto, clave):
    resultado = ""
    clave = clave.upper()
    j = 0  # índice para recorrer la clave

    for c in texto:
        if c.isalpha():
            offset = 65 if c.isupper() else 97
            p = ord(c.upper()) - 65
            k = ord(clave[j % len(clave)]) - 65
            cifrado = (p + k) % 26
            if c.isupper():
                resultado += chr(cifrado + 65)
            else:
                resultado += chr(cifrado + 97)
            j += 1
        else:
            resultado += c
    return resultado

def descifrar_vigenere(texto, clave):
    resultado = ""
    clave = clave.upper()
    j = 0

    for c in texto:
        if c.isalpha():
            offset = 65 if c.isupper() else 97
            p = ord(c.upper()) - 65
            k = ord(clave[j % len(clave)]) - 65
            descifrado = (p - k + 26) % 26
            if c.isupper():
                resultado += chr(descifrado + 65)
            else:
                resultado += chr(descifrado + 97)
            j += 1
        else:
            resultado += c
    return resultado

# Entrada de usuario
texto = input("Ingresa el texto: ")
clave = input("Ingresa la clave: ")

cifrado = cifrar_vigenere(texto, clave)
print("Texto cifrado:", cifrado)

descifrado = descifrar_vigenere(cifrado, clave)
print("Texto descifrado:", descifrado)
