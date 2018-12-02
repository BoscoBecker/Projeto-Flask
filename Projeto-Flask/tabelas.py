from peewee import Model, CharField

from peewee import SqliteDatabase
db = SqliteDatabase("teste.db")

#from peewee import PostgresqlDatabase
#db = PostgresqlDatabase('teste', user='postgres', password='', host='192.168.99.100', port=5432)

                           
class BaseModel(Model):
    class Meta:
        database = db
        
class postagem(BaseModel):
	titulo = CharField()
	foto_url = CharField(null=True)
	data = CharField()
	