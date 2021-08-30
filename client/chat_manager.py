from os import write
from select import select
import socket
from client_interface import clientInterface
from sys import stdin

#Classe responsavel pela comunicação peer-to-peer entre os usuários(clientes)
class ChatManager():
    
    #Instanciação da classe, onde o socket dos lados passivos e ativos são iniciados
    def __init__(self) -> None:
        self.interface = clientInterface()
        self.passive = socket.socket()
        self.porta = 1001
        self.host = ''
        reciever_initiated = False
        while not reciever_initiated:
            #um try except é usado para garantir que não tentemos nos conectar em portas já em uso
            try:
                self.passive.bind((self.host, self.porta))
                reciever_initiated = True
            except:
                self.porta = self.porta+1
        
        self.passive.listen(1)
        self.active = socket.socket()
    
    #Envia um convite de conversa para o outro cliente
    def send_invitation(self, sender, reciever_ip, reciever_porta, reciever_name):
        self.active.connect((reciever_ip, reciever_porta))
        self.active.send(sender.encode('utf-8'))
        accepted = str(self.active.recv(1024), 'utf-8')
        self.peer_name = reciever_name
        #recebe os códigos de aceite(1) ou não aceite(0) e toma as ações de acordo
        if accepted == '0':
            self.active.close()
            self.active = socket.socket()
            self.interface.chat_denied()
            self.peer_name = ''
        elif accepted == '1':
            self.chat(self.active)
            self.active = socket.socket()


    #Responde o convite enviado pelo método send_invitation
    def answer_invitation(self):
        self.peer_sock, peer_address = self.passive.accept()
        self.peer_name = str(self.peer_sock.recv(1024), 'utf-8')
        accepted = self.interface.recieve_invitation(self.peer_name)
        if accepted:
            answer = str(accepted)
            self.peer_sock.send(answer.encode('utf-8'))
            self.chat(self.peer_sock)
        else:
            answer = str(accepted)
            self.peer_sock.send(answer.encode('utf-8'))
            self.peer_sock.close()
            self.peer_name = ''


    #Define o fluxo de uma conversa entre dois clientes (recebe como parametro o socket (ativo ou passivo) que está sendo usado para a conversa)
    def chat(self, sock):
        self.interface.start_chat()
        input_list = [stdin, sock]
        while True:
            #Usa um select para que o cliente possa tanto receber quanto enviar as mensagens para o outro cliente
            read, write, excep = select(input_list, [], [])
            for ready in read:
                #Quando a mensagem veio do peer ela é exibida para o usuário, e caso a conexão seja encerrada, fecha o socket
                if ready == sock:
                    try:
                        msg = str(sock.recv(1024), 'utf-8')
                        if not msg:
                            sock.close()
                            self.interface.chat_ended()
                            return
                        self.interface.show_message(msg, self.peer_name)
                    except:
                        sock.close()
                        self.interface.show_message(msg, self.peer_name)
                        self.interface.chat_ended()
                        return
                
                #Quando a mensagem vem do usuário, ela é enviada para o peer
                elif ready == stdin:
                    msg = input()
                    if msg == '/fim':
                        sock.close()
                        return
                    sock.send(msg.encode('utf-8'))
