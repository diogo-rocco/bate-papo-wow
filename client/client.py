import rpyc
from client_interface import clientInterface
import socket

PORTA = 5000
SERVER = 'localhost'
IP = socket.gethostbyname('localhost')

conn = rpyc.connect(SERVER, PORTA)
interface = clientInterface()

def set_user():
    user_candidate = interface.set_username()
    fail, user = conn.root.set_user(user_candidate)
    while fail:
        user_candidate = interface.failed_username()
        fail, user = conn.root.set_user(user_candidate)
    
    ip = socket.gethostbyname(socket.gethostname())
    conn.root.register(user, ip)
    return user

def set_inactive(user):
    conn.root.set_inactive(user)

def set_active(user):
    conn.root.set_active(user)

def get_active_users():
    return conn.root.get_active_users()


user = set_user()
print(user)
while True:
    comand, peer = interface.get_command()
    if comand == 0:
        break
        
    
    if comand == 1:
        set_active(user)
    
    if comand == 2:
        set_inactive(user)

    if comand == 3:
        interface.show_active_users(get_active_users())
    
    if comand == 4:
        print('TODO')
        #solicitar a conversa com o <usuário> para o servidor

    if comand == 5:
        interface.get_help()

conn.remove_user(user)
conn.close()