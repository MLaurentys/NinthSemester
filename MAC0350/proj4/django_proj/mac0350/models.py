# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Amostra(models.Model):
    id_paciente = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='id_paciente')
    id_exame = models.ForeignKey('Exame', models.DO_NOTHING, db_column='id_exame')
    codigo_amostra = models.CharField(max_length=255)
    metodo_de_coleta = models.CharField(max_length=255)
    material = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'amostra'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Exame(models.Model):
    id_exame = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=255)
    virus = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'exame'


class Gerencia(models.Model):
    id_servico = models.ForeignKey('Servico', models.DO_NOTHING, db_column='id_servico')
    id_exame = models.ForeignKey(Exame, models.DO_NOTHING, db_column='id_exame')

    class Meta:
        managed = False
        db_table = 'gerencia'


class Historico(models.Model):
    id_usuario = models.ForeignKey('Paciente', models.DO_NOTHING, db_column='id_usuario')
    id_servico = models.ForeignKey('Servico', models.DO_NOTHING, db_column='id_servico')
    id_exame = models.ForeignKey(Exame, models.DO_NOTHING, db_column='id_exame')
    data_de_utilizacao = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'historico'


class Paciente(models.Model):
    id_paciente = models.IntegerField(primary_key=True)
    endereco = models.CharField(max_length=255)
    id_pessoa = models.ForeignKey('Pessoa', models.DO_NOTHING, db_column='id_pessoa', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paciente'


class Perfil(models.Model):
    id_perfil = models.IntegerField(primary_key=True)
    codigo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'perfil'


class Pertence(models.Model):
    id_servico = models.ForeignKey('Servico', models.DO_NOTHING, db_column='id_servico')
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')

    class Meta:
        managed = False
        db_table = 'pertence'


class Pessoa(models.Model):
    id_pessoa = models.IntegerField(primary_key=True)
    cpf = models.CharField(max_length=11)
    nome = models.CharField(max_length=255)
    data_de_nascimento = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pessoa'


class Possui(models.Model):
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')

    class Meta:
        managed = False
        db_table = 'possui'


class Realiza(models.Model):
    id_paciente = models.ForeignKey(Paciente, models.DO_NOTHING, db_column='id_paciente')
    id_exame = models.ForeignKey(Exame, models.DO_NOTHING, db_column='id_exame')
    codigo_amostra = models.CharField(max_length=255, blank=True, null=True)
    data_de_solicitacao = models.DateTimeField(blank=True, null=True)
    data_de_realizacao = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'realiza'


class Servico(models.Model):
    id_servico = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    classe = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'servico'


class Tutelamento(models.Model):
    id_tutelado = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_tutelado', related_name='%(class)s_id_tutelado')
    id_tutor = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_tutor', related_name='%(class)s_id_tutor')
    id_servico = models.ForeignKey(Servico, models.DO_NOTHING, db_column='id_servico')
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')
    data_de_inicio = models.DateField()
    data_de_termino = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tutelamento'


class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True)
    area_de_pesquisa = models.CharField(max_length=255, blank=True, null=True)
    instituicao = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)
    id_tutor = models.ForeignKey('self', models.DO_NOTHING, db_column='id_tutor', blank=True, null=True)
    id_pessoa = models.ForeignKey(Pessoa, models.DO_NOTHING, db_column='id_pessoa', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
