from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from .defines import *
from .query_helper import *

def dictfetchall(cursor):
	"Return all rows from a cursor as a dict"
	columns = [col[0] for col in cursor.description]
	return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Return correpondant form
def get_form(table):
    if table == 'Usuario':
        form = userForm()
    elif table == 'Perfil':
        form = profileForm()
    elif table == 'Servico':
        form = serviceForm()
    else:
        form = examForm()
    return form

# Inserts on user tabe
def insert_user(request, cursor):
    form = userForm(request.POST)
    try:
        user_id = int(form['id_usuario'].value())
        person_id = int(form['id_pessoa'].value())
    except:
        return render(request, create_html, {"operation": "create", "table": "Usuario", "form": userForm(), "message": "ERRO: id de usuário e/ou pessoa inválido"})
    cursor.execute(build_check_str('usuario', {'id_usuario':form['id_usuario'].value()}))
    user_result = dictfetchall(cursor)
    cursor.execute(build_check_str('pessoa', {'id_pessoa':form['id_pessoa'].value()}))
    person_result = dictfetchall(cursor)
    if not user_result[0]['count'] and person_result[0]['count']:
        if form['id_tutor'].value() != '':
            if form['id_tutor'].value() != form['id_usuario'].value():
                cursor.execute(build_check_str('usuario', {'id_usuario':form['id_tutor'].value()}))
                result = dictfetchall(cursor)
                if result[0]['count']:
                    cursor.execute(build_insert_query('usuario', ['id_usuario', 'id_pessoa', 'area_de_pesquisa', 'instituicao', 'id_tutor', 'login', 'senha'], [form['id_usuario'].value(), form['id_pessoa'].value(), form['area_de_pesquisa'].value(), form['instituicao'].value(), form['id_tutor'].value(), form['login'].value(), form['senha'].value()]))
                    page = render(request, create_html, {"operation": "create", "table": "Usuario", "form": userForm(), "message": create_success})
                else:
                    return render(request, create_html, {"operation": "create", "table": "Usuario", "form": userForm(), "message": "ERRO: id_tutor colocado não existe."})
            else:
                return render(request, create_html, {"operation": "create", "table": "Usuario", "form": userForm(), "message": "ERRO: id_tutor não pode ser igual a id_usuario"})
        else:
            cursor.execute(build_insert_query('usuario', ['id_usuario', 'id_pessoa', 'area_de_pesquisa', 'instituicao', 'login', 'senha'], [form['id_usuario'].value(), form['id_pessoa'].value(), form['area_de_pesquisa'].value(), form['instituicao'].value(), form['login'].value(), form['senha'].value()]))
        page = render(request, create_html, {"operation": "create", "table": "Usuario", "form": userForm(), "message": create_success})
    elif not person_result[0]['count']:
        page = render(request, create_html, {"operation": "create", "table": "Usuario", "form": userForm(), "message": error_nonexistant_person})
    else:
        page = render(request, create_html, {"operation": "create", "table": "Usuario", "form": userForm(), "message": error_existant_user})
    return page

# Inserts to profile table
def insert_profile(request, cursor):
    form = profileForm(request.POST)
    try:
        profile_id = int(form['id_perfil'].value())
    except:
        return render(request, create_html, {"operation": "create", "table": "Perfil", "form": profileForm(), "message": "ERRO: id inválido"})
    cursor.execute(build_check_str('perfil', {'id_perfil':form['id_perfil'].value()}))
    profile_result = dictfetchall(cursor)
    if not profile_result[0]['count']:
        cursor.execute(build_insert_query('perfil', ['id_perfil', 'codigo', 'tipo'], [form['id_perfil'].value(), form['codigo'].value(), form['tipo'].value()]))
        page = render(request, create_html, {"operation": "create", "table": "Perfil", "form": profileForm(), "message": create_success})
    else:
        page = render(request, create_html, {"operation": "create", "table": "Perfil", "form": profileForm(), "message": "ERRO: perfil já existente. Você pode VOLTAR e tentar atualizar a tabela."})
    return page

