from django import forms

class crudForm(forms.Form):
	OPERATION_CHOICES=[('create','Inserir'), ('read','Consultar'), ('update','Atualizar'), ('delete','Eliminar')]
	TABLE_CHOICES=[('Usuario','Usuário'), ('Perfil','Perfil'), ('Servico','Serviço'), ('Exame','Exame')]

	operation = forms.ChoiceField(choices=OPERATION_CHOICES, widget=forms.RadioSelect)
	table = forms.ChoiceField(choices=TABLE_CHOICES, widget=forms.RadioSelect)

class userForm(forms.Form):
	id_usuario = forms.CharField(label="id_usuario")
	id_pessoa = forms.CharField(label="id_pessoa")
	cpf = forms.CharField(label="CPF")
	nome = forms.CharField(label="nome")
	data_de_nascimento = forms.DateField(label="data de nasc")
	area_de_pesquisa = forms.CharField(label="area de pesquisa")
	instituicao = forms.CharField(label="instituicao")
	id_tutor = forms.CharField(label="id_tutor")
	login = forms.CharField(label="login")
	senha = forms.CharField(label="senha")

class profileForm(forms.Form):
	id_perfil = forms.CharField(label="id_perfil")
	codigo = forms.CharField(label="codigo")
	tipo = forms.CharField(label="tipo")

class serviceForm(forms.Form):
	CRUD_CHOICES=[('inserção','inserção'), ('visualização','visualização'), ('alteração','alteração'), ('remoção','remoção')]

	id_servico = forms.CharField(label="id_servico")
	classe = forms.ChoiceField(choices=CRUD_CHOICES, widget=forms.RadioSelect)
	nome = forms.CharField(label="nome")

class examForm(forms.Form):
	id_exame = forms.CharField(label="id_exame")
	tipo = forms.CharField(label="tipo")
	virus = forms.CharField(label="virus")
	
