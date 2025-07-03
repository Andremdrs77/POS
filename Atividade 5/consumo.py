import requests

URL = 'http://127.0.0.1:8000'

def listar_usuarios():
    pass

def cadastrar_livro(titulo, ano, edicao):
    livro = {
        "titulo":titulo,
        "ano":ano,
        "edicao":edicao
    }
    r = requests.post(f"{URL}/livros", json=livro)
    if r.status_code == 200:
        print(r.text)

def listar_livros():
    r = requests.get(f"{URL}/livros")
    if r.status_code == 200:
        print(r.text)

def listar_livro(titulo):
    r = requests.get(f"{URL}/livros/{titulo}")
    if r.status_code == 200:
        print(r.text)

def excluir_livro(titulo):
    r = requests.delete(f"{URL}/livros/{titulo}")
    if r.status_code == 200:
        print(r.text)

def menu():
    print("1 - Listar Livros")
    print("2 - Listar Livros pelo título")
    print("3 - Cadastrar Livro")
    print("4 - Deletar livro")
    print("5 - Sair")
    return int(input("Escolha uma opção: "))

opcao = menu()
while opcao != 5:
    if opcao == 1:
        listar_livros()
    elif opcao == 2:
        titulo = input("Digite o título do livro: ")
        listar_livro(titulo)
    elif opcao == 3:
        titulo = input("Digite o título do livro: ")
        ano = int(input("Digite o ano do livro: "))
        edicao = int(input("Digite a edição do livro: "))
        cadastrar_livro(titulo, ano, edicao)
    elif opcao == 4:
        titulo = input("Digite o título do livro: ")
        excluir_livro(titulo)
    opcao = menu()
