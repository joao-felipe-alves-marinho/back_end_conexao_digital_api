from ninja_extra import (
    NinjaExtraAPI,
    api_controller,
    ModelConfig, ModelControllerBase, ModelSchemaConfig, ModelEndpointFactory,
    permissions
)
from ninja_auth.api import router as auth_router

from .models import User, Interesse, Habilidade, FormacaoAcademica, ExperienciaProfissional, Projeto
from .schemas import (
    UserSchema,
    HabilitadeSchema, CreateOrUpdateHabilidadeSchema,
    InteresseSchema, CreateOrUpdateInteresseSchema,
    FormacaoAcademicaSchema, CreateOrUpdateFormacaoAcademicaSchema,
    ExperienciaProfissionalSchema, CreateOrUpdateExperienciaProfissionalSchema,
    ProjetoSchema, CreateOrUpdateProjetoSchema,
)

api = NinjaExtraAPI(
    version='1.0.0',
    title='Conexao Digital API',
    description='API para o projeto Conexao Digital',
    csrf=True,
)

api.add_router('/auth', auth_router)


@api_controller('/admin', tags=['admins'], permissions=[permissions.IsAdminUser])
class UserModelController(ModelControllerBase):
    model_config = ModelConfig(
        model=User,
        retrieve_schema=UserSchema,
        schema_config=ModelSchemaConfig(
            exclude=[
                'groups', 'user_permissions',
                'is_active', 'is_staff', 'is_superuser',
                'last_login', 'date_joined',
            ],
            read_only_fields=['id'],
            write_only_fields=['password'],
        ),
    )

    add_user_to_new_habilidade = ModelEndpointFactory.create(
        path='/{int:user_id}/habilidades',
        schema_in=CreateOrUpdateHabilidadeSchema,
        schema_out=HabilitadeSchema,
        custom_handler=lambda self, data, **kw: self.handle_add_user_to_new_habilidade(data, **kw),
    )

    def handle_add_user_to_new_habilidade(self, data: CreateOrUpdateHabilidadeSchema, **kw: any) -> Habilidade:
        user_id = self.service.get_one(pk=kw['user_id'])
        habilidade = Habilidade.objects.create(**data.dict())
        habilidade.user = user_id
        habilidade.save()
        return habilidade

    add_user_to_new_formacao_academica = ModelEndpointFactory.create(
        path='/{int:user_id}/formacoes-academicas',
        schema_in=CreateOrUpdateFormacaoAcademicaSchema,
        schema_out=FormacaoAcademicaSchema,
        custom_handler=lambda self, data, **kw: self.handle_add_user_to_new_formacao_academica(data, **kw),
    )

    def handle_add_user_to_new_formacao_academica(self, data: CreateOrUpdateFormacaoAcademicaSchema,
                                                  **kw: any) -> FormacaoAcademica:
        user_id = self.service.get_one(pk=kw['user_id'])
        formacao_academica = FormacaoAcademica.objects.create(**data.dict())
        formacao_academica.user = user_id
        formacao_academica.save()
        return formacao_academica

    add_user_to_new_experiencia_profissional = ModelEndpointFactory.create(
        path='/{int:user_id}/experiencias-profissionais',
        schema_in=CreateOrUpdateExperienciaProfissionalSchema,
        schema_out=ExperienciaProfissionalSchema,
        custom_handler=lambda self, data, **kw: self.handle_add_user_to_new_experiencia_profissional(data, **kw),
    )

    def handle_add_user_to_new_experiencia_profissional(self, data: CreateOrUpdateExperienciaProfissionalSchema,
                                                        **kw: any) -> ExperienciaProfissional:
        user_id = self.service.get_one(pk=kw['user_id'])
        experiencia_profissional = ExperienciaProfissional.objects.create(**data.dict())
        experiencia_profissional.user = user_id
        experiencia_profissional.save()
        return experiencia_profissional

    add_user_to_new_projeto = ModelEndpointFactory.create(
        path='/{int:user_id}/projetos',
        schema_in=CreateOrUpdateProjetoSchema,
        schema_out=ProjetoSchema,
        custom_handler=lambda self, data, **kw: self.handle_add_user_to_new_projeto(data, **kw),
    )

    def handle_add_user_to_new_projeto(self, data: CreateOrUpdateProjetoSchema, **kw: any) -> Projeto:
        user_id = self.service.get_one(pk=kw['user_id'])
        projeto = Projeto.objects.create(**data.dict())
        projeto.user = user_id
        projeto.save()
        return projeto


api.register_controllers(UserModelControler)
