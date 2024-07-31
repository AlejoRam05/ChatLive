"""
Ejercicio 2: Creación del Socket del Servidor
Crea un script Python (server.py) para el servidor.
Utiliza la biblioteca socket para crear un socket de servidor.
Haz que el servidor escuche en un puerto específico y acepte conexiones de clientes.
Requisitos:

Crear un socket de servidor.
Vincular el socket a una dirección y puerto.
Poner el servidor en modo de escucha.
Aceptar conexiones de clientes y enviarles un mensaje de bienvenida
"""

import socket, threading

HOST = "127.0.0.1"
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()
print(f"Server Running {HOST}:{PORT}")

clients = []  # Almacenamos a los clientes
usernames = []  # Almacenamos los nombres de los usuarios 

def transmicion(mensaje, _cliente = None):
    for cliente in clients:
        if cliente != _cliente:
          try:cliente.send(mensaje)
          except:
              cliente.close()
              clients.remove(cliente)

def manejo_cliente(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)  #1024 Bytes limite que puede leer
            transmicion(mensaje,cliente)     
        except:
            index = clients.index(cliente)
            clients.remove(cliente)
            cliente.close()
            username = usernames.pop(index)
            transmicion(f"ChatBot {username} desconectado".encode('utf-8')) #encode usamos para convertir de Str a Bytes
            break
        
def recibir_conexion():
    while True:
        cliente, direccion = server.accept() #Retorna dos datos el Objeto de la conexion y la conexion (HOST)
        print(f"New connection from {direccion}")
        
        cliente.send("@Username".encode('utf-8')) #Recibe la informacion y la transforma para poder leerlo
        username = cliente.recv(1024).decode('utf-8')
        clients.append(cliente)
        usernames.append(username)
        
        print(f"{username} esta conectado en la direccion {str(direccion)}")
        
        mensaje = f'ChatBot {username} esta conectado en el chat'.encode('utf-8')
        transmicion(mensaje)
        cliente.send("Te has conectado al servidor". encode('utf-8'))
        
        thread = threading.Thread(target=manejo_cliente, args=(cliente,))
        thread.start()         

if __name__ == "__main__":
    recibir_conexion()
    
"""
Avances
Creación del socket de servidor y su configuración: ✔️
Aceptación de conexiones y manejo de múltiples clientes: ✔️
Transmisión de mensajes entre clientes: ✔️
"""
