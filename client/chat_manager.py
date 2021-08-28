from os import write
from select import select
import socket
from client_interface import clientInterface
from sys import stdin

class ChatManager():

    def __init__(self) -> None:
        self.interface = clientInterface()
        self.passive = socket.socket()
        self.porta = 1001
        self.host = ''
        reciever_initiated = False
        while not reciever_initiated:
            try:
                self.passive.bind((self.host, self.porta))
                reciever_initiated = True
            except:
                self.porta = self.porta+1
        
        self.passive.listen(1)
        self.active = socket.socket()
    
    def send_invitation(self, sender, reciever_ip, reciever_porta, reciever_name):
        self.active.connect((reciever_ip, reciever_porta))
        self.active.send(sender.encode('utf-8'))
        #TODO permitir o usuario cancelar o envio de um convite
        accepted = str(self.active.recv(1024), 'utf-8')
        self.peer_name = reciever_name
        
        if accepted == '0':
            self.active.close()
            self.active = socket.socket()
            self.interface.chat_denied()
            self.peer_name = ''
        elif accepted == '1':
            self.chat(self.active)
            self.active = socket.socket()


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


    def chat(self, sock):
        self.interface.start_chat()
        input_list = [stdin, sock]
        while True:
            read, write, excep = select(input_list, [], [])
            for ready in read:
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
                
                elif ready == stdin:
                    msg = input()
                    if msg == '/fim':
                        sock.close()
                        return
                    sock.send(msg.encode('utf-8'))
