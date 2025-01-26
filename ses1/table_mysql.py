''' Коннект с бд'''
from peewee import Model, CharField, ForeignKeyField, \
            DateField, AutoField, DateTimeField
from playhouse.mysql_ext import MySQLDatabase


db = MySQLDatabase('avtoriz', user='root', password='lenok',
                   host='localhost', port=3306)


class BaseModel(Model):
    '''Базовая модель для всех моделей приложения.'''

    class Meta:
        '''Метаданные для базовой модели.'''
        database = db


class Guest(BaseModel):
    '''Класс гости .'''
    id = AutoField()  # id гостя
    first_name = CharField(max_length=100)  # имя
    last_name = CharField(max_length=100)  # фамилия
    email = CharField(max_length=255)  # почта
    phone = CharField(max_length=15)  # телефон


class Applications(BaseModel):
    ''' заявки'''
    id = AutoField()  # id
    guest = ForeignKeyField(Guest, backref='aplications', on_delete='CASCADE')  # id гостя
    apllication_date = DateField()  # дата подачи заявки
    status = CharField(max_length=15, choices=[('Подана', 'Подана'),
                                               ('Обработанна', 'Обработанна'),
                                               ('Откланена', 'Откланена')])  # статус заявки
    visit_date = DateField()  # дата посещения


class Employees(BaseModel):
    ''' Сотрудники'''
    id = AutoField()  # id
    first_name = CharField(max_length=100)  # имя
    last_name = CharField(max_length=100)  # фамилия
    departament = CharField(max_length=100)  # подразделение


class Visits(BaseModel):
    ''' посещения'''
    id = AutoField()  # id
    application = ForeignKeyField(Applications, backref='visits', on_delete='CASCADE')  # id заявки
    visit_time = DateTimeField()  # время посещения
    check_in = DateTimeField(null=True)  # время входа
    chech_out = DateTimeField(null=True)  # время выхода


class Passes(BaseModel):
    ''' пропуска '''
    id = AutoField()  # id
    applications = ForeignKeyField(Applications, backref='passes', on_delete='CASCADE')  # id заявки
    issue_date = DateField()  # дата выдачи
    expiry_data = DateField()  # дата окончания выдачи пропуска
    status = CharField(max_length=50, choices=[('Действующий', 'Действующий'),
                                               ('Истек', 'Истек')])  # статус пропуска


db.connect()
db.create_tables([Guest, Applications, Employees, Visits, Passes], safe=True)
db.close()
