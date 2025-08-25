def caesar_cipher(texto, corrimiento):
    resultado = ""

    for char in texto:
        # Si es letra minúscula
        if char.islower():
            resultado += chr((ord(char) - ord('a') + corrimiento) % 26 + ord('a'))
        # Si es letra mayúscula
        elif char.isupper():
            resultado += chr((ord(char) - ord('A') + corrimiento) % 26 + ord('A'))
        else:
            # Si no es letra, lo dejamos igual
            resultado += char
    return resultado


# Programa principal
if __name__ == "__main__":
    texto = input("Ingrese el texto a cifrar: ")
    corrimiento = int(input("Ingrese el corrimiento: "))

    texto_cifrado = caesar_cipher(texto, corrimiento)
    print("Texto cifrado:", texto_cifrado)
