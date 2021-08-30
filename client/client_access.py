import rpyc
from client_interface import clientInterface
import socket

PORTA = 5000
SERVER = 'localhost'

#Camada responsável pelo acesso do cliente ao servidor
class ClientAccess():

    def __init__(self, client_porta) -> None:
        self.interface = clientInterface()
        self.conn = rpyc.connect(SERVER, PORTA)
        self.client_porta = client_porta

    #Função responsável por definir o nome de usuário para o cliente
    def set_user(self):
        user_candidate = self.interface.set_username()
        fail, user = self.conn.root.set_user(user_candidate)
        #recebe do servidor a mensagem se o nome de usuário é valido ou não, e apenas aceita nomes de usuários válidos
        while fail:
            user_candidate = self.interface.failed_username()
            fail, user = self.conn.root.set_user(user_candidate)
        
        ip = socket.gethostbyname(socket.gethostname())
        self.conn.root.register(user, ip, self.client_porta)
        return user

    #Chama do servidor o método que faz o servidor definir o usuário como inativo
    def set_inactive(self, user):
        self.conn.root.set_inactive(user)

    #Chama do servidor o método que faz o servidor definir o usuário como ativo
    def set_active(self, user):
        self.conn.root.set_active(user)
    
    #Chama do servidor o método que faz o servidor definir o usuário como estando em uma conversa
    def set_on_conversation(self, user):
        self.conn.root.set_on_conversation(user)

    #Chama do servidor o método que faz o servidor definir o usuário como não estando mais ocupado em uma conversa
    def set_off_conversation(self, user):
        self.conn.root.set_off_conversation(user)

     #Chama do servidor o método que faz o servidor enviar uma lista de usuários ativos
    def get_active_users(self):
        return self.conn.root.get_active_users()

    #Chama do servidor o método que faz o servidor enviar o IP e portas do usuário com quem o cliente quer ter a conversa
    def request_chat(self, reciever):
        return self.conn.root.chat_request(reciever)

    #Chamam os métodos que encerram a conexão com o servidor
    def end(self, user):
        self.conn.root.remove_user(user)
        self.conn.close()
