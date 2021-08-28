from rpyc import ForkingServer
from rpyc.utils.server import ThreadedServer
from rpyc.utils.server import OneShotServer
from client_manager import ClientManager
import select
import sys

PORTA = 5000

server = ThreadedServer(ClientManager, port= PORTA)
#server = OneShotServer(ClientManager, port= PORTA)

server.start()