import json
class SistemaDeJogos:
    def __init__(self, arquivo_externo_quiz = "quiz.json"):
        self.arquivo_externo_quiz = arquivo_externo_quiz
        self.perguntas = self.carregarDadosQuiz()
        self.lista_palavras = ["Ariano Suassuna", "Clarice Lispector", "Manuel Bandeira","João Cabral de Melo Neto","A hora da estrela", "O auto da compadecida","A cinza das horas","João grilo","Macabea"]
         
    #Carrega os dados em formato json presentes em quiz.json
    def carregarDadosQuiz(self):
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
        import random
        if not self.perguntas:
            print("[ERRO] Nenhuma pergunta carregada para o quiz.")
            return
        dificuldade = input("Escolha a dificuldade (🌱 fácil |  ⚖️ médio | 🔥 difícil): ").strip().lower()
        perguntas_filtradas = [p for p in self.perguntas if p.get("dificuldade") == dificuldade] #list comprehenson para filtrar as perguntas com base na dificuldade

        if len(perguntas_filtradas > 8):
            random.sample(perguntas_filtradas,8) #Seleciona 8 perguntas aleaórias dentro da dificuldade selecionada

        if not perguntas_filtradas:
            print("[ERRO] Nenhuma pergunta encontrada para essa dificuldade.")
            return

        print(f"\nIniciando Quiz Literário - Dificuldade: {dificuldade.capitalize()}\n")

        acertos = 0
        erros = 0
        for pergunta in perguntas_filtradas:
            print(f"\n📖 Pergunta: {pergunta['pergunta']}")
            for i, opcao in enumerate(pergunta["opcoes"], 1):
                print(f"{i}. {opcao}")
            resposta_usuario = input("Digite o número da resposta: ").strip()

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
                    print(f"Você errou,  Resposta correta: {pergunta['resposta']} | ❌ Número de erros: {erros} | Perdeu {pontos_perdidos}pontos")

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

        print("\n=== 📝 Jogo: Adivinhe o livro pela citação (Múltipla Escolha) ===\n")
        acertos = 0
        quantidade = min(5, len(citacoes))
        citacoes_aleatorias = random.sample(citacoes, quantidade)

        for item in citacoes_aleatorias:
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
                    print(f"❌ Errado! A resposta correta era: {item['resposta']}")
            except (ValueError, IndexError):
                print("❌ Entrada inválida. Pulando pergunta.")

        pontos_ganhos = acertos * 15
        usuario.acumularPontos(pontos_ganhos)

        print(f"\n🧠 Você acertou {acertos} de {len(quantidade)} citações.")
        print(f"⭐ Pontos ganhos: {pontos_ganhos}")
        print(f"🏅 Pontuação total: {usuario.pontos} | Divisão: {usuario.divisao}")

    def forcaLiteraria(self, usuario):
        import random
        palavra = random.choice(self.lista_palavras).lower() #evita erro por divergência de minúsculas e maiúsculas
        letras_adivinhadas = set()
        tentativas_restantes = 6

        print("\n=== 🎭 Jogo da Forca Literária ===\n")
        print("Adivinhe o nome de uma obra, autor(a) ou personagem literário!\n")

        while tentativas_restantes > 0:
            exibicao = ""
            for letra in palavra:
                if letra in letras_adivinhadas or not letra.isalpha(): #Verifica se a letra já foi adivinhada ou se é número,caractere especial retornando false e retorna true caso seja uma letra válida
                    exibicao += letra #Se for true retorna a letra
                else:
                    exibicao += "_"
            print("Palavra: " + " ".join(exibicao))

            if "_" not in exibicao:
                print("🎉 Parabéns! Você acertou a palavra!")
                usuario.acumularPontos(20)
                print(f"🏆 Pontos ganhos: 20\n📊 Total: {usuario.pontos} | Divisão: {usuario.divisao}")
                return

            palpite = input("Digite uma letra: ").lower().strip()
            if len(palpite) != 1 or not palpite.isalpha():
                print("Digite apenas UMA letra válida.")
                continue

            if palpite in letras_adivinhadas:
                print("Você já tentou essa letra.")
                continue

            letras_adivinhadas.add(palpite)

            if palpite not in palavra:
                tentativas_restantes -= 1
                print(f"❌ Letra incorreta. Tentativas restantes: {tentativas_restantes}")
            else:
                print("✅ Letra correta!")

        print(f"\n💀 Fim de jogo! A palavra era: {palavra}")
        print(f"📊 Nenhum ponto ganho. Pontuação: {usuario.pontos}")

    def adivinharMusicaLetra(self,usuario):
        print("\n🎵 === Complete a Letra (Jogo Musical) === 🎵")
        print("Tema: Músicas populares ou tradicionais.\n")

        # Lista de trechos com lacunas e respostas corretas
        trechos = [
            {"trecho": "Asa branca quando ela bate no sertão é ___", "resposta": "saudade"},
            {"trecho": "Olha pro céu meu amor, vê como ele está ___", "resposta": "lindo"},
            {"trecho": "O xote das meninas é bonito de se ___", "resposta": "ver"},
            {"trecho": "Morena tropicana eu quero teu ___", "resposta": "sabor"},
            {"trecho": "É só o amor que reconhece o que é ___", "resposta":"verdade"}
        ]

        acertos = 0

        for item in trechos:
            print(f"\n🎶 Letra: {item['trecho']}")
            resposta = input("Complete a lacuna: ").strip().lower()

            if resposta == item['resposta'].lower():
                print("✅ Correto!")
                acertos += 1
            else:
                print(f"❌ Errado! A resposta correta era: {item['resposta']}")

        pontos_ganhos = acertos * 5
        usuario.acumularPontos(pontos_ganhos)

        print(f"\n🎯 Você acertou {acertos} de {len(trechos)} trechos.")
        print(f"🏆 Pontos ganhos: {pontos_ganhos}")
        print(f"📊 Pontuação total: {usuario.pontos} | Divisão: {usuario.divisao}")

