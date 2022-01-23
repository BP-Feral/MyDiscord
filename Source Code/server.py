import threading
import socket

settings = []

f = open("config.ini", "r")
settings = f.readlines()
f.close()

settings_host_address = settings[1][13:-1]
settings_host_host = settings[2][10:-1]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((settings_host_address, int(settings_host_host)))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        print(f"sending back {message}")
        client.send(message)

def handle(client):
    while True:
        try:
            index = clients.index(client)
            nickname = nicknames[index]
            message = client.recv(1024)
            if message != 'CONNECTION TERMINATED!':
                if message != b'':
                    broadcast(message)
                    print(f"{message} received from {nickname}")
            else:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat!\n'.encode('ascii'))
                nicknames.remove(nickname)
                break
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!\n'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        print("sending NICK")
        nickname = client.recv(1024).decode('ascii')
        print(f"received NICK {nickname}")
        if nickname[:3] == "SSH":
            print(nickname, "blocked!")
            print(f"Force-Disconnect {str(address)}")
            client.send('DISCONNECT'.encode('ascii'))
        else:
            nicknames.append(nickname)
            clients.append(client)

            print(f'Nickname of the client is {nickname}!')
            broadcast(f' < {nickname} HAS JOINED THE CHAT > \n'.encode('ascii'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

print("Server is listening...")
receive()