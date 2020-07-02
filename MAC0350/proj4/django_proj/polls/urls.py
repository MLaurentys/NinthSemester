from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('query1', views.query1, name='query1'),
    path('test1', views.test1, name='test1'),
    path('test2', views.test2, name='test2'),
    path('test3', views.test3, name='test3')
]
