def caesar_cipher(text, shift):
    result = ''
    for char in text:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
        elif char.isdigit():
            shifted_char = str((int(char) + shift) % 10)
        else:
            shifted_char = char
        result += shifted_char
    return result

texto_plano = "CHAO"
clave = 3
texto_cifrado = caesar_cipher(texto_plano, clave)

print(f"Texto cifrado: {texto_cifrado}")

texto_descifrado = caesar_cipher(texto_cifrado, -clave)
print(f"Texto descifrado: {texto_descifrado}")