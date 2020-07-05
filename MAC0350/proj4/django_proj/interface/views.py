from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from collections import namedtuple
from django.template import loader
from .defines import *
from .forms import crudForm, userForm, profileForm, serviceForm, examForm, selectForm
from django import forms
from .query_helper import *
from .functionality_helper import *

def query(request):
	if request.method != "POST":
		return HttpResponse(query_not_post)
	cursor = connection.cursor()
	page = None
	cur_table = request.POST['table']
	if cur_table == table_usuario:
		page = query_user(request, cursor)
	elif cur_table == table_profile:
		page = query_profile(request, cursor)
	elif cur_table == table_service:
		page = query_service(request, cursor)
	else:
		page = query_exam(request, cursor)
	return page

# Wrapper function for update AND select
def update(request):
	if request.method != "POST":
		return HttpResponse(create_not_post)
	cursor = connection.cursor()
	page = None
	cur_table = request.POST['table']
	if cur_table == table_usuario:
		cursor.execute(select_all_pessoa)
		person_table = dictfetchall(cursor)
		form = userForm(request.POST)
		if form['id_tutor'].value() == "":
			cursor.execute(build_update_query('usuario', ['area_de_pesquisa', 'instituicao', 'id_tutor', 'login', 'senha'], [form['area_de_pesquisa'].value(), form['instituicao'].value(), "NULL", form['login'].value(), form['senha'].value()], {'id_usuario':form['id_usuario'].value()}))
			cursor.execute(select_all_usuario)
			user_table = dictfetchall(cursor)
			page = render(request, update_html, {"operation": "update", "table": "Usuario", "form": selectForm(), 'user_table': user_table, 'person_table': person_table, "message": "Atualização feita com SUCESSO. Confira abaixo."})
		elif form['id_tutor'].value() == form['id_usuario'].value():
			cursor.execute(select_all_usuario)
			user_table = dictfetchall(cursor)
			for user in user_table:
				if user['id_usuario'] == int(form['id_usuario'].value()):
					form = userForm(initial={"area_de_pesquisa": user['area_de_pesquisa'], "instituicao": user['instituicao'], "id_tutor": user['id_tutor'], "login": user['login'], "senha": user['senha']})
					form.fields["id_usuario"] = forms.CharField(initial=user['id_usuario'], widget=forms.widgets.HiddenInput())
					form.fields["id_pessoa"] = forms.CharField(initial=user['id_pessoa'], widget=forms.widgets.HiddenInput())
					break
			page = render(request, update_html, {"operation": "update", "table": "Usuario", "form": form, 'user_table': user_table, 'person_table': person_table, "selected_id": True, "message": "ERRO: id_tutor não pode ser igual a id_usuario."})
		else:
			cursor.execute(build_check_str('usuario', {'id_usuario':form['id_tutor'].value()}))
			result = dictfetchall(cursor)
			if result[0]['count']:
				cursor.execute(build_update_query('usuario', ['area_de_pesquisa', 'instituicao', 'id_tutor', 'login', 'senha'], [form['area_de_pesquisa'].value(), form['instituicao'].value(), form['id_tutor'].value(), form['login'].value(), form['senha'].value()], {'id_usuario':form['id_usuario'].value()}))
				cursor.execute(select_all_usuario)
				user_table = dictfetchall(cursor)
				page = render(request, update_html, {"operation": "update", "table": "Usuario", "form": selectForm(), 'user_table': user_table, 'person_table': person_table, "message": "Atualização feita com SUCESSO. Confira abaixo."})
			else:
				cursor.execute(select_all_usuario)
				user_table = dictfetchall(cursor)
				for user in user_table:
					if user['id_usuario'] == int(form['id_usuario'].value()):
						form = userForm(initial={"area_de_pesquisa": user['area_de_pesquisa'], "instituicao": user['instituicao'], "id_tutor": user['id_tutor'], "login": user['login'], "senha": user['senha']})
						form.fields["id_usuario"] = forms.CharField(initial=user['id_usuario'], widget=forms.widgets.HiddenInput())
						form.fields["id_pessoa"] = forms.CharField(initial=user['id_pessoa'], widget=forms.widgets.HiddenInput())
						break
				page = render(request, update_html, {"operation": "update", "table": "Usuario", "form": form, 'user_table': user_table, 'person_table': person_table, "selected_id": True, "message": "ERRO: id_tutor colocado não existe."})
	elif cur_table == table_profile:
		form = profileForm(request.POST)			
		cursor.execute(build_update_query('perfil', ['codigo', 'tipo'], [form['codigo'].value(), form['tipo'].value()], {'id_perfil':form['id_perfil'].value()}))
		cursor.execute(select_all_profile)
		profile_table = dictfetchall(cursor)
		page = render(request, update_html, {"operation": "update", "table": "Perfil", "form": selectForm(), 'profile_table': profile_table, "message": "Atualização feita com SUCESSO. Confira abaixo."})
	elif cur_table == table_service:
		form = serviceForm(request.POST)			
		cursor.execute(build_update_query('servico', ['classe', 'nome'], [form['classe'].value(), form['nome'].value()], {'id_servico':form['id_servico'].value()}))
		cursor.execute(select_all_service)
		service_table = dictfetchall(cursor)
		page = render(request, update_html, {"operation": "update", "table": "Servico", "form": selectForm(), 'service_table': service_table, "message": "Atualização feita com SUCESSO. Confira abaixo."})
	else: # request.POST['table'] == exame
		form = examForm(request.POST)
		cursor.execute(build_update_query('exame', ['tipo', 'virus'], [form['tipo'].value(), form['virus'].value()], {'id_exame':form['id_exame'].value()}))
		cursor.execute(select_all_exam)
		exam_table = dictfetchall(cursor)
		page = render(request, update_html, {"operation": "update", "table": "Exame", "form": selectForm(), 'exam_table': exam_table, "message": "Atualização feita com SUCESSO. Confira abaixo."})
	cursor.close()
	return page

