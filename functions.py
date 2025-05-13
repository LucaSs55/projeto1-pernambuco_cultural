import os
import json
from getpass import getpass

caminho_arquivo = "users.txt"

class Usuario:
    def __init__(self,nome,email,senha,confirmacaoSenha):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.confirmacaoSenha = confirmacaoSenha
        



class SistemaDeUsuarios:
    def __init__(self,caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.usuarios = self.carregar_usuarios()


    def menu(self):
        print('''          
              <<<<<<<<<<<< === Pernambuco Cultural === >>>>>>>>>>>>>>

    [1] Cadastro de usuário
    [2] ver informações de usuário
    [3] Deletar conta
    [4] Ver eventos regionais
              

''')
        print("-------------------------------------")
        resp = input("Escolha uma das opções acima:")
        return resp
    
    def limparTerminal():
        return os.system('cls' if os.name == 'nt' else 'clear')

    def carregar_usuarios(self):
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo,"r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        else:
            return []
    def salvar_usuarios(self):
        with open(self.caminho_arquivo,"w") as f:
            json.dump(self.usuarios,f,indent= 4)


    def checkNomeAndEmail(self,novo_usuario):
        for item in self.usuarios:
            if item.get("Nome") == novo_usuario["Nome"] or item.get("Email") == novo_usuario["Email"]:
                return True
        return False
    
    


    def cadastrar_usuario(self):
        SistemaDeUsuarios.limparTerminal()
        print("============> Cadastro de Usuário <============")
        nome = input("Digite seu nome:").strip()
        email = input("Digite seu email:").strip()
        senha = input("Digite sua senha:").strip()
        confirmacaoSenha = input("Confirme sua senha:").strip()

        novo_usuario = { 
            "Nome":nome,
            "Email": email,
            "Senha": senha,
            "ConfirmacaoDeSenha": confirmacaoSenha
        }
        
        if self.checkNomeAndEmail(novo_usuario):
            print("[ERRO] Nome ou Email já existente")
            return
        
        self.usuarios.append(novo_usuario)
        self.salvar_usuarios()
        print("Usuário cadastrado com sucesso!")
    
    def ver_conta(self):
        SistemaDeUsuarios.limparTerminal()
        print("============> Ver informações de Usuário <============")

        email = input("Digite seu Email:")
        senha = input("Digite sua senha:")

        for item in self.usuarios:
           if item.get("Email") == email and item.get("Senha") == senha:
                print(" <========= Informações de Usuário ========>")
                print(f"\033[32m \nNome:{item.get('Nome')} \033[m ")
                print(f"\033[32m Email: {item.get('Email')} \033[m")
                print(f"\033[32m Senha: {item.get('Senha')} \033[m")
                return

        print("[ERRO] Email ou Senha incorretos")
    
    def deletar_conta(self):
        SistemaDeUsuarios.limparTerminal()
        print("==================> Deletar Usuário <==================")
        email = input("Email da conta a ser deletada:")
        senha = input("Senha da conta a ser deletada:")

        for i,usuario in enumerate(self.usuarios):
            if usuario.get("Email") == email and usuario.get("Senha") == senha:
                confirmacao = input("Deseja realmente deletar a conta?(s/n):")
                if confirmacao == "s":
                    del self.usuarios[i]
                    self.salvar_usuarios()
                    print(" \033[32m Conta deletada com Sucesso. \033[m")
                    return
                else:
                    print(" \033[31m Operação cancelada \033[m")
                    return
                
        print("[ERRO] email ou senha inválidos")




        

        

            





