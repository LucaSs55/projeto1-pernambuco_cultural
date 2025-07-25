import os
import json
from validations import *

#Classe que modela os dados de usuário
class Usuario:
    def __init__(self, nome, email, senha, divisao ="Ferro", pontos = 0):
        """
        Inicializa um novo usuário

        Parâmetros:
            nome (str): Nome do usuário
            email (str): Email do usuário
            senha (str): Senha do usuário
            divisão(str): Divisão do usuário que é inicializada como ferro
            pontos(int): Número de pontos do usuário que é inicializado com valor 0
        """
        self.nome = nome
        self.email = email
        self.senha = senha
        self.divisao = divisao
        self.pontos = pontos

    def modelarUsuario(self):
        """
        Modela o objeto Usuario em um dicionário

        Retorna:
            dicionário: Dicionário com os dados do usuário
            chaves: nome, email, senha, divisão, pontos
        """
        return {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "divisao":self.divisao,
            "pontos":self.pontos
        }

    def __str__(self):
        """
        Representação em string do objeto usuário.

        Retorna:
            str: Nome, Email , Divisão e Pontos do usuário formatados.
        """


        return f"Nome:{self.nome} | Email:{self.email} | Divisão:{self.divisao} | Pontos:{self.pontos}"
    
    def acumularPontos(self,numero_de_pontos):
        self.pontos += numero_de_pontos
        self.alterarDivisao()

    def perderPontos(self,numero_de_pontos):
        self.pontos -= numero_de_pontos
        self.alterarDivisao()

    def alterarDivisao(self):
        if self.pontos >= 2000:
            self.divisao = "Diamante"

        elif self.pontos >= 1000:
            self.divisao = "Rubi"

        elif self.pontos >= 500:
            self.divisao = "Esmeralda"

        elif self.pontos >= 300:
            self.divisao = "Ouro"

        elif self.pontos >= 250:
            self.divisao = "Prata"

        elif self.pontos >= 125:
            self.divisao = "Bronze"
            
        else:
            self.divisao = "Ferro"

