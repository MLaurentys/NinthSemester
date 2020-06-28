from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query1', views.query1, name='query1')
]
