from django import forms

# def make_form (columns):
# 	choices = {col:forms.CharField() for col in columns}
# 	dynamic_form = type('dynamic_form', (myForm,), choices)
# 	return dynamic_form

class myForm(forms.Form):
	def __init__(self, form_fields=[], *args, **kwargs):
		super().__init__(*args, **kwargs)
		for k in form_fields:
			print("k =", k)
			self.fields[k] = forms.CharField(label=k)


class crudForm(forms.Form):
	OPERATION_CHOICES=[('create','Inserir'), ('read','Consultar'), ('update','Atualizar'), ('delete','Eliminar')]
	TABLE_CHOICES=[('Usuario','Usuário'), ('Perfil','Perfil'), ('Servico','Serviço'), ('Exame','Exame')]

	operation = forms.ChoiceField(choices=OPERATION_CHOICES, widget=forms.RadioSelect)
	table = forms.ChoiceField(choices=TABLE_CHOICES, widget=forms.RadioSelect)

class userForm(forms.Form):
	cpf = forms.CharField(label="CPF")
	nome = forms.CharField(label="nome")
	data_de_nascimento = forms.DateField(label="data de nasc")
	area_de_pesquisa = forms.CharField(label="area de pesquisa")
	instituicao = forms.CharField(label="instituicao")
	login = forms.CharField(label="login")
	senha = forms.CharField(label="senha")

class profileForm(forms.Form):
	codigo = forms.CharField(label="codigo")
	tipo = forms.CharField(label="tipo")

class serviceForm(forms.Form):
	classe = forms.CharField(label="classe")
	nome = forms.CharField(label="nome")

class examForm(forms.Form):
	tipo = forms.CharField(label="tipo")
	virus = forms.CharField(label="virus")
	
