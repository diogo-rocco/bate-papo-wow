from typing import NoReturn
import rpyc
import socket

#Objeto com todos os clientes conectados ao servidor. É um dicionário onde as chaves são nomes de usuário e os valores são os seus endereços de ip e porta
clients = {}

#Lista de usuários que estão ativos
active_users = []

#Lista de usuários que estão inativos
inactive_users = []

#Lista de usuários que estão em uma conversa
busy_users = []

#Camada responsavel por centralizar as informações que cada cliente pode querer um sobre o outro
class ClientManager(rpyc.Service):

    def on_connect(self, conn):
        print("Conexao iniciada:")

    def on_disconnect(self, conn):
        print("Conexao finalizada:")

    #Retorna a lista de todos os usuários
    def exposed_get_userlist(self):
        return clients.keys()
    
    #verifica se o nome de usuário já está em uso, caso esteja, retorna um erro, caso contrário, cria o novo usuário
    def exposed_set_user(self, new_user):
        if new_user in clients.keys():
            return 1, ''
        else:
            clients[new_user] = {}
            return 0, new_user

    #Registra o IP e a porta do lado passivo da aplicação da camada de gerenciamento de conversas do cliente
    def exposed_register(self, user, ip, porta):
        active_users.append(user)
        clients[user]['ip'] = ip
        clients[user]['porta'] = porta
        print(clients[user])

    def exposed_set_inactive(self, user):
        active_users.remove(user)
        inactive_users.append(user)

    def exposed_set_active(self, user):
        inactive_users.remove(user)
        active_users.append(user)

    def exposed_set_on_conversation(self, user):
        active_users.remove(user)
        busy_users.append(user)

    def exposed_set_off_conversation(self, user):
        busy_users.remove(user)
        active_users.append(user)
    
    def exposed_get_active_users(self):
        return active_users
    
    #Verifica se o usuário que o cliente está solicitando a conversa é valido (se ele existe, se ele está ativo e não está em uma conversa) e retorna o código de erro, no caso de erro, ou o ip e porta do usuário que foi solicitado
    def exposed_chat_request(self, reciever):
        if reciever not in clients.keys():
            return 1
        if reciever in inactive_users:
            return 2
        if reciever in busy_users:
            return 3
        else:
            return clients[reciever]['ip'], clients[reciever]['porta']
        
    #Remove o usuário da lista de usuários no servidor
    def exposed_remove_user(self, user):
        del clients[user]
        if user in active_users:
            active_users.remove(user)
        else:
            inactive_users.remove(user)