# Inserts on service tabe
def insert_service(request, cursor):
    form = serviceForm(request.POST)
    try:
        service_id = int(form['id_servico'].value())
    except:
        return render(request, create_html, {"operation": "create", "table": "Servico", "form": serviceForm(), "message": "ERRO: id inválido"})
    cursor.execute(build_check_str('servico', {'id_servico':form['id_servico'].value()}))
    service_result = dictfetchall(cursor)
    if not service_result[0]['count']:
        cursor.execute(build_insert_query('servico', ['id_servico', 'classe', 'nome'], [form['id_servico'].value(), form['classe'].value(), form['nome'].value()]))
        page = render(request, create_html, {"operation": "create", "table": "Servico", "form": serviceForm(), "message": "Inserção feita com SUCESSO. Realize outra inserção ou faça uma consulta para conferir."})
    else:
        page = render(request, create_html, {"operation": "create", "table": "Servico", "form": serviceForm(), "message": "ERRO: serviço já existente. Você pode VOLTAR e tentar atualizar a tabela."})
    return page

# Inserts on exam tabe
def insert_exame(request, cursor):
    form = examForm(request.POST)
    try:
        exam_id = int(form['id_exame'].value())
    except:
        return render(request, create_html, {"operation": "create", "table": "Exame", "form": examForm(), "message": "ERRO: id inválido"})
    cursor.execute(build_check_str('exame', {'id_exame':form['id_exame'].value()}))
    exam_result = dictfetchall(cursor)
    if not exam_result[0]['count']:
        cursor.execute(build_insert_query('exame', ['id_exame', 'tipo', 'virus'], [form['id_exame'].value(), form['tipo'].value(), form['virus'].value()]))
        page = render(request, create_html, {"operation": "create", "table": "Exame", "form": examForm(), "message": "Inserção feita com SUCESSO. Realize outra inserção ou faça uma consulta para conferir."})
    else:
        page = render(request, create_html, {"operation": "create", "table": "Exame", "form": examForm(), "message": "ERRO: exame já existente. Você pode VOLTAR e tentar atualizar a tabela."})
    return page

def delete_user(request, cursor):
    cursor.execute(select_all_usuario)
    user_table = dictfetchall(cursor)
    cursor.execute(select_all_pessoa)
    person_table = dictfetchall(cursor)
    form = selectForm(request.POST)
    try:
        selected_id = int(form['selected_id'].value())
    except:
        return render(request, delete_html, {"operation": "delete", "table": "Usuario", "form": form, 'user_table': user_table, 'person_table': person_table, "message": "ERRO: id inválido"})
    cursor.execute(build_check_str('usuario', {'id_usuario':form['selected_id'].value()}))
    selected_result = dictfetchall(cursor)
    if selected_result[0]['count']:
        cursor.execute(build_delete_query('usuario', {'id_usuario':form['selected_id'].value()}))
        cursor.execute(select_all_usuario)
        user_table = dictfetchall(cursor)
        page = render(request, delete_html, {"operation": "delete", "table": "Usuario", "form": form, 'user_table': user_table, 'person_table': person_table, "message": "Eliminação feita com SUCESSO. Confira abaixo."})
    else:
        page = render(request, delete_html, {"operation": "delete", "table": "Usuario", "form": form, 'user_table': user_table, 'person_table': person_table, "message": "ERRO: usuário não existe. Você pode VOLTAR e tentar inseri-lo na tabela."})
    return page

def delete_profile(request, cursor):
    cursor.execute('SELECT * FROM perfil')
    profile_table = dictfetchall(cursor)
    form = selectForm(request.POST)
    try:
        selected_id = int(form['selected_id'].value())
    except:
        return render(request, delete_html, {"operation": "delete", "table": "Perfil", "form": form, 'profile_table': profile_table, "message": "ERRO: id inválido"})
    cursor.execute(build_check_str('perfil', {'id_perfil':form['selected_id'].value()}))
    selected_result = dictfetchall(cursor)
    if selected_result[0]['count']:
        cursor.execute(build_delete_query('perfil', {'id_perfil':form['selected_id'].value()}))
        cursor.execute('SELECT * FROM perfil')
        profile_table = dictfetchall(cursor)
        page = render(request, delete_html, {"operation": "delete", "table": "Perfil", "form": form, 'profile_table': profile_table, "message": "Eliminação feita com SUCESSO. Confira abaixo."})
    else:
        page = render(request, delete_html, {"operation": "delete", "table": "Perfil", "form": form, 'profile_table': profile_table, "message": "ERRO: perfil não existe. Você pode VOLTAR e tentar inseri-lo na tabela."})
    return page

