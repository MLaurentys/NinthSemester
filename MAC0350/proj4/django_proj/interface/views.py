from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from collections import namedtuple
from django.template import loader
from .defines import *
from .forms import crudForm, userForm, profileForm, serviceForm, examForm
from .query_helper import *

def dictfetchall(cursor):
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [dict(zip(columns, row)) for row in cursor.fetchall()]

def create(request):
	if request.method != "POST":
		return HttpResponse(create_not_post)
	cursor = connection.cursor()
	page = None
	print(request.POST['table'])
	print(request.POST['table'] == usuario)
	if request.POST['table'] == usuario:
		print("ENTROU 1")
		form = userForm(request.POST)
		try:
			user_id = int(form['id_usuario'].value())
			person_id = int(form['id_pessoa'].value())
			tutor_id = int(form['id_tutor'].value())
		except:
			page = render(request, create_html_path, {"operation": "create", "table": "Usuario", "form": userForm(), "message": "ERRO: id inválido"})
		cursor.execute(build_check_str('usuario', {'id_usuario':form['id_usuario'].value()}))
		user_result = dictfetchall(cursor)
		cursor.execute(build_check_str('pessoa', {'id_pessoa':form['id_pessoa'].value()}))
		person_result = dictfetchall(cursor)
		if not user_result[0]['count'] and person_result[0]['count']:
			cursor.execute(build_insert_query('usuario', ['id_usuario', 'area_de_pesquisa', 'instituicao', 'id_tutor', 'login', 'senha'], [form['id_usuario'].value(), form['area_de_pesquisa'].value(), form['instituicao'].value(), form['id_tutor'].value(), form['login'].value(), form['senha'].value()]))
			page = render(request, create_html_path, {"operation": "create", "table": "Usuario", "form": userForm(), "message": create_success})
		else:
			page = render(request, create_html_path, {"operation": "create", "table": "Usuario", "form": userForm(), "message": create_existant_user})
	elif request.POST['table'] == "Perfil":
		form = profileForm(request.POST)
		try:
			profile_id = int(form['id_perfil'].value())
		except:
			page = render(request, create_html_path, {"operation": "create", "table": "Perfil", "form": profileForm(), "message": "ERRO: id inválido"})
		cursor.execute(build_check_str('perfil', {'id_perfil':form['id_perfil'].value()}))
		profile_result = dictfetchall(cursor)
		if not profile_result[0]['count']:
			cursor.execute(build_insert_query('perfil', ['id_perfil', 'codigo', 'tipo'], [form['id_perfil'].value(), form['codigo'].value(), form['tipo'].value()]))
			page = render(request, create_html_path, {"operation": "create", "table": "Perfil", "form": profileForm(), "message": create_success})
		else:
			page = render(request, create_html_path, {"operation": "create", "table": "Perfil", "form": profileForm(), "message": "ERRO: perfil já existente. Você pode VOLTAR e tentar atualizar a tabela."})
	elif request.POST['table'] == "Servico":
		form = serviceForm(request.POST)
		try:
			service_id = int(form['id_servico'].value())
		except:
			return render(request, create_html_path, {"operation": "create", "table": "Servico", "form": serviceForm(), "message": "ERRO: id inválido"})
		cursor.execute(build_check_str('servico', {'id_servico':form['id_servico'].value()}))
		service_result = dictfetchall(cursor)
		if not service_result[0]['count']:
			cursor.execute(build_insert_query('servico', ['id_servico', 'classe', 'nome'], [form['id_servico'].value(), form['classe'].value(), form['nome'].value()]))
			page = render(request, create_html_path, {"operation": "create", "table": "Servico", "form": serviceForm(), "message": "Inserção feita com SUCESSO. Realize outra inserção ou faça uma consulta para conferir."})
		else:
			page = render(request, create_html_path, {"operation": "create", "table": "Servico", "form": serviceForm(), "message": "ERRO: serviço já existente. Você pode VOLTAR e tentar atualizar a tabela."})
	else:
		print("ENTROU 2")
		form = examForm(request.POST)
		try:
			exam_id = int(form['id_exame'].value())
		except:
			page = render(request, create_html_path, {"operation": "create", "table": "Exame", "form": examForm(), "message": "ERRO: id inválido"})
		cursor.execute(build_check_str('exame', {'id_exame':form['id_exame'].value()}))
		exam_result = dictfetchall(cursor)
		if not exam_result[0]['count']:
			cursor.execute(build_insert_query('exame', ['id_exame', 'tipo', 'virus'], [form['id_exame'].value(), form['tipo'].value(), form['virus'].value()]))
			page = render(request, create_html_path, {"operation": "create", "table": "Exame", "form": examForm(), "message": "Inserção feita com SUCESSO. Realize outra inserção ou faça uma consulta para conferir."})
		else:
			page = render(request, create_html_path, {"operation": "create", "table": "Exame", "form": examForm(), "message": "ERRO: exame já existente. Você pode VOLTAR e tentar atualizar a tabela."})
	cursor.close()
	return page
def index(request):
	if request.method == "POST":
		crudform = crudForm(request.POST)
		operation = crudform['operation'].value()
		table = crudform['table'].value()
		if operation == 'create':
			if table == 'Usuario':
				form = userForm()
			elif table == 'Perfil':
				form = profileForm()
			elif table == 'Servico':
				form = serviceForm()
			else:
				form = examForm()
			return render(request, create_html_path, {"operation": operation, "table": table, "form": form})
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