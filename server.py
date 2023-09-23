# -------- Boilerplate Code and Previous class Code Start ------
import socket
from  threading import Thread
import time

IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
BUFFER_SIZE = 4096

clients = {}
# -------- Boilerplate Code and Previous class Code End ------

# Teacher Activity
def handleShowList(client):
    global clients
    counter = 0

    for c in clients:
        counter += 1
        client_address = clients[c]['address'][0]
        connected_with = clients[c]['connected_width']
        message = ''
        if (connected_with):
            message = f'{counter},{c},{client_address}, connected with {connected_with}, tiul, \n'
        else:
            message = f'{counter},{c},{client_address}, available, tiul,\n'
        client.send(message.encode())
        time.sleep(1)


# Boilerlate Code
def handleMessges(client, message, client_name):
    if(message == 'show list'):
        handleShowList(client)
    


# Bolierplate Code
def handleClient(client, client_name):
    global clients
    global BUFFER_SIZE
    global SERVER

    # Sending welcome message
    banner1 = "Welcome, You are now connected to Server!\nClick on Refresh to see all available users.\nSelect the user and click on Connect to start chatting."
    client.send(banner1.encode())

    while True:
        try:
            BUFFER_SIZE = clients[client_name]["file_size"]
            chunk = client.recv(BUFFER_SIZE)
            message = chunk.decode().strip().lower()
            if(message):
                handleMessges(client, message, client_name)
            else:
                removeClient(client_name)
        except:
            pass


# Boilerplate Code
def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()

        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
                "client"         : client,
                "address"        : addr,
                "connected_with" : "",
                "file_name"      : "",
                "file_size"      : 4096
            }

        print(f"Connection established with {client_name} : {addr}")

        thread = Thread(target = handleClient, args=(client,client_name,))
        thread.start()


def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    # Getting global values
    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    # Listening incomming connections
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()



setup_thread = Thread(target=setup)           #receiving multiple messages
setup_thread.start()
