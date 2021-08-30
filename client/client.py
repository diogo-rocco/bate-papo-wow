from client_interface import clientInterface
from client_access import ClientAccess
from chat_manager import ChatManager
from sys import stdin
import select

PORTA = 5000
SERVER = 'localhost'

#Inicializa a camada responsavel pela interface com o usuário
interface = clientInterface()

#Inicializa a camada responsavel pela comunicação peer-to-peer
chat_manager = ChatManager()

#Inicializa a camada responsavel pelo acesso do cliente ao servidor
access = ClientAccess(chat_manager.porta)
#Adquiri a string com o nome de usuário
user = access.set_user()
input_list = [stdin, chat_manager.passive]

#Função responsável pelo fluxo principal de execução do cliente
def client():
    while True:
        interface.main_menu()
        #Usa um select para que o usuário seja capaz de receber um convite para chat ou para digitar comandos para o cliente
        read, write, excep = select.select(input_list, [], [])
        for ready in read:
            #Quando a entrada vem do socket passivo da camada de gerenciamento do chat, o cliente pode aceitar ou não o convite para um chat
            if ready == chat_manager.passive:
                access.set_on_conversation(user)
                chat_manager.answer_invitation()
                access.set_off_conversation(user)
            
            #Quando a entrada vem do teclado, a camada de interface vai receber o comando e enviar ele para o cliente, e o cliente responde de acordo
            if ready == stdin:
                comand, peer = interface.get_command()
                #Código 0 -> sair da aplicação
                if comand == 0:
                    return
                    
                #Código 1 -> definir o usuário como ativo
                if comand == 1:
                    access.set_active(user)
                
                #Código 2 -> definir o usuário como inativo
                if comand == 2:
                    access.set_inactive(user)

                #Código 3 -> adquirir a lista de usuários ativos
                if comand == 3:
                    interface.show_active_users(access.get_active_users())
                
                #Código 4 -> enviar um convite de chat para outro usuário
                if comand == 4:
                    response =  access.request_chat(peer)
                    if peer == user:
                        interface.error_self_chat()
                    if type(response) == int:
                        interface.show_invitation_errors(response)
                    else:
                        reciever_ip, reciever_porta = response
                        access.set_on_conversation(user)
                        chat_manager.send_invitation(user, reciever_ip, reciever_porta, peer)
                        access.set_off_conversation(user)
                
                #Código 5 -> receber uma lista com os comandos válidos
                if comand == 5:
                    interface.get_help()

client()
access.end(user)
