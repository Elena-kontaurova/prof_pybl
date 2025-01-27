''' kjkj'''
from datetime import date, datetime
from fastapi import FastAPI, HTTPException
from metod import MetodGuest, MetodApplication, MetodEmployees, MetodVisits, MetodPasses
from table_mysql import User, UserCreate, hash_password, InfoSkippingOneCreate
from passlib.hash import md5_crypt
from peewee import DoesNotExist
from applicationone import process_application


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


@app.get('/applications')
async def get_applications():
    ''' получение всех заявок'''
    return MetodApplication.get_all_application()


@app.get('/applications/{applic_id}')
async def get_num_aplica(applic_id: int):
    ''' получение заявки по id'''
    return MetodApplication.get_number_application(applic_id)


@app.post('/applications')
async def create_aplic(guest: int, apllication_date: date,
                       status: str, visit_date: date):
    ''' создание заявки'''
    return MetodApplication.create_application(guest=guest, apllication_date=apllication_date,
                                               status=status, visit_date=visit_date)


@app.put('/application/{aplic_id}')
async def update_aplic(aplic_id: int, guest: int, apllication_date: date,
                       status: str, visit_date: date):
    ''' обновление записи'''
    return MetodApplication.upddate_application(aplic_id=aplic_id, guest=guest,
                                                apllication_date=apllication_date,
                                                status=status, visit_date=visit_date)


@app.delete('/application/{aplic_id}')
async def delete_aplic(aplic_id: int):
    ''' удаление записи'''
    return MetodApplication.delete_application(aplic_id=aplic_id)


@app.get('/employees')
async def get_employees():
    ''' получение всех сотрудиков'''
    return MetodEmployees.get_all_employ()


@app.get('/employees/{employ_id}')
async def num_get_emply(employ_id: int):
    ''' получение сотрудника по id'''
    return MetodEmployees.get_num_employ(employ_id=employ_id)


@app.post('/employees')
async def create_employees(first_name: str, last_name: str, departament: str):
    ''' создание нового сотрудника'''
    return MetodEmployees.create_employ(first_name=first_name, last_name=last_name,
                                        departament=departament)


@app.put('/employees/{eploy_id}')
async def update_employees(eploy_id: int, first_name: str, last_name: str,
                           departament: str):
    ''' обновление пользователя'''
    return MetodEmployees.update_emply(eploy_id=eploy_id, first_name=first_name,
                                       last_name=last_name, departament=departament)


@app.delete('/employees/{eploy_id}')
async def delete_employees(eploy_id: int):
    ''' удаление пользователя'''
    return MetodEmployees.delete_employ(eploy_id=eploy_id)


@app.get('/visits')
async def get_visits():
    ''' получение всех визитов'''
    return MetodVisits.get_all_visit()


@app.get('/visits/{visit_id}')
async def get_num_visit(visit_id):
    ''' получение визитов по id'''
    return MetodVisits.get_num_visit(visit_id=visit_id)


@app.post('/visits')
async def create_visits(application: int, visit_time: datetime,
                        check_in: datetime, chech_out: datetime):
    ''' создание визита'''
    return MetodVisits.create_visit(application=application, visit_time=visit_time,
                                    check_in=check_in, chech_out=chech_out)


@app.put('/visits/{visit_id}')
async def update_visits(visit_id: int, application: int, visit_time: datetime,
                        check_in: datetime, chech_out: datetime):
    ''' обновление визитов'''
    return MetodVisits.update_visit(visit_id=visit_id, application=application,
                                    visit_time=visit_time, check_in=check_in, chech_out=chech_out)


@app.delete('/visits/{visit_id}')
async def delete_visits(visit_id: int):
    ''' удаление записи о визите'''
    return MetodVisits.delete_visit(visit_id=visit_id)


@app.get('/passes')
async def get_all_pass():
    ''' получение всез пропусков'''
    return MetodPasses.get_all_passes()


@app.get('/passes/{pas_id}')
async def get_number_passes(pas_id):
    ''' получене пропуска по id'''
    return MetodPasses.get_num_passes(pas_id=pas_id)


@app.post('/passes')
async def create_pas(applications: int, issue_date: date,
                     expiry_date: date, status: str):
    ''' создание нового пропуска'''
    return MetodPasses.create_passes(applications=applications, issue_date=issue_date,
                                     expiry_data=expiry_date, status=status)


@app.put('/passes/{pus_id}')
async def update_pas(pas_id: int, applications: int, issue_date: date,
                     expiry_data: date, status: str):
    ''' обновление записи пропуска'''
    return MetodPasses.update_passes(pas_id=pas_id, applications=applications,
                                     issue_date=issue_date, expiry_data=expiry_data, status=status)


@app.delete('/passes/{pus_id}')
async def delete_pas(pas_id: int):
    ''' удаление пропуска'''
    return MetodPasses.delete_passes(pas_id=pas_id)


@app.post('/reqister')
async def register_users(user: UserCreate):
    ''' РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ'''
    if (
        len(user.password) < 8
        or not any(c.islower for c in user.password)
        or not any(c.isupper for c in user.password)
        or not any(c.isdigit for c in user.password)
        or not any(c in '!@#$%^&*()-_+=' for c in user.password)
    ):
        raise HTTPException(status_code=400, detail="Пароль должен быть не мение 8 символов, \
                            использоваться верхний и нижный регистр, специсивол, цифра.")
    try:
        user = User.create(email=user.email, password=hash_password(user.password))
        return {"msg": "Пользователь успешно зарегестрирован", "user_id": user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail='Email уже сузествует') from e


@app.post('/login')
async def login_users(user: UserCreate):
    ''' вход пользователь'''
    try:
        users = User.get(User.email == user.email)
        if md5_crypt.verify(user.password, users.password):
            return {"msg": "Успешный вход"}
        else:
            raise DoesNotExist(status_code=404, detail="Неверный пароль.")
    except Exception as e:
        raise HTTPException(status_code=404, detail='Пользователь не найден') from e


@app.post("/infoskippingonecreate")
async def create_application(application: InfoSkippingOneCreate, user_email: str):
    ''' информация для пропуска - один'''
    try:
        return await process_application(application, user_email)
    except HTTPException as e:
        raise e
