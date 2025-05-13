from fastapi import FastAPI, HTTPException
from models import Livro, Leitor, Emprestimo, Biblioteca
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

app = FastAPI()

livros:List[Livro]=[]
leitores:List[Leitor]=[]
emprestimos:List[Emprestimo]=[]
devolucoes: List[Emprestimo] = []

@app.post("/livros/", response_model=Livro)
def cadastrar_livro(livro: Livro):
    livros.append(livro)
    print(f"Log message - Livros[POST]: Livro cadastrado: {livro.titulo}.")
    return livro


@app.get("/livros/", response_model=List[Livro])
def listar_livros(titulo: Optional[str] = None):
    resultado = []
    if titulo:
        for livro in livros:
            if livro.titulo.lower() == titulo.lower():
                resultado.append(livro)
    else:
        for livro in livros:
            if livro.disponivel:
                resultado.append(livro)

    if resultado:
        print("Log message - Livros[GET]: Listar Livros executado com sucesso.")
        return resultado
    print("Log message - Livros[GET]: Listar livros falhou.")
    raise HTTPException(status_code=404, detail="Livros não encontrados ou indisponíveis.")
        

@app.post("/leitores/", response_model=Leitor)
def cadastrar_leitor(leitor: Leitor):
    leitores.append(leitor)
    print(f"Log message - Leitores[POST]: Leitor cadastrado: {leitor.nome}.")
    return leitor


@app.get("/leitores/", response_model=List[Leitor])
def listar_leitores(nome: Optional[str] = None):
    resultado = []

    if nome:
        for leitor in leitores:
            if leitor.nome.lower() == nome.lower():
                resultado.append(leitor)
    else:
        for leitor in leitores:
            resultado.append(leitor)

    if resultado:
        print("Log message - Leitores[GET]: Listar Leitores executado com sucesso.")
        return resultado

    print("Log message - Leitores[GET]: Listar Leitores falhou.")
    raise HTTPException(status_code=404, detail="Leitores não encontrados.")


@app.post("/emprestimos/",response_model=Emprestimo) #Cadastrar empréstimo
def cadastrar_emprestimo(emprestimo:Emprestimo):
    usuario = None
    for usr in leitores:
        if usr.uuid == emprestimo.usuario:
            usuario = usr
            break

    if not usuario:
        print("Log message - Empréstimo [POST]: Usuário inexistente.")
        raise HTTPException(status_code=404, detail="O usuário não existe.")

    livro = None
    for liv in livros:
        if liv.uuid == emprestimo.livro:
            livro = liv
            break

    if not livro:
        print("Log message - Empréstimo[POST]: Livro inexistente.")
        raise HTTPException(status_code=404, detail="O livro não existe.")   

    if not livro.disponivel:
        print("Log message - Empréstimo[POST]: Livro indisponível.")
        raise HTTPException(status_code=404, detail="O livro não está disponível.")
 
    else:
        livro.disponivel = False
        usuario.livros.append(livro.uuid)


    novo_emprestimo = Emprestimo(
        id=uuid4(),
        livro=livro.uuid,
        usuario=usuario.uuid,
        dataEmprestimo=datetime.now(),
        dataDevolucao=None
    )

    emprestimos.append(emprestimo)
    print(f"Log message - Empréstimo[POST]: Livro '{livro.titulo}' para {usuario.nome}")
    return novo_emprestimo


@app.post("/devolucoes/", response_model=Emprestimo)
def registrar_devolucao(usuario_id: UUID, livro_id: UUID):
    emprestimo = None

    # Verifica se existe um empréstimo ativo (sem dataDevolucao)
    for e in emprestimos:
        if e.usuario == usuario_id and e.livro == livro_id and e.dataDevolucao is None:
            emprestimo = e
            break

    if not emprestimo:
        print("Log message - Devolução[POST]: Empréstimo não encontrado ou já devolvido.")
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado ou já devolvido.")

    # Atualiza livro para disponível
    for livro in livros:
        if livro.uuid == livro_id:
            livro.disponivel = True
            break

    # Remove livro da lista do usuário
    for leitor in leitores:
        if leitor.uuid == usuario_id:
            if livro_id in leitor.livros:
                leitor.livros.remove(livro_id)
            break

    emprestimo.dataDevolucao = datetime.now()
    devolucoes.append(emprestimo)

    print("Log message - Devolução[POST]: Devolução registrada com sucesso.")
    return emprestimo


@app.get("/biblioteca/", response_model=Biblioteca)
def listar_biblioteca():
        print("Log message - Biblioteca[GET]: Biblioteca encontrada.")
        
        return Biblioteca(
        usuarios=leitores,
        livros=livros,
        emprestimos=emprestimos,
        devolucoes=devolucoes
    )