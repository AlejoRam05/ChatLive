import socket, threading, queue

HOST = "127.0.0.1"
PORT = 55555

username = input("Ingresa el nombre para tu usuario: ")

clientes = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientes.connect((HOST,PORT))

mensaje_queue = queue.Queue()

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
        mensaje = mensaje_queue.get()
        if mensaje:
            clientes.send(mensaje.encode('utf-8'))
        
recibido = threading.Thread(target=recibir_mensaje)
recibido.start()

leido = threading.Thread(target=escribir_mensaje)
leido.start()

while True:
    try:
        mensaje = f"{username}: {input('*mensaje*: ')}"
        mensaje_queue.put(mensaje)
    except KeyboardInterrupt:
        print('Chat cerrado')
        break