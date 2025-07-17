import tkinter 
import tkinter.ttk
import requests
from PIL import Image, ImageTk
import webbrowser
import io

class BuscadorLivros:
    def __init__(self):
        self.links = {}
        self.imagens = []

    def executarInterfaceBuscador(self):
        self.janela = tkinter.Tk()
        self.janela.title("Buscador de Livros - Open Library")
        self.janela.geometry("950x800")
        self.janela.configure(bg="#f0f0f0")

        tituloPrincipal = tkinter.Label(self.janela, text="Buscador de Livros", 
                                font=("Arial", 16, "bold"), bg="#f0f0f0")
        tituloPrincipal.pack(pady=10)

        # Substituindo o Notebook por Frame simples
        self.aba_busca = tkinter.Frame(self.janela, bg="#f0f0f0")
        self.aba_busca.pack(fill="both", expand=True)

        self.criarFiltros(self.aba_busca)
        self.criarAreaResultados(self.aba_busca)

        self.janela.mainloop()

    def criarFiltros(self, parent):
        frame_filtros = tkinter.Frame(parent, bg="#f0f0f0")
        frame_filtros.pack(pady=10)

        tkinter.Label(frame_filtros, text="Título:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        self.entry_titulo = tkinter.ttk.Entry(frame_filtros, width=25)
        self.entry_titulo.grid(row=0, column=1, padx=5)

        tkinter.Label(frame_filtros, text="Autor:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
        self.entry_autor = tkinter.ttk.Entry(frame_filtros, width=25)
        self.entry_autor.grid(row=0, column=3, padx=5)

        tkinter.Label(frame_filtros, text="Ano:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5)
        self.entry_ano = tkinter.ttk.Entry(frame_filtros, width=10)
        self.entry_ano.grid(row=0, column=5, padx=5)

        tkinter.ttk.Button(frame_filtros, text="🔍 Buscar", command=self.buscar_livros).grid(row=0, column=6, padx=10)
        tkinter.ttk.Button(frame_filtros, text="🧹 Limpar", command=self.limpar_filtros).grid(row=0, column=7)

    def criarAreaResultados(self, parent):
        self.canvas = tkinter.Canvas(parent, bg="#ffffff", width=910, height=600)
        self.scroll_y = tkinter.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        
        # Frame com largura fixa
        self.frame_resultados = tkinter.Frame(self.canvas, bg="#ffffff", width=850)

        # Define o frame com largura fixa 
        self.canvas_window_id = self.canvas.create_window((0, 0), window=self.frame_resultados, anchor="n", width=750)
        
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.frame_resultados.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.centralizar_resultados())

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")
    
    def centralizar_resultados(self):
        canvas_largura = self.canvas.winfo_width()
        frame_largura = 750  # largura definida acima
        x_centro = (canvas_largura - frame_largura) // 2
        self.canvas.coords(self.canvas_window_id, x_centro, 0)

    def limpar_filtros(self):
        self.entry_titulo.delete(0, tkinter.END)
        self.entry_autor.delete(0, tkinter.END)
        self.entry_ano.delete(0, tkinter.END)
        for widget in self.frame_resultados.winfo_children():
            widget.destroy()

    def buscar_livros(self):
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        ano = self.entry_ano.get().strip()

        for widget in self.frame_resultados.winfo_children():
            widget.destroy()
        self.links.clear()
        self.imagens.clear()

        if not titulo and not autor and not ano:
            tkinter.Label(self.frame_resultados, text="⚠️ Digite pelo menos um critério de busca.", bg="#D10D0D").pack(pady=20)
            return

        query_parts = []
        if titulo: query_parts.append(titulo)
        if autor: query_parts.append(f"author:{autor}")
        if ano: query_parts.append(f"year:{ano}")
        query_parts.append("has_fulltext:true")  #Exibe apenas os livros com link para download

        query = " ".join(query_parts)
        url = "https://openlibrary.org/search.json"
        params = {"q": query, "limit": 15}

        try:
            resposta = requests.get(url, params=params)
            dados = resposta.json()
        except Exception as e:
            tkinter.Label(self.frame_resultados, text=f"Erro: {e}", bg="#ffffff").pack()
            return

        livros = dados.get("docs", [])
        livros_filtrados = [livro for livro in livros if livro.get("has_fulltext") and "ia" in livro]

        if not livros_filtrados:
            tkinter.Label(self.frame_resultados, text="Nenhum livro com link de leitura encontrado.", bg="#ffffff").pack()
            return
        

        for livro in livros_filtrados:
            self.exibir_livro(livro)

    def exibir_livro(self, livro):
        frame = tkinter.Frame(self.frame_resultados, bg="white", borderwidth=1, relief="solid", padx=10, pady=10)
        frame.pack(pady=10)
        
        titulo = livro.get("title", "Título não disponível")
        autores = ", ".join(livro.get("author_name", ["Autor desconhecido"]))
        ano = livro.get("first_publish_year", "Data desconhecida")
        sinopse = self.extrair_sinopse(livro)
        ia_id = livro["ia"][0]
        link_leitura = f"https://archive.org/details/{ia_id}"

        capa_img = None
        if "cover_i" in livro:
            cover_id = livro["cover_i"]
            url_capa = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            try:
                img_data = requests.get(url_capa).content
                pil_img = Image.open(io.BytesIO(img_data)).resize((100, 150))
                capa_img = ImageTk.PhotoImage(pil_img)
                self.imagens.append(capa_img)
            except:
                pass

        conteudo = tkinter.Frame(frame, bg="white")
        conteudo.pack(anchor="center", pady=5)
    

        if capa_img:
            tkinter.Label(conteudo, image=capa_img, bg="white").pack(side="left", padx=10)

        texto = f"Título: {titulo}\nAutor(es): {autores}\nAno: {ano}\n\nSinopse: {sinopse}"
        tkinter.Label(conteudo, text=texto, justify="left", bg="white", font=("Arial", 10), wraplength=700).pack(anchor="w")

        tkinter.Button(
            conteudo, text="📖 Acessar Livro", bg="blue", fg="white",
            command=lambda url=link_leitura: webbrowser.open(url)
        ).pack(anchor="w", pady=5)

    def extrair_sinopse(self, livro):
        """Extrai a sinopse do campo first_sentence se existir"""
        sinopse = livro.get("first_sentence")
        if isinstance(sinopse, dict) and "value" in sinopse:
            return sinopse["value"]
        elif isinstance(sinopse, list):
            return sinopse[0]
        elif isinstance(sinopse, str):
            return sinopse
        return "Sinopse não disponível"