def delete_service(request, cursor):
    cursor.execute('SELECT * FROM servico')
    service_table = dictfetchall(cursor)
    form = selectForm(request.POST)
    try:
        selected_id = int(form['selected_id'].value())
    except:
        return render(request, delete_html, {"operation": "delete", "table": "Servico", "form": form, 'service_table': service_table, "message": "ERRO: id inválido"})
    cursor.execute(build_check_str('servico', {'id_servico':form['selected_id'].value()}))
    selected_result = dictfetchall(cursor)
    if selected_result[0]['count']:
        cursor.execute(build_delete_query('servico', {'id_servico':form['selected_id'].value()}))
        cursor.execute('SELECT * FROM servico')
        service_table = dictfetchall(cursor)
        page = render(request, delete_html, {"operation": "delete", "table": "Servico", "form": form, 'service_table': service_table, "message": "Eliminação feita com SUCESSO. Confira abaixo."})
    else:
        page = render(request, delete_html, {"operation": "delete", "table": "Servico", "form": form, 'service_table': service_table, "message": "ERRO: serviço não existe. Você pode VOLTAR e tentar inseri-lo na tabela."})
    return page

def delete_exam(request, cursor):
    cursor.execute(select_all_exam)
    exam_table = dictfetchall(cursor)
    form = selectForm(request.POST)
    try:
        selected_id = int(form['selected_id'].value())
    except:
        return render(request, delete_html, {"operation": "delete", "table": "Exame", "form": form, 'exam_table': exam_table, "message": "ERRO: id inválido"})
    cursor.execute(build_check_str('exame', {'id_exame':form['selected_id'].value()}))
    selected_result = dictfetchall(cursor)
    if selected_result[0]['count']:
        cursor.execute(build_delete_query('exame', {'id_exame':form['selected_id'].value()}))
        cursor.execute(select_all_exam)
        exam_table = dictfetchall(cursor)
        page = render(request, delete_html, {"operation": "delete", "table": "Exame", "form": form, 'exam_table': exam_table, "message": delete_success})
    else:
        page = render(request, delete_html, {"operation": "delete", "table": "Exame", "form": form, 'exam_table': exam_table, "message": error_nonexistant_exam})
    return page

def query_user(request, cursor):
    cursor.execute(select_all_usuario)
    user_table = dictfetchall(cursor)
    cursor.execute(select_all_pessoa)
    person_table = dictfetchall(cursor)
    form = selectForm(request.POST)
    try:
        selected_id = int(form['selected_id'].value())
    except:
        page = render(request, update_html, {"operation": "update", "table": "Usuario", "form": form, 'user_table': user_table, 'person_table': person_table, "message": "ERRO: id inválido"})
    cursor.execute(build_check_str('usuario', {'id_usuario':form['selected_id'].value()}))
    selected_result = dictfetchall(cursor)
    if selected_result[0]['count']:
        for user in user_table:
            if user['id_usuario'] == int(form['selected_id'].value()):
                form = userForm(initial={"area_de_pesquisa": user['area_de_pesquisa'], "instituicao": user['instituicao'], "id_tutor": user['id_tutor'], "login": user['login'], "senha": user['senha']})
                form.fields["id_usuario"] = forms.CharField(initial=user['id_usuario'], widget=forms.widgets.HiddenInput())
                form.fields["id_pessoa"] = forms.CharField(initial=user['id_pessoa'], widget=forms.widgets.HiddenInput())
                break
        page = render(request, update_html, {"operation": "update", "table": "Usuario", "form": form, 'user_table': user_table, 'person_table': person_table, "selected_id": True})
    else:
        page = render(request, update_html, {"operation": "update", "table": "Usuario", "form": form, 'user_table': user_table, 'person_table': person_table, "message": "ERRO: usuário não existe. Você pode VOLTAR e tentar inseri-lo na tabela."})
    return page

