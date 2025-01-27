''' заявка на одного'''
from datetime import datetime, timedelta
from fastapi import HTTPException
from table_mysql import InfoSkippingOne, User, Employees, Visitor, VisitorCreate


async def get_user_by_email(email: str) -> User:
    '''Логика для получения пользователя по email'''
    return User.get(User.email == email)


async def process_application(application, user_email: str):
    ''' проверки'''
    user = await get_user_by_email(user_email)  # Получаем пользователя по email

    # Проверка даты начала заявки (должна быть минимум на следующий день)
    today = datetime.now()
    if application.start_date < today + timedelta(days=1):
        raise HTTPException(status_code=400,
                            detail="Дата начала заявки, должна быть на следующий день")

    # Проверка даты окончания заявки
    if application.end_date < application.start_date:
        raise HTTPException(status_code=400,
                            detail="Конечная дата, должна быть больше или равна начальной")

    # Проверка максимального срока
    if application.start_date > today + timedelta(days=15):
        raise HTTPException(status_code=400,
                            detail="Дата начала не может превышать 15 дне1, со дня начала")

    if application.end_date > application.start_date + timedelta(days=15):
        raise HTTPException(status_code=400,
                            detail="Дата окончания не может превышать 15 дней с даты начала.")

    # Проверка цели посещения
    if not application.purpose.strip():
        raise HTTPException(status_code=400, detail="Требуется указать цель визита.")

    # проверка подраздлеления для помощения
    if not application.division.strip():
        raise HTTPException(status_code=400,
                            detail='Подразделение не отпределнно')

    if not application.employee_name.strip():
        raise HTTPException(status_code=400,
                            detail='Требуется указать полное имя сотрудника')

    if not employee_belongs_to_division(application.employee_name, application.division):
        raise HTTPException(status_code=400,
                            detail="Сотрудник не принадлежит к выбранному подразделению.")

    application_data = InfoSkippingOne.create(
        user=user,
        start_date=application.start_date,
        end_date=application.end_date,
        purpose=application.purpose,
        division=application.division,
        employee_name=application.employee_name
    )

    return {"msg": "Заявка успешно подана", "application_id": application_data.id}


def employee_belongs_to_division(employee_name: str, departament: str) -> bool:
    ''' лоло'''
    return Employees.select().where((
        Employees.last_name == employee_name) & (
            Employees.departament == departament)).exists()


async def create_visitor(visitor: VisitorCreate):
    ''' создание информации о пользователе'''
    # Проверка существования email в БД
    if Visitor.select().where(Visitor.email == visitor.email).exists():
        raise HTTPException(status_code=400, detail="Почта уже существует.")

    # Создание записи о посетителе
    visitor_data = Visitor.create(
        last_name=visitor.last_name,
        first_name=visitor.first_name,
        patronymic=visitor.patronymic,
        phone=visitor.phone,
        email=visitor.email,
        organization=visitor.organization,
        note=visitor.note,
        birth_date=visitor.birth_date,
        passport_serial=visitor.passport_seria,
        passport_number=visitor.passport_number,
        photo=visitor.photo
    )

    return {"msg": "Данные усешно добавленный", "visitor_id": visitor_data.id}
