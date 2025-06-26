import webbrowser
import os
import json

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

    

  