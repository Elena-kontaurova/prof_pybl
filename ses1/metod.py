''' jhjh'''
from table_mysql import Guest


class MetodGuest:
    ''' класс для методов пользователей'''
    @staticmethod
    def get_all_guest():
        ''' получение всех пользователей'''
        guest = Guest.select()
        return [{'id': guests.id, 'first_name': guests.first_name,
                 'last_name': guests.last_name, 'email': guests.email,
                 'phone': guests.phone}
                for guests in guest]

    @staticmethod
    def get_all_guest_number(guest_id: int):
        ''' получение по id'''
        guest = Guest.get(Guest.id == guest_id)
        return {'id': guest.id, 'first_name': guest.first_name,
                'last_name': guest.last_name, 'email': guest.email,
                'phone': guest.phone}

    @staticmethod
    def greate_guest(first_name: str, last_name: str,
                     email: str, phone: str):
        ''' создание нового пользователя'''
        guest = Guest.create(first_name=first_name, last_name=last_name,
                             email=email, phone=phone)
        return {
            'first_name': guest.first_name,
            'last_name': guest.last_name,
            'email': guest.email,
            'phone': guest.phone
        }

    @staticmethod
    def update_guest(gue_id: int, first_name: str, last_name: str,
                     email: str, phone: str):
        ''' обновление пользователя'''
        guest = Guest.get(Guest.id == gue_id)
        guest.first_name = first_name
        guest.last_name = last_name
        guest.email = email
        guest.phone = phone
        guest.save()
        return {
            'id': guest.id,
            'first_name': guest.first_name,
            'last_name': guest.last_name,
            'email': guest.email,
            'phone': guest.phone
        }

    @staticmethod
    def delete_guest(guest_id: int):
        ''' удаление пользователя'''
        guest = Guest.get(Guest.id == guest_id)
        guest.delete_instance()
