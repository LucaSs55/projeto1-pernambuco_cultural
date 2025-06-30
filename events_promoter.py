import webbrowser
import os
import json
import tkinter
from PIL import Image, ImageTk

class SistemaDeEventos:
    def __init__(self,arquivo_externo_eventos = "eventos.json"):
        """
        Inicializa o sistema de eventos e carrega os dadoquivo JSON.

        Parâmetrosquivo_externo_eventos (str): Caminho paquivo JSON com os dados dos eventos.
        """
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.arquivo = os.path.join(base_path,arquivo_externo_eventos)
        self.eventos = self.carregar_eventos(self.arquivo)
        self.filtros = {"data":"","cidade":"","busca":""}
        
    def carregar_eventos(self,caminho):
        """
        Carrega os eventoquivo JSON

        Retorna:
            list: Lista de eventos
        """
        try:
            with open(caminho,"r",encoding= "utf-8") as f: #Abre o arquivo de eventos no modo de leitura para trazer as strings salvas dentro do arquivo
                return json.load(f)
            
        except FileNotFoundError:
            tkinter.messagebox.showerror("Errquivo não encontrado.")
            return []
        
        except json.JSONDecodeError:
            tkinter.messagebox.showerror("Errquivo JSON inválido ou não encontrado.")
            return []
    #Cria os filtros por data,cidade e palavra chave para buscar eventos regionais específicos
    def criar_filtros(self):
        tkinter.Label(self.frame_filtros, text="Data:", bg="#003366",fg="white", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5)
        self.entry_data = tkinter.Entry(self.frame_filtros)
        self.entry_data.grid(row=0, column=1, padx=5)

        tkinter.Label(self.frame_filtros, text="Cidade:", bg="#003366",fg="white", font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=5)
        self.entry_cidade = tkinter.Entry(self.frame_filtros)
        self.entry_cidade.grid(row=0, column=3, padx=5)

        tkinter.Label(self.frame_filtros, text="Busca (palavra-chave):", bg="#003366",fg="white", font=("Helvetica", 10, "bold")).grid(row=0, column=4, padx=5)
        self.entry_busca = tkinter.Entry(self.frame_filtros, width=25)
        self.entry_busca.grid(row=0, column=5, padx=5)

        tkinter.Button(self.frame_filtros, text="Filtrar", command=self.aplicar_filtros, bg="green", fg="white").grid(row=0, column=6, padx=10)
        tkinter.Button(self.frame_filtros, text="Limpar", command=self.limpar_filtros, bg="gray", fg="white").grid(row=0, column=7, padx=5)
    #Traz o determinado evento a partir do que é digitado no input de filtro e previne possíveis erros de usuário
    def aplicar_filtros(self):
        self.filtros["data"] = self.entry_data.get().strip().lower()
        self.filtros["cidade"] = self.entry_cidade.get().strip().lower()
        self.filtros["busca"] = self.entry_busca.get().strip().lower()
        self.criar_interface()
    #Faz a limpeza depois que algo é digitado no filtro
    def limpar_filtros(self):
        self.entry_data.delete(0, tkinter.END)
        self.entry_cidade.delete(0, tkinter.END)
        self.entry_busca.delete(0, tkinter.END)
        self.filtros = {"data": "", "cidade": "", "busca": ""}
        self.criar_interface()

    def criar_interface(self):
        for widget in self.frame_resultado.winfo_children():
            widget.destroy()

        eventos_filtrados = self.filtrar_eventos()

        if not eventos_filtrados:
            tkinter.Label(self.frame_resultado, text="Nenhum evento encontrado.", bg="white", font=("Helvetica", 14)).pack(pady=20)
            return

        for evento in eventos_filtrados:
            self.adicionar_evento(evento)
    
    def filtrar_eventos(self):
        resultado = []
        for evento in self.eventos:
            data_ok = self.filtros["data"] in evento["data"].lower()
            cidade_ok = self.filtros["cidade"] in evento.get("cidade", "").lower()
            busca_ok = self.filtros["busca"] in evento["titulo"].lower() or self.filtros["busca"] in evento["descricao"].lower()

            if all([
                self.filtros["data"] == "" or data_ok,
                self.filtros["cidade"] == "" or cidade_ok,
                self.filtros["busca"] == "" or busca_ok
            ]):
                resultado.append(evento)
        return resultado
    
    def adicionar_evento(self, evento):
        frame = tkinter.Frame(self.frame_resultado, bd=2, relief="ridge", bg="#f4f4f4", width=750, height=200)
        frame.pack_propagate(False)
        frame.pack(pady=10)

        container = tkinter.Frame(frame, bg="#f4f4f4")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        imagem_relativa = evento.get("imagem", "")
        imagem_path = os.path.join(os.path.dirname(self.arquivo), imagem_relativa)

        if imagem_relativa and os.path.isfile(imagem_path):
            try:
                imagem = Image.open(imagem_path)
                imagem = imagem.resize((180, 130))
                foto = ImageTk.PhotoImage(imagem)

                img_label = tkinter.Label(container, image=foto, bg="#f4f4f4")
                img_label.image = foto
                img_label.grid(row=0, column=0, rowspan=4, padx=10, pady=5)
            except Exception as e:
                print(f"\033[31m[ERRO] Falha ao abrir imagem: {e} \033[m")
        else:
            print(f"[AVISO] Imagem não encontrada: {imagem_relativa}")

        text_frame = tkinter.Frame(container, bg="#f4f4f4")
        text_frame.grid(row=0, column=1, sticky="nw")

        tkinter.Label(text_frame, text=evento["titulo"], font=("Helvetica", 14, "bold"), bg="#f4f4f4", fg="#003366").pack(anchor="w")
        tkinter.Label(text_frame, text=f"Data: {evento['data']} | Cidade: {evento['cidade']}", bg="#f4f4f4", font=("Helvetica", 11)).pack(anchor="w", pady=2)
        tkinter.Label(text_frame, text=f"Descrição: {evento['descricao']}", wraplength=520, justify="left", bg="#f4f4f4").pack(anchor="w", pady=2)

        tkinter.Button(text_frame, text="Abrir link do evento", bg="#003366", fg="white",
                       command=lambda url=evento["link"]: webbrowser.open(url)).pack(anchor="w", pady=5)
        
    #Centraliza horizontalmente os cards
    def centralizar_eventos(self):
        frame_largura = 750
        canvas_largura = self.canvas.winfo_width()
        x_centro = (canvas_largura - frame_largura) // 2
        self.canvas.coords(self.canvas_window_id, x_centro, 0)
        
    def executar_interface_de_eventos(self):
        self.janela = tkinter.Tk()
        self.janela.title("Divulgador de Eventos Regionais")
        self.janela.geometry("850x750")
        self.janela.configure(bg = "#003366")

        # Parâmetros iniciais
        largura_final = 850
        altura_final = 750
        largura, altura = 200, 100  # tamanho inicial da janela
        x = int((self.janela.winfo_screenwidth() - largura_final) / 2)
        y = int((self.janela.winfo_screenheight() - altura_final) / 2)

        # Animação de crescimento
        for i in range(20):
            largura_anim = largura + int((largura_final - largura) * (i + 1) / 20)
            altura_anim = altura + int((altura_final - altura) * (i + 1) / 20)
            self.janela.geometry(f"{largura_anim}x{altura_anim}+{x}+{y}")
            self.janela.update()
            self.janela.after(10)  # Delay para suavizar a transição para interface gráfica

        # Define o tamanho final após a animação
        self.janela.geometry(f"{largura_final}x{altura_final}+{x}+{y}")


        self.frame_filtros = tkinter.Frame(self.janela,bg = "#003366")
        self.frame_filtros.pack(pady=10)
 
        self.canvas = tkinter.Canvas(self.janela, bg="#003366", highlightthickness=0)
        self.scrollbar = tkinter.Scrollbar(self.janela, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

       
        self.frame_resultado = tkinter.Frame(self.canvas, bg="#003366")
       
        self.canvas_window_id = self.canvas.create_window((0, 0), window=self.frame_resultado, anchor="n")

        self.frame_resultado.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.centralizar_eventos())

        #chamada das principais funções para ativar a interface gráfica

        self.criar_filtros()
        self.criar_interface()
        self.janela.mainloop()
