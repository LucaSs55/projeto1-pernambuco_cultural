from functions import SistemaDeUsuarios

sistema = SistemaDeUsuarios(caminho_arquivo= "users.txt")

while True:
    opcao = sistema.menu()

    if opcao == "1":
        sistema.cadastrar_usuario()

    elif opcao == "2":
        sistema.ver_conta()

    elif opcao == "3":
        sistema.deletar_conta()

    elif opcao == "4":
        pass




