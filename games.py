import json
class SistemaDeJogos:
    def __init__(self, arquivo_externo_quiz = "quiz.json"):
        '''
        Inicia os jogos presentes na classe SistemaDeJogos e traz como parâmetro o arquivo quiz.json que armazena perguntas.

        Parâmetros:
        - arquivo_externo_quiz: traz o caminho do arquivo json onde são armazenadas as perguntas do quiz literário
    
        '''
        self.arquivo_externo_quiz = arquivo_externo_quiz
        self.perguntas = self.carregarDadosQuiz()
        self.lista_palavras = ["Ariano Suassuna", "Clarice Lispector", "Manuel Bandeira","João Cabral de Melo Neto","A hora da estrela", "O auto da compadecida","A cinza das horas","João grilo","Macabea"]
         
    #Carrega os dados em formato json presentes em quiz.json
    def carregarDadosQuiz(self):
        """
        Carrega as perguntas do quiz, com base no caminho especificado no init da classe.

        Retorna:
        - lista: Lista de dicionários contendo as perguntas, opções, respostas e dificuldade de cada item do quiz.
        """
        try:
            with open(self.arquivo_externo_quiz, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                return json.loads(conteudo) if conteudo else []
        except FileNotFoundError:
            print("[ERRO] Arquivo de perguntas não encontrado.")
            return []
        except json.JSONDecodeError:
            print("[ERRO] O Json do arquivo de perguntas está mal formatado.")
            return []

    def quizLiterario(self, usuario):
        """
        Inicia um quiz literário com perguntas de múltipla escolha acerca de temas literários regionais e universais.

        Parâmetros:
        - usuario (objeto): É o objeto que representa o usuário, que como um jogador pode ganhar ou perder pontos conforme as perguntas acertadas e erraddas respectivamente.
        """
        import random
        letra_dificuldade = {
        "f": "fácil",
        "m": "médio",
        "d": "difícil"
        }
        if not self.perguntas:
            print("[ERRO] Nenhuma pergunta carregada para o quiz.")
            return
        letra = input("\033[33mEscolha a dificuldade (😊 fácil(digite f) | 🤔 médio(digite m) | 😰 difícil(digite d)): ").strip().lower()
        dificuldade = letra_dificuldade.get(letra)
        perguntas_filtradas = [p for p in self.perguntas if p.get("dificuldade") == dificuldade] #list comprehenson para filtrar as perguntas com base na dificuldade

        if len(perguntas_filtradas) > 8:
            perguntas_filtradas = random.sample(perguntas_filtradas,8) #Seleciona 8 perguntas aleaórias dentro da dificuldade selecionada

        if not perguntas_filtradas:
            print("[ERRO] Nenhuma pergunta encontrada para essa dificuldade.")
            return

        print(f"\n\033[34mIniciando Quiz Literário - Dificuldade: {dificuldade.capitalize()}\033[m\n")

        acertos = 0
        erros = 0
        for pergunta in perguntas_filtradas:
            print("\033[33m")
            print(f"\n📖 Pergunta: {pergunta['pergunta']}")
            for i, opcao in enumerate(pergunta["opcoes"], 1):
                print(f"{i}. {opcao}")
            resposta_usuario = input("Digite o número da resposta(0 para desistir e retornar ao menu de games): ").strip()

            if resposta_usuario == "0":
                print("\033[33m ⚠️  Você desistiu do quiz, Retornando ao menu de games...\033[m")
                return

            try:
                indice = int(resposta_usuario) - 1
                if pergunta["opcoes"][indice].lower() == pergunta["resposta"].lower():
                    print("✅ Resposta correta!")
                    acertos += 1
                else:
                    erros += 1
                    if dificuldade == "fácil":
                        pontos_por_erro = 5

                    elif dificuldade == "médio":
                        pontos_por_erro = 8

                    else:
                        pontos_por_erro = 10

                    pontos_perdidos = erros * pontos_por_erro
                    usuario.perderPontos(pontos_perdidos)
                    print(f"\033[31m😭Você errou | Resposta correta: {pergunta['resposta']} | ❌ Número de erros: {erros} | Perdeu: -{pontos_perdidos} pontos\033[m")

                    if erros == 3:
                        print(f"\033[31m 🤯 Você excedeu o limite de 3 erros | Pontos Perdidos: -{pontos_perdidos}\033[m")
                        break

            except (ValueError, IndexError):
                print(" O valor digitado é inválido, Pulando pergunta...")

        if dificuldade == "fácil":
            pontos_por_acerto = 10

        elif dificuldade == "médio":
            pontos_por_acerto = 15

        else:
            pontos_por_acerto = 20

        pontos_ganhos = acertos * pontos_por_acerto
        usuario.acumularPontos(pontos_ganhos)
        print(f"\n🧠Parabéns, Você acertou {acertos} de {len(perguntas_filtradas)} perguntas.")
        print(f"⭐Pontos ganhos: {pontos_ganhos}")
        print(f"🏅 Pontuação total: {usuario.pontos} | Divisão: {usuario.divisao}")

    def adivinharQuotes(self, usuario, arquivo_citacoes="quotes.json"):
        """
            Jogo de adivinhação onde o jogador deve descobrir a qual obra literária pertence a respectiva citação.

            Parâmetros:
            - usuario (objeto): Objeto do usuário que poder perder ou acumular pontos conforme as citações acertadas e perder pontos por cada citação errada.
            - arquivo_citacoes (string): Caminho para o arquivo JSON contendo as citações quotes.json que guarda as informações de citação, opções e a resposta da respectiva citação.
        """
        import random
        try:
            with open(arquivo_citacoes, "r", encoding="utf-8") as f:
                conteudo = f.read().strip()
                citacoes = json.loads(conteudo) if conteudo else []
        except FileNotFoundError:
            print("[ERRO] Arquivo de citações não encontrado.")
            return
        except json.JSONDecodeError:
            print("[ERRO] O JSON do arquivo de citações está mal formatado.")
            return

        if not citacoes:
            print("[ERRO] Nenhuma citação carregada.")
            return

        print("\n\033[34m=== 📝 Jogo: Adivinhe o livro pela citação (Múltipla Escolha) ===\033[m\n")
        acertos = 0
        erros = 0
        quantidade = min(5, len(citacoes))
        citacoes_aleatorias = random.sample(citacoes, quantidade)

        for item in citacoes_aleatorias:
            print("\033[33m")
            print(f"\n📖 Citação:\n\"{item['citacao']}\"")
            for i, opcao in enumerate(item["opcoes"], 1):
                print(f"{i}. {opcao}")

            escolha = input("Escolha a alternativa correta (1-4): ").strip()

            try:
                indice = int(escolha) - 1
                if item["opcoes"][indice].strip().lower() == item["resposta"].strip().lower():
                    print("✅ Correto!")
                    acertos += 1
                else:
                    erros += 1
                    pontos_perdidos = erros * 10
                    usuario.perderPontos(pontos_perdidos)
                    print(f"\033[31m[ERROU] Resposta correta: {item['resposta']} | ❌ Número de erros: {erros} | Perdeu {pontos_perdidos} pontos\033[m")

                    if erros == 5:
                        print(f"\033[31m🤯 Você excedeu o limite de 5 erros | Pontos Perdidos: -{pontos_perdidos}\033[m")
                        break
             

                    
            except (ValueError, IndexError):
                print("❌ Entrada inválida. Pulando pergunta.")

        pontos_ganhos = acertos * 15
        usuario.acumularPontos(pontos_ganhos)

        print(f"\n🧠 Você acertou {acertos} de {(quantidade)} citações.")
        print(f"⭐ Pontos ganhos: {pontos_ganhos}")
        print(f"🏅 Sua Pontuação total: {usuario.pontos} | Divisão: {usuario.divisao}")

    def forcaLiteraria(self, usuario):

        """
        Jogo da forca com nomes de autores, obras ou personagens literários famosos tanto em Pernambuco quanto na literatura universal.

        Parâmetros:
        - usuario (objeto): Objeto do usuário que acumula pontos se acertar a palavra secreta da forca e não perde pontos neste jogo.
        """
        import random
        palavra = random.choice(self.lista_palavras).lower() #evita erro por divergência de minúsculas e maiúsculas
        letras_adivinhadas = set()
        tentativas_restantes = 6

        print("\n\033[34m=== 🎭 Jogo da Forca Literária ===\033[m\n")
        print("\033[34mAdivinhe o nome de uma obra, autor(a) ou personagem literário!\033[m\n")

        while tentativas_restantes > 0:
            exibicao = ""
            for letra in palavra:
                if letra in letras_adivinhadas or not letra.isalpha(): #Verifica se a letra já foi adivinhada ou se é número,caractere especial retornando false e retorna true caso seja uma letra válida
                    exibicao += letra #Se for true retorna a letra
                else:
                    exibicao += "_"
            print("Palavra: " + " ".join(exibicao))

            if "_" not in exibicao:
                print("🎉 \033[32mParabéns! Você acertou a palavra!\033[m")
                usuario.acumularPontos(20)
                print(f"🏆 Pontos ganhos: 20\n📊 Total: {usuario.pontos} | Divisão: {usuario.divisao}")
                return

            palpite = input("Digite uma letra: ").lower().strip()
            if len(palpite) != 1 or not palpite.isalpha():
                print("Digite apenas UMA letra válida.")
                continue

            if palpite in letras_adivinhadas:
                print("\033[31mVocê já tentou essa letra\033[31m")
                continue

            letras_adivinhadas.add(palpite)

            if palpite not in palavra:
                tentativas_restantes -= 1
                print(f"❌\033[31m Letra incorreta | Tentativas restantes: {tentativas_restantes}\033[m")
            else:
                print("✅\033[32m Letra correta!\033[m")

        print(f"\n💀\033[31m Fim de jogo! A palavra era: {palavra}\033[m")
        print(f"📊\033[31m Nenhum ponto ganho | Sua Pontuação: {usuario.pontos}\033[m")

    def completeLetraMusica(self,usuario):

        """
            Jogo em que o jogador deve completar letras de músicas tradicionais ou populares.

            Parâmetros:
            - usuario (obj): Objeto do usuário que acumula pontos ao longo das letras de músicas acertadas.
        """
        print("\n\033[34m🎵 === Complete a Letra (Jogo Musical) === 🎵\033[m")
        print("\033[33mTema: Músicas populares ou tradicionais.\033[m\n")

        # Lista de trechos com lacunas e respostas corretas
        trechos = [
            {"trecho": "Asa branca quando ela bate no sertão é ___", "resposta": "saudade"},
            {"trecho": "Olha pro céu meu amor, vê como ele está ___", "resposta": "lindo"},
            {"trecho": "O xote das meninas é bonito de se ___", "resposta": "ver"},
            {"trecho": "Morena tropicana eu quero teu ___", "resposta": "sabor"},
            {"trecho": "É só o amor que reconhece o que é ___", "resposta":"verdade"}
        ]

        acertos = 0
        erros = 0
        for item in trechos:
            print(f"\n🎶 Letra: {item['trecho']}")
            resposta = input("Complete a lacuna: ").strip().lower()

            if resposta == item['resposta'].lower():
                print("✅ Correto!")
                acertos += 1
            else:
                erros += 1
                print(f"\033[31m[ERROU] A resposta correta era: {item['resposta']} | ❌ Número de erros: {erros} \033[m")
                

                if erros == 3:
                    print("")
                    print("\033[31m💀 Fim de jogo, Você ultrapassou o limite de 3 erros\033[m")
                    break

        pontos_ganhos = acertos * 5
        usuario.acumularPontos(pontos_ganhos)
        print(f"\033[32m🎯 Você acertou {acertos} de {len(trechos)} trechos.")
        print(f"🏆 Pontos ganhos: {pontos_ganhos}")
        print(f"📊 Pontuação total: {usuario.pontos} | Divisão: {usuario.divisao}")

