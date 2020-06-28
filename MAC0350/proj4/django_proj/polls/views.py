from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from collections import namedtuple
from django.template import loader

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def query1(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM usuario')
        result = dictfetchall(cursor)
        print(result)
    
    template = loader.get_template('queries/query1.html')
    context = {'query1_result_list': result,}
    
    return HttpResponse(template.render(context, request))


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