#Classe que administra operações gerais de usuários
class SistemaUsuarios:

    def __init__(self, arquivo_externo_usuarios="usuarios.json"):

        """
        Inicializa o sistema de usuários e carrega os dados do arquivo JSON

        Parâmetros:
            arquivo_externo_usuarios (str): Caminho para o arquivo JSON com os dados dos usuários
        """
        self.arquivo_externo_usuarios = arquivo_externo_usuarios
        self.usuarios = []
        self.carregarDadosUsuarios()

    def menu(self):
       
       """
        Exibe o menu principal com as opções disponíveis para o usuário.

        Retorna:
            str: Opção escolhida pelo usuário.
        """
       print("\033[34m|======================================|\033[m")
       print("\033[34m|        >>> MENU PRINCIPAL <<<        |\033[m")
       print("\033[34m|--------------------------------------|\033[m")
       print("\033[34m|\033[33m  [1]\033[m \033[34m -  Cadastro de Usuário         |\033[m")
       print("\033[34m|\033[33m  [2]\033[m \033[34m -  Ver Informações de Usuário  |\033[m")
       print("\033[34m|\033[33m  [3]\033[m \033[34m -  Deletar Conta               |\033[m")
       print("\033[34m|\033[33m  [4]\033[m \033[34m -  Atualizar Dados da Conta    |\033[m")
       print("\033[34m|\033[33m  [5]\033[m \033[34m -  Login                       |\033[m")
       print("\033[34m|\033[33m  [6]\033[m \033[34m -  Recomendações de Eventos    |\033[m")
       print("\033[34m|======================================|\033[m ")
       return input("\033[34mEscolha uma das opções acima:\033[m")
       
    def limparTerminal(self):

        """
        Limpa o terminal com base no sistema operacional.

        Retorna:
            nt: Código de status do comando de limpeza do terminal.
        """
        return os.system("cls" if os.name == "nt" else "clear")

    # Envio e modelagem dos dados para o arquivo externo json
    def carregarDadosUsuarios(self):

        """
        Carrega os usuários do arquivo JSON e os armazena em uma lista.
        """
        if os.path.exists(self.arquivo_externo_usuarios):
            with open(self.arquivo_externo_usuarios, "r", encoding="utf-8") as d:
                try:
                    conteudo = d.read().strip()
                    if not conteudo:
                        self.usuarios = []
                        return
                    dados = json.loads(conteudo)
                    self.usuarios = []
                    for item in dados:
                        nome = item.get("nome")
                        email = item.get("email")
                        senha = item.get("senha")
                        divisao = item.get("divisao")
                        pontos = item.get("pontos")
                        usuario = Usuario(
                            nome,
                            email,
                            senha,
                            divisao=divisao if divisao is not None else "Ferro",
                            pontos=pontos if pontos is not None else 0
                        )
                        self.usuarios.append(usuario)
                except json.JSONDecodeError:
                    print("\033[31m[ERRO] Arquivo JSON inválido. Reiniciando lista de usuários...\033[m")
                    self.usuarios = []
        else:
            self.usuarios = []

    #Salva dados do usuário no arquivo externo json
    def salvaradosUsuarios(self):

        """
        Salva os dados dos usuários no arquivo usuarios.json.
        """
        with open(self.arquivo_externo_usuarios,"w",encoding="utf-8") as d: #Abre o arquivo json no modo de escrita
            json.dump([item.modelarUsuario() for item in self.usuarios],d,indent=4,ensure_ascii=False)


    def cadastrarUsuario(self):

        """
        Realiza o cadastro de um novo usuário.

        Solicita nome, email e senha; realiza validações; armazena o novo usuário se todas
        as informações forem válidas.
        """
        self.limparTerminal()
        print("\033[34m============> Cadastro de Usuário <============\033[m")
        # Loop para nome
        while True:
            nome = input("\033[33mDigite seu nome:\033[m ").strip().lower()
            if validacaoNome(nome, self.usuarios):
                break

        # Loop para email até ser digitado um email com domínio válido
        while True:
            email = input("\033[33mDigite seu email (ex: @gmail.com, @hotmail.com, @yahoo.com):\033[m ").strip()
            if validacaoEmail(email,self.usuarios):
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

            if not validacaoSenha(senha):
                print("\033[31m[ERRO] A senha deve conter:\n- No mínimo 8 caracteres\n- Uma letra maiúscula\n- Um número\n- Um caractere especial.\033[m")
                continue
            break

        # Se tudo estiver certo, cria e salva o usuário
        novo_usuario = Usuario(nome, email, senha)
        self.usuarios.append(novo_usuario) # Salva o novo usuário na lista
        self.salvaradosUsuarios()
        self.limparTerminal()
        print("\033[32m Novo Usuário cadastrado com sucesso! \033[m")


    def verContaUsuario(self):
        ''' 
        Possibilita a leitura dos dados de usuário, após a validação com dos dados com base no que já foi previamente cadastrado

        Solicita Email, Senha e realiza validações se estiverem corretos imprime os dados de usuário na tela 
        '''
        self.limparTerminal()
        print("\033[34m============> Ver Informações de Usuário <============\033[m")
        email = input("\033[33mDigite seu email:\033[m").strip()
        senha = input("\033[33mDigite sua senha:\033[m").strip()
        for usuario in self.usuarios: #Escaneia os pares chave-valor dentro da lista usuarios
            if usuario.email == email and usuario.senha == senha: #verifica se o email e a senha batem com o que está salvo no arquivo de usuarios
                self.limparTerminal()
                print(f"Dados de Usuário:\033[32m\n•Nome: {usuario.nome} \n•Email:{usuario.email} \n•Senha:{usuario.senha}\033[m")
                return  # Sai da função após encontrar o usuário

            # Se o laço terminar sem encontrar, mostra uma única vez:
        print(" \033[31m[ERRO] Email ou Senha Incorretos \033[m")

    def deletarUsuario(self):
        ''' 
        Deleta usuários já cadastrados

        Solicita Email e Senha, se ambos forem validados, então há um input de confirmação da deleção de conta por parte do usuario
        '''
        self.limparTerminal()
        print("\033[34m============> Deletar Conta <============\033[m")
    
        email = input("\033[33mDigite seu email:\033[m ").strip()
        senha = input("\033[33mDigite sua senha:\033[m ").strip()
        #Loop com índice para passar pela lista usuarios, trazendo cada usuario e seu respectivo índice
        for i, usuario in enumerate(self.usuarios):
            if usuario.email == email and usuario.senha == senha:
                confirmacao = input("Tem certeza que deseja deletar sua conta? (s/n): ").strip().lower()
                if confirmacao == "s":
                    del self.usuarios[i] #Exclui o item da lista permanentemente utilizando a func del() a partir do índice[i].
                    self.salvaradosUsuarios()
                    print("\033[32mConta deletada com sucesso!\033[m")
                else:
                    print("\033[33mOperação cancelada.\033[m")
                return

        print("\033[31m[ERRO] Email ou senha incorretos.\033[m")

    def atualizarUsuario(self):
        '''
        Permite a edição dos dados de usuário depois da validação do email e da senha, com base nos dados previamente cadastrados

        Solicita Email e Senha, e se ambos forem validados, então é aberto um menu de escolha das informações a serem alteradas [1]Nome,[2]Email,[3]Senha,[4] Todos os dados
        
        '''
        self.limparTerminal()
        print("\033[34m============> Atualizar Conta <============\033[m")

        email = input("\033[33mDigite seu email atual:\033[m ").strip()
        senha = input("\033[33mDigite sua senha atual:\033[m ").strip()

        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha:
                print("\033[32mUsuário encontrado.\033[m")
                print("O que você deseja atualizar?")
                print("\033[33m[1] Nome\n[2] Email\n[3] Senha\n[4] Todos os dados\033[m") # Menu para exclusão de dados
                opcao = input("Escolha uma opção: ").strip()

                if opcao == "1" or opcao == "4":
                    novo_nome = input("Novo nome: ").strip().lower()
                    if novo_nome:
                        usuario.nome = novo_nome
                    else:
                        print("\033[31m[ERRO] Nome não pode ser vazio.\033[m")
                        return

                if opcao == "2" or opcao == "4":
                    while True:
                        novo_email = input("Novo email: ").strip()
                        if validacaoEmail(novo_email):
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
                        if not validacaoSenha(nova_senha):
                            print("\033[31m[ERRO] A senha deve conter:\n- No mínimo 8 caracteres\n- Uma letra maiúscula\n- Um número\n- Um caractere especial.\033[m")
                            continue
                        usuario.senha = nova_senha
                        break

                self.limparTerminal()
                self.salvaradosUsuarios()
                print("\033[32mDados atualizados com sucesso!\033[m")
                return

        print("\033[31m[ERRO] Email ou senha incorretos.\033[m")

    def loginUsuario(self):
        '''
        Esta função solicita o email e a senha do usuário, verifica as credenciais
        em uma lista de usuários previamente cadastrados e, se válidas, exibe um menu 
        interativo com diversas opções de jogos literários e uma ferramenta de busca de livros.

        Após a validação de login e senha o usuário pode selecionar as opções do menu de:
        - Jogar um quiz literário
        - Adivinhar o livro com base em uma citação
        - Complete a letra da música
        - Jogar um jogo da forca com temas literários
        - Pesquisar livros usando a API de busca
        - Retornar ao menu principal (encerrar sessão)

        Imports:
        - `SistemaDeJogos` (módulo: games): classe responsável pelos jogos disponíveis.
        - `BuscadorLivros` (módulo: book_search): classe responsável pela busca de livros via API.
        '''
        self.limparTerminal()
        print("\033[34m +==============+ Login +==============+\033[m")
        from games import SistemaDeJogos
        from book_search import BuscadorLivros
        sistema_jogos = SistemaDeJogos()
        sistema_buscador_Livros = BuscadorLivros()
        email = input("\033[33mEmail:").strip()
        senha = input("Senha:").strip()
        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha:
                self.limparTerminal()
                print(f"\033[32mSeja Bem vindo, {usuario.nome}!\033[m")

                while True:
                    print("\033[36m|=========================================|\033[m")
                    print("\033[36m|           >>> Menu de Games <<<         |\033[m")
                    print("\033[36m|=========================================|\033[m")
                    print("\033[36m| \033[33m[1]\033[36m - Quiz Literário                    |\033[m")
                    print("\033[36m| \033[33m[2]\033[36m - Adivinhe o livro pela Citação     |\033[m")
                    print("\033[36m| \033[33m[3]\033[36m - Adivinhe a Música pela letra      |\033[m")
                    print("\033[36m| \033[33m[4]\033[36m - Forca de conhecimentos literários |\033[m")
                    print("\033[36m| \033[33m[5]\033[36m - Encontrar Livros                  |\033[m")
                    print("\033[36m| \033[33m[6]\033[36m - Retornar ao menu principal        |\033[m")
                    print("\033[36m|=========================================|\033[m")
                    esc = input("\033[36mEscolha uma opção:\033[m")

                    if esc == "1":
                        sistema_jogos.quizLiterario(usuario)
                        self.salvaradosUsuarios()

                    elif esc == "2":
                        sistema_jogos.adivinharQuotes(usuario)
                        self.salvaradosUsuarios()
                    
                    elif esc == "3":
                        sistema_jogos.completeLetraMusica(usuario)
                        self.salvaradosUsuarios()

                    elif esc == "4":
                        sistema_jogos.forcaLiteraria(usuario)
                        self.salvaradosUsuarios()

                    elif esc == "5":
                        sistema_buscador_Livros.executarBuscadorLivros()
                        
                    elif(esc == "6"):
                        print("Retornando ao menu principal")
                        break
                return
                
        print("\033[31m[ERRO] usuário não encontrado\033[m")
