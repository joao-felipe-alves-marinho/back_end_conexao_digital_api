from ninja import ModelSchema, Schema
from typing import List

from .models import User, Interesse, FormacaoAcademica, ExperienciaProfissional, Habilidade, Projeto


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
    interesses: List[InteresseSchema]
    habilidades: List[HabilidadeSchema]
    formacoes_academicas: List[FormacaoAcademicaSchema]
    experiencias_profissionais: List[ExperienciaProfissionalSchema]
    projetos: List[ProjetoSchema]

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
            'interesses',
            'habilidades',
            'formacoes_academicas',
            'experiencias_profissionais',
            'projetos',
        )


class ErrorSchema(Schema):
    detail: str
