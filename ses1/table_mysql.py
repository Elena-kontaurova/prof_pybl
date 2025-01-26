''' Коннект с бд'''
from peewee import Model, CharField, ForeignKeyField, \
            DateField, AutoField, DateTimeField, MySQLDatabase
from pydantic import BaseModel, EmailStr
from passlib.hash import md5_crypt


db = MySQLDatabase('avtoriz', user='root', password='lenok',
                   host='localhost', port=3306)


class BaseModels(Model):
    '''Базовая модель для всех моделей приложения.'''

    class Meta:
        '''Метаданные для базовой модели.'''
        database = db


class Guest(BaseModels):
    '''Класс гости .'''
    id = AutoField()  # id гостя
    first_name = CharField(max_length=100)  # имя
    last_name = CharField(max_length=100)  # фамилия
    email = CharField(max_length=255)  # почта
    phone = CharField(max_length=15)  # телефон


class Applications(BaseModels):
    ''' заявки'''
    id = AutoField()  # id
    guest = ForeignKeyField(Guest, backref='aplications', on_delete='CASCADE')  # id гостя
    apllication_date = DateField()  # дата подачи заявки
    status = CharField(max_length=15, choices=[('Подана', 'Подана'),
                                               ('Обработанна', 'Обработанна'),
                                               ('Откланена', 'Откланена')])  # статус заявки
    visit_date = DateField()  # дата посещения


class Employees(BaseModels):
    ''' Сотрудники'''
    id = AutoField()  # id
    first_name = CharField(max_length=100)  # имя
    last_name = CharField(max_length=100)  # фамилия
    departament = CharField(max_length=100)  # подразделение


class Visits(BaseModels):
    ''' посещения'''
    id = AutoField()  # id
    application = ForeignKeyField(Applications, backref='visits', on_delete='CASCADE')  # id заявки
    visit_time = DateTimeField()  # время посещения
    check_in = DateTimeField(null=True)  # время входа
    chech_out = DateTimeField(null=True)  # время выхода


class Passes(BaseModels):
    ''' пропуска '''
    id = AutoField()  # id
    applications = ForeignKeyField(Applications, backref='passes', on_delete='CASCADE')  # id заявки
    issue_date = DateField()  # дата выдачи
    expiry_data = DateField()  # дата окончания выдачи пропуска
    status = CharField(max_length=50, choices=[('Действующий', 'Действующий'),
                                               ('Истек', 'Истек')])  # статус пропуска


class User(BaseModels):
    ''' класс для регистрации пользователя'''
    id = AutoField()  # id
    email = CharField(unique=True)
    password = CharField()


class UserCreate(BaseModel):
    ''' регистрация'''
    email: EmailStr
    password: str


def hash_password(password: str) -> str:
    ''' хеширование'''
    return md5_crypt.hash(password)


db.connect()
db.create_tables([Guest, Applications, Employees, Visits, Passes, User], safe=True)
db.close()
