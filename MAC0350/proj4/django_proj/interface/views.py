from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from collections import namedtuple
from django.template import loader

from .forms import crudForm
from .query_helper import *

def index(request):
    if request.method == "POST":
        form = crudForm(request.POST)
        operation_value = form['operation'].value()
        table_value = form['table'].value()
        return HttpResponse("%s, %s" %(operation_value, table_value))
    else:
        form = crudForm()
    return render(request, 'interface/index.html', {"form": form})

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def query1(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM usuario')
        result = dictfetchall(cursor)
        print(result)

    template = loader.get_template('interface/query1.html')
    context = {'query1_result_list': result,}

    return HttpResponse(template.render(context, request))

def test1(request):
    template = loader.get_template('interface/test1.html')
    return HttpResponse(template.render())

def test2(request):
    check_query = build_check_str('exame', {'id_exame':'999'})
    insert_query = build_insert_query('exame', ['id_exame', 'tipo', 'virus'],
                                      [ '999', 'PCR', 'H1N1'])
    data_exists = False
    with connection.cursor() as cursor:
        cursor.execute(check_query)
        result = dictfetchall(cursor)
        if result[0]['count']:
            data_exists = True
        print(result)
        if not data_exists:
            cursor.execute(insert_query)
    if data_exists:
        response = HttpResponse("Data already exists!")
    else:
        response = HttpResponse("Data added to table!")
    return response

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
