import base64
import codecs
import math

class SimpleBlockCipher:
    
    def __init__(self, key, block_size, intermittent_skip=0):
        """
        Inicializa el cifrador con los parámetros dados.
        
        :param key: La llave (string) a utilizar para el cifrado XOR.
        :param block_size: El tamaño del bloque (int) en bytes.
        :param intermittent_skip: int, número de bloques a *saltar* después de cifrar uno.
                                  0 = Cifrado normal (cifra todo).
                                  1 = Cifrar 1, saltar 1, cifrar 1, saltar 1...
                                  2 = Cifrar 1, saltar 2, cifrar 1, saltar 2...
        """
        if block_size <= 0:
            raise ValueError("El tamaño del bloque debe ser un entero positivo.")
        if not key:
            raise ValueError("La llave no puede estar vacía.")
            
        self.block_size = block_size
        self.intermittent_skip = intermittent_skip
        
        # Prepara la llave (requisito: "repetir si es más corta")
        self.prepared_key = self._prepare_key(key, block_size)

    def _prepare_key(self, key_str, block_size):
        """
        Expande o trunca la llave para que coincida con el tamaño del bloque.
        """
        key_bytes = key_str.encode('utf-8')
        key_len = len(key_bytes)
        
        if key_len == block_size:
            return key_bytes
        
        if key_len > block_size:
            # Si es más larga, la truncamos (comportamiento común)
            return key_bytes[:block_size]
        
        if key_len < block_size:
            # Si es más corta, la repetimos (como pide el requisito)
            repeats = math.ceil(block_size / key_len)
            return (key_bytes * repeats)[:block_size]

    def _pad_pkcs7(self, data):
        """
        Aplica padding PKCS7 a los datos.
        """
        # Calcula cuántos bytes de padding se necesitan
        padding_len = self.block_size - (len(data) % self.block_size)
        
        # El padding es el byte que representa la longitud del padding,
        # repetido 'padding_len' veces.
        padding = bytes([padding_len]) * padding_len
        return data + padding

    def _unpad_pkcs7(self, data):
        """
        Quita el padding PKCS7 de los datos.
        """
        if not data:
            raise ValueError("No se pueden desrellenar datos vacíos.")
            
        # El último byte indica la longitud del padding
        padding_len = data[-1]
        
        # Validación básica del padding
        if padding_len > self.block_size or padding_len == 0:
            raise ValueError("Padding incorrecto: longitud de padding inválida.")
        if padding_len > len(data):
            raise ValueError("Padding incorrecto: datos más cortos que el padding.")
        
        # Verifica que todos los bytes de padding sean correctos
        if data[-padding_len:] != bytes([padding_len]) * padding_len:
            raise ValueError("Padding incorrecto: bytes de padding no coinciden.")
            
        # Devuelve los datos sin el padding
        return data[:-padding_len]

    def _xor_bytes(self, data_block, key_block):
        """
        Realiza la operación XOR entre dos bloques de bytes.
        """
        return bytes([b1 ^ b2 for b1, b2 in zip(data_block, key_block)])

    def encrypt(self, message, output_format='base64'):
        """
        Cifra un mensaje de texto.
        
        :param message: El string de texto plano a cifrar.
        :param output_format: 'base64' o 'hex' para la salida.
        :return: El mensaje cifrado como string.
        """
        # 1. Convertir mensaje a bytes y aplicar padding
        data_bytes = message.encode('utf-8')
        padded_data = self._pad_pkcs7(data_bytes)
        
        # 2. Dividir en bloques
        blocks = [padded_data[i:i + self.block_size] 
                  for i in range(0, len(padded_data), self.block_size)]
        
        encrypted_blocks = []
        
        # 3. Cifrar bloques (XOR y cifrado intermitente)
        for i, block in enumerate(blocks):
            # Lógica intermitente:
            # (self.intermittent_skip + 1) es el tamaño del "ciclo"
            # (i % ciclo) == 0 significa que es el primer bloque del ciclo (el que se cifra)
            if self.intermittent_skip == 0 or (i % (self.intermittent_skip + 1) == 0):
                # Cifrar este bloque
                encrypted_blocks.append(self._xor_bytes(block, self.prepared_key))
            else:
                # Saltar este bloque (dejarlo sin modificar)
                encrypted_blocks.append(block)
                
        # 4. Unir bloques cifrados
        encrypted_data = b''.join(encrypted_blocks)
        
        # 5. Devolver en el formato solicitado
        if output_format == 'base64':
            return base64.b64encode(encrypted_data).decode('utf-8')
        elif output_format == 'hex':
            return codecs.encode(encrypted_data, 'hex').decode('utf-8')
        else:
            raise ValueError("Formato de salida no válido. Use 'base64' o 'hex'.")

    def decrypt(self, encrypted_message, input_format='base64'):
        """
        Descifra un mensaje.
        
        :param encrypted_message: El string cifrado (Base64 o Hex).
        :param input_format: 'base64' o 'hex' para la entrada.
        :return: El mensaje descifrado como string de texto plano.
        """
        # 1. Decodificar desde Base64 o Hex
        try:
            if input_format == 'base64':
                encrypted_data = base64.b64decode(encrypted_message)
            elif input_format == 'hex':
                encrypted_data = codecs.decode(encrypted_message, 'hex')
            else:
                raise ValueError("Formato de entrada no válido. Use 'base64' o 'hex'.")
        except Exception as e:
            return f"[Error al decodificar: {e}]"

        if len(encrypted_data) % self.block_size != 0:
             raise ValueError("Longitud de datos cifrados inválida (no es múltiplo del tamaño de bloque).")

        # 2. Dividir en bloques
        blocks = [encrypted_data[i:i + self.block_size] 
                  for i in range(0, len(encrypted_data), self.block_size)]
        
        decrypted_blocks = []
        
        # 3. Descifrar bloques (la lógica intermitente debe ser idéntica)
        for i, block in enumerate(blocks):
            if self.intermittent_skip == 0 or (i % (self.intermittent_skip + 1) == 0):
                # Descifrar (XOR es su propia inversa)
                decrypted_blocks.append(self._xor_bytes(block, self.prepared_key))
            else:
                # Este bloque se saltó, añadirlo tal cual
                decrypted_blocks.append(block)
                
        # 4. Unir bloques descifrados
        decrypted_padded_data = b''.join(decrypted_blocks)
        
        # 5. Quitar padding
        try:
            unpadded_data = self._unpad_pkcs7(decrypted_padded_data)
        except ValueError as e:
            return f"[Error de padding (llave o parámetros incorrectos?): {e}]"
        
        # 6. Decodificar a string
        try:
            return unpadded_data.decode('utf-8')
        except UnicodeDecodeError:
            return "[Error al decodificar UTF-8 (llave o parámetros incorrectos)]"