def query_profile(request, cursor):
    cursor.execute(select_all_profile)
    profile_table = dictfetchall(cursor)
    form = selectForm(request.POST)
    try:
        selected_id = int(form['selected_id'].value())
    except:
        page = render(request, update_html, {"operation": "update", "table": "Perfil", "form": form, 'profile_table': profile_table, "message": "ERRO: id inválido"})
    cursor.execute(build_check_str('perfil', {'id_perfil':form['selected_id'].value()}))
    selected_result = dictfetchall(cursor)
    if selected_result[0]['count']:
        for profile in profile_table:
            if profile['id_perfil'] == int(form['selected_id'].value()):
                form = profileForm(initial={"codigo": profile['codigo'], "tipo": profile['tipo']})
                form.fields["id_perfil"] = forms.CharField(initial=profile['id_perfil'], widget=forms.widgets.HiddenInput())
                break
        page = render(request, update_html, {"operation": "update", "table": "Perfil", "form": form, 'profile_table': profile_table, "selected_id": True})
    else:
        page = render(request, update_html, {"operation": "update", "table": "Perfil", "form": form, 'profile_table': profile_table, "message": "ERRO: perfil não existe. Você pode VOLTAR e tentar inseri-lo na tabela."})
    return page

def query_service(request, cursor):
    cursor.execute(select_all_service)
    service_table = dictfetchall(cursor)
    form = selectForm(request.POST)
    try:
        selected_id = int(form['selected_id'].value())
    except:
        page = render(request, update_html, {"operation": "update", "table": "Servico", "form": form, 'service_table': service_table, "message": "ERRO: id inválido"})
    cursor.execute(build_check_str('servico', {'id_servico':form['selected_id'].value()}))
    selected_result = dictfetchall(cursor)
    if selected_result[0]['count']:
        for service in service_table:
            if service['id_servico'] == int(form['selected_id'].value()):
                form = serviceForm(initial={"classe": service['classe'], "nome": service['nome']})
                form.fields["id_servico"] = forms.CharField(initial=service['id_servico'], widget=forms.widgets.HiddenInput())
                break
        page = render(request, update_html, {"operation": "update", "table": "Servico", "form": form, 'service_table': service_table, "selected_id": True})
    else:
        page = render(request, update_html, {"operation": "update", "table": "Servico", "form": form, 'service_table': service_table, "message": "ERRO: serviço não existe. Você pode VOLTAR e tentar inseri-lo na tabela."})
    return page

def query_exam(request, cursor):
    cursor.execute(select_all_exam)
    exam_table = dictfetchall(cursor)
    form = selectForm(request.POST)
    try:
        selected_id = int(form['selected_id'].value())
    except:
        page = render(request, update_html, {"operation": "update", "table": "Exame", "form": form, 'exam_table': exam_table, "message": "ERRO: id inválido"})
    cursor.execute(build_check_str('exame', {'id_exame':form['selected_id'].value()}))
    selected_result = dictfetchall(cursor)
    if selected_result[0]['count']:
        for exam in exam_table:
            if exam['id_exame'] == int(form['selected_id'].value()):
                form = examForm(initial={"tipo": exam['tipo'], "virus": exam['virus']})
                form.fields["id_exame"] = forms.CharField(initial=exam['id_exame'], widget=forms.widgets.HiddenInput())
                break
        page = render(request, update_html, {"operation": "update", "table": "Exame", "form": form, 'exam_table': exam_table, "selected_id": True})
    else:
        page = render(request, update_html, {"operation": "update", "table": "Exame", "form": form, 'exam_table': exam_table, "message": "ERRO: exame não existe. Você pode VOLTAR e tentar inseri-lo na tabela."})
    return page

# def update_service(request, cursor):
# def update_exam(request, cursor):
# def update_service(request, cursor):
# def update_exam(request, cursor):
