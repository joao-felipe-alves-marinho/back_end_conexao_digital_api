from django.core.mail import send_mail

from ninja import Query

from ninja_extra import (
    NinjaExtraAPI,
    api_controller,
    ControllerBase, route,
    ModelConfig, ModelControllerBase, ModelSchemaConfig, ModelEndpointFactory,
    permissions
)

from dj_ninja_auth.jwt.authentication import JWTAuth
from dj_ninja_auth.jwt.controller import NinjaAuthJWTController

from .models import User, Interesse, Habilidade, FormacaoAcademica, ExperienciaProfissional, Projeto
from .schemas import (
    UserSchema, CreateUserSchema, UpdateUserSchema,
    HabilitadeSchema, CreateOrUpdateHabilidadeSchema,
    InteresseSchema, CreateOrUpdateInteresseSchema,
    FormacaoAcademicaSchema, CreateOrUpdateFormacaoAcademicaSchema,
    ExperienciaProfissionalSchema, CreateOrUpdateExperienciaProfissionalSchema,
    ProjetoSchema, CreateOrUpdateProjetoSchema,
    EmailRequestSchema, FilterEmailSchema
)

api = NinjaExtraAPI(
    version='1.0.0',
    title='Conexao Digital API',
    description='API para o projeto Conexao Digital',
    auth=[JWTAuth()],
)

api.register_controllers(NinjaAuthJWTController)


