from ninja import ModelSchema, Schema
from typing import List, Optional

from .models import User, Interesse, FormacaoAcademica, ExperienciaProfissional, Habilidade, Projeto

from pydantic import BaseModel


class SignInSchema(BaseModel):
    email: str
    password: str


class InteresseSchema(ModelSchema):
    class Meta:
        model = Interesse
        fields = (
            'id',
            'nome',
        )


class HabilidadeSchema(ModelSchema):
    class Meta:
        model = Habilidade
        fields = (
            'id',
            'nome',
            'nivel',
        )


class FormacaoAcademicaSchema(ModelSchema):
    class Meta:
        model = FormacaoAcademica
        fields = (
            'id',
            'curso',
            'instituicao',
            'ano_inicio',
            'ano_conclusao',
            'semestre',
        )


class ExperienciaProfissionalSchema(ModelSchema):
    class Meta:
        model = ExperienciaProfissional
        fields = (
            'id',
            'cargo',
            'empresa',
            'ano_inicio',
            'ano_fim',
            'descricao',
        )


class ProjetoSchema(ModelSchema):
    class Meta:
        model = Projeto
        fields = (
            'id',
            'nome',
            'link',
        )


class UserSchema(ModelSchema):
    interesses: list[InteresseSchema] = []
    habilidades: list[HabilidadeSchema] = []
    formacoes_academicas: list[FormacaoAcademicaSchema] = []
    experiencias_profissionais: list[ExperienciaProfissionalSchema] = []
    projetos: list[ProjetoSchema] = []
    avatar: str = ''

    class Meta:
        model = User
        fields = (
            'id',
            'nome',
            'email',
            'ano_nascimento',
            'genero',
            'telefone',
            'deficiencia',
            'resumo',
            'avatar',
            'interesses',
            'habilidades',
            'formacoes_academicas',
            'experiencias_profissionais',
            'projetos',
        )


class CreateUserSchema(ModelSchema):
    class Meta:
        model = User
        fields = (
            'nome',
            'email',
            'password',
            'ano_nascimento',
            'genero',
            'telefone',
            'deficiencia',
            'resumo',
        )


class ErrorSchema(Schema):
    detail: str
