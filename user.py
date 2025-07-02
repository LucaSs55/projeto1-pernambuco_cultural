import os
import json
from validations import *
#Classe que modela os dados de usuário
class Usuario:
    def __init__(self, nome, email, senha):
        """
        Inicializa um novo usuário

        Parâmetros:
            nome (str): Nome do usuário
            email (str): Email do usuário
            senha (str): Senha do usuário
        """
        self.nome = nome
        self.email = email
        self.senha = senha
        


    def modelar_usuario(self):
        """
        Converte o objeto Usuario em um dicionário

        Retorna:
            dict: Dicionário com os dados do usuário
        """
        return {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha
        }

    def __str__(self):
        """
        Representação em string do usuário.

        Retorna:
            str: Nome e email do usuário formatados.
        """


        return f"Nome:{self.nome}, Email:{self.email}"
    


#Classe que administra operações de usuários
class SistemaDeUsuarios:

    def __init__(self, arquivo_externo_usuarios="usuarios.json"):

        """
        Inicializa o sistema de usuários e carrega os dados do arquivo JSON

        Parâmetros:
            arquivo_externo_usuarios (str): Caminho para o arquivo JSON com os dados dos usuários
        """
        self.arquivo_externo_usuarios = arquivo_externo_usuarios
        self.usuarios = [] 
        self.carregar_usuarios()


    def login_conta(self):
        if self.usuario_logado:
            print(f"\033[33m[INFO] Você já está logado como {self.usuario_logado.nome}.\033[m")
            return
        
        print("+============+ LOGIN +============+")
        email = input("Email: ").strip()
        senha = input("Senha: ").strip()

        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha:
                self.usuario_logado = usuario
                self.limpar_terminal() 
                print(f"\033[32m Seja bem-vindo(a), {usuario.nome}!\033[m")
                return
        print("\033[31m[ERRO] Email ou senha incorretos. \033[m")


    def menu(self):
       
       """
        Exibe o menu principal com as opções disponíveis para o usuário.

        Retorna:
            str: Opção escolhida pelo usuário.
        """
       print("===============> MENU PRINCIPAL <=================")
       print(20*"=-")
       print("-[1] Cadastro de Usuário")
       print("-[2] Ver informações de usuário")
       print("-[3] Deletar conta")
       print("-[4] Atualizar dados da conta")
       print("-[5] Login ")
       print("-[6] Recomendações de Eventos Regionais ")
       print(20 * "=-")
       return input("Escolha uma das opções acima:")
    
    
    def limpar_terminal(self):

        """
        Limpa o terminal com base no sistema operacional.

        Retorna:
            int: Código de status do comando de limpeza do terminal.
        """
        return os.system("cls" if os.name == "nt" else "clear")

    # Envio e modelagem dos dados para o arquivo externo json
    def carregar_usuarios(self):

        """
        Carrega os usuários do arquivo JSON e os armazena em uma lista.
        """
        if os.path.exists(self.arquivo_externo_usuarios):
            with open(self.arquivo_externo_usuarios,"r") as d:
                try:
                    dados = json.load(d)
                    self.usuarios = []
                    for item in dados:
                        nome = item.get("nome")
                        email = item.get("email")
                        senha = item.get("senha")
                        usuario = Usuario(nome, email, senha)
                        self.usuarios.append(usuario)
                except json.JSONDecodeError:
                    print("Arquivo JSON inválido")
                    self.usuarios = []
        else:
            self.usuarios = []

    #Salva dados do usuário no arquivo externo json
    def salvar_dados_usuarios(self):

        """
        Salva os dados dos usuários no arquivo JSON.
        """
        with open(self.arquivo_externo_usuarios,"w") as d: #Abre o arquivo json no modo de escrita
            json.dump([item.modelar_usuario() for item in self.usuarios],d,indent=4)


    def cadastrar_usuario(self):

        """
        Realiza o cadastro de um novo usuário.

        Solicita nome, email e senha, realiza validações, e armazena o novo usuário se todas
        as informações forem válidas.
        """
        print("============> Cadastro de Usuário <============")
        # Loop para nome
        while True:
            nome = input("Digite seu nome: ").strip()
            if validacao_de_nome(nome,self.usuarios):
                break

        # Loop para email até ser digitado um email com domínio válido
        while True:
            email = input("Digite seu email (ex: @gmail.com, @hotmail.com, @yahoo.com): ").strip()
            if validacao_de_email(email,self.usuarios):
                break

        # Loop para senha e confirmação de senha até ambas serem validadas
        while True:
            senha = input("Digite sua senha: ").strip()
            confirmacao = input("Confirme sua senha: ").strip()

            if senha != confirmacao:
                print("\033[31m[ERRO] As senhas não coincidem.\033[m")
                continue #serve para interromper a iteração das condicionais de forma que se uma das condições de erro for atendida, as outras não são executadas e há a volta para o início do loop.

            if senha == "":
                print("\033[31m[ERRO], o preenchimento da senha e obrigatório\033[m")
                continue

            if not validacao_de_senha(senha):
                print("\033[31m[ERRO] A senha deve conter:\n- No mínimo 8 caracteres\n- Uma letra maiúscula\n- Um número\n- Um caractere especial.\033[m")
                continue
            break

        # Se tudo estiver certo, cria e salva o usuário
        novo_usuario = Usuario(nome, email, senha)
        self.usuarios.append(novo_usuario) # Salva o novo usuário na lista
        self.salvar_dados_usuarios()
        self.limpar_terminal()
        print("\033[32m Novo Usuário cadastrado com sucesso! \033[m")


    def ver_conta(self):
        ''' 
        Possibilita a leitura dos dados de usuário

        Solicita Email, Senha e realiza validações se estiverem corretos imprime os dados de usuário na tela 
        '''
        print("============> Ver Informações de Usuário <============")
        email = input("Digite seu email:").strip()
        senha = input("Digite sua senha:").strip()
        for usuario in self.usuarios: #Escaneia os pares chave-valor dentro da lista usuarios
            if usuario.email == email and usuario.senha == senha: #verifica se o email e a senha batem com o que está salvo no arquivo de usuarios
                self.limpar_terminal()
                print(f"Dados de Usuário:\033[32m\n•Nome: {usuario.nome} \n•Email:{usuario.email} \n•Senha:{usuario.senha}\033[m")
                return  # Sai da função após encontrar o usuário

            # Se o laço terminar sem encontrar, mostra uma única vez:
        print(" \033[31m[ERRO] Email ou Senha Incorretos \033[m")

    def deletar_conta(self):
        ''' 
        Deleta usuários já cadastrados

        Solicita Email e Senha, se ambos forem validados, então há um input de confirmação da deleção de conta por parte do usuario
        '''
        print("============> Deletar Conta <============")
    
        email = input("Digite seu email: ").strip()
        senha = input("Digite sua senha: ").strip()
        #Loop com índice para passar pela lista usuarios, trazendo cada usuario e seu respectivo índice
        for i, usuario in enumerate(self.usuarios):
            if usuario.email == email and usuario.senha == senha:
                confirmacao = input("Tem certeza que deseja deletar sua conta? (s/n): ").strip().lower()
                if confirmacao == "s":
                    del self.usuarios[i] #Exclui o item da lista permanentemente utilizando a func del() a partir do índice[i].
                    self.salvar_dados_usuarios()
                    print("\033[32mConta deletada com sucesso!\033[m")
                else:
                    print("\033[33mOperação cancelada.\033[m")
                return

        print("\033[31m[ERRO] Email ou senha incorretos.\033[m")


    def atualizar_usuario(self):
        '''
        Permite a edição dos dados de usuário

        Solicita Email e Senha, e se ambos forem validados, então é aberto um menu de escolha das informações a serem alteradas [1]Nome,[2]Email,[3]Senha,[4] Todos os dados
        
        '''
        print("============> Atualizar Conta <============")

        email = input("Digite seu email atual: ").strip()
        senha = input("Digite sua senha atual: ").strip()

        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha:
                print("\033[32mUsuário encontrado.\033[m")
                print("O que você deseja atualizar?")
                print("[1] Nome\n[2] Email\n[3] Senha\n[4] Todos os dados") # Menu para exclusão de dados
                opcao = input("Escolha uma opção: ").strip()

                if opcao == "1" or opcao == "4":
                    novo_nome = input("Novo nome: ").strip()
                    if novo_nome:
                        usuario.nome = novo_nome
                    else:
                        print("\033[31m[ERRO] Nome não pode ser vazio.\033[m")
                        return

                if opcao == "2" or opcao == "4":
                    while True:
                        novo_email = input("Novo email: ").strip()
                        if validacao_de_email(novo_email):
                            usuario.email = novo_email
                            break
                        else:
                            print("\033[31m[ERRO] Email inválido. Use @gmail.com, @hotmail.com ou @yahoo.com.\033[m")

                if opcao == "3" or opcao == "4":
                    while True:
                        nova_senha = input("Nova senha: ").strip()
                        confirmar = input("Confirme a nova senha: ").strip()
                        if nova_senha != confirmar:
                            print("\033[31m[ERRO] As senhas não coincidem.\033[m")
                            continue
                        if not validacao_de_senha(nova_senha):
                            print("\033[31m[ERRO] A senha deve conter:\n- No mínimo 8 caracteres\n- Uma letra maiúscula\n- Um número\n- Um caractere especial.\033[m")
                            continue
                        usuario.senha = nova_senha
                        break
                self.limpar_terminal()
                self.salvar_dados_usuarios()
                print("\033[32mDados atualizados com sucesso!\033[m")
                return

        print("\033[31m[ERRO] Email ou senha incorretos.\033[m")

    def login_conta(self):
        print("+==============+ Login +==============+")
        email = input("Email:").strip()
        senha = input("Senha:").strip()
        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha:
                self.limpar_terminal()
                print(f"Seja Bem vindo {usuario.nome}!")
                return
        print("[ERRO]")
