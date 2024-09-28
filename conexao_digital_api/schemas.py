from ninja import ModelSchema, Schema, FilterSchema, Field
from typing import List, Optional
from .models import User, Interesse, FormacaoAcademica, ExperienciaProfissional, Habilidade, Projeto


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
        include = (
            'id',
            'nome',
            'nivel',
        )
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
    habilidades: List[UserHabilidadeSchema] = None
    formacoes_academicas: List[UserFormacaoAcademicaSchema] = None
    experiencias_profissionais: List[UserExperienciaProfissionalSchema] = None
    projetos: List[UserProjetoSchema] = None

    class Meta:
        model = User
        fields = (
            'id',
            'nome',
            'email',
            'idade',
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
            'password',
            'email',
            'idade',
            'genero',
            'telefone',
            'deficiencia',
        )


class UpdateUserSchema(ModelSchema):
    class Meta:
        model = User
        fields = (
            'nome',
            'email',
            'idade',
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


class FilterEmailSchema(FilterSchema):
    genero: Optional[str] = Field(None, q='genero')
    is_active: Optional[bool] = Field(None, q='is_active')
    deficiencia: Optional[bool] = Field(None, q='deficiencia')

    # Filters for idade
    idade_maior_que: Optional[int] = Field(None, q='idade__gte')  # Users with age greater than or equal
    idade_menor_que: Optional[int] = Field(None, q='idade__lte')  # Users with age less than or equal

    # Filters for academic formation
    curso: Optional[str] = Field(None, q='formacoes_academicas__curso__icontains')
    instituicao: Optional[str] = Field(None, q='formacoes_academicas__instituicao__icontains')

    # Filter for semestre above or below a given value
    semestre_maior_que: Optional[int] = Field(None,
                                              q='formacoes_academicas__semestre__gte')  # Semestre greater than or equal
    semestre_menow_que: Optional[int] = Field(None,
                                              q='formacoes_academicas__semestre__lte')  # Semestre less than or equal

    # Filter by interests and skills (habilidades)
    interesses: Optional[List[str]] = Field(None, q='interesses__nome__in')
    habilidades: Optional[List[str]] = Field(None, q='habilidades__nome__in')
    nivel_habilidade: Optional[int] = Field(None, q='habilidades__nivel')  # Filtering by skill level

    # Filter by project involvement
    projeto_nome: Optional[str] = Field(None, q='projetos__nome__icontains')
    projeto_link: Optional[str] = Field(None, q='projetos__link__icontains')


class EmailRequestSchema(Schema):
    subject: str
    message: str
    emails: Optional[List[str]] = []
