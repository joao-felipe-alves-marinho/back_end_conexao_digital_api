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
    avatar: Optional[str] = None
    interesses: List[InteresseSchema] = None
    habilidades: List[InteresseSchema] = None
    formacoes_academicas: List[FormacaoAcademicaSchema] = None
    experiencias_profissionais: List[ExperienciaProfissionalSchema] = None
    projetos: List[ProjetoSchema] = None

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
