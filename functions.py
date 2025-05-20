import os
import json
import re


#Classe que modela os dados de usuário
class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    #Monta instâncias apartir de dicionários
    @staticmethod #Método que não possui acesso a atributos ou métodos de instâncias ou classes
    def from_dict(dados):
        return Usuario(dados["nome"], dados["email"], dados["senha"])

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha
        }

    def __str__(self):
        return f"Nome:{self.nome}, Email:{self.email}"

#Classe que administra operações de usuários
class SistemaDeUsuarios:

   def __init__(self, arquivo_externo_usuarios="usuarios.json"):
        self.arquivo_externo_usuarios = arquivo_externo_usuarios
        self.usuarios = []
        self.carregar_usuarios()

   def menu(self):
       print('''

        ===============> MENU PRINCIPAL <=================

        [1] Cadastro de Usuário
        [2] Ver informações de usuário
        [3] Deletar conta
        [4] Atualizar dados da conta

       ''')
       return input("Escolha uma das opções acima:")

    # Validações Dos dados de usuário
   def validacao_de_email(self, email):
        dominios_validos = ("@gmail.com", "@hotmail.com", "@yahoo.com")
        return email.endswith(dominios_validos)
            


   def validacao_de_senha(self,senha):
       if len(senha) <= 8:
           return False
       if not re.search(r'[A-Z]',senha): return False
       if not re.search(r'[0-9]', senha): return False
       if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha): return False
       return True
        

    # Envio e modelagem dos dados para o arquivo externo json
   def carregar_usuarios(self):
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
       with open(self.arquivo_externo_usuarios,"w") as d:
           json.dump([item.to_dict() for item in self.usuarios],d,indent=4)


   def cadastrar_usuario(self):
        print("============> Cadastro de Usuário <============")

        # Loop para nome
        while True:
            nome = input("Digite seu nome: ").strip()
            if nome:
                break
            else:
                print("\033[31m[ERRO] Nome não pode estar vazio.\033[m")

        # Loop para email
        while True:
            email = input("Digite seu email (ex: @gmail.com, @hotmail.com, @yahoo.com): ").strip()
            if self.validacao_de_email(email):
                break
            else:
                print("\033[31m[ERRO] Email inválido. Tente novamente com um domínio válido.\033[m")

        # Loop para senha e confirmação de senha
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
        self.usuarios.append(novo_usuario)
        self.salvar_dados_usuarios()
        print("\033[32m Novo Usuário cadastrado com sucesso! \033[m")


   def deletar_conta(self):
        print("============> Deletar Conta <============")
    
        email = input("Digite seu email: ").strip()
        senha = input("Digite sua senha: ").strip()

        for i, usuario in enumerate(self.usuarios):
            if usuario.email == email and usuario.senha == senha:
                confirmacao = input("Tem certeza que deseja deletar sua conta? (s/n): ").strip().lower()
                if confirmacao == "s":
                    del self.usuarios[i]
                    self.salvar_dados_usuarios()
                    print("\033[32mConta deletada com sucesso!\033[m")
                else:
                    print("\033[33mOperação cancelada.\033[m")
                return

        print("\033[31m[ERRO] Email ou senha incorretos.\033[m")


   def atualizar_usuario(self):
        print("============> Atualizar Conta <============")

        email = input("Digite seu email atual: ").strip()
        senha = input("Digite sua senha atual: ").strip()

        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha:
                print("\033[32mUsuário encontrado.\033[m")
                print("O que você deseja atualizar?")
                print("[1] Nome\n[2] Email\n[3] Senha\n[4] Todos os dados")
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
                            print("\033[31m[ERRO] A senha deve conter:\n- No mínimo 8 caracteres\n- Uma letra maiúscula\n- Uma letra minúscula\n- Um número\n- Um caractere especial.\033[m")
                            continue
                        usuario.senha = nova_senha
                        break

                self.salvar_dados_usuarios()
                print("\033[32mDados atualizados com sucesso!\033[m")
                return

        print("\033[31m[ERRO] Email ou senha incorretos.\033[m")











       
       










        

        

            





