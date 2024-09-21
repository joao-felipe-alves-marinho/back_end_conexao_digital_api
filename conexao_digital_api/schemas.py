from ninja import ModelSchema, Schema
from typing import List, Optional

from .models import User, Interesse, FormacaoAcademica, ExperienciaProfissional, Habilidade, Projeto

from pydantic import BaseModel


class UserInteresseSchema(ModelSchema):
    class Meta:
        model = Interesse
        fields = (
            'id',
            'nome',
        )


class UserHabilidadeSchema(ModelSchema):
    class Meta:
        model = Habilidade
        fields = (
            'id',
            'nome',
            'nivel',
        )


class UserFormacaoAcademicaSchema(ModelSchema):
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


class UserExperienciaProfissionalSchema(ModelSchema):
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


class UserProjetoSchema(ModelSchema):
    class Meta:
        model = Projeto
        fields = (
            'id',
            'nome',
            'link',
        )


class UserSchema(ModelSchema):
    avatar: Optional[str] = None
    interesses: List[UserInteresseSchema] = None
    habilidades: List[UserInteresseSchema] = None
    formacoes_academicas: List[UserFormacaoAcademicaSchema] = None
    experiencias_profissionais: List[UserExperienciaProfissionalSchema] = None
    projetos: List[UserProjetoSchema] = None

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


class CreateOrUpdateUserSchema(ModelSchema):
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


class RelationshipUserSchema(ModelSchema):
    class Meta:
        model = User
        fields = (
            'id',
            'nome',
            'email',
        )


class InteresseSchema(ModelSchema):
    users: List[RelationshipUserSchema] = None

    class Meta:
        model = Interesse
        fields = (
            'id',
            'nome',
        )


class CreateOrUpdateInteresseSchema(ModelSchema):
    class Meta:
        model = Interesse
        fields = (
            'nome',
        )


class HabilitadeSchema(ModelSchema):
    user: RelationshipUserSchema

    class Meta:
        model = Habilidade
        fields = (
            'id',
            'nome',
            'nivel',
        )


class CreateOrUpdateHabilidadeSchema(ModelSchema):
    class Meta:
        model = Habilidade
        fields = (
            'nome',
            'nivel',
        )


class FormacaoAcademicaSchema(ModelSchema):
    user: RelationshipUserSchema

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


class CreateOrUpdateFormacaoAcademicaSchema(ModelSchema):
    class Meta:
        model = FormacaoAcademica
        fields = (
            'curso',
            'instituicao',
            'ano_inicio',
            'ano_conclusao',
            'semestre',
        )


class ExperienciaProfissionalSchema(ModelSchema):
    user: RelationshipUserSchema

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


class CreateOrUpdateExperienciaProfissionalSchema(ModelSchema):
    class Meta:
        model = ExperienciaProfissional
        fields = (
            'cargo',
            'empresa',
            'ano_inicio',
            'ano_fim',
            'descricao',
        )


class ProjetoSchema(ModelSchema):
    user: RelationshipUserSchema

    class Meta:
        model = Projeto
        fields = (
            'id',
            'nome',
            'descricao',
            'link',
        )


class CreateOrUpdateProjetoSchema(ModelSchema):
    class Meta:
        model = Projeto
        fields = (
            'nome',
            'descricao',
            'link',
        )


class ErrorSchema(Schema):
    detail: str
