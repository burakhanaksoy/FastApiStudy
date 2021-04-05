from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

db = []


class City(BaseModel):
    name: str
    timezone: str


@app.get('/demo')
def demo_city():
    timezone = 'Asia/Shanghai'
    r = requests.get(f'http://worldtimeapi.org/api/timezone/{timezone}')
    current_time = r.json()['datetime']
    return {'name': 'Shanghai', 'timezone': timezone,
            'current_time': current_time}


@app.get('/cities')
def get_cities():
    results = []
    for city in db:
        r = requests.get(
            f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
        current_time = r.json()['datetime']
        results.append(
            {'name': city['name'], 'timezone': city['timezone'], 'current_time': current_time})
    return results


@app.get('/cities/{city_id}')
def get_city(city_id: int):
    city = db[city_id - 1]
    r = requests.get(
        f'http://worldtimeapi.org/api/timezone/{city["timezone"]}')
    current_time = r.json()['datetime']
    return {'name': city['name'], 'timezone': city['timezone'],
            'current_time': current_time}


@ app.post('/cities', status_code=201)
def create_city(city: City):
    if not city in db:
        db.append(city.dict())


@ app.delete('/cities/{city_id', status_code=204)
def delete_city(city_id: int):
    db.pop(city_id - 1)
    return {}
