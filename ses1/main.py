''' kjkj'''
from fastapi import FastAPI
from metod import MetodGuest

app = FastAPI()


@app.get('/guest')
async def get_guest():
    ''' получение всех пользователей'''
    return MetodGuest.get_all_guest()


@app.get('/guest/{guest_id}')
async def get_guest_num(guest_id: int):
    ''' получение информации о определенном пользователе'''
    return MetodGuest.get_all_guest_number(guest_id)


@app.post('/guest')
async def create_gue(first_name: str, last_name: str,
                     email: str, phone: str):
    ''' создание пользователя'''
    return MetodGuest.greate_guest(first_name=first_name, last_name=last_name,
                                   email=email, phone=phone)


@app.put('/guest/{guest_id}')
async def update_guests_num(gue_id: int, first_name: str, last_name: str,
                            email: str, phone: str):
    ''' обновление пользователя'''
    return MetodGuest.update_guest(gue_id=gue_id, first_name=first_name, last_name=last_name,
                                   email=email, phone=phone)


@app.delete('/guest/{guest_id}')
async def delete_guests(guest_id: int):
    ''' удаление пользователя'''
    return MetodGuest.delete_guest(guest_id)
