#Camada responsável pela interface com o usuário
class clientInterface():

    #Inicializa a classe com uma lista de comandos válidos e seus códigos de erro
    def __init__(self) -> None:
        self.valid_commands = {'/sair': 0, '/ativo': 1, '/inativo': 2, '/lista_ativos': 3, '/papo': 4, '/help': 5}

    def set_username(self):
        name = input('>> Olá! Insira seu nome de usuario:\n')
        return name

    def failed_username(self):
        name = input('>> Esse nome já está sendo usado. Favor insira outro nome:\n')
        return name
    
    def main_menu(self):
        print('>> Digite um comando (para obter uma lista de comandos validos digite /help):')

    #Recebe um comando do usuário e verifica se esse é um comando válido
    def get_command(self):
        msg = input()
        msg_array = msg.split()
        while msg_array[0] not in self.valid_commands.keys():
            msg = input('>> Comando inválido. Digite um comando válido ou digite /help para obter uma lista os comandos válidos:\n')
            msg_array = msg.split()
        
        if msg_array[0] == '/papo':
            return self.valid_commands[msg_array[0]], msg[len(msg_array[0])+1:]
        
        else:
            return self.valid_commands[msg_array[0]], None
        
    def get_help(self):
        print('>> /sair: encerra a aplicação')
        print('>> /ativo: define seu status como ativo')
        print('>> /inativo: define seu status como inativo')
        print('>> /lista_ativos: exibe a lista de usuarios ativos')
        print('>> /papo <usuario>: inicia uma conversa com um usuário\n')
    
    #Recebe a lista de usuários ativos e mostra ela para o usuário
    def show_active_users(self, active_users):
        print('>> Usuarios ativos:')
        for user in active_users:
            print(user)
    
    def chat_denied(self):
        print('>> O convite foi recusado')
    
    #Informa para o usuário que ele recebeu um convite para um chat, recebe a resposta do usuário e retorna 1 se ele aceitou e 0 caso contrário
    def recieve_invitation(self, sender_name):
        print('>> Você recebeu um convite para um chat com', sender_name)
        answer = input('>> deseja aceitar o convite? (s/n)\n')
        while True:
            answer = answer.lower()
            if answer == 's':
                return 1
            elif answer == 'n':
                return 0
            else:
                answer = input('>> Digite uma resposta válida (s/n)\n')
    
    def start_chat(self):
        print('>> Chat iniciado. Envie mensagens ou digite /fim para encerrar o chat\n')

    def show_message(self, msg, peer_name):
        print('>> (' + peer_name + '):', msg)
    
    def chat_ended(self):
        print('>> chat encerrado\n')
    
    #Quando o cliente tenta enviar um convite para outro e não consegue, esse método diz ao cliente o motivo de não ter conseguido
    def show_invitation_errors(self, error_code):
        if error_code == 1:
            print('>> O usuário não existe, digite /lista_ativos para ver a lista de usuários ativos\n')
        elif error_code == 2:
            print('>> O usuário está inativo, digite /lista_ativos para ver a lista de usuários ativos\n')
        elif error_code == 3:
            print('>> O usuário está em uma conversa, digite /lista_ativos para ver a lista de usuarios ativos\n')

    def error_self_chat(self):
        print('Não é possivel iniciar uma conversa consigo mesmo\n')
