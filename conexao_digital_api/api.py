from typing import List
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from ninja.security import django_auth
from ninja_extra import NinjaExtraAPI, api_controller, ControllerBase, route, permissions

from .models import User
from .schemas import UserSchema, CreateUserSchema, SignInSchema

api = NinjaExtraAPI(
    version='1.0.0',
    title='Conexao Digital API',
    description='API para o projeto Conexao Digital',
    csrf=True,
    auth=django_auth,
)


@api.get("/set-csrf-token", auth=None)
def get_csrf_token(request):
    return {"csrftoken": get_token(request)}


@api.post('/login', auth=None)
def login(request, payload: SignInSchema):
    """ Autentica um usuário """
    user = authenticate(request, username=payload.email, password=payload.password)
    if user is not None:
        login(request, user)
        return {"success": True}
    return {"success": False, "message": "Invalid credentials"}


@api.post('/logout')
def logout(request):
    """ Desautentica um usuário """
    logout(request)
    return None


@api_controller('/users', tags=['users'], permissions=[permissions.IsAdminUser])
class UserController(ControllerBase):
    @route.post('', response=UserSchema, auth=None, permissions=[permissions.AllowAny])
    def create_user(self, payload: CreateUserSchema):
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
    def update_user(self, user_id: int, request):
        """ Atualiza um usuário específico """
        user = get_object_or_404(User, id=user_id)
        user.__dict__.update(**request.dict())
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
    def update_me(self, request):
        """ Atualiza o usuário autenticado """
        user = request.user
        user.__dict__.update(**request.dict())
        user.save()
        return user

    @route.delete('/me', response=UserSchema, permissions=[permissions.IsAuthenticated])
    def delete_me(self, request):
        """ Deleta o usuário autenticado """
        user = request.user
        user.delete()
        return user


api.register_controllers(UserController)
