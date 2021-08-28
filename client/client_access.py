import rpyc
from client_interface import clientInterface
import socket

PORTA = 5000
SERVER = 'localhost'

class ClientAccess():

    def __init__(self, client_porta) -> None:
        self.interface = clientInterface()
        self.conn = rpyc.connect(SERVER, PORTA)
        self.client_porta = client_porta

    def set_user(self):
        user_candidate = self.interface.set_username()
        fail, user = self.conn.root.set_user(user_candidate)
        while fail:
            user_candidate = self.interface.failed_username()
            fail, user = self.conn.root.set_user(user_candidate)
        
        ip = socket.gethostbyname(socket.gethostname())
        self.conn.root.register(user, ip, self.client_porta)
        return user

    def set_inactive(self, user):
        self.conn.root.set_inactive(user)

    def set_active(self, user):
        self.conn.root.set_active(user)
    
    def set_on_conversation(self, user):
        self.conn.root.set_on_conversation(user)

    def set_off_conversation(self, user):
        self.conn.root.set_off_conversation(user)

    def get_active_users(self):
        return self.conn.root.get_active_users()

    def request_chat(self, reciever):
        return self.conn.root.chat_request(reciever)

    
    def end(self, user):
        self.conn.root.remove_user(user)
        self.conn.close()