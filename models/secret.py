from pydantic import BaseModel

class Secret(BaseModel):
    title = ''
    description = ''
    monetary_value = 0.0
    day = 1
    month = 1
    year = 1
    place = ''
    lat = 0.0
    lon = 0.0