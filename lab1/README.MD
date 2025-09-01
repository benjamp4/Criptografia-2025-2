Primero hay que situarse en la carpeta lab1

cd lab1

Para ejecutar la actividad 1 y 2 es necesario ejecutar el código main.py de la siguiente manera.

python3 main.py

Esto nos preguntará que texto queremos cifrar y hará el envío de paquetes ICMP, que deben ser sniffeados con wireshark.

La carpeta de lab1 incluye una captura de ejemplo con el texto "criptografia y seguridad en redes" con un corriemiento de 9.

Para realizar un nuevo test se debe ejecutar main.py y capturar con wireshark con las siguientes reglas icmp && ip.dst == 8.8.8.8.

Este archivo se debe guardar como archivo.pcapng y después ser descifrado con el siguiente comando

python3 des.py archivo.pcapng