@api_controller('/admin/users', tags=['admins'], permissions=[permissions.IsAdminUser])
class AdminUserModelController(ModelControllerBase):
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

    # Create SuperUser
    create_superuser = ModelEndpointFactory.create(
        path='/superuser',
        schema_in=UserSchema,
        schema_out=UserSchema,
        custom_handler=lambda self, data, **kw: self.handle_create_superuser(data, **kw),
        summary='Cria um super usuário',
    )

    @staticmethod
    def handle_create_superuser(data: UserSchema, **kw: any) -> User:
        user = User.objects.create_superuser(**data.dict())
        return user

    # Interesses
    add_user_to_new_interesse = ModelEndpointFactory.create(
        path='/{int:user_id}/interesses',
        schema_in=CreateOrUpdateInteresseSchema,
        schema_out=InteresseSchema,
        custom_handler=lambda self, data, **kw: self.handle_add_user_to_new_interesse(data, **kw),
        summary='Adiciona um novo interesse ao usuário',
    )

    def handle_add_user_to_new_interesse(self, data: CreateOrUpdateInteresseSchema, **kw: any) -> Interesse:
        user_id = self.service.get_one(pk=kw['user_id'])
        interesse = Interesse.objects.filter(nome=data.nome).first()
        if not interesse:
            interesse = Interesse.objects.create(**data.dict())
        interesse.users.add(user_id)
        interesse.save()
        return interesse

    get_interesse = ModelEndpointFactory.find_one(
        path='/interesses/{int:interesse_id}',
        schema_out=InteresseSchema,
        lookup_param='interesse_id',
        object_getter=lambda self, pk, **kw: Interesse.objects.get(pk=pk),
        summary='Busca um interesse pelo id',
    )

    get_interesses_from_user = ModelEndpointFactory.list(
        path='/{int:user_id}/interesses',
        schema_out=InteresseSchema,
        queryset_getter=lambda self, **kw: Interesse.objects.filter(users__id=kw['user_id']),
        summary='Lista todos os interesses de um usuário',
    )

    update_interesse = ModelEndpointFactory.update(
        path='/interesses/{int:interesse_id}',
        schema_in=CreateOrUpdateInteresseSchema,
        schema_out=InteresseSchema,
        lookup_param='interesse_id',
        object_getter=lambda self, pk, **kw: Interesse.objects.get(pk=pk),
        summary='Atualiza um interesse pelo id',
    )

    delete_interesse = ModelEndpointFactory.delete(
        path='/interesses/{int:interesse_id}',
        lookup_param='interesse_id',
        object_getter=lambda self, pk, **kw: Interesse.objects.get(pk=pk),
        summary='Deleta um interesse pelo id',
    )

    delete_user_from_interesse = ModelEndpointFactory.delete(
        path='/{int:user_id}/interesses/{int:interesse_id}',
        lookup_param='interesse_id',
        object_getter=lambda self, pk, **kw: Interesse.objects.get(pk=pk),
        custom_handler=lambda self, **kw: self.handle_delete_user_from_interesse(**kw),
        summary='Deleta um interesse de um usuário',
    )

    def handle_delete_user_from_interesse(self, instance: Interesse, **kw: any):
        user_id = self.service.get_one(pk=kw['user_id'])
        instance.users.remove(user_id)
        instance.save()
        return instance

    # Habilidades
    create_new_habilidade_to_user = ModelEndpointFactory.create(
        path='/{int:user_id}/habilidades',
        schema_in=CreateOrUpdateHabilidadeSchema,
        schema_out=HabilitadeSchema,
        custom_handler=lambda self, data, **kw: self.handle_create_new_habilidade_to_user(data, **kw),
        summary='Adiciona uma nova habilidade ao usuário',
    )

    def handle_create_new_habilidade_to_user(self, data: CreateOrUpdateHabilidadeSchema, **kw: any) -> Habilidade:
        user_id = self.service.get_one(pk=kw['user_id'])
        habilidade = Habilidade.objects.create(**data.dict())
        habilidade.user = user_id
        habilidade.save()
        return habilidade

    get_habilidade = ModelEndpointFactory.find_one(
        path='/habilidades/{int:habilidade_id}',
        schema_out=HabilitadeSchema,
        lookup_param='habilidade_id',
        object_getter=lambda self, pk, **kw: Habilidade.objects.get(pk=pk),
        summary='Busca uma habilidade pelo id',
    )

    get_habilidades_from_user = ModelEndpointFactory.list(
        path='/{int:user_id}/habilidades',
        schema_out=HabilitadeSchema,
        queryset_getter=lambda self, **kw: Habilidade.objects.filter(user_id=kw['user_id']),
        summary='Lista todas as habilidades de um usuário',
    )

    update_habilidade = ModelEndpointFactory.update(
        path='/habilidades/{int:habilidade_id}',
        lookup_param='habilidade_id',
        schema_in=CreateOrUpdateHabilidadeSchema,
        schema_out=HabilitadeSchema,
        object_getter=lambda self, pk, **kw: Habilidade.objects.get(pk=pk),
        summary='Atualiza uma habilidade pelo id',
    )

    delete_habilidade = ModelEndpointFactory.delete(
        path='/habilidades/{int:habilidade_id}',
        lookup_param='habilidade_id',
        object_getter=lambda self, pk, **kw: Habilidade.objects.get(pk=pk),
        summary='Deleta uma habilidade pelo id',
    )

    # Formações Acadêmicas
    create_new_formacao_academica_to_user = ModelEndpointFactory.create(
        path='/{int:user_id}/formacoes-academicas',
        schema_in=CreateOrUpdateFormacaoAcademicaSchema,
        schema_out=FormacaoAcademicaSchema,
        custom_handler=lambda self, data, **kw: self.handle_create_new_formacao_academica_to_user(data, **kw),
        summary='Adiciona uma nova formação acadêmica ao usuário',
    )

    def handle_create_new_formacao_academica_to_user(self, data: CreateOrUpdateFormacaoAcademicaSchema,
                                                     **kw: any) -> FormacaoAcademica:
        user_id = self.service.get_one(pk=kw['user_id'])
        formacao_academica = FormacaoAcademica.objects.create(**data.dict())
        formacao_academica.user = user_id
        formacao_academica.save()
        return formacao_academica

    get_formacao_academica = ModelEndpointFactory.find_one(
        path='/formacoes-academicas/{int:formacao_academica_id}',
        schema_out=FormacaoAcademicaSchema,
        lookup_param='formacao_academica_id',
        object_getter=lambda self, pk, **kw: FormacaoAcademica.objects.get(pk=pk),
        summary='Busca uma formação acadêmica pelo id',
    )

    get_formacoes_academicas_from_user = ModelEndpointFactory.list(
        path='/{int:user_id}/formacoes-academicas',
        schema_out=FormacaoAcademicaSchema,
        queryset_getter=lambda self, **kw: FormacaoAcademica.objects.filter(user_id=kw['user_id']),
        summary='Lista todas as formações acadêmicas de um usuário',
    )

    update_formacao_academica_from_user = ModelEndpointFactory.update(
        path='/formacoes-academicas/{int:formacao_academica_id}',
        schema_in=CreateOrUpdateFormacaoAcademicaSchema,
        schema_out=FormacaoAcademicaSchema,
        lookup_param='formacao_academica_id',
        object_getter=lambda self, pk, **kw: FormacaoAcademica.objects.get(pk=pk),
        summary='Atualiza uma formação acadêmica pelo id',
    )

    delete_formacao_academica_from_user = ModelEndpointFactory.delete(
        path='/formacoes-academicas/{int:formacao_academica_id}',
        lookup_param='formacao_academica_id',
        object_getter=lambda self, pk, **kw: FormacaoAcademica.objects.get(pk=pk),
        summary='Deleta uma formação acadêmica pelo id',
    )

    # Experiências Profissionais
    create_new_experiencia_profissional_to_user = ModelEndpointFactory.create(
        path='/{int:user_id}/experiencias-profissionais',
        schema_in=CreateOrUpdateExperienciaProfissionalSchema,
        schema_out=ExperienciaProfissionalSchema,
        custom_handler=lambda self, data, **kw: self.handle_create_new_experiencia_profissional_to_user(data, **kw),
        summary='Adiciona uma nova experiência profissional ao usuário',
    )

    def handle_create_new_experiencia_profissional_to_user(self, data: CreateOrUpdateExperienciaProfissionalSchema,
                                                           **kw: any) -> ExperienciaProfissional:
        user_id = self.service.get_one(pk=kw['user_id'])
        experiencia_profissional = ExperienciaProfissional.objects.create(**data.dict())
        experiencia_profissional.user = user_id
        experiencia_profissional.save()
        return experiencia_profissional

    get_experiencia_profissional = ModelEndpointFactory.find_one(
        path='/experiencias-profissionais/{int:experiencia_profissional_id}',
        schema_out=ExperienciaProfissionalSchema,
        lookup_param='experiencia_profissional_id',
        object_getter=lambda self, pk, **kw: ExperienciaProfissional.objects.get(pk=pk),
        summary='Busca uma experiência profissional pelo id',
    )

    get_experiencias_profissionais_from_user = ModelEndpointFactory.list(
        path='/{int:user_id}/experiencias-profissionais',
        schema_out=ExperienciaProfissionalSchema,
        queryset_getter=lambda self, **kw: ExperienciaProfissional.objects.filter(user_id=kw['user_id']),
        summary='Lista todas as experiências profissionais de um usuário',
    )

    update_experiencia_profissional_from_user = ModelEndpointFactory.update(
        path='/experiencias-profissionais/{int:experiencia_profissional_id}',
        schema_in=CreateOrUpdateExperienciaProfissionalSchema,
        schema_out=ExperienciaProfissionalSchema,
        lookup_param='experiencia_profissional_id',
        object_getter=lambda self, pk, **kw: ExperienciaProfissional.objects.get(pk=pk),
        summary='Atualiza uma experiência profissional pelo id',
    )

    delete_experiencia_profissional_from_user = ModelEndpointFactory.delete(
        path='/experiencias-profissionais/{int:experiencia_profissional_id}',
        lookup_param='experiencia_profissional_id',
        object_getter=lambda self, pk, **kw: ExperienciaProfissional.objects.get(pk=pk),
        summary='Deleta uma experiência profissional pelo id',
    )

    # Projetos
    create_new_projeto_to_user = ModelEndpointFactory.create(
        path='/{int:user_id}/projetos',
        schema_in=CreateOrUpdateProjetoSchema,
        schema_out=ProjetoSchema,
        custom_handler=lambda self, data, **kw: self.handle_create_new_projeto_to_user(data, **kw),
        summary='Adiciona um novo projeto ao usuário',
    )

    def handle_create_new_projeto_to_user(self, data: CreateOrUpdateProjetoSchema, **kw: any) -> Projeto:
        user_id = self.service.get_one(pk=kw['user_id'])
        projeto = Projeto.objects.create(**data.dict())
        projeto.user = user_id
        projeto.save()
        return projeto

    get_projeto = ModelEndpointFactory.find_one(
        path='/projetos/{int:projeto_id}',
        schema_out=ProjetoSchema,
        lookup_param='projeto_id',
        object_getter=lambda self, pk, **kw: Projeto.objects.get(pk=pk),
        summary='Busca um projeto pelo id',
    )

    get_projetos_from_user = ModelEndpointFactory.list(
        path='/{int:user_id}/projetos',
        schema_out=ProjetoSchema,
        queryset_getter=lambda self, **kw: Projeto.objects.filter(user_id=kw['user_id']),
        summary='Lista todos os projetos de um usuário',
    )

    update_projeto = ModelEndpointFactory.update(
        path='/projetos/{int:projeto_id}',
        schema_in=CreateOrUpdateProjetoSchema,
        schema_out=ProjetoSchema,
        lookup_param='projeto_id',
        object_getter=lambda self, pk, **kw: Projeto.objects.get(pk=pk),
        summary='Atualiza um projeto pelo id',
    )

    delete_projeto = ModelEndpointFactory.delete(
        path='/projetos/{int:projeto_id}',
        lookup_param='projeto_id',
        object_getter=lambda self, pk, **kw: Projeto.objects.get(pk=pk),
        summary='Deleta um projeto pelo id',
    )