# --- NUEVA SECCIÓN: INTERFAZ DE TERMINAL ---

def get_validated_input(prompt, type_converter, validator=None, error_message="Entrada inválida"):
    """
    Función de ayuda para obtener y validar la entrada del usuario.
    """
    while True:
        user_input = input(prompt)
        try:
            value = type_converter(user_input)
            if validator is None or validator(value):
                return value
            else:
                print(error_message)
        except ValueError:
            print(error_message)

def main_cli():
    """
    Función principal para la interfaz de línea de comandos.
    """
    print("--- Cifrador por Bloques Simple ---")
    
    while True:
        # 1. Elegir acción
        action = get_validated_input(
            "¿Qué deseas hacer? [cifrar / descifrar / salir]: ",
            str.lower,
            lambda s: s in ['cifrar', 'descifrar', 'salir'],
            "Opción no válida. Escribe 'cifrar', 'descifrar' o 'salir'."
        )
        
        if action == 'salir':
            print("¡Adiós!")
            break
            
        # 2. Obtener parámetros
        key = input("Ingresa la llave: ")
        
        block_size = get_validated_input(
            "Ingresa el tamaño del bloque (ej: 8, 16): ",
            int,
            lambda n: n > 0,
            "El tamaño del bloque debe ser un número entero positivo."
        )
        
        intermittent_skip = get_validated_input(
            "Ingresa bloques a saltar (0 = cifrado normal, 1 = saltar 1, etc.): ",
            int,
            lambda n: n >= 0,
            "Debe ser un número entero 0 o positivo."
        )
        
        io_format = get_validated_input(
            "Ingresa el formato de entrada/salida [base64 / hex]: ",
            str.lower,
            lambda s: s in ['base64', 'hex'],
            "Opción no válida. Escribe 'base64' o 'hex'."
        )
        
        # 3. Inicializar el cifrador
        try:
            cipher = SimpleBlockCipher(key, block_size, intermittent_skip)
        except ValueError as e:
            print(f"Error al inicializar el cifrador: {e}")
            print("-" * 40 + "\n")
            continue # Reiniciar el bucle

        # 4. Ejecutar acción
        if action == 'cifrar':
            message = input("Ingresa el mensaje a cifrar: ")
            try:
                encrypted_message = cipher.encrypt(message, output_format=io_format)
                print("\n--- Resultado ---")
                print(f"Mensaje Cifrado ({io_format}):")
                print(encrypted_message)
            except Exception as e:
                print(f"Ocurrió un error al cifrar: {e}")
                
        elif action == 'descifrar':
            encrypted_message = input(f"Ingresa el mensaje cifrado ({io_format}): ")
            try:
                decrypted_message = cipher.decrypt(encrypted_message, input_format=io_format)
                print("\n--- Resultado ---")
                print("Mensaje Descifrado:")
                print(decrypted_message)
            except Exception as e:
                print(f"Ocurrió un error al descifrar: {e}")

        print("\n" + "=" * 40 + "\n")

# Ejecutar la interfaz de terminal si el script se corre directamente
if __name__ == "__main__":
    main_cli()