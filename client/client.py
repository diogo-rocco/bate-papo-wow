from client_interface import clientInterface
from client_access import ClientAccess
from chat_manager import ChatManager
from sys import stdin
import select

PORTA = 5000
SERVER = 'localhost'

interface = clientInterface()
chat_manager = ChatManager()
access = ClientAccess(chat_manager.porta)
user = access.set_user()
input_list = [stdin, chat_manager.passive]

def client():
    while True:
        interface.main_menu()
        read, write, excep = select.select(input_list, [], [])
        for ready in read:
            if ready == chat_manager.passive:
                access.set_on_conversation(user)
                chat_manager.answer_invitation()
                access.set_off_conversation(user)
            
            if ready == stdin:
                comand, peer = interface.get_command()
                if comand == 0:
                    return
                    
                if comand == 1:
                    access.set_active(user)
                
                if comand == 2:
                    access.set_inactive(user)

                if comand == 3:
                    interface.show_active_users(access.get_active_users())
                
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
    

                if comand == 5:
                    interface.get_help()

client()
access.end(user)