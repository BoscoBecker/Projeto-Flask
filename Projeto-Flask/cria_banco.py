
from tabelas import postagem, db

lista_de_postagem = [ postagem, ]

db.connect()
db.create_tables(lista_de_postagem)