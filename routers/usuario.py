from fastapi import APIRouter
from models.serverResult import ServerResult
from models.user import User, UserLog, UserUpdate
from db import dbdata
import secrets
import re

router = APIRouter()

@router.post('/api/register')
async def register(user:User):

    u = await dbdata.get_user_by_email(user.email)

    if not u:
        if not check_email(user.email):
            return ServerResult(ok=False, message="Agrege una direccion de correo valida")

        token = secrets.token_urlsafe(20)

        nuser = await dbdata.add_user(user, token)

        return ServerResult(response={
            'token': token
            }, message="Usuario creado")
    else:
        return ServerResult(ok=False, message="El usuario ya existe")

@router.post('/api/login')
async def login(user:UserLog):

    u = await dbdata.get_user(user)

    if u:
        if u["token"]:
            return ServerResult(response=u["token"], message="Ya ha iniciado sesion")

        token = secrets.token_urlsafe(20)
        dbdata.update_user_token(u["key"], token)
        
        return ServerResult(response={
            'token': token
            }, message="Sesion iniciada")
    else:
        return ServerResult(ok=False, message="El usuario no existe, revise sus credenciales")

@router.post('/api/logout')
async def logout(token:str):
    user = await dbdata.get_user_by_token(token)

    if user:
        await dbdata.update_user_token(user[0]["key"], token="")

        return ServerResult(message="Sesion cerrada")
    else:
        return ServerResult(ok=False, message="Token invalido")

@router.put('/api/user/modify/data')
async def modify_data(token:str, newData:UserUpdate):
    user = await dbdata.get_user_by_token(token)

    if user:
        if not check_email(newData.email):
            return ServerResult(ok=False, message="Agrege una direccion de correo valida")
        
        updates = {"key": newData.email}
        if newData.email:
            updates["email"] = newData.email
        if newData.name:
            updates["name"] = newData.name
        
        await dbdata.update_user_data(updates, user[0]["key"])

        return ServerResult(response={
            'nombre': updates["name"],
            'email': updates["email"]
            }, message="Cambios guardados")
    else:
        return ServerResult(ok=False, message="Token invalido")

@router.put('/api/user/modify/password')
async def modify_password(token:str, newPassword:str):
    user = await dbdata.get_user_by_token(token)

    if user:
        dbdata.update_user_password(user[0]["key"], newPassword)

        return ServerResult(message="Cambios guardados")
    else:
        return ServerResult(ok=False, message="Token invalido")

def check_email(email:str):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return True
    return False