from models import user, secret
from deta import Deta
import os

deta = Deta(os.getenv("DETA_PROJECT_KEY"))
dbUsers = deta.Base('users')
dbSecrets = deta.Base('secrets')

idActual = 0

def set_id():
    idActual = len(next(dbSecrets.fetch()))

async def next_id():
    global idActual
    idActual += 1
    return str(idActual)

async def add_user(user:user.User, token:str):
    user = dbUsers.put({
        "key": user.email,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "token": token
    })

    return user

async def add_secret(secret:secret.Secret, userEmail:str):
    secret = dbSecrets.put({
        "key": await next_id(),
        "user_email": userEmail,
        "title": secret.title,
        "description": secret.description,
        "monetary_value": secret.monetary_value,
        "day": secret.day,
        "month": secret.month,
        "year": secret.year,
        "place": secret.place,
        "lat": secret.lat,
        "lon": secret.lon
    })

    return secret

async def get_user(user:user.UserLog):
    return next(dbUsers.fetch({"email": user.email, "password": user.password}))[0]

async def get_user_by_email(email:str):
    return dbUsers.get(email)

async def get_user_by_token(token:str):
    return next(dbUsers.fetch({"token": token}))

async def update_user_data(updates:dict, key:str):
    dbUsers.update(updates, key=key)

async def update_user_token(key:str, token:str):
    dbUsers.update({"token": token}, key=key)

async def update_user_password(key:str, newPassword:str):
    dbUsers.update({"password": newPassword}, key=key)

async def all_users():
    return next(dbUsers.fetch())

async def all_secrets(token:str):
    userEmail = next(dbUsers.fetch({"token": token}))
    if userEmail:
        return {"secrets": next(dbSecrets.fetch({"user_email": userEmail[0]["email"]}))}
    else:
        return False

async def get_secret(key:str):
    return dbSecrets.get(key)

async def delete_secret(key:str):
    secret = dbSecrets.get(key)
    if secret:
        dbSecrets.delete(secret['key'])
        return True
    else:
        return False

# Justo al iniciar la app...
set_id()