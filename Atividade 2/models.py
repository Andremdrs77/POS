from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional

class Livro(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    titulo: str
    autor: str
    ano: int
    disponivel: bool #disponível ou emprestado

class Leitor(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    nome: str
    livros: List[UUID] = []

class Emprestimo(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    usuario: UUID
    livro: UUID
    dataEmprestimo: datetime
    dataDevolucao: Optional[datetime] = None 

class Biblioteca(BaseModel):
    usuarios: List[Leitor] = []
    livros: List[Livro] = []
    emprestimos: List[Emprestimo] = []
    devolucoes: List[Emprestimo] = []
    