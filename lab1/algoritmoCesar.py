# algoritmoCesar.py

def caesar_cipher(texto, corrimiento):
    resultado = ""

    for char in texto:
        if char.islower():
            resultado += chr((ord(char) - ord('a') + corrimiento) % 26 + ord('a'))
        elif char.isupper():
            resultado += chr((ord(char) - ord('A') + corrimiento) % 26 + ord('A'))
        else:
            resultado += char
    return resultado

if __name__ == "__main__":
    texto = input("Ingrese el texto a cifrar: ")
    corrimiento = int(input("Ingrese el corrimiento: "))
    texto_cifrado = caesar_cipher(texto, corrimiento)
    print("Texto cifrado:", texto_cifrado)
