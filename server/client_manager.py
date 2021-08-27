from typing import NoReturn
import rpyc
import socket


clients = {}
active_users = []
inactive_users = []

class ClientManager(rpyc.Service):

    def __init__(self) -> None:
        super().__init__()
        #o objeto clients armazena todos os clientes do servico, as chaves sao os nomes de usuarios e os valores sao o endereco de IP e o status (ativo/inativo/em conversa) do usuario

    #inicia a conexao com o cliente e envia para ele uma lista com todos os nomes de usuario sendo usados
    def on_connect(self, conn):
        print(clients)
        print("Conexao iniciada:")

    def on_disconnect(self, conn):
        print("Conexao finalizada:")

    def exposed_get_userlist(self):
        return clients.keys()
    
    def exposed_set_user(self, new_user):
        if new_user in clients.keys():
            return 1, ''
        else:
            clients[new_user] = ''
            return 0, new_user

    def exposed_register(self, user, ip):
        active_users.append(user)
        clients[user] = ip
        print(clients[user])

    def exposed_set_inactive(self, user):
        active_users.remove(user)
        inactive_users.append(user)

    def exposed_set_active(self, user):
        inactive_users.remove(user)
        active_users.append(user)
    
    def exposed_get_active_users(self):
        return active_users
    
    def chat_request(self, sender, reciever):
        '''
        1) conferir se o reciever existe, se não exister, avisar pro sender
        2) conferir se o reciever está ativo, se não estiver, avisar pro sender
        3) conferir se o reciever está numa conversa, se estiver, avisar pro sender
        4) enviar o convite pro reciever
        5) o reciever pode aceitar ou não (isso vai ser implementado em outro lugar (usar select no while do client?))
        5.1) se o reciever aceitar a conversa começa
        5.2) se o reciever recusar, avisar o sender
        '''

    def exposed_remove_user(self, user):
        del clients[user]
        if user in active_users:
            active_users.remove(user)
        else:
            inactive_users.remove(user)