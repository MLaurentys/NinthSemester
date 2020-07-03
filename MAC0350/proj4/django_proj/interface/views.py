from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from collections import namedtuple
from django.template import loader

from .forms import *
from .query_helper import *

def dictfetchall(cursor):
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [dict(zip(columns, row)) for row in cursor.fetchall()]

def test2(request):
	with connection.cursor() as cursor:
		get_columns(cursor, 'usuario')
	return HttpResponse("<p><a href='/'>INÍCIO</a></p><p>Nenhuma inserção foi solicitada. Volte ao início da interface.</p>")

def test3(request):
	check_query = build_check_str('exame', {'id_exame':'999'})
	delete_query = build_delete_query('exame', {'id_exame':'999'})
	data_exists = False
	with connection.cursor() as cursor:
		cursor.execute(check_query)
		result = dictfetchall(cursor)
		if result[0]['count']:
			data_exists = True
		print(result)
		if data_exists:
			cursor.execute(delete_query)
	if data_exists:
		response = HttpResponse("Data used to exist!")
	else:
		response = HttpResponse("Data did not exist!")
	return response


def create(request):
	if request.method != "POST":
		return HttpResponse("<p><a href='/'>INÍCIO</a></p><p>Nenhuma inserção foi solicitada. Volte ao início da interface.</p>")
	if request.POST['table'] == "Usuario":
		form = userForm(request.POST)
		with connection.cursor() as cursor:
			cursor.execute(build_check_str('usuario', {'cpf':form['CPF'].value()}))
			result = dictfetchall(cursor)
			if not result[0]['count']:
				cursor.execute(build_insert_query('usuario', ['id_usuario', 'cpf', 'nome', 'data_de_nascimento', 'area de pesquisa', 'instituicao', 'id_tutor', 'login', 'senha', 'id_pessoa'], []))
				return HttpResponse("<p><a href='/'>REALIZAR NOVO CRUD</a></p><p>Inserção feita com sucesso na tabela Usuário. Você pode realizar uma consulta para conferir.</p>")
			else:
				return HttpResponse("<p><a href='/'>REALIZAR NOVO CRUD</a></p><p>Dado já existe na tabela Usuário. Você pode tentar atualizá-lo, se quiser.</p>")
	if request.POST['table'] == "Perfil":
		form = profileForm(request.POST)
		with connection.cursor() as cursor:
			cursor.execute(build_check_str('perfil', {'codigo':str(form['codigo'].value())}))
			result = dictfetchall(cursor)
			if not result[0]['count']:
				cursor.execute(build_insert_query('perfil', ['codigo', 'tipo'], [str(form['codigo'].value()), str(form['tipo'].value())]))
				return HttpResponse("<p><a href='/'>REALIZAR NOVO CRUD</a></p><p>Inserção feita com sucesso na tabela Perfil. Você pode realizar uma consulta para conferir.</p>")
			else:
				return HttpResponse("<p><a href='/'>REALIZAR NOVO CRUD</a></p><p>Dado já existe na tabela Perfil. Você pode tentar atualizá-lo, se quiser.</p>")
	else:
		return HttpResponse("<p><a href='/'>REALIZAR NOVO CRUD</a></p><p>Inserção feita com sucesso na tabela Exame.</p>")
	cursor.close()

def index(request):
	if request.method == "POST":
		crudform = crudForm(request.POST)
		operation = crudform['operation'].value()
		table = crudform['table'].value()
		if operation == 'create':
			cursor2 = connection.cursor()
			columns = get_columns(cursor2, table)
			form = myForm(columns)
			cursor2.close()
			# for a in dir(form):
			# 	if not a.startswith('__'):
			# 		print(a)
			return render(request, 'interface/create.html',
					{"operation": operation, "table": table, "form": form})
		elif operation == 'read':
			if table == 'Usuario':
				with connection.cursor() as cursor:
					cursor.execute('SELECT * FROM usuario')
					user_table = dictfetchall(cursor)
					cursor.execute('SELECT * FROM pessoa')
					person_table = dictfetchall(cursor)
				context = {'user_table': user_table, 'person_table': person_table}
			elif table == 'Perfil':
				with connection.cursor() as cursor:
					cursor.execute('SELECT * FROM perfil')
					profile_table = dictfetchall(cursor)
				context = {'profile_table': profile_table,}
			elif table == 'Servico':
				with connection.cursor() as cursor:
					cursor.execute('SELECT * FROM servico')
					service_table = dictfetchall(cursor)
				context = {'service_table': service_table,}
			else:
				with connection.cursor() as cursor:
					cursor.execute('SELECT * FROM exame')
					exam_table = dictfetchall(cursor)
				context = {'exam_table': exam_table,}	
			template = loader.get_template('interface/read.html')
			return HttpResponse(template.render(context, request))
		elif operation == 'update':	
			# Mostar os ids (ou linhas inteiras) disponíveis, o usuário seleciona uma e atualiza... ?
			return HttpResponse("<p><a href='/'>REALIZAR NOVO CRUD</a></p><p>Imagine que você pode escolher qual linha você quer ATUALIZAR!</p>")
		else:
			# Mostar os ids (ou linhas inteiras) disponíveis, o usuário seleciona uma e deleta... ?
			return HttpResponse("<p><a href='/'>REALIZAR NOVO CRUD</a></p><p>Imagine que você pode escolher qual linha você quer DELETAR!</p>")
	else:
		crudform = crudForm()
	return render(request, 'interface/index.html', {"crudform": crudform})
