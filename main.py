from user import SistemaUsuarios
from events_promoter import SistemaDeEventos

#Arquivo que chama as funções

sistema_usuarios = SistemaUsuarios(arquivo_externo_usuarios = "usuarios.json")
sistema_eventos = SistemaDeEventos(arquivo_externo_eventos = "eventos.json")

while True:
    opcao = sistema_usuarios.menu()

    if opcao == "1":
        sistema_usuarios.cadastrarUsuario()

    elif opcao == "2":
        sistema_usuarios.verContaUsuario()

    elif opcao == "3":
        sistema_usuarios.deletarUsuario()

    elif opcao == "4":
        sistema_usuarios.atualizarUsuario()
    
    elif opcao == '5':
        sistema_usuarios.loginUsuario()

    elif opcao == "6":
        sistema_eventos.executarInterfaceEventos()




