import socket, threading

HOST = "127.0.0.1"
PORT = 55555

username = input("Ingresa el nombre para tu usuario: ")

clientes = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientes.connect((HOST,PORT))

def recibir_mensaje():
    while True:
        try:
            mensaje = clientes.recv(1024).decode('utf-8')
            
            if mensaje == "@Username":
                clientes.send(username.encode('utf-8'))
            else: print(mensaje)
            
        except:
            print("Ha ocurrido un error")
            clientes.close()
            break
        
def escribir_mensaje():
    while True:
        # Se pone en un loop por que estamos trabajando en consola
        mensaje = f"{username}: {input('*mensaje*: ')}"
        clientes.send(mensaje.encode('utf-8'))
        
recibido = threading.Thread(target=recibir_mensaje)
recibido.start()

leido = threading.Thread(target=escribir_mensaje)
leido.start()