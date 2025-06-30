from user import SistemaDeUsuarios
from events_promoter import SistemaDeEventos

#Arquivo que chama as funções

sistema_usuarios = SistemaDeUsuarios(arquivo_externo_usuarios = "usuarios.json")
sistema_eventos = SistemaDeEventos(arquivo_externo_eventos = "eventos.json")

while True:
    opcao = sistema_usuarios.menu()

    if opcao == "1":
        sistema_usuarios.cadastrar_usuario()

    elif opcao == "2":
        sistema_usuarios.ver_conta()

    elif opcao == "3":
        sistema_usuarios.deletar_conta()

    elif opcao == "4":
        sistema_usuarios.atualizar_usuario()
    
    elif opcao == '5':
        sistema_usuarios.login_conta()

    elif opcao == "6":
        sistema_eventos.executar_interface_de_eventos()




