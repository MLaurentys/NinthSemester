from django import forms

class crudForm(forms.Form):
	OPERATION_CHOICES=[('Create','Inserir'), ('Read','Consultar'), ('Update','Atualizar'), ('Delete','Eliminar')]
	TABLE_CHOICES=[('User','Usuário'), ('Profile','Perfil'), ('Service','Serviço'), ('Exam','Exame')]

	operation = forms.ChoiceField(choices=OPERATION_CHOICES, widget=forms.RadioSelect)
	table = forms.ChoiceField(choices=TABLE_CHOICES, widget=forms.RadioSelect)