def delete(request):
	if request.method != "POST":
		return HttpResponse(delete_not_post)
	cursor = connection.cursor()
	page = None
	cur_table = request.POST['table']
	if cur_table == table_usuario:
		page = delete_user(request, cursor)
	elif cur_table == perfil:
		page = delete_profile(request, cursor)
	elif cur_table == servico:
		page = delete_service(request, cursor)
	else:
		page = delete_exam(request, cursor)
	cursor.close()
	return page

def create(request):
	if request.method != "POST":
		return HttpResponse(create_not_post)
	cursor = connection.cursor()
	page = None
	cur_table = request.POST['table']
	if cur_table == table_usuario:
		page = insert_user(request, cursor)
	elif cur_table == table_profile:
		page = insert_profile(request, cursor)
	elif cur_table == table_service:
		page = insert_service(request, cursor)
	else:
		page = insert_exame(request, cursor)
	cursor.close()
	return page

def index(request):
	if request.method != "POST":
		crudform = crudForm()
		return render(request, index_html, {"crudform": crudform})
	crudform = crudForm(request.POST)
	operation = crudform['operation'].value()
	table = crudform['table'].value()
	page = None
	cursor = connection.cursor()
	if operation == 'create':
		form = get_form(table)
		page = render(request, create_html, {"operation": operation, "table": table, "form": form})
	elif operation == 'read':
		if table == 'Usuario':
			cursor.execute(select_all_usuario)
			user_table = dictfetchall(cursor)
			cursor.execute(select_all_pessoa)
			person_table = dictfetchall(cursor)
			context = {'user_table': user_table, 'person_table': person_table}
		elif table == 'Perfil':
			cursor.execute(select_all_profile)
			profile_table = dictfetchall(cursor)
			context = {'profile_table': profile_table,}
		elif table == 'Servico':
			cursor.execute(select_all_service)
			service_table = dictfetchall(cursor)
			context = {'service_table': service_table,}
		else:
			cursor.execute(select_all_exam)
			exam_table = dictfetchall(cursor)
			context = {'exam_table': exam_table,}	
		template = loader.get_template('interface/read.html')
		page = HttpResponse(template.render(context, request))
	else: # operation == 'delete' or operation == 'update'
		if table == 'Usuario':
			cursor.execute(select_all_usuario)
			user_table = dictfetchall(cursor)
			cursor.execute(select_all_pessoa)
			person_table = dictfetchall(cursor)
			context = {'user_table': user_table, 'person_table': person_table, 'form': selectForm(), "operation": operation, "table": table}
		elif table == 'Perfil':
			cursor.execute(select_all_profile)
			profile_table = dictfetchall(cursor)
			context = {'profile_table': profile_table, 'form': selectForm(), "operation": operation, "table": table}
		elif table == 'Servico':
			cursor.execute(select_all_service)
			service_table = dictfetchall(cursor)
			context = {'service_table': service_table, 'form': selectForm(), "operation": operation, "table": table}
		else:
			cursor.execute(select_all_exam)
			exam_table = dictfetchall(cursor)
			context = {'exam_table': exam_table, 'form': selectForm(), "operation": operation, "table": table}	
		if operation == 'delete':
			template = loader.get_template(delete_html)
		else: # operation == 'update'
			template = loader.get_template(update_html)
		page = HttpResponse(template.render(context, request))
	cursor.close()
	return page
