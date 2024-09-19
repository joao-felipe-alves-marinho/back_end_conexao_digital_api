from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório.')
        if not password:
            raise ValueError('A senha é obrigatória.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório.')
        if not password:
            raise ValueError('A senha é obrigatória.')
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    gender_choices = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    ]

    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=200, unique=True)
    ano_nascimento = models.IntegerField()
    genero = models.CharField(max_length=1, choices=gender_choices, default=None)
    telefone = models.CharField(max_length=15)
    deficiencia = models.BooleanField(default=False)
    resumo = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    interesses = models.ManyToManyField('Interesse', related_name='usuarios', blank=True)
    habilidades = models.ForeignKey('Habilidade', related_name='usuario', blank=True, on_delete=models.CASCADE,
                                    null=True)
    formacoes_academicas = models.ForeignKey('FormacaoAcademica', related_name='usuario', blank=True,
                                             on_delete=models.CASCADE, null=True)
    experiencias_profissionais = models.ForeignKey('ExperienciaProfissional', related_name='usuario', blank=True,
                                                   on_delete=models.CASCADE, null=True)
    projetos = models.ForeignKey('Projeto', related_name='usuario', blank=True, on_delete=models.CASCADE, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'ano_nascimento', 'genero', 'telefone']
    objects = UserManager()

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ("nome",)
        verbose_name = "pessoa"
        verbose_name_plural = "pessoas"


class Interesse(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ("nome",)
        verbose_name = "interesse"
        verbose_name_plural = "interesses"


class FormacaoAcademica(models.Model):
    curso = models.CharField(max_length=100)
    instituicao = models.CharField(max_length=100)
    ano_inicio = models.IntegerField()
    ano_conclusao = models.IntegerField()
    semestre = models.IntegerField()

    def __str__(self):
        return self.curso

    class Meta:
        ordering = ("curso",)
        verbose_name = "formação acadêmica"
        verbose_name_plural = "formações acadêmicas"


class ExperienciaProfissional(models.Model):
    cargo = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    ano_inicio = models.IntegerField()
    ano_fim = models.IntegerField(blank=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.cargo

    class Meta:
        ordering = ("cargo",)
        verbose_name = "experiência profissional"
        verbose_name_plural = "experiências profissionais"


class Habilidade(models.Model):
    niveis = [
        (1, 'Iniciante'),
        (2, 'Intermediário'),
        (3, 'Avançado'),
    ]
    nome = models.CharField(max_length=100)
    nivel = models.IntegerField(choices=niveis)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ("nome",)
        verbose_name = "habilidade"
        verbose_name_plural = "habilidades"


class Projeto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    link = models.URLField()

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ("nome",)
        verbose_name = "projeto"
        verbose_name_plural = "projetos"
