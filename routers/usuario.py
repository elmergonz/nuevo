from fastapi import APIRouter
from models.serverResult import ServerResult
from models.user import User, UserLog
from db import dbdata
import secrets
import re

router = APIRouter()

@router.post('/api/register')
def register(user:User):

    u = dbdata.get_user_by_email(user.email)

    if not u:
        nuser = dbdata.User()
        nuser.name = user.name

        if not check_email(user.email):
            return ServerResult(ok=False, message="Agrege una direccion de correo valida")

        nuser.email = user.email
        nuser.password = user.password
        nuser.token = secrets.token_urlsafe(20)

        nuser.save()

        return ServerResult(response={
            'token': nuser.token
            }, message="Usuario creado")
    else:
        return ServerResult(ok=False, message="El usuario ya existe")

@router.post('/api/login')
def login(user:UserLog):

    u = dbdata.get_user(user.email, user.password)

    if u:
        if u.token:
            return ServerResult(response=u.token, message="Ya ha iniciado sesion")

        u.token = secrets.token_urlsafe(20)
        u.save()
        
        return ServerResult(response={
            'token': u.token
            }, message="Sesion iniciada")
    else:
        return ServerResult(ok=False, message="El usuario no existe, revise sus credenciales")

@router.post('/api/logout')
def logout(token:str):
    user = dbdata.get_user_by_token(token)

    if user:
        user.token = ''
        user.save()

        return ServerResult(message="Sesion cerrada")
    else:
        return ServerResult(ok=False, message="Token invalido")

@router.put('/api/user/modify/data')
def modify_data(token:str, newName:str, newEmail:str):
    user = dbdata.get_user_by_token(token)

    if user:
        user.name = newName

        if not check_email(newEmail):
            return ServerResult(ok=False, message="Agrege una direccion de correo valida")
        
        user.email = newEmail
        user.save()

        return ServerResult(response={
            'nombre': user.name,
            'email': user.email
            }, message="Cambios guardados")
    else:
        return ServerResult(ok=False, message="Token invalido")

@router.put('/api/user/modify/password')
def modify_password(token:str, newPassword:str):
    user = dbdata.get_user_by_token(token)

    if user:
        user.password = newPassword
        user.save()

        return ServerResult(message="Cambios guardados")
    else:
        return ServerResult(ok=False, message="Token invalido")

def check_email(email:str):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return True
    return False