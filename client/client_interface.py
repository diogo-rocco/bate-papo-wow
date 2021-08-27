class clientInterface():

    def __init__(self) -> None:
        self.valid_commands = {'/sair': 0, '/ativo': 1, '/inativo': 2, '/lista_ativos': 3, '/papo': 4, '/help': 5}

    def set_username(self):
        name = input('Olá! Insira seu nome de usuario: ')
        return name
    
    def failed_username(self):
        name = input('Esse nome já está sendo usado. Favor insira outro nome: ')
        return name
    
    def get_command(self):
        msg = input('Digite um comando: ')
        msg_array = msg.split()
        while msg_array[0] not in self.valid_commands.keys():
            msg = input('Comando inválido. Digite um comando válido ou digite /help para obter uma lista os comandos válidos: ')
            msg_array = msg.split()
        
        if msg_array[0] == '/papo':
            return self.valid_commands[msg_array[0]], msg_array[1]
        
        else:
            return self.valid_commands[msg_array[0]], None
        
    def get_help(self):
        print('/sair: encerra a aplicação')
        print('/ativo: define seu status como ativo')
        print('/inativo: define seu status como inativo')
        print('/lista_ativos: exibe a lista de usuarios ativos')
        print('/papo <usuario>: inicia uma conversa com um usuário')
    
    def show_active_users(self, active_users):
        print('Usuarios ativos:')
        for user in active_users:
            print(user)
