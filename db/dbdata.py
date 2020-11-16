from peewee import *
from playhouse.sqliteq import SqliteQueueDatabase
# from deta import Deta

# deta = Deta('b0wjwc47_vDEHNf1P9XWKQmQm5Yk7REWacUxZJjVV')
# db = deta.Base('usuarios')
db = SqliteDatabase('usuarios.db', pragmas=[('journal_mode', 'wal')])

# db = SqliteDatabase('usuarios.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField(max_length=50)
    email = CharField(max_length=70)
    password = CharField(max_length=50)
    token = CharField(max_length=70)

class Secret(BaseModel):
    user = ForeignKeyField(User, backref='users')
    title = CharField(max_length=70)
    description = CharField()
    monetary_value = FloatField()
    date = DateField()
    place = CharField()
    lat = FloatField()
    lon = FloatField()

    def data(self):
        return {
            'id': self.id,
            'titulo': self.title,
            'descripcion': self.description,
            'valor': self.monetary_value,
            'fecha': self.date,
            'lugar': self.place,
            'latitut': self.lat,
            'longitut': self.lon
        }

def get_user(email:str, password:str):
    try:
        return User.get(User.email == email and User.password == password)
    except User.DoesNotExist:
        return None

def get_user_by_token(token:str):
    try:
        return User.get(User.token == token)
    except User.DoesNotExist:
        return None

def get_user_by_email(email:str):
    try:
        return User.get(User.email == email)
    except User.DoesNotExist:
        return None

def get_secrets(token:str):
    try:
        l = []
        for s in Secret.select():
            if s.user.token == token:
                l.append(s.data())
        
        return l
    except Secret.DoesNotExist:
        return None

def delete_secret(id):
    try:
        return Secret.get(Secret.id == id).delete_instance()
    except Secret.DoesNotExist:
        return None

# db.connect()
# db.create_tables([User, Secret])
