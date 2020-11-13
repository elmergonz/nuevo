from fastapi import APIRouter
from models.serverResult import ServerResult
from models.secret import Secret
from opencage.geocoder import OpenCageGeocode
from datetime import date
from db import dbdata

router = APIRouter()
geocoder = OpenCageGeocode('d4a9005f502d448ead5ee941b4943630')

@router.get('/secret/list')
def secret_list(token:str):
    secrets = dbdata.get_secrets(token)
    user = dbdata.get_user_by_token(token)

    if secrets and user:
        l = [s for s in secrets]

        return ServerResult(response=l, message="Lista de secretos")
    elif not user:
        return ServerResult(ok=False, message="Token invalido")
    else:
        return ServerResult(ok=False, message="No ha creado secretos")

@router.post('/secret/create')
def create_secret(token:str, secret:Secret):
    '''
    La ubicacion que usted escriba tiene prioridad sobre las coordenadas, estas se rellenaran en base al lugar.

    Si no se encuentra la ubicacion o se deja vacia, entonces automaticamente se rellenara en base a las coordenadas ingresadas.
    '''
    user = dbdata.get_user_by_token(token)

    if user:
        nsecret = dbdata.Secret()
        nsecret.user = user
        nsecret.title = secret.title
        nsecret.description = secret.description
        nsecret.monetary_value = secret.monetary_value
        nsecret.date = date(secret.year, secret.month, secret.day)
        nsecret.place = secret.place
        nsecret.lat = secret.lat
        nsecret.lon = secret.lon

        if secret.place:
            res = geocoder.geocode(secret.place)
            if res:
                nsecret.place = res[0]['formatted']
                nsecret.lat, nsecret.lon = res[0]['geometry'].values()
            else:
                nsecret.place = geocoder.reverse_geocode(secret.lat, secret.lon)[0]['formatted']    
        else:
            nsecret.place = geocoder.reverse_geocode(secret.lat, secret.lon)[0]['formatted']

        nsecret.save()

        return ServerResult(response=nsecret.data(), message="Secreto agregado")
    else:
        return ServerResult(ok=False, message="Token invalido o ha cerrado sesion")

@router.delete('/secret/delete')
def create_secret(token:str, id:int):
    user = dbdata.get_user_by_token(token)
    secrets = dbdata.get_secrets(token)

    if secrets and user:
        res = {}
        for s in secrets:
            if id is s['id']:
                res = s
                dbdata.delete_secret(id)
                break
        else:
            return ServerResult(ok=False, message="No tiene un secreto con esta id")

        return ServerResult(response=res, message="Secreto Eliminado")
    elif not user:
        return ServerResult(ok=False, message="Token invalido o ha cerrado sesion")
    else:
        return ServerResult(ok=False, message="No ha creado secretos")
