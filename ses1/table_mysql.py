''' Коннект с бд'''
import re
from datetime import datetime, date
from peewee import Model, CharField, ForeignKeyField, \
            DateField, AutoField, DateTimeField, MySQLDatabase, TextField
from pydantic import BaseModel, EmailStr, field_validator
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


class InfoSkippingOne(BaseModels):
    ''' информация для пропуска - один'''
    id = AutoField()
    user = ForeignKeyField(User, backref='application', on_delete='CASCADE')
    start_date = DateTimeField()
    end_date = DateTimeField()
    purpose = TextField()
    division = CharField()  # подразделение для посещения
    employee_name = CharField()  # фио сотрудника


class InfoSkippingOneCreate(BaseModel):
    ''' получение информация для пропуска - один'''
    start_date: datetime
    end_date: datetime
    purpose: str
    division: str
    employee_name: str


class Visitor(BaseModels):
    ''' информация о посетителе'''
    id = AutoField()
    last_name = CharField()
    first_name = CharField()
    patronymic = CharField(null=True)  # отчество
    phone = CharField(null=True)
    email = CharField(unique=True)
    organization = CharField(null=True)
    note = TextField()  # примечание
    birth_dat = DateField()
    passport_seria = CharField()
    passport_number = CharField()
    photo = CharField(null=True)


class VisitorCreate(BaseModel):
    ''' информация о посетителе создание'''
    last_name: str
    first_name: str
    patronymic: str = None
    phone: str = None
    email: EmailStr
    organization: str = None
    note: str
    birth_date: date
    passport_seria: str
    passport_number: str
    photo: str = None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value):
        ''' валидация номера'''
        if value and not re.match(r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$', value):
            raise ValueError('Номер в формате "+7 (###) ###-##-##".')
        return value

    @field_validator('passport_seria')
    @classmethod
    def get_passport_seria(cls, value):
        '''валидация серии паспорта'''
        if len(value) != 4:
            raise ValueError('Серия паспорта должна быть 4 цифры')
        return value

    @field_validator('passport_number')
    @classmethod
    def get_passport_number(cls, value):
        '''валидация номеры паспорта'''
        if len(value) != 6:
            raise ValueError('Номер паспорта должна быть 6 цифры')
        return value

    @field_validator('birth_date')
    @classmethod
    def gwt_birth_date(cls, value: date):
        ''' проверка возраста'''
        if (date.today() - value).days < 16 * 365:
            raise ValueError('Возраст должен быть больше 16.')
        return value


db.connect()
db.create_tables([Guest, Applications, Employees, Visits, Passes, User, InfoSkippingOne,
                  Visitor], safe=True)
db.close()
