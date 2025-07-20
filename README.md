# Pernambuco Cultural    

## 📌Descrição do Projeto:
Pernambuco cultural é um projeto amplo que visa propiciar para os cidadãos de Pernambuco, e do Brasil maior visibilidade ao rico panorama cultural de Pernambuco em seus elementos mais variados, além de propicionar a interação dos futuros usuários do projeto com obras e jogos de cunho artístico literário como uma forma de incentivo ao consumo e a divulgação de tais bens, assim proporcionando maior valorização em âmbito social a tais conteúdos muitas vezes negligenciados no dia a dia.

## 🛠️Recursos e funcionalidades:

- **Cadastro de Nome, Email e Senha:** Permite a criação e o salvamento dos dados de usuário após algumas validações de dados em formato de dicionário dentro de uma lista no arquivo usuarios.json.
- **Atualizar dados de usuário:** Após uma validação de Email e Senha, mostra um menu com as opções para atualização dos dados de usuário.
- **Login de usuário:** Permite que o usuário utilizando os dados previamente cadastrados acesse um novo menu com diversas funcionalidades
- **Deletar dados de usuário:** Após uma validação de Email e Senha, pede uma confirmação para continuidade da operação e por fim deleta um usuário.
- **Ver dados de usuário:** Após uma validação de Email e Senha com base em dados já salvos no arquivo de usuários, permite a vericação dos dados por parte do usuário.

- **Validação de Email:** Verifica se o email tem os domínios(gmail.com, hotmail.com, yahoo.com) e se o espaço de preenchimento do email está vazio.
- **Validação de Senha:** Verifica se a senha possui pelo menos 8 caracteres, e 1 letra maiúscula[A-Z], 1 número[0-9], e 1 caractere especial.
- **Validação de dados salvos na lista de usuários:** Faz a verificação dos dados de usuário salvos no arquivo de usuários para a efetivação de certas operações no código.
- **Divulgador de Eventos Culturais:** Permite a visualização dos eventos culturais disponíveis no Estado com informação de Nome, Data, Descrição e um link externo com direcionamento para o site oficial do Evento.
  
## 💻Tecnologias Utilizadas no código:
- Python 3
- **Bibliotecas:**
  - `os`Permite a interação do terminal com a interface do sistema operacional`
  - `re` Serve para fazer manipulação das expressões regulares durante a validação de senha.
  - `Json` Serve para modelar e manipular os dados de usuário no formato json.
  - `Webbrowser` Permite abrir o link dos eventos pelo terminal python.
  - `pillow` Serve para facilitar a manipulação de imagens trazidas no divulgador de eventos e no buscador de livros.
  - `Io` Possibilita a correta leitura das imagens trazidas pela API utilizada no código.
  - `requests` Facilita o envio de requisições para a API google library utilizada no buscador de livros.
## 🔨 Como executar o projeto:
- **É preciso que o python 3 esteja instalado no sistema na versão 3.12.0**
- **É necessário que as bibliotecas não nativas do python pillow e requests sejam instaladas nas dependências dos sistema**
- **Utilize os respectivos comandos no terminal:**
 ```sh
 pip install pillow
  ```
```sh
pip install requests
```
## 📁Estrutura do Projeto:
- main.py: Arquivo que inicializa o projeto através da chamada das funções e classes principais utilizadas no código.
- user.py: Arquivo com o Crud, e com as operações principais que o usuário pode realizar ao longo do código.
- validations.py: Arquivo com as validações utilizadas nas operações do Crud em user.py.
- games.py: Arquivo com as funções principais relativas aos jogos presentes no código.
- events_promoter.py: Arquivo com o código principal do divulgador de eventos.
- book_search.py: Arquivo com o código principal do Buscador de livros que utiliza a API Google Library.
- usuarios.json: Arquivo de armazenamento em formato json dos dados dos usuários.
- eventos.json: Arquivo de armazenamento em formato json dos dados dos eventos trazidos no divulgador de eventos.
- quiz.json: Arquivo de armazenamento em formato json, que traz as perguntas que são exibidas no quiz presente em games.py.
- quotes.json: Arquivo de armazenamento em formato json, que traz as citações utilizadas no jogo de citações em games.py.
## 📚Fluxogramas do Projeto:
- https://drive.google.com/drive/folders/19kttBrvtWz4mDgYm-UhQ76ITOs4oD630?usp=drive_link
## 🔧 Possíveis melhorias futuras:
- Implementação de interface gráfica para possibilitar uma melhor UX.
- Criação de um chat que permita a interação entre os usuários.
## 🙋‍♂️Colaboradores:
- Lucas Santos | https://github.com/LucaSs55
- Davi Eufrásio | https://github.com/Davi2904efr

## 📄 Licença:
Este projeto está sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.

