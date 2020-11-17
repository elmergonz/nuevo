from fastapi import APIRouter
from models.serverResult import ServerResult
from models.secret import Secret
from opencage.geocoder import OpenCageGeocode
from datetime import date
from db import dbdata

router = APIRouter()
geocoder = OpenCageGeocode('d4a9005f502d448ead5ee941b4943630')

@router.get('/api/secret/list')
async def secret_list(token:str):
    secrets = await dbdata.all_secrets(token)
    user = await dbdata.get_user_by_token(token)
    print(secrets, user)
    if secrets and user:
        return ServerResult(response=secrets, message="Lista de secretos")
    elif not user:
        return ServerResult(ok=False, message="Token invalido")
    else:
        return ServerResult(ok=False, message="No ha creado secretos")

@router.post('/api/secret/create')
async def create_secret(token:str, secret:Secret):
    '''
    La ubicacion que usted escriba tiene prioridad sobre las coordenadas, estas se rellenaran en base al lugar.

    Si no se encuentra la ubicacion o se deja vacia, entonces automaticamente se rellenara en base a las coordenadas ingresadas.
    '''
    user = await dbdata.get_user_by_token(token)

    if user[0]:
        if secret.place:
            res = await geocoder.geocode(secret.place)
            if res:
                secret.place = res[0]['formatted']
                secret.lat, secret.lon = res[0]['geometry'].values()
            else:
                secret.place = geocoder.reverse_geocode(secret.lat, secret.lon)[0]['formatted']    
        else:
            secret.place = geocoder.reverse_geocode(secret.lat, secret.lon)[0]['formatted']

        print(secret)
        nsecret = await dbdata.add_secret(secret, user[0]["email"])

        return ServerResult(response=nsecret, message="Secreto agregado")
    else:
        return ServerResult(ok=False, message="Token invalido o ha cerrado sesion")

@router.delete('/api/secret/delete')
async def delete_secret(token:str, id:str):
    user = await dbdata.get_user_by_token(token)
    secret = await dbdata.get_secret(id)

    if secret[0] and user[0]:
        res = await dbdata.delete_secret(id)
        if res:
            return ServerResult(message="Secreto Eliminado")
        else:
            return ServerResult(ok=False, message="No tiene un secreto con esta id")
    elif not user:
        return ServerResult(ok=False, message="Token invalido o ha cerrado sesion")
    else:
        return ServerResult(ok=False, message="No ha creado secretos")
