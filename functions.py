import os
import re
import json
import webbrowser


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

    #Monta instâncias apartir de dicionários
    @staticmethod #Método que não possui acesso a atributos ou métodos de instâncias ou classes
    def from_dict(dados):

        """
        Cria uma instância da classe Usuario a partir de um dicionário

        Parâmetros:
            dados (dict): Dicionário contendo as chaves 'nome', 'email' e 'senha'

        Retorna:
            Usuario: Um objeto da classe Usuario
        """
        return Usuario(dados["nome"], dados["email"], dados["senha"])

    def to_dict(self):
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

    #Validações Dos dados de usuário
    
    def validacao_de_email(self, email):

        """
        Verifica se o email termina com um dos domínios válidos.

        Parâmetros:
            email (str): Email a ser validado.

        Retorna:
            bool: True se o email for válido, False caso contrário.
        """
        
        dominios_validos = ("@gmail.com", "@hotmail.com", "@yahoo.com")
        return email.endswith(dominios_validos) #Verifica se o email termina com os domínios válidos
            


    def validacao_de_senha(self,senha):
       
       """
        Verifica se a senha atende aos critérios de complexidade.

        Parâmetros:
            senha (str): Senha a ser validada.

        Retorna:
            bool: True se a senha for considerada forte, False caso contrário.
        """
       if len(senha) < 8: return False
       if not re.search(r'[A-Z]',senha): return False 
       if not re.search(r'[0-9]', senha): return False
       if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha): return False
       return True
        

    # Envio e modelagem dos dados para o arquivo externo json
    def carregar_usuarios(self):

        """
        Carrega os usuários do arquivo JSON e os armazena em uma lista.
        """
        if os.path.exists(self.arquivo_externo_usuarios):
            with open(self.arquivo_externo_usuarios,"r") as d:
                try:
                    dados = json.load(d)
                    self.usuarios = [Usuario.from_dict(item) for item in dados]
                except json.JSONDecodeError:
                    print("Arquivo Json Inválido")
                    self.usuarios = []
        else:
            self.usuarios = []

    #Salva dados do usuário no arquivo externo json
    def salvar_dados_usuarios(self):

        """
        Salva os dados dos usuários no arquivo JSON.
        """
        with open(self.arquivo_externo_usuarios,"w") as d: #Abre o arquivo json no modo de escrita
            json.dump([item.to_dict() for item in self.usuarios],d,indent=4)


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
            if nome:
                break
            else:
                print("\033[31m[ERRO] Nome não pode estar vazio.\033[m")

        # Loop para email até ser digitado um email com domínio válido
        while True:
            email = input("Digite seu email (ex: @gmail.com, @hotmail.com, @yahoo.com): ").strip()
            if self.validacao_de_email(email):
                break
            else:
                print("\033[31m[ERRO] Email inválido. Tente novamente com um domínio válido.\033[m")

        # Loop para senha e confirmação de senha até ambas serem validadas
        while True:
            senha = input("Digite sua senha: ").strip()
            confirmacao = input("Confirme sua senha: ").strip()

            if senha != confirmacao:
                print("\033[31m[ERRO] As senhas não coincidem.\033[m")
                continue

            if not self.validacao_de_senha(senha):
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
        for i, usuario in enumerate(self.usuarios): #Escaneia os pares chave-valor dentro da lista usuarios
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
                        if self.validacao_de_email(novo_email):
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
                        if not self.validacao_de_senha(nova_senha):
                            print("\033[31m[ERRO] A senha deve conter:\n- No mínimo 8 caracteres\n- Uma letra maiúscula\n- Um número\n- Um caractere especial.\033[m")
                            continue
                        usuario.senha = nova_senha
                        break
                self.limpar_terminal()
                self.salvar_dados_usuarios()
                print("\033[32mDados atualizados com sucesso!\033[m")
                return

        print("\033[31m[ERRO] Email ou senha incorretos.\033[m")

#Classe para modelar a leitura e a apresentação dos dados de eventos regionais
class SistemaDeEventos:
    def __init__(self,arquivo_externo_eventos = "eventos.json"):
        """
        Inicializa o sistema de eventos e carrega os dados do arquivo JSON.

        Parâmetros:
            arquivo_externo_eventos (str): Caminho para o arquivo JSON com os dados dos eventos.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.arquivo_externo_eventos = os.path.join(base_path,arquivo_externo_eventos)
        self.eventos = self.carregar_eventos()
        
    def carregar_eventos(self):
        """
        Carrega os eventos do arquivo JSON

        Retorna:
            list: Lista de eventos
        """
        try:
            with open(self.arquivo_externo_eventos,"r",encoding= "utf-8") as f: #Abre o arquivo de eventos no modo de leitura para trazer as strings salvas dentro do arquivo
                return json.load(f)
            
        except FileNotFoundError:
            print("[ERRO]Arquivo não encontrado")
            return []
        
        except json.JSONDecodeError:
            print("[ERRO] Arquivo json inválido")
            return []

    def mostrar_eventos(self):

        '''Permite a Exibição dos eventos recomendados no terminal com o link de direcionamento para mais informações do evento  
        
        Há um laço de repetição que pega o par chave-valor e permite a exibição do evento com o respectivo índice na tela
        '''
        print(" \033[33m <============ Eventos Recomendados ============> \033[m")
        print("")
        print(f"\033[33m{30*"+="} \033[m")
        for i, evento in enumerate(self.eventos,1):
            print(f"\033[32m{i}-{evento["titulo"]} \033[m")
            print(f"\033[32m• Data:{evento["data"]}") 
            print(f"• Descrição:{evento["descricao"]}")
            print(f"• Link:{evento["link"]}\033[m \n")
        print(f"\033[33m {30*"+="} \033[m")

    def abrir_link_evento(self,i):
        ''' 
        Permite o direcionamento do usuário para uma página no navegador com o respectivo evento

        Por meio da biblioteca webbrowser ocorre o direcionamento para uma página do navegador do respectivo evento por meio da abertura de seu link
        
        '''
        try:
            evento = self.eventos[i-1]
            print(f"Abrindo link do evento: {evento["titulo"]}")
            webbrowser.open(evento["link"])
        except IndexError:
            print("[ERRO]Endereço do evento não encontrado")

    def recomendar_eventos(self):

        '''
        Permite a recomendação dos eventos para o usuário por meio de uma chamada única de função

        Cria o loop que mantém os eventos na tela e possibilita a saída do usuário ao digitar 0
        
        '''
        while True:
            self.mostrar_eventos()
            opcao = input("Digite o número de um dos eventos (Digite 0 para sair):")

            if opcao == "0":
                print("Saindo do divulgador de eventos...")
                break
            elif opcao.isdigit():
                self.abrir_link_evento(int(opcao))

            else:
                print("[ERRO] O valor digitado é inválido")

    

  


             











       
       










        

        

            





