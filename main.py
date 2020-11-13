# Elmer Gonzalez 2019-8091

from fastapi import FastAPI
from routers import usuario, secrets

app = FastAPI()

app.include_router(usuario.router, tags=['Usuario'])
app.include_router(secrets.router, tags=['Secrets'])

@app.get('/', tags=['Inicio'])
def read_root():
    return {
        'proyecto': 'Api de secretos personales',
        'docs': app.docs_url
    }
