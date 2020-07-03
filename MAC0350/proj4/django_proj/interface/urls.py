from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('create', views.create, name='create'),

    path('test2', views.test2, name='test2'),
    path('test3', views.test3, name='test3')
]