api.register_controllers(AdminUserModelController)


@api_controller('/me', tags=['users'], permissions=[permissions.IsAuthenticated])
class MeController(ControllerBase):
    @route.get('', response=UserSchema)
    def get_me(self, request):
        return request.user

    @route.put('', response=UserSchema)
    def update_me(self, request, payload: UpdateUserSchema):
        user = request.user
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(user, attr, value)
        user.save()
        return user

    @route.delete('')
    def delete_me(self, request):
        request.user.delete()
        return None

    @route.post('/interesses', response=InteresseSchema)
    def create_interesse(self, request, payload: CreateOrUpdateInteresseSchema):
        interesse = Interesse.objects.filter(nome=payload.nome).first()
        if not interesse:
            interesse = Interesse.objects.create(**payload.dict())
        interesse.users.add(request.user)
        interesse.save()
        return interesse

    @route.get('/interesses', response=InteresseSchema)
    def get_interesses(self, request):
        return Interesse.objects.filter(users__id=request.user.id)

    @route.delete('/interesses/{int:interesse_id}')
    def delete_user_from_interesse(self, request, interesse_id: int):
        interesse = Interesse.objects.get(pk=interesse_id)
        interesse.users.remove(request.user)
        interesse.save()
        return None

    @route.post('/habilidades', response=HabilitadeSchema)
    def create_habilidade(self, request, payload: CreateOrUpdateHabilidadeSchema):
        habilidade = Habilidade.objects.create(**payload.dict())
        habilidade.user = request.user
        habilidade.save()
        return habilidade

    @route.get('/habilidades', response=HabilitadeSchema)
    def get_habilidades(self, request):
        return Habilidade.objects.filter(user=request.user)

    @route.put('/habilidades/{int:habilidade_id}', response=HabilitadeSchema)
    def update_habilidade(self, request, habilidade_id: int, payload: CreateOrUpdateHabilidadeSchema):
        habilidade = Habilidade.objects.get(pk=habilidade_id)
        if habilidade.user == request.user:
            for attr, value in payload.dict(exclude_unset=True).items():
                setattr(habilidade, attr, value)
            habilidade.save()
        return habilidade

    @route.delete('/habilidades/{int:habilidade_id}')
    def delete_habilidade(self, request, habilidade_id: int):
        habilidade = Habilidade.objects.get(pk=habilidade_id)
        if habilidade.user == request.user:
            habilidade.delete()
        return None

    @route.post('/formacoes-academicas', response=FormacaoAcademicaSchema)
    def create_formacao_academica(self, request, payload: CreateOrUpdateFormacaoAcademicaSchema):
        formacao_academica = FormacaoAcademica.objects.create(**payload.dict())
        formacao_academica.user = request.user
        formacao_academica.save()
        return formacao_academica

    @route.get('/formacoes-academicas', response=FormacaoAcademicaSchema)
    def get_formacoes_academicas(self, request):
        return FormacaoAcademica.objects.filter(user=request.user)

    @route.put('/formacoes-academicas/{int:formacao_academica_id}', response=FormacaoAcademicaSchema)
    def update_formacao_academica(self, request, formacao_academica_id: int,
                                  payload: CreateOrUpdateFormacaoAcademicaSchema):
        formacao_academica = FormacaoAcademica.objects.get(pk=formacao_academica_id)
        if formacao_academica.user == request.user:
            for attr, value in payload.dict(exclude_unset=True).items():
                setattr(formacao_academica, attr, value)
            formacao_academica.save()
        return formacao_academica

    @route.delete('/formacoes-academicas/{int:formacao_academica_id}')
    def delete_formacao_academica(self, request, formacao_academica_id: int):
        formacao_academica = FormacaoAcademica.objects.get(pk=formacao_academica_id)
        if formacao_academica.user == request.user:
            formacao_academica.delete()
        return None

    @route.post('/experiencias-profissionais', response=ExperienciaProfissionalSchema)
    def create_experiencia_profissional(self, request, payload: CreateOrUpdateExperienciaProfissionalSchema):
        experiencia_profissional = ExperienciaProfissional.objects.create(**payload.dict())
        experiencia_profissional.user = request.user
        experiencia_profissional.save()
        return experiencia_profissional

    @route.get('/experiencias-profissionais', response=ExperienciaProfissionalSchema)
    def get_experiencias_profissionais(self, request):
        return ExperienciaProfissional.objects.filter(user=request.user)

    @route.put('/experiencias-profissionais/{int:experiencia_profissional_id}', response=ExperienciaProfissionalSchema)
    def update_experiencia_profissional(self, request, experiencia_profissional_id: int,
                                        payload: CreateOrUpdateExperienciaProfissionalSchema):
        experiencia_profissional = ExperienciaProfissional.objects.get(pk=experiencia_profissional_id)
        if experiencia_profissional.user == request.user:
            for attr, value in payload.dict(exclude_unset=True).items():
                setattr(experiencia_profissional, attr, value)
            experiencia_profissional.save()
        return experiencia_profissional

    @route.delete('/experiencias-profissionais/{int:experiencia_profissional_id}')
    def delete_experiencia_profissional(self, request, experiencia_profissional_id: int):
        experiencia_profissional = ExperienciaProfissional.objects.get(pk=experiencia_profissional_id)
        if experiencia_profissional.user == request.user:
            experiencia_profissional.delete()
        return None

    @route.post('/projetos', response=ProjetoSchema)
    def create_projeto(self, request, payload: CreateOrUpdateProjetoSchema):
        projeto = Projeto.objects.create(**payload.dict())
        projeto.user = request.user
        projeto.save()
        return projeto

    @route.get('/projetos', response=ProjetoSchema)
    def get_projetos(self, request):
        return Projeto.objects.filter(user=request.user)

    @route.put('/projetos/{int:projeto_id}', response=ProjetoSchema)
    def update_projeto(self, request, projeto_id: int, payload: CreateOrUpdateProjetoSchema):
        projeto = Projeto.objects.get(pk=projeto_id)
        if projeto.user == request.user:
            for attr, value in payload.dict(exclude_unset=True).items():
                setattr(projeto, attr, value)
            projeto.save()
        return projeto

    @route.delete('/projetos/{int:projeto_id}')
    def delete_projeto(self, request, projeto_id: int):
        projeto = Projeto.objects.get(pk=projeto_id)
        if projeto.user == request.user:
            projeto.delete()
        return None


api.register_controllers(MeController)


@api.post('/me', tags=['users'], auth=None, response=UserSchema)
def create_user(request, payload: CreateUserSchema):
    user = User.objects.create_user(**payload.dict())
    return user


@api.post('/send-email', tags=['admins'])
def send_emails_to_filtered_users(request, payload: EmailRequestSchema, filters: FilterEmailSchema = Query(...)):
    # Filter the users based on the filter schema
    users = User.objects.filter(filters.get_filter_expression(), is_superuser=False, is_staff=False)
    emails = list(users.values_list('email', flat=True)) + payload.emails

    # Send the email to the filtered users
    send_mail(
        payload.subject,
        payload.message,
        'conexaodigital@gmail.com',
        emails,
    )

    return {"message": "Email enviado com sucesso! para {} usuários".format(len(emails))}
