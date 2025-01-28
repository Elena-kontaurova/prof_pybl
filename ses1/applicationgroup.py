''' групповая заявка'''
from datetime import datetime, timedelta
from fastapi import HTTPException
from table_mysql import User, InfoSkippingGroup, Employees, VisitorGroup, VisitorGroupCreate


async def get_by_user_email_group(email: str) -> User:
    ''' получение email'''
    return User.get(User.email == email)


async def process_application_group(application: str, user_email: str):
    ''' проверки группа'''
    user = await get_by_user_email_group(user_email)

    today = datetime.now()
    if application.start_date < today + timedelta(days=1):
        raise HTTPException(status_code=400,
                            detail='Дата начала заявки, должна быть на слудующий день')

    if application.end_date < application.start_date:
        raise HTTPException(status_code=400,
                            detail='Конечная дата, должна быть больше или равна начальной')

    if application.start_date > today + timedelta(days=15):
        raise HTTPException(status_code=400,
                            detail='Дата начала не может превышать 15 дней с начала')

    if application.end_date > application.start_date + timedelta(days=15):
        raise HTTPException(status_code=400,
                            detail='Конечная дата не может превышать 15 дней с начальной')

    if not application.purpose.strip():
        raise HTTPException(status_code=400,
                            detail='Требуется указать цель визита.')

    if not application.employee_name.strip():
        raise HTTPException(status_code=400,
                            detail='Требуется указать полное имя сотрудника')

    if not employee_belongs_to_division(application.employee_name, application.division):
        raise HTTPException(status_code=400,
                            detail="Сотрудник не принадлежит к выбранному подразделению.")

    application_date = InfoSkippingGroup.create(
        user=user,
        start_date=application.start_date,
        end_date=application.end_date,
        purpose=application.purpose,
        division=application.division,
        employee_name=application.employee_name
    )

    return {'msg': 'Заявка успешно подана', 'application_id': application_date.id}


def employee_belongs_to_division(employee_name: str, departament: str) -> bool:
    ''' лоло'''
    return Employees.select().where((
        Employees.last_name == employee_name) & (
            Employees.departament == departament)).exists()


async def create_visitor_gr(visitor: VisitorGroupCreate):
    ''' создание информации о пользователе'''
    # Проверка существования email в БД
    if VisitorGroup.select().where(VisitorGroup.email == visitor.email).exists():
        raise HTTPException(status_code=400, detail="Почта уже существует.")

    # Создание записи о посетителе
    visitor_data = VisitorGroup.create(
        last_name=visitor.last_name,
        first_name=visitor.first_name,
        patronymic=visitor.patronymic,
        phone=visitor.phone,
        email=visitor.email,
        organization=visitor.organization,
        note=visitor.note,
        birth_date=visitor.birth_date,
        passport_seria=visitor.passport_seria,
        passport_number=visitor.passport_number,
        photo=visitor.photo
    )

    return {"msg": "Данные успешно добавленный", "visitor_id": visitor_data.id}
