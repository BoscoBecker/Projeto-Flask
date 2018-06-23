#encoding: utf-8
import os
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from playhouse.shortcuts import  model_to_dict
from tabelas import postagem

app = Flask(__name__)

def processa_upload(name_do_input):
	if name_do_input not in request.files:
		return ""
	else:
		arquivo_temporario = request.files[name_do_input]
		nome_do_arquivo = secure_filename(arquivo_temporario.filename)
		caminho_do_arquivo = "static/uploads/" + nome_do_arquivo
		arquivo_temporario.save(caminho_do_arquivo)
		url_do_arquivo = "/"+caminho_do_arquivo
		return url_do_arquivo

@app.route("/")
def index():
	postagems = postagem.select().order_by(postagem.titulo)
	return render_template("index.html", lista_de_postagem = postagems)
	
		
@app.route("/remover/<id>/")
def remover(id):
	postagems = postagem.get_by_id(id)
	# [:1] remove o primeiro caracter da url, ou seja, remove o "/" inicial
	caminho_foto = postagems.foto_url[1:] 
	# deleta foto do sistema de arquivo
	os.unlink(caminho_foto)
	# deleta do banco
	postagems.delete().where(postagem.id==id).execute()
	return redirect("/")

	
@app.route("/cadastrar/",methods=["GET","POST"])
def cadastrar():
	if request.method=="POST":
		try:
			p = postagem()
			p.titulo = request.form['titulo'] 
			p.data = request.form['data']
			p.foto_url = processa_upload("foto_url")
			p.save()
			return redirect("/")
		except Exception as error:
			return render_template("cadastrar.html", msg_error = error,	form = request.form.to_dict())
	else:
		return render_template("cadastrar.html", form={})

		
@app.route("/editar/<id>/",methods=["GET","POST"])
def atualizar(id):
	if request.method=="POST":
		try:
			if request.form['titulo'] == "":
				raise Exception(u"titulo não informado!")	
			p = postagem.get_by_id(id)
			p.titulo = request.form['titulo'] 
			p.data = request.form['data']
			p.foto_url = processa_upload("foto_url")
			p.save()
			return redirect("/")
		except Exception as error:
			return render_template("editar.html", id = id,  msg_error = error, form = request.form.to_dict())
	else:
		p = postagem.get(id)
		return render_template("editar.html",id = id, form=model_to_dict(p))