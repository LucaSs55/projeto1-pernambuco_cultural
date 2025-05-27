# Pernambuco Cultural    

## Descrição do Projeto:
Pernambuco cultural é um projeto que visa propiciar aos seus usuários maior exposição e contato com eventos regionais de Pernambuco por meio de um divulgador de eventos e também incentivar o acesso a obras literárias de caráter regional e universal por meio de um sistema baseado na gamificação, por meio de jogos e testes de conhecimento acerca de obras literárias, assim dinamizando o processo de aprendizado, através da leitura e propiciando uma maior exposição da riqueza cultural Pernambucana para o mundo.

## Recursos e funcionalidades:

- **Cadastro de Nome, Email e Senha:** Permite a criação e o salvamento dos dados de usuário após algumas validações de dados em formato de dicionário dentro de uma lista no arquivo usuarios.json.
- **Atualizar dados de usuário:** Após uma validação de Email e Senha, mostra um menu com as opções para atualização dos dados de usuário.
- **Login de usuário:** Permite que o usuário utilizando os dados previamente cadastrados acesse um novo menu com diversas funcionalidades
- **Deletar dados de usuário:** Após uma validação de Email e Senha, pede uma confirmação para continuidade da operação e por fim deleta um usuário.
- **Ver dados de usuário:** Após uma validação de Email e Senha com base em dados já salvos no arquivo de usuários, permite a vericação dos dados por parte do usuário.

- **Validação de Email:** Verifica se o email tem os domínios(gmail.com, hotmail.com, yahoo.com) e se o espaço de preenchimento do email está vazio.
- **Validação de Senha:** Verifica se a senha possui pelo menos 8 caracteres, e 1 letra maiúscula[A-Z], 1 número[0-9], e 1 caractere especial.
- **Validação de dados salvos na lista de usuários:** Faz a verificação dos dados de usuário salvos no arquivo de usuários para a efetivação de certas operações no código.
- **Divulgador de Eventos Culturais:** Permite a visualização dos eventos culturais disponíveis no Estado com informação de Nome, Data, Descrição e um link externo com direcionamento para o site oficial do Evento.
  
## Tecnologias Utilizadas no código:
- Python 3
- **Biblioteca:**
  - `os`Permite a interação do terminal com a interface do sistema operacional`
  - `re` Serve para fazer manipulação das expressões regulares durante a validação de senha.
  -`Json` Serve para modelar e manipular os dados de usuário no formato json.
  - `Webbrowser` Permite abrir o link dos eventos pelo terminal python.
## Como executar o projeto:
- **É preciso que o python 3 esteja baixado no sistema.**
  
## Estrutura do Projeto:
- usuarios.py: Arquivo de armazenamento de usuários.
- eventos.py: Arquivo de armazenamento de eventos, adicionados manualmente.
