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
    '''Класс .'''
    id = AutoField()
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    email = CharField(max_length=255)
    phone = CharField(max_length=15)


class Applications(BaseModel):
    ''' kjkj'''
    id = AutoField()
    guest = ForeignKeyField(Guest, backref='aplications')
    apllication_date = DateField()
    status = CharField(max_length=15, choices=[('Подана', 'Подана'),
                                               ('Обработанна', 'Обработанна'),
                                               ('Откланена', 'Откланена')])
    visit_date = DateField()


class Employees(BaseModel):
    ''' jkjk'''
    id = AutoField()
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    departament = CharField(max_length=100)


class Visits(BaseModel):
    ''' jhjh'''
    id = AutoField()
    application = ForeignKeyField(Applications, backref='visits')
    visit_time = DateTimeField()
    check_in = DateTimeField(null=True)
    chech_out = DateTimeField(null=True)


class Passes(BaseModel):
    ''' jkkj'''
    id = AutoField()
    applications = ForeignKeyField(Applications, backref='passes')
    issue_date = DateField()
    expiry_data = DateField()
    status = CharField(max_length=50, choices=[('Действующий', 'Действующий'),
                                               ('Истек', 'Истек')])


db.connect()
db.create_tables([Guest, Applications, Employees, Visits, Passes], safe=True)
db.close()
