import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO

class BuscadorLivros:
    def __init__(self, api_key=None):
        """
        Inicializa a instância do buscador com uma chave de API do Google Books.

        Parâmetros:
        - api_key (str, opcional): Chave de API do Google Books. Se não for fornecida, 
          as requisições serão feitas de forma anônima, com limite reduzido de requisições.
        """
        self.api_key = api_key

    def executarBuscadorLivros(self):
        """
        Executa a interface gráfica do buscador de livros com campos de filtro 
        por título, autor e ano, além de haver a rolagem vertical dentro da interface.
        """
        self.janela = tk.Tk()
        self.janela.title("Buscador Google Books")
        self.janela.geometry("900x700")
        self.janela.configure(bg="#727070")

        # Campos de busca
        frame_busca = tk.Frame(self.janela, bg="#727070")
        frame_busca.pack(pady=10)

        tk.Label(frame_busca, text="Título:", bg="#727070").grid(row=0, column=0, padx=5)
        self.entry_titulo = tk.Entry(frame_busca, width=30); self.entry_titulo.grid(row=0, column=1)

        tk.Label(frame_busca, text="Autor:", bg="#727070").grid(row=0, column=2, padx=5)
        self.entry_autor = tk.Entry(frame_busca, width=30); self.entry_autor.grid(row=0, column=3)

        tk.Label(frame_busca, text="Ano:", bg="#727070").grid(row=0, column=4, padx=5)
        self.entry_ano = tk.Entry(frame_busca, width=10); self.entry_ano.grid(row=0, column=5)

        tk.Button(frame_busca, text="Buscar Livros", command=self.buscadorFiltros, bg="green", fg="white")\
            .grid(row=0, column=6, padx=10)

        # Container com scroll
        self.canvas = tk.Canvas(self.janela, bg="#727070", highlightthickness=0)
        sb = tk.Scrollbar(self.janela, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.frame_resultado = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0,0), window=self.frame_resultado, anchor="nw")
        self.frame_resultado.bind("<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.janela.mainloop()

    def buscadorFiltros(self):
        """
        Realiza a busca de livros na API do Google Books com base nos filtros
        preenchidos (título e/ou autor). Se o campo de ano for preenchido, 
        aplica filtro adicional nos resultados.
        
        Exibe uma mensagem de erro ou alerta caso a busca falhe ou os campos 
        obrigatórios não sejam preenchidos.
        """
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        ano = self.entry_ano.get().strip()
        query = []

        if titulo:
            query.append(f'intitle:{titulo}')
        if autor:
            query.append(f'inauthor:{autor}')
        if not query:
            messagebox.showwarning("Aviso", "Preencha título e/ou autor para buscadorFiltros.")
            return

        q = "+".join(query)
        params = {"q": q, "maxResults": 20}
        if self.api_key:
            params["key"] = self.api_key

        endpoint_api = "https://www.googleapis.com/books/v1/volumes" #URL que faz a solicitação dos serviços da Api Google books
        try:
            resp = requests.get(endpoint_api, params=params, timeout=5)
            resp.raise_for_status()
            itens = resp.json().get("items", [])
            # Filtrar por ano se solicitado
            if ano:
                itens = [v for v in itens
                         if "volumeInfo" in v and ano in v["volumeInfo"].get("publishedDate", "")]
            self.exibirResultadosBusca(itens)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na busca: {e}")

    def exibirResultadosBusca(self, volumes):
        """
        Exibe os resultados da busca de livros na interface gráfica.

        Parâmetros:
        - volumes (list): Lista de dicionários retornados pela API do Google Books,
          contendo informações dos livros como título, autor, data e imagem que são utilizados e exibidos na interface do buscador.
        
        Se nenhum resultado for encontrado, exibe uma saída informativa.
        """
        for w in self.frame_resultado.winfo_children():
            w.destroy()

        if not volumes:
            tk.Label(self.frame_resultado, text="Nenhum resultado encontrado.",
                     bg="white", font=("Arial",12)).pack(pady=20)
            return

        for v in volumes:
            vi = v.get("volumeInfo", {})
            title = vi.get("title", "Sem título")
            authors = ", ".join(vi.get("authors", ["Autor desconhecido"]))
            pub_date = vi.get("publishedDate", "Desconhecido")
            image_url = vi.get("imageLinks", {}).get("thumbnail")
            reader_link = v.get("accessInfo", {}).get("webReaderLink")

            card = tk.Frame(self.frame_resultado, bd=1, relief="solid", bg="#f0f0f0")
            card.pack(fill="x", padx=10, pady=6)

            # Link da imagem
            if image_url:
                try:
                    data = requests.get(image_url, timeout=3).content
                    img = Image.open(BytesIO(data)).resize((80, 120))
                    photo = ImageTk.PhotoImage(img)
                    lbl = tk.Label(card, image=photo, bg="#f0f0f0")
                    lbl.image = photo
                    lbl.pack(side="left", padx=10, pady=10)
                except:
                    pass

            info = tk.Frame(card, bg="#f0f0f0")
            info.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            tk.Label(info, text=f"Título: {title}", font=("Arial",14,"bold"), fg="blue", bg="#f0f0f0").pack(anchor="w")
            tk.Label(info, text=f"Autor(es): {authors}", font=("Arial",12), bg="#f0f0f0").pack(anchor="w")
            tk.Label(info, text=f"Ano: {pub_date}", font=("Arial",12), bg="#f0f0f0").pack(anchor="w")

            if reader_link:
                tk.Button(info, text="Ler no Google Books", bg="#0066cc", fg="white",
                          command=lambda u=reader_link: webbrowser.open(u)).pack(anchor="e", pady=5)