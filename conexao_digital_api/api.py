from typing import List
from django.shortcuts import get_object_or_404
from ninja_extra import NinjaExtraAPI, api_controller, ControllerBase, route, permissions
from ninja_auth.api import router as auth_router

from .models import User
from .schemas import UserSchema, CreateOrUpdateUserSchema

api = NinjaExtraAPI(
    version='1.0.0',
    title='Conexao Digital API',
    description='API para o projeto Conexao Digital',
    csrf=True,
)

api.add_router('/auth', auth_router)


@api_controller('/users', tags=['users'], permissions=[permissions.IsAdminUser])
class UserController(ControllerBase):
    @route.post('', response=UserSchema, auth=None, permissions=[permissions.AllowAny])
    def create_user(self, payload: CreateOrUpdateUserSchema):
        """ Cria um novo usuário """
        user = User.objects.create_user(**payload.dict())
        return user

    @route.get('/admins', response=List[UserSchema])
    def get_admins(self):
        """ Lista todos os administradores """
        return User.objects.filter(is_superuser=True).all()

    @route.get('', response=List[UserSchema])
    def get_users(self):
        """ Lista todos os usuários """
        return User.objects.filter(is_superuser=False).all()

    @route.get('/{int:user_id}', response=UserSchema)
    def get_user(self, user_id: int):
        """ Retorna um usuário específico """
        return get_object_or_404(User, id=user_id)

    @route.put('/{int:user_id}', response=UserSchema)
    def update_user(self, user_id: int, payload: CreateOrUpdateUserSchema):
        """ Atualiza um usuário específico """
        user = get_object_or_404(User, id=user_id)
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(user, key, value)
        user.save()
        return user

    @route.delete('/{int:user_id}', response=UserSchema)
    def delete_user(self, user_id: int):
        """ Deleta um usuário específico """
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return user

    @route.get('/me', response=UserSchema, permissions=[permissions.IsAuthenticated])
    def get_me(self, request):
        """ Retorna o usuário autenticado """
        # retornar user com habilidades
        user = get_object_or_404(User, id=request.user.id)
        return user

    @route.put('/me', response=UserSchema, permissions=[permissions.IsAuthenticated])
    def update_me(self, payload: CreateOrUpdateUserSchema, request):
        """ Atualiza o usuário autenticado """
        user = request.user
        for key, value in payload.dict(exclude_unset=True).items():
            setattr(user, key, value)
        user.save()
        return user

    @route.delete('/me', response=UserSchema, permissions=[permissions.IsAuthenticated])
    def delete_me(self, request):
        """ Deleta o usuário autenticado """
        user = request.user
        user.delete()
        return user


api.register_controllers(UserController)
