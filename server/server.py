from rpyc.utils.server import ThreadedServer
from client_manager import ClientManager

#Inicializa a camada de gerenciamento dos clientes
server = ThreadedServer(ClientManager)

server.start()
