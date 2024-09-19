from typing import List
from django.shortcuts import get_object_or_404
from ninja.security import django_auth
from ninja_extra import NinjaExtraAPI, api_controller, ControllerBase, route, permissions

from .models import User
from .schemas import UserSchema

api = NinjaExtraAPI(
    version='1.0.0',
    title='Conexao Digital API',
    description='API para o projeto Conexao Digital',
    csrf=True,
    auth=django_auth,
)


@api_controller('/users', tags=['users'], permissions=[permissions.IsAdminUser])
class UserController(ControllerBase):
    @route.post('/users', response=UserSchema, permissions=[permissions.IsAuthenticated])
    def create_user(self, request):
        """ Cria um novo usuário """
        user = User.objects.create_user(**request.dict())
        return user

    @route.get('/users', response=List[UserSchema])
    def get_users(self):
        """ Lista todos os usuários """
        return User.objects.filter(is_superuser=False).all()

    @route.get('/users/{user_id}', response=UserSchema)
    def get_user(self, user_id: int):
        """ Retorna um usuário específico """
        return get_object_or_404(User, id=user_id)

    @route.put('/users/{user_id}', response=UserSchema)
    def update_user(self, user_id: int, request):
        """ Atualiza um usuário específico """
        user = get_object_or_404(User, id=user_id)
        user.__dict__.update(**request.dict())
        user.save()
        return user

    @route.delete('/users/{user_id}', response=UserSchema)
    def delete_user(self, user_id: int):
        """ Deleta um usuário específico """
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return user

    @route.get('/users/me', response=UserSchema, permissions=[permissions.IsAuthenticated])
    def get_me(self, request):
        """ Retorna o usuário autenticado """
        return request.user

    @route.put('/users/me', response=UserSchema, permissions=[permissions.IsAuthenticated])
    def update_me(self, request):
        """ Atualiza o usuário autenticado """
        user = request.user
        user.__dict__.update(**request.dict())
        user.save()
        return user

    @route.delete('/users/me', response=UserSchema, permissions=[permissions.IsAuthenticated])
    def delete_me(self, request):
        """ Deleta o usuário autenticado """
        user = request.user
        user.delete()
        return user


api.register_controllers(UserController)
